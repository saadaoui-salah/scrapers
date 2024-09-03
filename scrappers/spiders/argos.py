import scrapy
import json
from scrapy import Request

class ArgosSpider(scrapy.Spider):
    name = "argos"
    allowed_domains = ["argos.co.uk"]
    start_urls = ["https://www.argos.co.uk/"]

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
