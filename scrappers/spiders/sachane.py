import scrapy
from scrapy import Request
import json
from scrappers.items import Product
import math


class SachaneSpider(scrapy.Spider):
    name = "sachane"
    allowed_domains = ["sachane.com"]
    start_urls = ["https://sachane.com/markalar"]
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Te": "trailers"
    }
    ITEMS_PER_PAGE = 100
    api_url = 'https://sch.sachane.com/api.php?_d=Products&sa_mbl=1&subcats=Y&cid={}&items_per_page={}&sort_by=popularity&sort_order=desc&page={}&status=A'

    def start_requests(self):
        yield Request(
            url='https://sachane.com/markalar',
            callback=self.parse_brands,
            headers=self.headers
        )

    def parse_brands(self, response):
        data = json.loads(response.css("#__NEXT_DATA__::text").get())
        categories = data['props']['pageProps']['data']
        categories = list(categories.values())
        for list_ in categories:
            for category in list_:
                url = self.api_url.format(category["category_id"], self.ITEMS_PER_PAGE, 1)
                yield Request(
                    url=url,
                    callback=self.parse_products,
                    headers=self.headers,
                    meta={'category_id': category['category_id']}
                )
    
    def parse_products(self, response):
        data = response.json()
        products = data['products']

        for product in products:
            item = Product()
            item['title'] = product['product']
            item['url'] = f"https://sachane.com/{product['seo_name']}-p-{product['product_id']}"
            item['image'] = product['main_pair']['detailed']['image_path']
            item['price'] = round(float(product['price']), 2)
            yield Request(
                url=item['url'],
                callback=self.parse_pdp,
                headers=self.headers,
                meta={'item': item}
            )
        if (pages := int(data['params']['total_items'])) > self.ITEMS_PER_PAGE and response.meta.get('category_id'):
            pages = math.ceil(round(int(pages)/self.ITEMS_PER_PAGE))
            for i in range(1, pages):
                url = self.api_url.format(response.meta["category_id"],self.ITEMS_PER_PAGE, i+1)
                yield Request(
                    url=url,
                    callback=self.parse_products,
                    headers=self.headers,
                )
        
    def parse_pdp(self, response):
        data = json.loads(response.css("#__NEXT_DATA__::text").get())
        item = response.meta['item']
        product = data['props']['pageProps']['data']
        item['brand'] = product['schema_brand'].replace('\t', '')
        item['upc'] = product['schema_gtin']
        yield item