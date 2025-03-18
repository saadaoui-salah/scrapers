import scrapy
import json
from scrapy import Request
from core.items import Product
import math

class ArgosSpider(scrapy.Spider):
    name = "argos"
    allowed_domains = ["argos.co.uk"]
    start_urls = ["https://www.argos.co.uk/"]
    custom_settings = {
        "RETRY_HTTP_CODES": [403]
    }
    def parse(self, response):
        script = response.css('#header-wrapper > script::text').get()
        categories = script.replace("window.__INITIAL_HEADER_STATE__ = ","").replace(";",'')
        categories = json.loads(categories)['taxonomy']
        for category in categories:
            for column in category['columns']:
                if type(column) == list:
                    for cat in column:
                        for link in cat['links']:
                            self.logger.info(f"Moving to category {link['title']}")
                            url = f"https://www.argos.co.uk{link['link']}"
                            yield Request(url, self.get_sub_cats)

    def get_sub_cats(self, response):
        sub_cats = response.css('li[data-el="category-item"] a::text').getall()
        for sub_cat in sub_cats:
            self.logger.info(f"New Category found {sub_cat}")
            sub_cats = response.css('li[data-el="category-item"] a::attr(href)').getall()
            for link in sub_cats:
                url = f"https://www.argos.co.uk{link}"
                yield Request(url, self.parse_products)
        
    def parse_products(self, response):
        data = response.css("#__NEXT_DATA__::text").get()
        products = []

        if data:
            data = json.loads(data)["props"]["pageProps"]
            products = data["productData"]
            if data["productMetadata"]['totalPages'] > data["productMetadata"]['currentPage']:
                yield Request(f"{response.url}opt/page:{data['productMetadata']['currentPage']+1}/") 
        else:
            data = response.xpath("//script[contains(text(), 'window.App')]//text()").get()
            data = json.loads(data)['redux']['product']
            products = data['products']
            pages = math.ceil(data['numberOfResults']/data['pageSize'])
            if data['currentPage'] < pages:
                yield Request(f"{response.url}opt/page:{data['currentPage']+1}/") 

        for product in products:
            item = Product()
            item['name'] = product['attributes']['name']
            ean = list(filter(lambda x: x['name'] == "EAN" ,product['attributes']['detailAttributes']))
            if len(ean):
                item['ean'] = ean[0]['value']
            item['url'] = f"https://www.argos.co.uk/product/{product['attributes']['productId']}"
            item['image'] = f"https://media.4rgos.it/s/Argos/{product['attributes']['productId']}_R_SET?w=270&h=270&qlt=75&fmt=webp"
            item['now_price'] = product['attributes']['price']
            item['was_price'] = product['attributes']['wasPrice']
            if item['was_price'] > 0:
                drop = ((item['was_price'] - item['now_price']) / item['was_price']) * 100
                item['price_drop'] = drop
            item['promotion'] = product['attributes']["specialOfferText"]
            yield item