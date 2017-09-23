import io_handler as io
import tqdm
import data_handler as dh


def run():

    df = io.read_csv("boliga_prices.csv")
    
    dh.add_geocode(df)


run()