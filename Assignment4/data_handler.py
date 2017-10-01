import pandas as pd
import math
import collections

def create_int_zip_label(dataframe):
    zip_df = pd.DataFrame(dataframe['zip_code'].str.split(' ',1).tolist(), columns = ['zip','city'])
    dataframe = dataframe.assign(zip_int=zip_df['zip'])
    dataframe['price_per_sq_m'] = pd.to_numeric(dataframe['price_per_sq_m'], errors='coerce')
    dataframe['zip_int'] = pd.to_numeric(dataframe['zip_int'], errors='coerce')
    return dataframe

def get_house_trade_freq_by_zipcode(dataframe):
    
    unique_zips = dataframe['zip_int'].unique()
    unique_zips.sort()
    # Sorted by order of insertion, so we sort the zips first.
    sales_by_zip = collections.OrderedDict()
    
    for zip in unique_zips:
        no_of_sales = len(dataframe[dataframe['zip_int'] == zip])
        sales_by_zip[zip] = no_of_sales
        
    return sales_by_zip
    
def get_house_trade_freq_with_room_no(dataframe):
    
    unique_zips = dataframe['zip_int'].unique()
    unique_zips.sort()
    # Sorted by order of insertion, so we sort the zips first.
    sales_by_zip = collections.OrderedDict()
    
    num_rooms_variance = range(1,20)
    num_rooms_variance = [str(i) for i in num_rooms_variance]
    
    for zip in unique_zips:
        
        zip_df = dataframe[dataframe['zip_int'] == zip]
        rooms_dict = {}
        
        for room_amount in num_rooms_variance:
            occurences = len(zip_df[zip_df['no_rooms'] == room_amount])
            #if occurences > 0:
            rooms_dict[room_amount] = occurences
            
        sales_by_zip[zip] = rooms_dict
    
    
    return sales_by_zip
    
    
    
def get_dataframe_by_year(dataframe,requested_year):

    return dataframe[dataframe['sell_date'].dt.year == requested_year]
    
    
def get_dataframes_by_zip(dataframe,zip_list):

    return dataframe[dataframe['zip_int'].isin(zip_list)]
    
def haversine_to_location(mult,dataframe):
    
    # For every series, plot haversine distance from lat and long. 'axis' tells it to read it row by row on the Y axis, instead of X.
    if mult is 1:
        return dataframe.apply(lambda row: multiple_haversines(row),axis=1)
    else:
        return dataframe.apply(lambda row: calc_haversine(row),axis=1)
    
    
def plot_haversine_from_copenhagen(dataframe):
    
    # For every series, plot haversine distance from lat and long. 'axis' tells it to read it row by row on the Y axis, instead of X.
    
    dataframe = dataframe.assign(km_to_cph=haversine_to_location(0,dataframe))
    
    return dataframe[dataframe['km_to_cph'] <= 50]
    
def plot_haversine_from_kfc(dataframe):
    
    return dataframe.assign(km_to_kfc=haversine_to_location(1,dataframe))
    
def multiple_haversines(row):
    
    kfc_geos = [(55.676448,12.569685),(55.659483,12.606444),(55.631115,12.577801),(55.671519,12.455936)]
    results = []
    for kfc in kfc_geos:
        results.append(calc_haversine(row,kfc))
    return min(results)
   
#def calc_haversine_kfc(kfc,row):

    # Done in a hurry, will refactor if have the time

#    lat_orig, lon_orig = kfc
#    lat_dest = row['lat']
#    lon_dest = row['lon']
    
#    radius = 6371

 #   dlat = math.radians(lat_dest-lat_orig)
 #   dlon = math.radians(lon_dest-lon_orig)
 #   a = (math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat_orig)) 
 #       * math.cos(math.radians(lat_dest)) * math.sin(dlon / 2) * math.sin(dlon / 2))
 #   c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
 #   d = radius * c

    return d
   
def calc_haversine(row,kfc=''):
    
    if kfc is not '':
        lat_orig, lon_orig = kfc
    else:
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