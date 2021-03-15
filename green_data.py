"""
This file contains functions for loading Seattle geospatial data into GeoDataFrames.
"""

#import datetime
import pandas as pd    
import geopandas as gpd
#from geopandas.tools import geocode
#from shapely.geometry import Point
import numpy as np
#import shapely
#from shapely import speedups
#speedups.enabled
#import matplotlib 
#from matplotlib import pyplot as plt
#matplotlib.rcParams.update({'font.size': 20})

# Greening Seattle package for loading census tract and zip code geospatial data into GeoDataFrames
import get_geodata
from get_geodata import get_gdf
from get_geodata import get_census_bounds
from get_geodata import get_zipcode_bounds

# Greening Seattle package for loading urban geospatial data into GeoDataFrames
import get_trafficdata
from get_trafficdata import get_alltraffic

def get_zips():
    """
    This function returns a GeoDataFrame of zip code boundaries.
    """
    return get_zipcode_bounds()

def get_tracts():
    """
    This function returns a GeoDataFrame of census tract boundaries.
    """
    return get_census_bounds()

def get_tractcenters():
    """
    This function returns a GeoDataFrame of census tract centroids.
    """
    census_cent = get_tracts().copy()
    census_cent['geometry'] = census_cent['geometry'].centroid
    return census_cent

def get_traffic():
    """
    This function returns a GeoDataFrame of traffic volume by zip code and year.
    """
    return get_alltraffic
    
# Loads bike rack data
racks_url = 'https://opendata.arcgis.com/datasets/f86c29ce743e47819e588c3d643ceb63_0.geojson'
r = gpd.read_file(racks_url)

def get_racks():
    """
    This function returns a GeoDataFrame of bike rack capacities by zip code and year.
    """
    # Creates dataframe
    racks = r[['INSTALL_DATE', 'RACK_CAPACITY', 'geometry']]
    racks = racks[racks.INSTALL_DATE.notnull()]
    racks['Year'] = pd.DatetimeIndex(racks['INSTALL_DATE']).year
    racks = racks.drop(columns='INSTALL_DATE')
    
    # Filters dataframe to include only years 2007 - 2018
    filter1 = racks['Year'] >= 2007
    filter2 = racks['Year'] <= 2018
    racks_filtered = racks[filter1 & filter2]
    
    # Spatially joins bike racks dataframe with zip code boundaries dataframe
    zips_racks = gpd.sjoin(get_zips(), racks_filtered, op='contains')
    zips_racks.reset_index(inplace=True)
    zips_racks = zips_racks[['ZIPCODE', 'Year', 'RACK_CAPACITY']]
    zips_racks.drop_duplicates(subset=['ZIPCODE', 'Year'], inplace=True)
    zips_racks.sort_values(by=['ZIPCODE', 'Year'], inplace=True)
    return zips_racks

# Loads bike lane and walkway data
bike_lanes_url = 'https://gisdata.seattle.gov/server/rest/services/SDOT/SDOT_Bikes/MapServer/1/query?where=1%3D1&outFields=OBJECTID,STREET_NAME,LENGTH_MILES,SHAPE,DATE_COMPLETED,SHAPE_Length&outSR=4326&f=json'
lanes = gpd.read_file(bike_lanes_url)

def get_lanes():
    """
    This function returns a GeoDataFrame of existing bike lane lengths by zip code and year.
    """
    # Creates dataframe
    lane_columns = ['LENGTH_MILES', 'DATE_COMPLETED', 'geometry']
    bike_lane = lanes[lane_columns]
    bike_lane['DATE_COMPLETED'] = pd.to_datetime(bike_lane['DATE_COMPLETED'], unit='ms')
    bike_lane['Year'] = pd.DatetimeIndex(bike_lane['DATE_COMPLETED']).year
    bike_lane = bike_lane.drop(columns='DATE_COMPLETED')
    bike_lane['Year'] = bike_lane['Year'].fillna(0)

    # Filters dataframe to include only years 2007 - 2018
    filter1 = bike_lane['Year'] >= 2007
    filter2 = bike_lane['Year'] <= 2018
    bike_lane_filtered = bike_lane[filter1 & filter2]

    # Spatially joins bike lanes dataframe with zip code boundaries dataframe
    zips_lanes = gpd.sjoin(get_zips(), bike_lane_filtered, op='intersects')
    zips_lanes['Year'] = zips_lanes['Year'].astype(int)
    zips_lanes.reset_index(inplace=True)
    zips_lanes.drop_duplicates(subset=['ZIPCODE', 'Year'], inplace=True)
    zips_lanes = zips_lanes[['ZIPCODE', 'Year', 'LENGTH_MILES']]
    zips_lanes.rename(columns={'LENGTH_MILES': 'Miles_Bike_Lane'}, inplace=True)
    zips_lanes.sort_values(by=['ZIPCODE', 'Year'], inplace=True)

    return zips_lanes

