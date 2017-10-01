import warnings
warnings.filterwarnings('ignore')
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import pylab as P
import numpy as np
import folium
import data_handler as dh
import math
from tqdm import tqdm 

def generate_histogram_by_room_numbers(sales):
    
    fig = plt.figure()
    
    zip_ints = []
    rooms_dict = {}
    rooms_col = []
    highest_y = 0
    
    for zip, room_dict in sales.items():
        rooms_amounts = []
        for rooms, amount in room_dict.items():
            if (amount > highest_y) : 
                highest_y = amount
            rooms_amounts.append(amount)
        rooms_col.append(rooms_amounts)
        zip_ints.append(zip)
        
    
    rooms_col = np.asarray(rooms_col)
    bins = len(rooms_col)
    
    n, bins, patches = plt.hist(rooms_col, bins, normed=1, cumulative=True, histtype='bar', stacked=True)
    
    
    fig.savefig('./data/histogram_by_rooms.png')
    
def generate_3d_histogram(sales_by_zip):
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    # Cannot use zip(), too many items. Have to iterate.
    x = []
    y = []
    for zip, no_of_sales in sales_by_zip.items():
        x.append(zip)
        y.append(no_of_sales)
    
    hist, xedges, yedges = np.histogram2d(x, y, bins=(7,7))
    xpos, ypos = np.meshgrid(xedges[:-1] + xedges[1:], yedges[:-1] + yedges[1:])
    
    print (xedges[:-1])
    print (xedges[1:])
    print (yedges[:-1])
    print (yedges[1:])
    
    xpos = xpos.flatten()/2
    ypos = ypos.flatten()/2
    zpos = np.zeros_like(xpos)
    
    dx = xedges [1] - xedges [0]
    dy = yedges [1] - yedges [0]
    dz = hist.flatten()

    ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color='b', zsort='average')
    
    fig.savefig('./data/sales_by_zip_3d.png')
    
def generate_basemap_for_copenhagen(dataframe):
    
    fig = plt.figure(figsize=(8, 8))
    m = Basemap(projection='lcc', resolution=None,
            width=5000000, height=5000000, 
            lat_0=55, lon_0=10,)
    
    coords = generate_coord_sets(dataframe)
    idx = 0
    for city, coord in coords.items():
    
        x, y = m(coord[1], coord[0])
        plt.plot(x, y, 'ok', markersize=5)
    
    fig.savefig('./data/copenhagen_haver.png')
    
def generate_histogram_for_sales_by_zip(sales_by_zip):
    
    fig = plt.figure(figsize=(80,15))
    
    # Cannot use zip(), too many items. Have to iterate.
    x = []
    y = []
    for zip, no_of_sales in sales_by_zip.items():
        x.append(zip)
        y.append(no_of_sales)
    
    plt.bar(x,y,align='center')
    
    fig.savefig('./data/sales_by_zip.png')
    
    
    
def generate_norreport_distance_plot(dataframe):

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
    
def generate_kfc_distance_plot(dataframe):

    # Again, refactor if have time.
    
    fig = plt.figure()
    
    y = dataframe['km_to_kfc'].values
    x = dataframe['price_per_sq_m'].values
    
    # Reverse sort
    y[::-1].sort()
    x.sort()
    
    plt.plot(x,y,'ro')
    plt.xlabel('Price Per m2, in Thousands')
    plt.ylabel('Distance to Nearest KFC')
    plt.gca().invert_yaxis()
    
    fig.savefig('./data/kfc_sales.png')
    
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
    

    