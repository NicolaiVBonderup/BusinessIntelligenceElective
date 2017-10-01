import io_handler as io
import data_handler as dh
import plotter as plot
import os

def run():

    #### Setup
    
    boliga_dataframe = io.read_csv_to_dataframe("datetime_data.csv",{'year_of_construction': str, 'no_rooms': str})
    boliga_dataframe = dh.create_int_zip_label(boliga_dataframe)
    
    #### Step 1
    
    #generate_cph_basemap(boliga_dataframe)
    
    #### Step 2
    
    #generate_folium_map(boliga_dataframe)
    
    #### Step 3
    
    #generate_norreport_distance_plot(boliga_dataframe)
    
    #### Step 4
    
    #generate_zip_trade_histogram(boliga_dataframe)
    
    #### Step 5
    
    generate_zip_trade_3d(boliga_dataframe)
    
    #### Step 6
    
    
    
def generate_zip_trade_3d(dataframe):
    
    sales_by_zip = dh.get_house_trade_freq_by_zipcode(dataframe)
    plot.generate_3d_histogram(sales_by_zip)
    
def generate_zip_trade_histogram(dataframe):
    
    sales_by_zip = dh.get_house_trade_freq_by_zipcode(dataframe)
    plot.generate_histogram_for_sales_by_zip(sales_by_zip)
    
    s = dh.get_house_trade_freq_with_room_no(dataframe)
    plot.generate_histogram_by_room_numbers(s)
    
def generate_cph_basemap(dataframe):
    
    sales_in_2015 = dh.get_dataframe_by_year(dataframe,2015)
    
    cities_in_50km_radius = dh.plot_haversine_from_copenhagen(sales_in_2015)
    
    plot.generate_basemap_for_copenhagen(cities_in_50km_radius)
    
def generate_folium_map(dataframe):
    
    zip_list = []
    zip_list.extend(range(1050,1549))
    zip_list.extend([5000,8000,9000])
    
    folium_df = dh.get_dataframes_by_zip(dataframe,zip_list)
    
    plot.generate_folium_map(folium_df)
    
def generate_norreport_distance_plot(dataframe):
    
    sales_in_2005 = dh.get_dataframe_by_year(dataframe,2005)
    norreport_df = dh.get_dataframes_by_zip(dataframe,zips_for_sjaelland())
    norreport_df = norreport_df[norreport_df['price_per_sq_m'] >= 80.000]
    
    plot.generate_norreport_distance_plot(norreport_df)
    
    
    
def zips_for_sjaelland():
    # Creating a list with every zipcode on Sjælland
    zips = []
    zips.extend(range(1000,3670))
    zips.extend(range(4000,4793))
    return zips
    

run()