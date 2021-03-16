import numpy as np
import os

import geopandas as gpd
import pandas as pd

url_list = \
        ['https://opendata.arcgis.com/datasets/7015d5d46a284f94ac05c2ea4358bcd7_0.geojson',  # noqa: E501
         'https://opendata.arcgis.com/datasets/5fc63b2a48474100b560a7d98b5097d7_1.geojson',  # noqa: E501
         'https://opendata.arcgis.com/datasets/27af9a2485c5442bb061fa7e881d7022_2.geojson',  # noqa: E501
         'https://opendata.arcgis.com/datasets/4f62515558174f53979b3be0335004d3_3.geojson',  # noqa: E501
         'https://opendata.arcgis.com/datasets/29f801d03c9b4b608bca6a8e497278c3_4.geojson',  # noqa: E501
         'https://opendata.arcgis.com/datasets/a0019dd0d6464747a88921f5e103d509_5.geojson',  # noqa: E501
         'https://opendata.arcgis.com/datasets/40bcfbc4054549ebba8b5777bbdd40ff_6.geojson',  # noqa: E501
         'https://opendata.arcgis.com/datasets/16cedd233d914118a275c6510115d466_7.geojson',  # noqa: E501
         'https://opendata.arcgis.com/datasets/902fd604ecf54adf8579894508cacc68_8.geojson',  # noqa: E501
         'https://opendata.arcgis.com/datasets/170b764c52f34c9497720c0463f3b58b_9.geojson',  # noqa: E501
         'https://opendata.arcgis.com/datasets/2c37babc94d64bbb938a9b520bc5538c_10.geojson',  # noqa: E501
         'https://opendata.arcgis.com/datasets/a35aa9249110472ba2c69cc574eff984_11.geojson']  # noqa: E501


def get_tracts():
    """
    This function returns a GeoDataFrame of census tract boundaries
    """
    tracts_url = \
        'https://opendata.arcgis.com/datasets/de58dc3e1efc49b782ab357e044ea20c_9.geojson'  # noqa: E501
    tracts = gpd.read_file(tracts_url)
    tracts_columns = ['NAME10', 'SHAPE_Area', 'geometry']
    tracts_cleaned = tracts.loc[:, tracts_columns]
    tracts_cleaned['NAME10'] = tracts_cleaned['NAME10'].astype(float)
    tracts_cleaned.rename(columns={'NAME10': 'Tract'}, inplace=True)
    return tracts_cleaned


def get_tractcenters():
    """
    This function returns a GeoDataFrame of census tract centroids
    """
    tract_centers = get_tracts().copy()
    tract_centers['geometry'] = tract_centers['geometry'].centroid
    return tract_centers


def get_zips():
    """
    This function returns a GeoDataFrame of zip code boundaries.
    """
    zips_url = \
        'https://opendata.arcgis.com/datasets/83fc2e72903343aabff6de8cb445b81c_2.geojson'  # noqa: E501
    zipcodes = gpd.read_file(zips_url)
    zipcodes_columns = ['ZIPCODE', 'SHAPE_Area', 'geometry']
    zipcodes_cleaned = zipcodes.loc[:, zipcodes_columns]
    zipcodes_cleaned['ZIPCODE'] = zipcodes_cleaned['ZIPCODE'].astype(int)
    zipcodes_cleaned.head()

    tracts_cleaned = get_tracts()
    zips = gpd.sjoin(zipcodes_cleaned, tracts_cleaned, op='intersects')
    zips_columns = ['ZIPCODE', 'SHAPE_Area_left', 'geometry']
    zips = zips[zips_columns]
    zips = zips.dissolve(by='ZIPCODE')
    zips.rename(columns={'SHAPE_Area_left': 'SHAPE_Area'}, inplace=True)
    zips.reset_index(inplace=True)
    zips = zips[['ZIPCODE', 'SHAPE_Area', 'geometry']]
    return zips


