# -*- coding: utf-8 -*-
import scrapy
import os
import platform
import csv
import collections


class SalesSpider(scrapy.Spider):
    name = 'sales'
    allowed_domains = ['138.197.184.35']
    start_urls = ['http://138.197.184.35/boliga/']
    base_url = 'http://138.197.184.35/boliga/'

    def parse(self, response):

        pages_to_crawl = response.xpath('//a/@href').extract()

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
        
        # Checks the operating system in order to determine newline rules.
        if platform.system() == 'Windows':
            newline = ''
        else:
            newline = None
        
        # Checks if the .csv file exists.
        # If it doesn't, create the file, and add a header. If it does, just append to the file.
        if os.path.exists("boliga_prices.csv"):
            append_write = 'a'
        else:
            append_write = 'w'
            title_row = ("address","zip_code","price","sell_date","sell_type","price_per_sq_m","no_rooms","housing_type","size_in_sq_m","year_of_construction","price_change_in_pct")
            data_rows = [title_row] + data_rows

        # Output the .csv file in the working directory.
        csv_output_path = os.path.join(os.getcwd(), "boliga_prices.csv")

        # Open/Create the file, then write the tuples to it.
        with open(csv_output_path, append_write, newline=newline, encoding='utf-8') as f:
            output_writer = csv.writer(f)
            for row in data_rows:
                output_writer.writerow(row)
        
        
