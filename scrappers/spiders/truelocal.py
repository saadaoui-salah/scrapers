import scrapy
import os
from scrappers.items import Service
from scrappers.utils import read_json

class TruelocalSpider(scrapy.Spider):
    name = "truelocal"
    allowed_domains = ["truelocal.com.au"]
    start_urls = ["https://google.com"]

    def parse(self, response):
        dirs = os.listdir('./clean-data')
        for dir_ in dirs:
            yield from self.parse_json_files(dir_)

    def parse_json_files(self, dir_):
        dirs = os.listdir(f'./clean-data/{dir_}')
        for file in dirs:
            data = read_json(f'./clean-data/{dir_}/{file}')
            yield from self.parse_data(data, dir_)

    def parse_data(self, data, dir_):
        services = data['data']['listing']
        for service in services:
            email = list(filter(lambda x: x['type'] == 'email', service['contacts']['contact']))
            website = list(filter(lambda x: x['type'] == 'website', service['contacts']['contact']))
            phone_number = list(filter(lambda x: x['type'] in ['phone', 'fax', 'mobile'], service['contacts']['contact']))
            email = email[0]['value'] if email else None
            website = website[0]['value'] if website else ''
            phone_number = phone_number[0]['value'] if phone_number else None
            social_media = None
            address = service['matchAddress']
            if 'facebook.com' in website:
                social_media = website
                website = ''
            elif 'instagram.com' in website:
                social_media = website
                website = ''
            elif 'linkedin.com' in website:
                social_media = website
                website = ''

            item = Service()
            item['business_name'] = service['name']
            item['abn'] = service['abn']
            item['trade_type'] = dir_
            item['description'] = service['description']
            item['phone_number'] = phone_number
            item['email'] = email
            item['social_media'] = social_media
            item['category'] = service['primaryCategory']['name']
            item['location'] = f'{address['streetNo']} {address['streetName']} {address['streetType']}, {address['suburb']}, {address['state']}, {address['postcode']}'
            item['reviews'] = service['statistics']['reviews']
            item['rating_avg'] = service['statistics']['averageRating']
            item['availability'] = service['openingHours'] if 'openingHours' in list(service.keys()) else None
            item['website'] = website
            item['current_url'] = f"https://www.truelocal.com.au/business/{service['seoUrl']}"
            yield item