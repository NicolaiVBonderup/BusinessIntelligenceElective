import io_handler as io
import data_handler as dh
import plotter as plot
import os

def run():

    if not os.path.exists("./geodata/geolocated_data.csv"):
        print("Geolocated data not found. Processing .osm and adding geolocations to sales data.")
        generate_geocoded_data()
    
    if not os.path.exists("./geodata/datetime_data.csv"):
        print("Present data has not been cast to datetime64. Processing sales dates.")
        generate_datetime_data()
    
    datetime_dataframe = io.read_csv_to_dataframe("./geodata/datetime_data.csv",{'year_of_construction': str, 'no_rooms': str})
    
    if not os.path.exists("./data/mean_sales.csv"):
        print("Mean sales of select cities not found. Processing sales data.")
        dh.average_price_per_square_meter(datetime_dataframe)
    
    generate_scatter_plots(datetime_dataframe)

    
def generate_geocoded_data():
    df = io.read_csv_to_dataframe("boliga_prices.csv")
    dh.add_geocode(df)
    
def generate_datetime_data():
    coded_dataframe = io.read_csv_to_dataframe("./geodata/geolocated_data.csv")
    dh.format_dataframe_date(coded_dataframe)
    
def generate_scatter_plots(datetime_dataframe):
    print("Generating scatter plot for full sales data.")
    plot.generate_scatter_plot_from_dataframe(datetime_dataframe)
    print("Generating scatter plot with pretty colors.")
    plot.plot_haversine_for_roskilde(datetime_dataframe)

run()