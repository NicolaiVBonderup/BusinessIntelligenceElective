import pandas as pd
import os
import csv
import platform

def read_csv(csv_path):

    df = pd.read_csv(csv_path)

    return df
    
def write_to_csv(string,output_path):
    #print(string)
    
    with open(output_path, 'a', newline=define_newline(), encoding='utf-8') as f:
        output_writer = csv.writer(f)
        output_writer.writerow(string)
        


def setup_dataframe_csv():
    if not os.path.exists("geodata"):
        os.makedirs("geodata")
    
    if not os.path.exists("geodata/geolocated_data.csv"):
        # Output the .csv file in the working directory.
        create_csv_with_header("geodata/geolocated_data.csv")
        
        
def create_csv_with_header(output_path):

    title_row = ("address","zip_code","price","sell_date","sell_type","price_per_sq_m","no_rooms","housing_type","size_in_sq_m","year_of_construction","price_change_in_pct","longitude","latitude")
    with open(output_path, 'w', newline=define_newline(), encoding='utf-8') as f:
        output_writer = csv.writer(f)
        output_writer.writerow(title_row)
        
def define_newline():
    # Checks the operating system in order to determine newline rules.
    if platform.system() == 'Windows':
        return ''
    else:
        return None