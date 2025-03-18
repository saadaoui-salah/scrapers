import json
import scrapy
from  scrapy import Selector
from core.items import Service
import os
from w3lib.html import remove_tags 

class GumtreeSpider(scrapy.Spider):
    name = "gumtree"
    start_urls = ["https://www.google.com/"]

    def parse(self, response):
        for file in os.listdir('/home/pydev/Desktop/scrappers/html'):
            with open(f"/home/pydev/Desktop/scrappers/html/{file}", 'r', encoding='utf-8') as f:
                html_content = f.read()
            response = Selector(text=html_content)
            yield from self.parse_results(response, file)

    def parse_data(self, response):
        if data := response.css('#__NEXT_DATA__::text').get():
            data = json.loads(data)
            return data

    def parse_results(self, response, file):
        data = self.parse_data(response)

        results = json.load(open("/home/pydev/Desktop/scrappers/results.json"))
        pdp_data = list(filter(lambda x: file.replace(' ', '').replace('(1)', '').replace('.html', '').replace('_', '/') == x['pdp'], results))[0]
        avg = pdp_data['review']['score'] if isinstance(pdp_data['review'], dict) else 0
        count = pdp_data['review']['count'] if isinstance(pdp_data['review'], dict) else 0

        description = response.css('#descriptionContainer p::text').getall()
        description = ''.join(description) + remove_tags(response.css('.vip-ad-description__content').get(''))
        location = response.css('.vip-ad-title__location-address::text').get()
        abn = remove_tags(response.css('.vip-ad-attributes__item').get(''))
        services = response.css('.vip-ad-services__item-text::text').getall()
        availability = response.css('.trading-hours__item::text').get('')
        website = response.css('.view-item-page__seller-website a::attr(href)').get()
        name = response.css('.vip-ad-title__header::text').get('')
        categories = response.css('.breadcrumbs__desktop span a::text').getall()
        category  = categories[-1] if categories else None
        email = ''
        phone_number = ''
        if data:
            needed_data = list(filter(lambda x: '/fetchers/vipinitdata' in x['queryHash'], data['props']['pageProps']['dehydratedState']['queries']))[0]
            needed_data = needed_data['state']['data'] 
            website = needed_data.get('website')
            description = needed_data['description']
            category = needed_data['categoryName']
            name = needed_data['title']
            phone_number = '\n'.join([info.get('phoneNumber', '') for info in needed_data.get('externalProviderData',{}).get('listingAgentsData', [])])
            location = list(filter(lambda x: 'IconPinLocation' in x['icon'], needed_data['listingInfo']))[0]
            location = location['value']
            email = list(filter(lambda x: '/fetchers/vipextendedmetadata' in x['queryHash'], data['props']['pageProps']['dehydratedState']['queries']))[0]
            email = email['state']['data']['common']['user']['email']


        item = Service()
        item['business_name'] = name
        item['abn'] = abn
        item['trade_type'] = pdp_data['keyword']
        item['description'] = description
        item['email'] = email
        item['phone_number'] = phone_number
        item['category'] = category
        item['location'] = location
        item['reviews'] = count
        item['rating_avg'] = avg
        item['specializations'] = services
        item['availability'] = availability
        item['website'] = website
        item['current_url'] = f"https://www.gumtree.com.au{pdp_data['pdp']}"
        yield item