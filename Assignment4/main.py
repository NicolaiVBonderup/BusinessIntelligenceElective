import io_handler as io
import data_handler as dh
import plotter as plot
import os

def run():
    
    boliga_dataframe = io.read_csv_to_dataframe("datetime_data.csv",{'year_of_construction': str, 'no_rooms': str})
    
    #sales_in_2015 = dh.get_dataframe_by_year(boliga_dataframe,2015)
    
    #cities_in_50km_radius = dh.plot_haversine_from_copenhagen(sales_in_2015)
    
    #plot.generate_basemap_for_copenhagen(cities_in_50km_radius)
    
    zip_list = []
    zip_list.extend(map(str,range(1050,1549)))
    zip_list.extend(map(str,[5000,8000,9000]))
    
    folium_df = dh.get_dataframes_by_zip(boliga_dataframe,zip_list)
    
    plot.generate_folium_map(folium_df)
    

run()