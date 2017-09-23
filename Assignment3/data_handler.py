import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import io_handler as io
import os
from tqdm import tqdm
from osmread import parse_file, Node

def add_geocode(sales_dataframe):
    
    #coded_dataframe = sales_dataframe
    
    #coded_dataframe['lat'] = np.nan
    #coded_dataframe['long'] = np.nan
    
    io.setup_dataframe_csv()
    
    # Rename with descriptive name later once coding is finished
    #df = concat_address_and_zipcode(coded_dataframe)
    
    pbar = tqdm()
    for file in os.listdir('./data/'):
        if not file.endswith('xml'): continue
        for idx, decoded_node in enumerate(decode_node_to_csv(file)):
            try:
                full_address = decoded_node.tags['addr:street'] + " " + decoded_node.tags['addr:housenumber'] + " " + decoded_node.tags['addr:postcode'] + " " + decoded_node.tags['addr:city']
                addr_with_geo = (full_address,decoded_node.lon,decoded_node.lat)
            
                io.write_to_csv(addr_with_geo,"geodata/addr_with_geo.csv")
            
                pbar.update()
            
            except (KeyError,ValueError):
                pass
        print('Finished parsing file: ' + file)
            
def decode_node_to_csv(filename):
    
    for entry in parse_file('./data/' + filename):
        
        if (isinstance(entry, Node) and 
            'addr:street' in entry.tags and 
            'addr:postcode' in entry.tags and 
            'addr:housenumber' in entry.tags and
            'addr:city' in entry.tags):

            yield entry


def concat_address_and_zipcode(sales_dataframe):
    
    
    api_addresses = [' '.join([a.split(',')[0], z]) for a, z in sales_dataframe[['address', 'zip_code']].values]
    # Adds the truncated addresses 
    sales_dataframe = sales_dataframe.assign(api_addresses=api_addresses)
    # Removes all Series with duplicate values in the truncated address field
    sales_dataframe = sales_dataframe.drop_duplicates(subset="api_addresses")
    
    return sales_dataframe