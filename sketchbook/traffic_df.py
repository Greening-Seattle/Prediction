#Import libraries
import pandas as pd 
import geopandas as gpd
import shapely
from shapely.geometry import Point
import numpy as np

#Load in traffic data
#List of traffic download URLs for 2007 - 2018
url_list = ['https://opendata.arcgis.com/datasets/7015d5d46a284f94ac05c2ea4358bcd7_0.geojson',
            'https://opendata.arcgis.com/datasets/5fc63b2a48474100b560a7d98b5097d7_1.geojson',
            'https://opendata.arcgis.com/datasets/27af9a2485c5442bb061fa7e881d7022_2.geojson',
            'https://opendata.arcgis.com/datasets/4f62515558174f53979b3be0335004d3_3.geojson',
            'https://opendata.arcgis.com/datasets/29f801d03c9b4b608bca6a8e497278c3_4.geojson',
            'https://opendata.arcgis.com/datasets/a0019dd0d6464747a88921f5e103d509_5.geojson',
            'https://opendata.arcgis.com/datasets/40bcfbc4054549ebba8b5777bbdd40ff_6.geojson',
            'https://opendata.arcgis.com/datasets/16cedd233d914118a275c6510115d466_7.geojson',
            'https://opendata.arcgis.com/datasets/902fd604ecf54adf8579894508cacc68_8.geojson',
            'https://opendata.arcgis.com/datasets/170b764c52f34c9497720c0463f3b58b_9.geojson',
            'https://opendata.arcgis.com/datasets/2c37babc94d64bbb938a9b520bc5538c_10.geojson',
            'https://opendata.arcgis.com/datasets/a35aa9249110472ba2c69cc574eff984_11.geojson']

#Long (but necessary) function written by Sarah to homogenize column titles for traffic data downloads.
def get_gdf(year):
    '''Enter the desired year to download the traffic flow count
    data for that year. Example: enter '7' for the year 2007.
    '''
    num = year-7
    gdf_year = gpd.read_file(url_list[num])
    if year == 11:
        gdf_year = gdf_year.rename(columns={"YEAR_" : 'YEAR'})
    if year == 12:
        gdf_year = gdf_year.rename(columns={'STDY_YEAR' : 'YEAR'})
    if year == 15 or year == 16:
        gdf_year = gdf_year.rename(columns={"COUNTAAWDT" : 'AAWDT', "FLOWSEGID" : "GEOBASID", 'FIRST_STNAME_ORD' : 'STNAME'})
        gdf_year = gdf_year[['AAWDT', 'GEOBASID', 'STNAME', 'SHAPE_Length', 'geometry']]
        if year == 15:
            year_list = ['2015']*len(gdf_year)
            gdf_year['YEAR'] = year_list
        elif year == 16:
            year_list = ['2016']*len(gdf_year)
            gdf_year['YEAR'] = year_list
    elif year == 17 or year == 18:
        gdf_year = gdf_year.rename(columns={"AWDT" : 'AAWDT', "FLOWSEGID" : "GEOBASID", 'STNAME_ORD' : 'STNAME'})
        gdf_year = gdf_year[['AAWDT', 'GEOBASID', 'STNAME', 'SHAPE_Length', 'geometry']]
        if year == 17:
            year_list = ['2017']*len(gdf_year)
            gdf_year['YEAR'] = year_list
        elif year == 18:
            year_list = ['2018']*len(gdf_year)
            gdf_year['YEAR'] = year_list

    gdf_year = gdf_year[[ 'YEAR', 'AAWDT', 'GEOBASID', 'STNAME', 'SHAPE_Length', 'geometry']]
    return gdf_year
  
# Census tract boundaries
census_url = 'https://opendata.arcgis.com/datasets/de58dc3e1efc49b782ab357e044ea20c_9.geojson'
census_bounds = gpd.read_file(census_url)
census_columns = ['NAME10', 'SHAPE_Area', 'geometry']
census_bounds_cleaned = census_bounds.loc[:,census_columns]
census_bounds_cleaned['NAME10'] = census_bounds_cleaned['NAME10'].astype(float)

# Zip code boundaries
zipcodes_url = 'https://opendata.arcgis.com/datasets/83fc2e72903343aabff6de8cb445b81c_2.geojson'
zipcodes = gpd.read_file(zipcodes_url)
zipcodes_columns = ['ZIPCODE', 'SHAPE_Area', 'geometry']
zipcodes_cleaned = zipcodes.loc[:,zipcodes_columns]
zipcodes_cleaned['ZIPCODE'] = zipcodes_cleaned['ZIPCODE'].astype(int)

# Zip codes spatially joined with census tracts
zips = gpd.sjoin(zipcodes_cleaned, census_bounds_cleaned, op='intersects')
zips_columns = ['ZIPCODE', 'NAME10', 'SHAPE_Area_left', 'geometry']
zips = zips[zips_columns]

def traffic(year):
    '''Function to generate distributions of traffic flow by year in each zip
    '''
    gdf_test = get_gdf(year)

    midpoints = gdf_test.copy()
    midpoints['MIDPOINT'] = gdf_test['geometry'].interpolate(0.5, normalized = True)
    midpoint_columns = ['YEAR', 'AAWDT', 'MIDPOINT']
    midpoint_cleaned = midpoints.loc[:,midpoint_columns]
    midpoint_cleaned['geometry'] = midpoint_cleaned['MIDPOINT']
    
    zip_mids = gpd.sjoin(zips,midpoint_cleaned,op='contains')
    zip_mids_clean = zip_mids.copy()
    zip_mids_clean = zip_mids_clean.drop(columns=['SHAPE_Area_left','NAME10','index_right','MIDPOINT'])
    
    zip_mids_clean_c = zip_mids_clean.copy()
    zip_mids_clean_c.drop_duplicates(inplace=True)
    zip_mids_clean_cc = zip_mids_clean_c.copy()
    zip_mids_clean_cc.drop(columns=['geometry'])
    zip_mids_clean_cc = zip_mids_clean_cc.dissolve(by=['ZIPCODE'],aggfunc=sum)
    
    zip_traffic = zip_mids_clean_cc.copy()
    zip_traffic.drop(columns=['geometry'],inplace=True)
    zip_traffic['YEAR'] = year + 2000
    zip_traffic.reset_index(inplace=True)
    zip_traffic = zip_traffic[['ZIPCODE', 'YEAR', 'AAWDT']]
    zip_traffic.head(n=30)

    return zip_traffic

def total_traffic(years):
    df_total_traffic = pd.DataFrame()
    years = list(np.arange(7,19))
    for year in years:
        traffic_year = traffic(year)
        df_total_traffic = df_total_traffic.append(traffic_year)
    return df_total_traffic

def final_df():
    '''Ultimate function that returns total compiled traffic data frame by year and zip
    '''
    years = list(np.arange(7,19))
    total_df = total_traffic(years)
    total_traffic_df = total_df.copy()
    total_traffic_df.groupby(by='ZIPCODE')
    total_traffic_df.sort_values(['ZIPCODE','YEAR'],inplace=True)

    return total_traffic_df
