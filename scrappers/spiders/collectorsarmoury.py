import scrapy
from scrapy import Request
from w3lib.html import remove_tags


class Product(scrapy.Item):
    # define the fields for your item here like:
    category = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
    sku = scrapy.Field()
    price = scrapy.Field()
    MSRP = scrapy.Field()
    upc = scrapy.Field()
    Type = scrapy.Field()
    brand = scrapy.Field()
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



class CollectorsarmourySpider(scrapy.Spider):
    name = "collectorsarmoury"
    start_urls = ["https://collectorsarmoury.com"]

    def start_requests(self):
        self.cookies = {
            "fornax_anonymousId": "4b1e7554-d5dd-4acb-8c04-426c6b2971e6",
            "cliID": "be3f299f-fbb3-4d6d-a414-9401003582f9",
            "SF-CSRF-TOKEN": "04a90880-1a86-45b3-b578-35e7406b574e",
            "athena_short_visit_id": "effc58c3-131e-4015-a0d2-2fa0468fedf9:1738807353",
            "XSRF-TOKEN": "956c8471a166b83b8763ca3555b2178b6222ed000768e96709b9023f6dac9762",
            "SHOP_SESSION_TOKEN": "d70icuq95jk40ggcdbs18ahu5l",
            "__cf_bm": "RGLKxM66prxp7mcTXPD.h16KXogzVojcuF0A6aTtZxE-1738807354-1.0.1.1-ySTmN_C_7GXfjDXX07FdOTgkvznDD_UvaVmwKmbXfBUccMVHsZADE92HIWKXogIXCHT7RQ3jnvOM6qey_Lw5Hw",
            "SHOP_DEVICE_TOKEN": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3Mzg4MDczNzEsImV4cCI6MTc0MTM5OTM3MSwiaXNzIjoiaHR0cHM6Ly9jb2xsZWN0b3JzYXJtb3VyeS5jb20iLCJzdWIiOiJiY2Y2OGQ4Y2JkZjE3Y2MyMjMyYTU3NTQ5OWJhM2UzYmJiYmRjNmYwZDFmNWE2OTA1MjU5ZWRlMzBmOWIwYjE4IiwianRpIjoiNjEwYjYwYmZjYzFmNzdjNWU5N2NhMzM3MjQ4ZDA3Njk2NjZmNjIzOTE2MDdkODMzMDYxOGU5NzQ3OGRmMWNkNiJ9.Zs3PUDOOWP5CIlpqPr3Pynhb9o-v7tKXZ9On4N7ZlRc",
            "__HOST-SHOP_SESSION_ROTATION_TOKEN": "c1ddfe3dddb37fd7f1a0fd2c878d77cbaeabaa16282b9e37f2825d983b743ab4",
            "SHOP_SESSION_ROTATION_TOKEN": "c1ddfe3dddb37fd7f1a0fd2c878d77cbaeabaa16282b9e37f2825d983b743ab4",
            "SHOP_TOKEN": "4ce84fb379c5ccfc047b6502c070c37e5557fd8f63d75928f7f92149e1b2e97a_1739412171",
            "bc_consent": '{"allow":[2,3,4],"deny":[]}',
            "_gid": "GA1.2.630619838.1738807375",
            "STORE_VISITOR": "1",
            "lastVisitedCategory": "64",
            "_ga": "GA1.1.1121161553.1738807375",
            "__kla_id": '{"cid":"YTY3ZjY3ZWtYbU5pWkMwME1EWmhMV0ZoTVRjdE9HTXlZVEpsTlRZM05tTTMi,"$referrer":{"ts":1738427229,"value":"","first_page":"https://collectorsarmoury.com/"},"$last_referrer":{"ts":1738807406,"value":"","first_page":"https://collectorsarmoury.com/login.php"}}',
            "_ga_5BZMS9JCQ7": "GS1.1.1738807374.1.1.1738807406.0.0.0",
            "Shopper-Pref": "1765EA98F73564D8C6394D31E884A6E7752E47B3-1739412207535-x{\"cur\":\"USD\"}"
        }

        yield Request(
            url='https://collectorsarmoury.com/',
            callback=self.parse_categories,
            cookies=self.cookies
        )


    def parse_categories(self, response):
        categories_lev1 = response.css('.navPages-item')
        for category_lev1 in categories_lev1:
            path_1 = category_lev1.css('a::text').get().replace('\r','').replace('\n','').strip()
            categories_lev2 = categories_lev1.css('div ul li')
            for category_lev2 in categories_lev2:
                path_2 = category_lev1.css('a::text').get().replace('\r','').replace('\n','').strip()
                url = category_lev1.css('a::attr(href)').get()
                yield Request(
                    url=f'{url}?limit=96',
                    callback=self.parse_products,
                    cookies=self.cookies,
                    dont_filter=True,
                    meta={'path': f'{path_1} > {path_2}'}
                )

    def parse_products(self, response):
        for product in response.css('.card-title a::attr(href)'):
            yield Request(
                url=product.get(),
                cookies=self.cookies,
                meta=response.meta,
                dont_filter=True,
                callback=self.parse_pdp
            )

        if next_link := response.css('.pagination-link--next::attr(href)').get():
            yield Request(
                url=next_link,
                cookies=self.cookies,
                dont_filter=True,
                meta=response.meta,
                callback=self.parse_products
            )

    def parse_pdp(self, response):
        quantity = response.css('#form-action-addToCart::attr(value)').get().lower()
        quantity = 0 if 'pre-order' in quantity else 1
        upc = ''
        Type = ''
        for i, title in enumerate(response.css('.productView-info > dt::text').getall()):
            if title.lower() == 'type:':
                Type = response.css('.productView-info > dd::text').getall()[i]
            if title.lower() == 'upc:':
                upc = response.css('.productView-info > dd::text').getall()[i]
        images = response.css('.productView-images img::attr(src)').getall()
        item = Product()
        item['sku'] = response.css('dd[itemprop="sku"]::text').get().replace('\r','').replace('\n','').strip()
        item['upc'] = upc
        item['brand'] = remove_tags(response.css('.productView-brand').get('')).replace('\r','').replace('\n','').strip()
        item['Type'] = Type.replace('\r','').replace('\n','').strip()
        item['title'] = response.css('h1.productView-title::text').get('')
        item['description'] = remove_tags(response.css('#productDescription').get('')).replace('\r','').replace('\n','').strip()
        item['quantity'] = quantity 
        item['price'] = response.css('.productView-price .price-primary::text').get()
        item['MSRP'] = response.css('.productView-price [data-product-rrp-price-without-tax]::text').get().replace('\r','').replace('\n','').strip()
        item['url'] = response.url
        item['category'] = response.meta['path']
        for i, image in enumerate(images):
            item[f'image_{i+1}'] = image

        yield item
