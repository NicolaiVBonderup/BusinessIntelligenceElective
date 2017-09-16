# -*- coding: utf-8 -*-
import scrapy
import os
import platform
import csv
import collections
from tqdm import tqdm

class SalesSpider(scrapy.Spider):
    name = 'sales'
    allowed_domains = ['138.197.184.35']
    start_urls = ['http://138.197.184.35/boliga/']
    base_url = 'http://138.197.184.35/boliga/'
    
    
    # Add checks for if zipcode follows zipcode rules, lots of nonconforming values that need to be removed
    
    def __init__(self, zip_split='', *args, **kwargs):
        super(SalesSpider, self).__init__(*args, **kwargs)
        # Argument to determine if we're making one big CSV file, or CSV files separated by zip code.
        self.zip_split = zip_split
        
        # Checks the operating system in order to determine newline rules.
        if platform.system() == 'Windows':
            self.newline = ''
        else:
            self.newline = None
        
        if (zip_split is ''):
            print("zip_split argument not applied, saving data into one file.")
            self.zip_split = 'n'
        elif (zip_split is 'y'):
            print("Saving data into zipcode-separated CSV files. This will take a while.")
            # Using a dict as a lookup table for zipcodes
            # Dict lookup is O(1), list lookup is O(n)
            self.zip_dict = {'key':'value'}
            self.setup_file_split_zips()
        elif (zip_split is 'n'):
            print("Saving data into single CSV file.")
            self.setup_file()
        else:
            print("Invalid zip_split parameter.")
            quit()
            
            
        
    
    def start_requests(self):
            
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):

        pages_to_crawl = response.xpath('//a/@href').extract()
        page_amount = len(pages_to_crawl)
        
        # Instantiates a progress bar in the CLI through tqdm
        self.pbar = tqdm(total=page_amount)
        self.pbar.clear()
        
        for page in pages_to_crawl:
            yield scrapy.Request(self.base_url + page, callback=self.parse_page)
            
            
        pass
        

        
    def parse_page(self, response):

        data_rows = []
        rows = response.css('tr')
        
        for row in rows:

            data_row = (
                row.xpath('td[1]/h5/a/text()[1]').extract_first(),
                row.xpath('td[1]/h5/a/text()[2]').extract_first(),
                row.xpath('td[2]/h5/text()').extract_first(),
                row.xpath('td[3]/h5/text()[1]').extract_first(),
                row.xpath('td[3]/h5/text()[2]').extract_first(),
                row.xpath('td[4]/h5/text()').extract_first(),
                row.xpath('td[5]/h5/text()').extract_first(),
                row.xpath('td[6]/h5/text()').extract_first(),
                row.xpath('td[7]/h5/text()').extract_first(),
                row.xpath('td[8]/h5/text()').extract_first(),
            )
            
            
                
            
            # Checks if the row is filled with null values.
            if (data_row[0] is not None):
                # Checks if the zipcode row contains a valid zipcode
                zip_values = data_row[1].split()
                if (zip_values[0].isdigit() and len(zip_values[0]) is 4):
                    data_rows.append(data_row)
        
        
        if (self.zip_split is 'y'):
            self.save_rows_separate(data_rows,zip_values[0])
        else:
            self.save_rows(data_rows)
        
        
    def save_rows_separate(self, data_rows, zipcode):
    
        csv_output_path = 'sales/' + zipcode + '.csv'
        is_zip_file_created = self.dict_zip_lookup(zipcode)
    
        # Open/Create the file, then write the tuples to it.
        with open(csv_output_path, 'a', newline=self.newline, encoding='utf-8') as f:
            for row in data_rows:
                
                # Using a dict lookup instead of directory lookup to avoid I/O operations
                if not is_zip_file_created:
                    self.create_csv_with_header(csv_output_path)
                else:
                
                    output_writer = csv.writer(f)
                    output_writer.writerow(row)
                
        # Updates the progress bar
        self.pbar.update()
        
        
    def save_rows(self, data_rows):
        
        # Open/Create the file, then write the tuples to it.
        with open(self.csv_output_path, 'a', newline=self.newline, encoding='utf-8') as f:
            output_writer = csv.writer(f)
            for row in data_rows:
                output_writer.writerow(row)
                
        # Updates the progress bar
        self.pbar.update()
            
            
            
    def dict_zip_lookup(self, zipcode):
        # If zipcode is in the dict, we have a file for it already.
        if (zipcode in self.zip_dict):
            return True
        # If zipcode is not in dict, we need to create a file for it.
        else:
            self.zip_dict[zipcode] = zipcode
            return False
                
    def setup_file(self): 
        self.csv_output_path = os.path.join(os.getcwd(), "boliga_prices.csv")
    
        if not os.path.exists("boliga_prices.csv"):
            # Output the .csv file in the working directory.
            self.create_csv_with_header(self.csv_output_path)
                
    def setup_file_split_zips(self):
        if not os.path.exists("sales"):
            os.makedirs("sales")
     
    def create_csv_with_header(self, output_path):
        title_row = ("address","zip_code","price","sell_date","sell_type","price_per_sq_m","no_rooms","housing_type","size_in_sq_m","year_of_construction","price_change_in_pct")
        with open(output_path, 'w', newline=self.newline, encoding='utf-8') as f:
            output_writer = csv.writer(f)
            output_writer.writerow(title_row)
        
