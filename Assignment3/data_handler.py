import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import io_handler as io
import os
from pandas import Series
from tqdm import tqdm
from osmread import parse_file, Node

def add_geocode(sales_dataframe):
    
    coded_dataframe = sales_dataframe
    
    coded_dataframe['lat'] = np.nan
    coded_dataframe['lon'] = np.nan
    
    io.setup_dataframe_csv()
    
    # Rename with descriptive name later once coding is finished
    dataframe = concat_address_and_zipcode(coded_dataframe)
    
    dataframe.set_index("api_addresses", inplace=True)
    
    pbar = tqdm()
    for file in os.listdir('./data/'):
        if not file.endswith('xml'): continue
        for idx, decoded_node in enumerate(decode_node_to_csv(file)):
            try:
                full_address = decoded_node.tags['addr:street'] + " " + decoded_node.tags['addr:housenumber'] + " " + decoded_node.tags['addr:postcode'] + " " + decoded_node.tags['addr:city']
                addr_with_geo = (full_address,decoded_node.lon,decoded_node.lat)
            
                io.write_to_csv(addr_with_geo,"geodata/addr_with_geo.csv")
                
                pbar.update()
                
                geolocate_dataframe(dataframe,addr_with_geo)
            
            except (KeyError,ValueError):
                pass
        print('Finished parsing file: ' + file)
        
    io.write_dataframe_to_csv(dataframe,"geodata/geolocated_data.csv")
            
def decode_node_to_csv(filename):
    
    for entry in parse_file('./data/' + filename):
        
        if (isinstance(entry, Node) and 
            'addr:street' in entry.tags and 
            'addr:postcode' in entry.tags and 
            'addr:housenumber' in entry.tags and
            'addr:city' in entry.tags):

            yield entry


def geolocate_dataframe(dataframe, addr_with_geo):

    if dataframe.loc[addr_with_geo[0]] is not None:
        dataframe.set_value(addr_with_geo[0],'lon',addr_with_geo[1])
        dataframe.set_value(addr_with_geo[0],'lat',addr_with_geo[2])
    
            
def concat_address_and_zipcode(sales_dataframe):
    
    api_addresses = [' '.join([a.split(',')[0], z]) for a, z in sales_dataframe[['address', 'zip_code']].values]
    # Adds the truncated addresses 
    sales_dataframe = sales_dataframe.assign(api_addresses=api_addresses)
    # Removes all Series with duplicate values in the truncated address field
    sales_dataframe = sales_dataframe.drop_duplicates(subset="api_addresses")
    
    return sales_dataframe
    
    
def format_dataframe_date(dataframe):
    
    print ("Converting dataframe sales dates to DateTime objects, please hold.")
    dataframe['sell_date'] = pd.to_datetime(dataframe['sell_date'])
    io.write_dataframe_to_csv(dataframe,"geodata/datetime_data.csv")
    
    
    
def average_price_per_square_meter(dataframe):
    
    # There's an issue with the default cast retrieval of data from the dataframe.
    # Some years, such as 1992, get nothing, while some years, like 2016, get only some of the series in the dataframe.
    # No idea why this is happening, possibly a bug, but as a result, have to use strftime casting and str.contains() in order to retrieve all sales.
    
    # Works partially, but does not get everything. For example, all sales in '5000 Odense C' in 2016 are missing.
    #df_2016 = dataframe[dataframe['sell_date'] == '2016'] 
    
    #dataframe = dataframe[dataframe['price_per_sq_m'].apply(lambda x: isfloat(x))]
    
    # Converting the datetime objects in each series into a string for the lookup, so that '.str.contains()' can be used.
    df_1992 = get_dataframe_by_year(dataframe,'1992')
    df_2016 = get_dataframe_by_year(dataframe,'2016')
   
    mean_1992 = calculate_mean_ppsqm(df_1992)
    mean_2016 = calculate_mean_ppsqm(df_2016)
    
    mean_dataframe = pd.DataFrame({"city": ['København','Odense','Aarhus','Aalborg'], "mean_1992": mean_1992, "mean_2016": mean_2016}, columns=['city','mean_1992','mean_2016'])

    io.write_dataframe_to_csv(mean_dataframe,'./data/mean_sales.csv')
    
    
def get_dataframe_by_year(dataframe,year):
    columns_to_drop = ['address','api_addresses','sell_type','price','no_rooms','housing_type','year_of_construction','size_in_sq_m','price_change_in_pct']
    return dataframe[dataframe['sell_date'].apply(lambda x: x.strftime('%m%d%Y')).str.contains(year)] \
                                              .drop(columns_to_drop,1) \
                                              .sort_values('price_per_sq_m',ascending=True)
    
def calculate_mean_ppsqm(dataframe):
    # Seems like there's no sales in 1050/1049 in the years 1992 and 2016.
    # Might be that our scraper was too harsh.
    copenhagen_zips = dataframe[dataframe['zip_code'].str.contains('1050|1049')]
    odense_zips = dataframe[dataframe['zip_code'].str.contains('5000')]
    aarhus_zips = dataframe[dataframe['zip_code'].str.contains('8000')]
    aalborg_zips = dataframe[dataframe['zip_code'].str.contains('9000')]
    
    return calc_zip_floats([copenhagen_zips,odense_zips,aarhus_zips,aalborg_zips])
    
    
def calc_zip_floats(zip_list):
    means = []
    for zip in zip_list:
        if (len(zip['price_per_sq_m'].values) is not 0):
            float_list = create_float_array_from_zip_strings(zip['price_per_sq_m'].values)
            means.append(np.mean(float_list))
        else:
            means.append(0.0)
    return means

    
def create_float_array_from_zip_strings(zip_str_list):
    fl_list = []
    for zip in zip_str_list:
        if isfloat(zip):
            if zip is not 0:
                fl_list.append(float(zip))
        
    return fl_list
    
def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
    
    
    
    
    