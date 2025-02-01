import scrapy
from scrapy import Request
from w3lib.html import remove_tags
from urllib.parse import urlencode


class Product(scrapy.Item):
    # define the fields for your item here like:
    category = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
    sku = scrapy.Field()
    cost = scrapy.Field()
    quantity = scrapy.Field()
    images = scrapy.Field()

class AtlantacutlerySpider(scrapy.Spider):
    name = "atlantacutlery"
    start_urls = ["https://www.atlantacutlery.com/made-in-the-usa"]
    params = {
        'lastViewed': '404171,404809',
        'userId': 'a40b235c-dd67-4c3d-a38f-a98eb5fbe824',
        'domain': '',
        'sessionId': '40f1d1fb-a5ca-4e3e-94dc-75efd39ef98b',
        'pageLoadId': '27ac131a-2626-4dc6-9b0e-72d36632f456',
        'siteId': 'fkfsk9',
        'bgfilter.categories_hierarchy': '',
        'redirectResponse': 'full',
        'ajaxCatalog': 'Snap',
        'resultsFormat': 'native',
    }
    api_url = 'https://fkfsk9.a.searchspring.io/api/search/search.json?{}'


    def parse(self, response):
        categories = response.css('#navList-treeview > .navPages-item')
        for category in categories:
            name = category.css('a::text').get()
            sub_categories = category.css('ul li')
            if sub_categories:
                for sub_category in sub_categories:
                    sub_name = sub_category.css('a::text').get()
                    url = sub_category.css('a::attr(href)').get()
                    path = f'{name}>{sub_name}'
                    self.params['domain'] = url 
                    self.params['bgfilter.categories_hierarchy'] = path 
                    yield Request(
                        url=self.api_url.format(urlencode(self.params)),
                        callback=self.parse_products,
                        meta={'path': path}
                    )
            else:
                url = category.css('a::attr(href)').get()
                self.params['domain'] = url 
                self.params['bgfilter.categories_hierarchy'] = name
                yield Request(
                    url=self.api_url.format(urlencode(self.params)),
                    callback=self.parse_products,
                    meta={'path': path}
                )

    def parse_products(self, response):
        data = response.json()
        for product in data['results']:
            yield Request(
                url=product['url'],
                callback=self.parse_pdp,
                meta=response.meta
            )
        pagination = data['pagination']
        if pagination['currentPage'] == 1 and pagination['totalPages'] > 1:            
            for i in range(pagination['totalPages']):
                if i >= 1:
                    self.params['domain'] = response.url 
                    self.params['page'] = i+1 
                    self.params['bgfilter.categories_hierarchy'] = response.meta['path']
                    yield Request(
                        url=self.api_url.format(urlencode(self.params)),
                        callback=self.parse_products,
                        meta=response.meta
                    )

    def parse_pdp(self, response):
        item = Product()
        item['category'] = response.meta['path']
        item['title'] = response.css('.productView-title::text').get()
        item['description'] = remove_tags(response.css('#FullDescription').get(''))
        item['url'] = response.url
        item['sku'] = response.css('dd[data-product-sku]::text').get()
        item['cost'] = response.css('.productView-price .price--withoutTax::text').get()
        item['images'] = response.css('.productView-thumbnail img::attr(src)').getall()
        yield item