def get_gdf(year):
    '''
    Enter the desired year
    to download the traffic flow count data for that year.
    Example: enter '7' for the year 2007.
    '''
    num = year-7
    gdf_year = gpd.read_file(url_list[num])
    if year == 11:
        gdf_year = gdf_year.rename(columns={"YEAR_": 'YEAR'})
        gdf_year = gdf_year[gdf_year.STNAME != '16TH AVE S']
    if year == 12:
        gdf_year = gdf_year.rename(columns={'STDY_YEAR': 'YEAR'})
    if year == 15 or year == 16:
        gdf_year = gdf_year.rename(columns={"COUNTAAWDT": 'AAWDT',
                                            "FLOWSEGID": "GEOBASID",
                                            'FIRST_STNAME_ORD': 'STNAME'})
        gdf_year = gdf_year[['AAWDT', 'GEOBASID', 'STNAME',
                             'SHAPE_Length', 'geometry']]
        if year == 15:
            year_list = [2015]*len(gdf_year)
            gdf_year['YEAR'] = year_list
        elif year == 16:
            year_list = [2016]*len(gdf_year)
            gdf_year['YEAR'] = year_list
    elif year == 17 or year == 18:
        gdf_year = gdf_year.rename(columns={"AWDT": 'AAWDT',
                                            "FLOWSEGID": "GEOBASID",
                                            'STNAME_ORD': 'STNAME'})
        gdf_year = gdf_year[['AAWDT', 'GEOBASID',
                             'STNAME', 'SHAPE_Length',
                             'geometry']]
        if year == 17:
            year_list = [2017]*len(gdf_year)
            gdf_year['YEAR'] = year_list
        elif year == 18:
            year_list = [2018]*len(gdf_year)
            gdf_year['YEAR'] = year_list
    gdf_year = gdf_year[['YEAR', 'AAWDT',
                         'GEOBASID', 'STNAME',
                         'SHAPE_Length', 'geometry']]
    gdf_year = gdf_year[gdf_year.YEAR != 0]
    gdf_year = gdf_year[gdf_year.YEAR.notnull()]
    return gdf_year


def get_traffic(year):
    '''
    This function a GeoDataFrame of traffic volume
    by zip code for a given year.
    '''
    gdf_test = get_gdf(year)

    midpoints = gdf_test.copy()
    midpoints['MIDPOINT'] = \
        gdf_test['geometry'].interpolate(0.5, normalized=True)
    midpoint_columns = ['YEAR', 'AAWDT', 'MIDPOINT']
    midpoint_cleaned = midpoints.loc[:, midpoint_columns]
    midpoint_cleaned['geometry'] = midpoint_cleaned['MIDPOINT']

    zip_mids = gpd.sjoin(get_zips(), midpoint_cleaned, op='contains')
    zip_mids_clean = zip_mids.copy()
    zip_mids_clean = zip_mids_clean.drop(columns=['SHAPE_Area',
                                                  'index_right',
                                                  'MIDPOINT'])

    zip_mids_clean_c = zip_mids_clean.copy()
    zip_mids_clean_c.drop_duplicates(inplace=True)
    zip_mids_clean_cc = zip_mids_clean_c.copy()
    zip_mids_clean_cc.drop(columns=['geometry'])
    zip_mids_clean_cc = \
        zip_mids_clean_cc.dissolve(by=['ZIPCODE'], aggfunc=sum)

    zip_traffic = zip_mids_clean_cc.copy()
    zip_traffic.drop(columns=['geometry'], inplace=True)
    zip_traffic['YEAR'] = year + 2000
    zip_traffic.reset_index(inplace=True)
    zip_traffic = zip_traffic[['ZIPCODE', 'YEAR', 'AAWDT']]

    return zip_traffic