# Loads population data
pop_url_2010 = 'https://gisrevprxy.seattle.gov/arcgis/rest/services/CENSUS_EXT/CENSUS_2010_BASICS/MapServer/15/query?where=1%3D1&outFields=SHAPE,GEOID10,NAME10,ACRES_TOTAL,Total_Population,OBJECTID&outSR=4326&f=json'
p = gpd.read_file(pop_url_2010)

def get_pop2010():
    """
    This function returns a GeoDataFrame of population by zip code and year.
    """
    # Creates dataframe of 2010 population by census tract
    pop_2010 = p.copy()
    pop_2010.NAME10 = pop_2010.NAME10.astype(float)
    pop_2010['geometry'] = get_tractcenters()['geometry']

    # Spatially joins population dataframe with zip code boundaries dataframe
    pop_zips = gpd.sjoin(get_zips(), pop_2010, op='contains')
    pop_zips.reset_index(inplace=True)
    pop_zips = pop_zips[['ZIPCODE','geometry', 'Total_Population']]
    pop_zips = pop_zips.groupby(by='ZIPCODE').sum()
    pop_zips.reset_index(inplace=True)
    total_pop = pop_zips['Total_Population'].sum()

    # Adds a column for population fraction
    pop_zips['Pop_fraction'] = pop_zips['Total_Population']/total_pop

    return pop_zips

# Creates a dictionary of years and total populations
years = list(range(2007, 2019))
populations = [585436, 591870, 598539, 608660, 622694, 635928, 653588, 670109, 687386, 709631, 728661, 742235]
pop_by_year = dict(zip(years, populations))

def est_pop(year):
    """
    This function...
    """    
    pop = get_pop2010()
    pop_frac = pop['Pop_fraction'].values
    year_pop = pop_by_year.get(year)
    pop_zip_year = pop.copy()
    pop_zip_year['Total_Population'] = pop_frac*year_pop
    
    return pop_zip_year

def get_pop():
    """
    This function returns a GeoDataFrame of population by zip code and year.
    """
    pop_zips_years = gpd.GeoDataFrame()
    years = list(range(2007, 2019))

    for year in years:
        pop_zip_year = est_pop(year)
        pop_zip_year['Year'] = year
        pop_zips_years = pop_zips_years.append(pop_zip_year)
    pop_zips_years = pop_zips_years[['ZIPCODE', 'Year', 'Total_Population', 'Pop_fraction']]
    pop_zips_years.sort_values(by=['ZIPCODE', 'Year'], inplace=True)
    
    return pop_zips_years

def get_alldata():
    """
    This function returns a GeoDataFrame of population, bike rack capacities, bike lane lengths, and traffic volume
    by zip code and year.
    """
    a = pd.merge(get_pop(), get_racks(), how='left', on= ['Year', 'ZIPCODE'])
    b = pd.merge(a, get_lanes(), how='left', on= ['Year', 'ZIPCODE'])
    all_data = pd.merge(b, get_traffic(), how='left', on =['Year', 'ZIPCODE'])
    
    #a = pd.merge(get_traffic(), get_pops(), how='left', on= ['Year', 'ZIPCODE'])
    #b = pd.merge(a, get_racks(), how='left', on= ['Year', 'ZIPCODE'])
    #all_data = pd.merge(b, get_lanes(), how='left', on =['Year', 'ZIPCODE'])
    
    # Removes zip codes with lots of missing data
    all_data.fillna(0, inplace=True)
    removed_zips_index = [21, 23, 24, 25, 26, 27, 28]
    
    for i in removed_zips_index:
        all_data.drop(all_data[all_data.ZIPCODE==zip_list[i]].index, inplace=True)
    
    # Inserts cumulative bike rack capacities and bike lane lengths over time
    zip_list = all_data.ZIPCODE.unique()
    for zipcode in zip_list:
        indices = all_data[all_data.ZIPCODE==zipcode].index
        all_data.loc[indices, ['RACK_CAPACITY', 'Miles_Bike_Lanes']] = all_data.loc[indices, ['RACK_CAPACITY', 'Miles_Bike_Lanes']].cumsum()
    
    return all_data