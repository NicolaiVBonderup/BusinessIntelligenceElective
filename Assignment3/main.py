import reader
import tqdm
import data_handler as dh


def run():

    df = reader.read_csv("boliga_prices.csv")
    
    #pbar = tqdm(total=len(df))
    #pbar.clear()

    #print(df)
    dh.add_geocode(df)


run()