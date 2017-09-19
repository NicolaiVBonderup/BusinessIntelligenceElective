import reader
import tqdm


def run():

    df = reader.read_csv("boliga_prices.csv")
    
    pbar = tqdm(total=len(df))
    pbar.clear()

    print(df)


run()