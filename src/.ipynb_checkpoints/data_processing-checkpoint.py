from census_area import Census
import geopandas as gpd


# Census Data

# Households
# Household total ('hh_total'): 'B11001_001E'
# Marriedcouple family ('hh_married'): 'B11001_003E'
# Male householder, no wife present ('hh_m'): 'B11001_005E'
# Female housholder, no husband present ('hh_fm'): 'B11001_006E'


# Income
# Median household income in the past 12th months ('income_med'): 'B19013_001E'

# Female Education Attainment
# Total education, female ('edu_f_total'): 'B15002_019E'
# No schooling completed, female ('edu_f_none'): 'B15002_020E'
# Nursey to 4th grade, female ('edu_f_4th'): 'B15002_021E'
# 5th and 6th grade, female ('edu_f_5th6th'): 'B15002_022E'
# 7th and 8th grade, female ('edu_f_7th8th'): 'B15002_023E'
# 9th grade, female ('edu_f_9th'): 'B15002_024E'
# 10th grade, female ('edu_f_10th'): 'B15002_025E'
# 11 grade, female ('edu_f_11th'): 'B15002_026E'
# 12 grade, no diploma, female ('edu_f_12th'): 'B15002_027E'
# High school graduate, GED, or alternative, female ('edu_f_hs'): 'B15002_028E'
# Associate's degree, female ('edu_f_ad'): 'B15002_031E'
# Bachelor's degree, female ('edu_f_bd'): 'B15002_032E'
# Master's degree, female ('edu_f_md'): B15002_033E'
# Profession school degree, female ('edu_f_ps'): 'B15002_034E'
# Doctorate degree, female ('edu_f_dd'): 'B15002_035E'

# Male Education Attainment
# Total education, male ('edu_m_total'): 'B15002_002E'
# No schooling completed, male ('edu_m_none'): 'B15002_003E'
# Nursey to 4th grade, male ('edu_m_4th'): 'B15002_004E'
# 5th and 6th grade, male ('edu_m_5th6th'): 'B15002_005E'
# 7th and 8th grade, male ('edu_m_7th8th'): 'B15002_006E'
# 9th grade, male ('edu_m_9th'): 'B15002_007E'
# 10th grade, male ('edu_m_10th'): 'B15002_008E'
# 11 grade, male ('edu_m_11th'): 'B15002_009E'
# 12 grade, no diploma, male ('edu_m_12th'): 'B15002_010E'
# High school graduate, GED, or alternative, male ('edu_m_hs'): 'B15002_011E'
# Associate's degree, male ('edu_m_ad'): 'B15002_014E'
# Bachelor's degree, male ('edu_m_bd'): 'B15002_015E'
# Master's degree, male ('edu_m_md'): B15002_016E'
# Profession school degree, male ('edu_m_ps'): 'B15002_017E'
# Doctorate degree, male ('edu_m_dd'): 'B15002_018E'


# Collect_data function
def collect_data(city_code = None, year = 2013):
    
    '''Takes a city code and queries the US census API for census data of variables of interest.
    
    Args:
    
    city_code (list) : list with state code and city code (e.g. [17, 14000] for chicago)
    
    year (int): year of interest
    
    Returns:
    
    gdf (GeoDataFrame) : gdf of census data variables of interest for given city'''
    
    # Define variables
    variables_of_interest = ('NAME', 'B11001_001E', 'B11001_003E', 'B11001_005E', 'B11001_006E',
                              'B19013_001E', 'B15002_019E','B15002_020E', 'B15002_021E', 'B15002_022E', 
                              'B15002_023E', 'B15002_024E', 'B15002_025E', 'B15002_026E', 'B15002_027E', 
                              'B15002_028E', 'B15002_031E', 'B15002_032E', 'B15002_033E', 'B15002_034E', 
                              'B15002_035E', 'B15002_002E','B15002_003E', 'B15002_004E', 'B15002_005E', 
                              'B15002_006E', 'B15002_007E', 'B15002_008E', 'B15002_009E', 'B15002_010E', 
                              'B15002_011E', 'B15002_014E', 'B15002_015E', 'B15002_016E', 'B15002_017E', 
                              'B15002_018E')
    
    # API key for US census
    c = Census("eef663dd88d62e6fbe3fc3b00502ee8563658654", year = year)

    # Return total households, married couple households, single-male households, single-female households, median household income,
    # and education attainment types by sex, for every census block group in city of interest
    city= c.acs5.state_place_blockgroup(variables_of_interest, city_code[0], city_code[1], return_geometry=True)
    
    # Convert geojson to gdf
    gdf = gpd.GeoDataFrame.from_features(city['features'])
    
    return gdf


