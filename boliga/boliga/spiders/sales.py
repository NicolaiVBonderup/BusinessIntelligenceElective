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
    
    
    def start_requests(self):
        self.setup_file()
        
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
                data_rows.append(data_row)
        
        
        self.save_rows(data_rows)
        
        
    def save_rows(self, data_rows):
        
        # Open/Create the file, then write the tuples to it.
        with open(self.csv_output_path, 'a', newline=self.newline, encoding='utf-8') as f:
            output_writer = csv.writer(f)
            for row in data_rows:
                output_writer.writerow(row)
                
        # Updates the progress bar
        self.pbar.update()
            
            
                
    def setup_file(self): 
        self.csv_output_path = os.path.join(os.getcwd(), "boliga_prices.csv")
    
        # Checks the operating system in order to determine newline rules.
        if platform.system() == 'Windows':
            self.newline = ''
        else:
            self.newline = None
    
        if not os.path.exists("boliga_prices.csv"):
            # Output the .csv file in the working directory.
            title_row = ("address","zip_code","price","sell_date","sell_type","price_per_sq_m","no_rooms","housing_type","size_in_sq_m","year_of_construction","price_change_in_pct")
            with open(self.csv_output_path, 'w', newline=self.newline, encoding='utf-8') as f:
                output_writer = csv.writer(f)
                output_writer.writerow(title_row)
        
        
        
