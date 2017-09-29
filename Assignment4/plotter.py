import warnings
warnings.filterwarnings('ignore')
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import folium
import data_handler as dh
import math

#def generate_scatter_plot_from_dataframe(dataframe):
#    plot = dataframe.plot(kind='scatter',x='lon',y='lat')
#    plot.get_figure().savefig('./data/latlongscatter.png')
    
def generate_basemap_for_copenhagen(dataframe):
    
    fig = plt.figure(figsize=(8, 8))
    m = Basemap(projection='lcc', resolution=None,
            width=5000000, height=5000000, 
            lat_0=55, lon_0=10,)
    #m.etopo(scale=1.0, alpha=0.5)
    
    coords = generate_coord_sets(dataframe)
    idx = 0
    for city, coord in coords.items():
        #y_adjust = 100000 if city is 'Odense' else 0
    
        x, y = m(coord[1], coord[0])
        plt.plot(x, y, 'ok', markersize=5)
    
        #plt.text(x + 50000, y - y_adjust, city, fontsize=8)
        
        
    fig.savefig('./data/copenhagen_haver.png')
    
def generate_histogram_for_sales_by_zip(dataframe):
    zips = dataframe['zip_int'].values
    
    
def generate_norreport_distance_plot(dataframe):

    norreport_geo = (55.6833306,12.569664388)
    dataframe = dataframe.assign(km_to_nrp=dh.haversine_to_location(dataframe))
    
    fig = plt.figure()
    
    y = dataframe['km_to_nrp'].values
    x = dataframe['price_per_sq_m'].values
    
    # Reverse sort
    y[::-1].sort()
    x.sort()
    
    plt.plot(x,y,'ro')
    plt.xlabel('Price Per m2, in Thousands')
    plt.ylabel('Distance to Norreport Station')
    plt.gca().invert_yaxis()
    
    fig.savefig('./data/norreport_sales.png')
    
    
def generate_coord_sets(df):
    
    lats = df['lat']
    longs = df['lon']
    
    coords = {}
    
    for idx, row in df.iterrows():
        coords[row['address']] = (row['lat'], row['lon'])
        
    return coords
    
def generate_folium_map(dataframe):
    my_map = folium.Map(location=[55.88207495748612, 10.636574309440173], zoom_start=6)

    for coords in zip(dataframe.lon.values, 
                        dataframe.lat.values):
        if not np.isnan(coords[0]):
            folium.CircleMarker(location=[coords[1], coords[0]], radius=2).add_to(my_map)
        
    my_map.save('./data/large_flat_trades.html')
    #my_map
    

    