import scrapy
from scrapy import Request
from w3lib.html import remove_tags
from urllib.parse import urlencode
import json

class Product(scrapy.Item):
    # define the fields for your item here like:
    category = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
    sku = scrapy.Field()
    cost = scrapy.Field()
    quantity = scrapy.Field()
    image_1 = scrapy.Field()
    image_2 = scrapy.Field()
    image_3 = scrapy.Field()
    image_4 = scrapy.Field()
    image_5 = scrapy.Field()
    image_6 = scrapy.Field()
    image_7 = scrapy.Field()
    image_8 = scrapy.Field()
    image_9 = scrapy.Field()
    image_10 = scrapy.Field()
    image_11 = scrapy.Field()
    image_12 = scrapy.Field()
    image_13 = scrapy.Field()
    image_14 = scrapy.Field()
    image_15 = scrapy.Field()
    image_16 = scrapy.Field()
    image_17 = scrapy.Field()
    image_18 = scrapy.Field()
    image_19 = scrapy.Field()
    image_20 = scrapy.Field()

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

    def availability_request(self, id_, item):
        headers = {
            "accept": "*/*",
            "accept-language": "fr-FR,fr;q=0.9,ar-DZ;q=0.8,ar;q=0.7,en-US;q=0.6,en;q=0.5",
            "authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiJ9.eyJjaWQiOlsxXSwiY29ycyI6WyJodHRwczovL3d3dy5hdGxhbnRhY3V0bGVyeS5jb20iXSwiZWF0IjoxNzM4ODQyNDQ0LCJpYXQiOjE3Mzg2Njk2NDQsImlzcyI6IkJDIiwic2lkIjoxMDAyMTk2NTQ4LCJzdWIiOiJCQyIsInN1Yl90eXBlIjowLCJ0b2tlbl90eXBlIjoxfQ.-Q9TO2bpPFIMSoGa81kZExhBzo0zGVRph5o7pbuaa2xU1BKhKLu1H0vZUnT5KU1wPAQIZlvu2RBJKUzC7RmXAA",
            "cache-control": "no-cache",
            "content-type": "application/json",
            "cookie": "fornax_anonymousId=2dd28f6b-593d-415c-9cf6-6fe99d043368; SHOP_SESSION_TOKEN=93d48a07-ee30-4384-a6b1-646caa1df8da; ...",
            "dnt": "1",
            "origin": "https://www.atlantacutlery.com",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": "https://www.atlantacutlery.com/accusharp-worlds-fastest-sharpener",
            "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Linux"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
            "x-sf-csrf-token": "d67453b5-c7e0-4ce1-996a-a04348bedb0d",
            "x-xsrf-token": "e5109a73aeb4bf823d4f1dbed3137072f98832947e370edd3239ede62bcd2cb1",
        }

        payload = {
            "query": """
                query Getproduct {
                    site {
                        product(entityId: %s) {
                            entityId
                            name
                            sku
                            availabilityV2 {
                                status
                            }
                            inventory {
                                isInStock
                                aggregated {
                                    availableToSell
                                }
                                hasVariantInventory
                            }
                            variants(first: 50) {
                                edges {
                                    node {
                                        entityId
                                        sku
                                        isPurchasable
                                        options {
                                            edges {
                                                node {
                                                    entityId
                                                    displayName
                                                    values {
                                                        edges {
                                                            node {
                                                                entityId
                                                                label
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                        inventory {
                                            isInStock
                                            aggregated {
                                                availableToSell
                                            }
                                        }
                                        metafields(keys: ["backorder_configs", "backorder_configs", "backorder_configs"], namespace: "backorder_v2", first: 50) {
                                            edges {
                                                node {
                                                    id
                                                    entityId
                                                    key
                                                    value
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                            productOptions {
                                edges {
                                    node {
                                        entityId
                                        isRequired
                                        ... on MultipleChoiceOption {
                                            values {
                                                edges {
                                                    node {
                                                        entityId
                                                        isDefault
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                            metafields(keys: ["backorder_configs", "backorder_configs", "backorder_configs"], namespace: "backorder_v2", first: 50) {
                                edges {
                                    node {
                                        id
                                        entityId
                                        key
                                        value
                                    }
                                }
                            }
                        }
                    }
                }
            """ %(id_)
        }
        yield scrapy.Request(
            url='https://www.atlantacutlery.com/graphql',
            method="POST",
            headers=headers,
            body=json.dumps(payload),
            callback=self.parse_availability,
            meta={'item': item, 'id':id_},
            dont_filter=True
        )

    def parse_pdp(self, response):
        item = Product()
        quantity = response.xpath('//script[contains(text(), "window.storefrontSetting")]//text()').get('')
        quantity = quantity.replace('window.storefrontSetting = ', '')
        quantity = json.loads(json.loads(quantity))['in_stock_description'].lower()
        product_id = response.css('.bottomLine::attr(data-product-id)').get()

        if 'in stock now' in quantity:
            quantity = 5
        elif 'limited availability' in quantity:
            quantity = 1
        elif 'closeout' in quantity:
            quantity = 1
        elif 'not in stock' in quantity:
            quantity = 0
        elif 'pre-purchase' in quantity:
            quantity = 0


        item['category'] = response.meta['path']
        item['title'] = response.css('.productView-title::text').get()
        item['description'] = remove_tags(response.css('#FullDescription').get('')) + remove_tags(response.css('.speci').get(''))
        item['url'] = response.url
        item['sku'] = response.css('dd[data-product-sku]::text').get()
        item['cost'] = response.css('.productView-price .price--withoutTax::text').get()
        item['quantity'] = quantity
        images = response.css('.productView-thumbnail img::attr(src)').getall()
        for i, image in enumerate(images):
            item[f'image_{i+1}'] = image
        yield from self.availability_request(product_id, item)

    def parse_availability(self, response):
        item = response.meta['item']
        data = response.json()['data']['site']['product']['metafields']['edges']
        for product in data:
            product = json.loads(product['node']['value'])
            if str(product['product_id']) == str(response.meta['id']):
                if product['stock'] < 1:
                    item['quantity'] = 0
                elif 1 <= product['stock'] <= 5: 
                    item['quantity'] = 1
                else:
                    item['quantity'] = 5
                yield item