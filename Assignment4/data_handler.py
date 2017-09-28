import pandas as pd
import math

def get_dataframe_by_year(dataframe,requested_year):

    return dataframe[dataframe['sell_date'].dt.year == requested_year]
    
    
def get_dataframes_by_zip(dataframe,zip_list):
    pattern = '|'.join(zip_list)
    return dataframe[dataframe['zip_code'].str.contains(pattern)]
    
    
def plot_haversine_from_copenhagen(dataframe):

    
    # For every series, plot haversine distance from lat and long. 'axis' tells it to read it row by row on the Y axis, instead of X.
    hav_series = dataframe.apply(lambda row: plot_haversine_for_copenhagen(row),axis=1)
    dataframe = dataframe.assign(km_to_cph=hav_series)
    
    return dataframe[dataframe['km_to_cph'] <= 50]
    
   
def plot_haversine_for_copenhagen(row):

    lat_orig, lon_orig = (55.676111,12.568333)
    lat_dest = row['lat']
    lon_dest = row['lon']
    
    radius = 6371

    dlat = math.radians(lat_dest-lat_orig)
    dlon = math.radians(lon_dest-lon_orig)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat_orig)) 
        * math.cos(math.radians(lat_dest)) * math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c

    return d