def get_alldata():
    """
    This function returns a GeoDataFrame of population,
    bike rack capacities, bike lane lengths, and traffic volume
    by zip code and year.
    """

    def get_racks():
        """
        This function returns a GeoDataFrame of bike rack capacities
        by zip code and year.
        """
        # This data is downloaded from Seattle Open GIS
        racks_url = \
            'https://opendata.arcgis.com/datasets/f86c29ce743e47819e588c3d643ceb63_0.geojson'  # noqa: E501
        r = gpd.read_file(racks_url)

        # Selects wanted columns of dataframe, drops null values,
        # and puts install date into terms of years to matcho other data
        racks = r[['INSTALL_DATE', 'RACK_CAPACITY', 'geometry']]
        racks = racks[racks.INSTALL_DATE.notnull()]
        racks['Year'] = pd.DatetimeIndex(racks['INSTALL_DATE']).year
        racks.drop(columns='INSTALL_DATE', inplace=True)

        # Filters dataframe to include only years 2007 - 2018
        filter1 = racks['Year'] >= 2007
        filter2 = racks['Year'] <= 2018
        racks_filtered = racks[filter1 & filter2]

        # Spatially joins bike racks dataframe
        # with zip code boundaries dataframe
        racks_zips = gpd.sjoin(get_zips(), racks_filtered, op='contains')
        racks_zips.reset_index(inplace=True)

        # Dissolves data by zip code and year
        zips_racks = racks_zips.dissolve(by=['ZIPCODE', 'Year'], aggfunc=sum)
        zips_racks.reset_index(inplace=True)

        # Selects relevant columns
        zips_racks_cleaned = zips_racks[['ZIPCODE', 'Year', 'RACK_CAPACITY']]

        # Inserts cumulative bike rack capacities over time
        zip_list = zips_racks_cleaned.ZIPCODE.unique()
        for zipcode in zip_list:
            indices = \
                zips_racks_cleaned[zips_racks_cleaned.ZIPCODE == zipcode].index
            zips_racks_cleaned.loc[indices, 'RACK_CAPACITY'] = \
                zips_racks_cleaned.loc[indices, 'RACK_CAPACITY'].cumsum()

        return zips_racks_cleaned


    def get_lanes():
        """
        This function returns a GeoDataFrame of existing bike lane lengths
        by zip code and year.
        """
        # Downloads data from Seattle Open GIS
        bike_lanes_url = \
            'https://gisdata.seattle.gov/server/rest/services/SDOT/SDOT_Bikes/MapServer/1/query?where=1%3D1&outFields=OBJECTID,STREET_NAME,LENGTH_MILES,SHAPE,DATE_COMPLETED,SHAPE_Length&outSR=4326&f=json'  # noqa: E501
        input_lane = gpd.read_file(bike_lanes_url)

        # Initial selection of relevant columns
        lane_columns = ['LENGTH_MILES', 'DATE_COMPLETED', 'geometry']
        bike_lanes = input_lane[lane_columns]

        # Converts the date completed column to year
        bike_lanes['DATE_COMPLETED'] = \
            pd.to_datetime(bike_lanes['DATE_COMPLETED'], unit='ms')
        bike_lanes['Year'] = \
            pd.DatetimeIndex(bike_lanes['DATE_COMPLETED']).year
        bike_lanes.drop(columns='DATE_COMPLETED', inplace=True)
        bike_lanes['Year'] = bike_lanes['Year'].fillna(0)

        # Builds a baseline of bike lanes before 2007
        # to add cumulatively to the 2007-2018 data
        bike_lanes_baseline = bike_lanes[bike_lanes['Year'] < 2007]
        zips_lanes_base = \
            gpd.sjoin(get_zips(), bike_lanes_baseline, op='intersects')
        zips_lanes_base.reset_index(inplace=True)
        zips_lanes_base = zips_lanes_base.dissolve(by='ZIPCODE', aggfunc='sum')
        zips_lanes_base.reset_index(inplace=True)

        # Filters dataframe to include only years 2007 - 2018
        filter1 = bike_lanes['Year'] >= 2007
        filter2 = bike_lanes['Year'] <= 2018
        bike_lanes_filtered = bike_lanes[filter1 & filter2]

        # Spatially joins bike lanes dataframe
        # with zip code boundaries dataframe
        zips_lanes = gpd.sjoin(get_zips(),
                               bike_lanes_filtered, op='intersects')
        zips_lanes.reset_index(inplace=True)

        # Dissolves data by zip code and year
        zips_lanes = zips_lanes.dissolve(by=['ZIPCODE', 'Year'], aggfunc=sum)
        zips_lanes.reset_index(inplace=True)

        # Selects relevant columns and renames quantity variable for clarity
        zips_lanes_cleaned = zips_lanes[['ZIPCODE', 'Year', "LENGTH_MILES"]]
        zips_lanes_cleaned.rename(columns={'LENGTH_MILES': 'Miles_Bike_Lanes'},
                                  inplace=True)

        # Inserts cumulative bike lane lengths over time
        zip_list = zips_lanes_cleaned.ZIPCODE.unique()
        for zipcode in zip_list:
            indices = \
                zips_lanes_cleaned[zips_lanes_cleaned.ZIPCODE == zipcode].index
            zips_lanes_cleaned.loc[indices, 'Miles_Bike_Lanes'] = \
                zips_lanes_cleaned.loc[indices, 'Miles_Bike_Lanes'].cumsum()

        return zips_lanes_cleaned


    def get_pop():
        """
        This function returns
        a GeoDataFrame of population by zip code and year.
        """
        # This data is downloaded from Seattle Open GIS
        pop_url_2010 = \
            'https://gisrevprxy.seattle.gov/arcgis/rest/services/CENSUS_EXT/CENSUS_2010_BASICS/MapServer/15/query?where=1%3D1&outFields=SHAPE,GEOID10,NAME10,ACRES_TOTAL,Total_Population,OBJECTID&outSR=4326&f=json'  # noqa: E501
        pop_2010 = gpd.read_file(pop_url_2010)

        # Redefines census tract geometries
        # by their centroid points to avoid double counting,
        # when spatial join happens
        census_cent = get_tractcenters()
        # census_bounds_cleaned = get_census_bounds()
        # census_cent = census_bounds_cleaned.copy()
        # census_cent['geometry'] = census_cent['geometry'].centroid
        pop_2010['geometry'] = census_cent['geometry']

        # Spatial join to put populations with associated zipcode
        pop_zips = gpd.sjoin(get_zips(), pop_2010, op='contains')
        pop_zips.reset_index(inplace=True)
        pop_zips = pop_zips[['ZIPCODE', 'geometry', 'Total_Population']]

        # Dissolve into single zipcode geometry
        # and aggregate within that geometry
        pop_zips_diss = pop_zips.dissolve(by='ZIPCODE', aggfunc='sum')
        pop_zips_diss.reset_index(inplace=True)
        pop_zips_diss_clean = pop_zips_diss[['ZIPCODE', 'Total_Population']]

        # Create estimates for zip code populations
        # in years besides 2010 based on the population fraction
        # and total population
        total_pop = pop_zips_diss_clean['Total_Population'].sum()
        pop_zips_diss_clean['Pop_fraction'] = \
            pop_zips_diss_clean['Total_Population']/total_pop
        years = list(range(2007, 2019))
        populations = [585436, 591870, 598539,
                       608660, 622694, 635928,
                       653588, 670109, 687386,
                       709631, 728661, 742235]
        pop_by_year = dict(zip(years, populations))


        def est_zip_pop(year, pop_zips_diss_clean, pop_by_year):
            pop_frac = pop_zips_diss_clean['Pop_fraction'].values
            year_pop = pop_by_year.get(year)
            pop_zip_year = pop_zips_diss_clean.copy()
            pop_zip_year['Total_Population'] = pop_frac*year_pop
            return pop_zip_year

        pop_zips_years = gpd.GeoDataFrame()
        for year in years:
            pop_zip_year = est_zip_pop(year, pop_zips_diss_clean, pop_by_year)
            pop_zip_year['Year'] = year
            pop_zips_years = pop_zips_years.append(pop_zip_year)
        pop_zips_years.sort_values(by=['ZIPCODE', 'Year'], inplace=True)
        pop_zips_years = pop_zips_years[['ZIPCODE', 'Year',
                                         'Total_Population',
                                         'Pop_fraction']]

        return pop_zips_years


    def get_alltraffic():
        '''
        This function a GeoDataFrame of traffic volume by zip code and year.
        '''
        all_traffic = pd.DataFrame()
        years = list(np.arange(7, 19))
        for year in years:
            traffic = get_traffic(year)
            all_traffic = all_traffic.append(traffic)
        all_traffic.groupby(by='ZIPCODE')
        all_traffic.sort_values(['ZIPCODE', 'YEAR'], inplace=True)
        all_traffic.rename(columns={'YEAR': 'Year'}, inplace=True)

        return all_traffic

    # Creates dataframes for bike rack capacities,
    # bike lane lengths, population and traffic volumes
    rack_data = get_racks()
    lane_data = get_lanes()
    pop_data = get_pop()
    traffic_data = get_alltraffic()

    # Merges dataframes
    a = pd.merge(traffic_data, pop_data, how='left', on=['Year', 'ZIPCODE'])
    b = pd.merge(a, rack_data, how='left', on=['Year', 'ZIPCODE'])
    all_data = pd.merge(b, lane_data, how='left', on=['Year', 'ZIPCODE'])

    # Removes zip codes with lots of missing data
    all_data.fillna(0, inplace=True)
    zip_list = list(all_data.ZIPCODE.unique())
    removed_zips_index = [21, 23, 24, 25, 26, 27, 28]
    for i in removed_zips_index:
        all_data.drop(all_data[all_data.ZIPCODE == zip_list[i]].index,
                      inplace=True)

    return all_data


# Creates dataframe containing all features and targets
all_data = get_alldata()


def get_zipdata(zipcode):
    '''
    This function a GeoDataFrame of traffic volume
    by year for a given zip code.
    '''
    zip_data = all_data[all_data.ZIPCODE == zipcode]
    return zip_data


def get_csv(df, file_name):
    """
    This function takes an input DataFrame (df),
    file name (file_name),
    and writes the DataFrame to a csv file titled file_name.
    """
    directory = os.getcwd()
    path = directory + '/' + file_name + '.csv'
    csvfile = df.to_csv(path)
    return csvfile


def get_csv_alldata():
    """
    This function writes the DataFrame,
    with all attributes by zip code and year,
    to a csv file titled 'all_data.csv'.
    """
    get_csv(all_data, 'all_data')
    return