#Clean_columns function
def clean_columns(gdf = None):
    
    '''Renames gdf column names with a list, sums less than highschool diploma education for both females and males into
    'edu_f_less_hs' and 'edu_m_less_hs', drops uncessary columns, and replace -666666666.0 values for median income with 0

    args:
    
    gdf (GeoDataFrame) :gdf of variables of interest with census data variable naming

    Returns:

    gdf (GeoDataFrame) : gdf of renamed census data variables of interest for given city'''

    # Create list of new column names 
    colnames_ls = ['MTFCC', 'OID', 'GEOID', 'STATE', 'COUNTY', 'TRACT', 'BLKGRP', 'BASENAME', 'NAME', 'LSADC', 
                    'FUNCSTAT', 'AREALAND', 'AREAWATER', 'CENTLAT', 'CENTLON', 'INTPTLAT', 'INTPTLON', 'OBJECTID', 
                    'hh_total', 'hh_married', 'hh_m', 'hh_fm', 'income_med', 'edu_f_total', 'edu_f_none', 'edu_f_4th',
                    'edu_f_5th6th', 'edu_f_7th8th', 'edu_f_9th', 'edu_f_10th', 'edu_f_11th', 'edu_f_12th', 'edu_f_hs', 
                    'edu_f_ad', 'edu_f_bd', 'edu_f_md', 'edu_f_ps', 'edu_f_dd', 'edu_m_total', 'edu_m_none', 'edu_m_4th',
                    'edu_m_5th6th', 'edu_m_7th8th', 'edu_m_9th', 'edu_m_10th', 'edu_m_11th', 'edu_m_12th', 'edu_m_hs', 'edu_m_ad', 
                    'edu_m_bd', 'edu_m_md', 'edu_m_ps', 'edu_m_dd', 'block group', 'geometry']
    

    # Rename gdf column names with colnames_ls
    gdf.columns = colnames_ls

    # Create one column for less than highschool diploma for female by summing lower educations together, 'edu_f_less_hs'
    gdf['edu_f_less_hs'] = (gdf['edu_f_none'] + gdf['edu_f_4th'] + gdf['edu_f_5th6th'] 
                             + gdf['edu_f_7th8th'] + gdf['edu_f_9th'] + gdf['edu_f_10th'] + gdf['edu_f_11th'] + gdf['edu_f_12th'] )

    # Create one column for less than highschool diploma for male by summing lower educations together, 'edu_m_less_hs'
    gdf['edu_m_less_hs'] = (gdf['edu_m_none'] + gdf['edu_m_4th'] + gdf['edu_m_5th6th'] 
                             + gdf['edu_m_7th8th'] + gdf['edu_m_9th'] + gdf['edu_m_10th'] + gdf['edu_m_11th'] + gdf['edu_m_12th'] )

    # Create new dataframe and drop unncessary columns of individual instances of education less than highschool for both female and male
    gdf.drop(['edu_f_none', 'edu_f_4th', 'edu_f_5th6th', 'edu_f_7th8th', 'edu_f_9th', 'edu_f_10th', 'edu_f_11th', 'edu_f_12th', 
              'edu_m_none', 'edu_m_4th', 'edu_m_5th6th', 'edu_m_7th8th', 'edu_m_9th', 'edu_m_10th', 'edu_m_11th', 'edu_m_12th'], 
              axis=1, inplace=True)
    
    # Replace -666666666.0 values with 0
    gdf.replace(-666666666.0, 0, inplace=True)
    
    return gdf