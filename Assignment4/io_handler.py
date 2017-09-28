import pandas as pd
import os
import csv
import platform
import numpy as np

def read_csv_to_dataframe(csv_path, dtype=''):
    
    dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d')
    
    if (dtype is ''):
        df = pd.read_csv(csv_path)
    else:
        df = pd.read_csv(csv_path, dtype=dtype, parse_dates=['sell_date'], date_parser=dateparse)

    return df
    
    

        