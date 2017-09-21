import pandas as pd
import matplotlib.pyplot as plt
from osmread import parse_file, Node

def add_geocode(sales_dataframe):
    
    coded_dataframe['lat'] = np.nan
    coded_dataframe['long'] = np.nan
    
    for idx, decoded_node in enumerate(decode_node_to_csv()):
        if idx > 100:
            break
        print(idx, decoded_node)
    
    
    
def decode_node_to_csv():

    for entry in parse_file('./data/denmark-latest.osm'):
        if (isinstance(entry, Node) and 
            'addr:street' in entry.tags and 
            'addr:postcode' in entry.tags and 
            'addr:housenumber' in entry.tags):

            yield entry


