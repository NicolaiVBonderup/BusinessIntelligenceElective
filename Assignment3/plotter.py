import pandas as pd
import matplotlib.pyplot as plt
import math
import io_handler as io
import os
from pandas import Series

def generate_scatter_plot_from_dataframe(dataframe):
    plot = dataframe.plot(kind='scatter',x='lon',y='lat')
    plot.get_figure().savefig('latlongscatter.png')
    
def generate_scatter_plot_from_roskilde(lats,longs,distances):
    plot = plt.scatter(longs,lats,c=distances)
    plot.get_figure().savefig('roskildescatter.png')
    
def plot_haversine_for_roskilde(dataframe):
    
    lat_list = dataframe['lat'].tolist()
    long_list = dataframe['lon'].tolist()
    latlong_tuples = zip(lat_list,long_list)
    roskilde_distance = (55.65,12.083333)
    haversine_distances = []
    for sale in latlong_tuples:
        distance = haversine_distance(roskilde_distance, sale)
        haversine_distances.append(distance)
    generate_scatter_plot_from_roskilde(lat_list,long_list,haversine_distances)
    
def haversine_distance(origin, destination):

    lat_orig, lon_orig = origin
    lat_dest, lon_dest = destination
    radius = 6371

    dlat = math.radians(lat_dest-lat_orig)
    dlon = math.radians(lon_dest-lon_orig)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat_orig)) 
        * math.cos(math.radians(lat_dest)) * math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c

    return d