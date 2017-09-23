import io_handler as io
import tqdm
import data_handler as dh
import plotter as plot

def run():

    #df = io.read_csv_to_dataframe("boliga_prices.csv")
    
    #dh.add_geocode(df)
    
    # Temporary.
    # TODO: Add check for if CSV files are present or not. If present, load in. If not, use the dataframe from add_geocode().
    #del df
    
    #coded_dataframe = io.read_csv_to_dataframe("./geodata/geolocated_data.csv")
    #dh.format_dataframe_date(coded_dataframe)
    
    datetime_dataframe = io.read_csv_to_dataframe("./geodata/datetime_data.csv")
    #dh.average_price_per_square_meter(datetime_dataframe)
    #dh.average_price_per_square_meter_no_datetime(datetime_dataframe)
    plot.generate_scatter_plot(datetime_dataframe)


run()