import scrapy
from w3lib.html import remove_tags
import json

class Product(scrapy.Item):
    # define the fields for your item here like:
    category = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
    sku = scrapy.Field()
    coast = scrapy.Field()
    retail_coast = scrapy.Field()
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
    image_21 = scrapy.Field()
    image_22 = scrapy.Field()
    image_23 = scrapy.Field()
    image_24 = scrapy.Field()
    image_25 = scrapy.Field()
    image_26 = scrapy.Field()
    image_27 = scrapy.Field()
    image_28 = scrapy.Field()
    image_29 = scrapy.Field()
    image_30 = scrapy.Field()
    image_31 = scrapy.Field()
    image_32 = scrapy.Field()
    image_33 = scrapy.Field()
    image_34 = scrapy.Field()
    image_35 = scrapy.Field()

class SwordsswordsSpider(scrapy.Spider):
    name = "swordsswords"
    allowed_domains = ["swordsswords.com"]
    start_urls = ["https://swordsswords.com"]
    cookies = {
        "fornax_anonymousId": "303d586a-9515-4a36-8905-5045ed704ef6",
        "_ga": "GA1.1.668681826.1738427260",
        "SF-CSRF-TOKEN": "75e0830a-520d-4fe7-8361-05d972a6462b",
        "athena_short_visit_id": "700ba6c8-62c6-4b43-af8f-9cf4fa184463:1739739681",
        "XSRF-TOKEN": "d039baff6f0a0bae08b7474901e602d66e516a39118fbe6ea4552cc0c0303f6c",
        "SHOP_SESSION_TOKEN": "d466c7ac-214b-4ca7-a860-cfd28b260ebb",
        "__cf_bm": "IAVxmfq2hLRHBFsR.jmuJgNj4MGOTmaf.2X_VkeQUrM-1739739681-1.0.1.1-_iCL2Ekj6Jn6s9SX8QmhaHAdfiExvWygOmN.USdW_phx3HO_W0hiVRaalGh88XRw2390fBZw06hNwfb5QlwgaA",
        "STORE_VISITOR": "1",
        "lastVisitedCategory": "453",
        "SHOP_DEVICE_TOKEN": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3Mzk3NDA1NjcsImV4cCI6MTc0MjMzMjU2NywiaXNzIjoiaHR0cHM6Ly9zd29yZHNzd29yZHMuY29tIiwic3ViIjoiMmU4OWZjZmU2MWUyMjlmMmFjMTNhNWVmYjE2ZTI1MThkOWIwZGMxNGFlYmU2NGY0NzY2OGFlMDkxYzRkYzI2NSIsImp0aSI6IjI4MzVmNzFhNjdhMjQwNWQ3NDIwNjg5NjlmMjI0YzQwZjFjNzg1ZjAyZjEzYjlmOTg0MDVjOTJlMjM5YzFlNjYifQ.8KpxMwJxzbWmczB_jH8Bz-1WzGZvWniWZezap8bQ3HM",
        "__HOST-SHOP_SESSION_ROTATION_TOKEN": "a4f4c2bacf59a549b0780ba9cf88a23c14dc8a219311e345b65491b08fcd0913",
        "SHOP_SESSION_ROTATION_TOKEN": "a4f4c2bacf59a549b0780ba9cf88a23c14dc8a219311e345b65491b08fcd0913",
        "SHOP_TOKEN": "0ccb232788b236f8068ff493eff5d611e32d38052bde3ecd7edd5b0911fc979f_1740345367",
        "_ga_QYYRE5DMP5": "GS1.1.1739739723.2.1.1739740575.0.0.0",
        "Shopper-Pref": "9638ED3A11C82D75358D738E3E1C156BCB207F10-1740345375870-x%7B%22cur%22%3A%22USD%22%7D"
    }


    def start_requests(self):
        yield scrapy.Request(
            url='https://swordsswords.com/',
            callback=self.parse_categories,
            cookies=self.cookies
        )

    def parse_categories_tree(self, categories, path):
        for category in categories:
            path_copy = path.copy()
            path_copy += [category.css('a::text').get()]
            if menu := category.css('.navPages-item > div > .navPage-subMenu-list'):
                yield from self.parse_categories_tree(menu.css('li'), path_copy)
            else:
                slug = category.css("a::attr(href)").get() 
                url =  f'https://swordsswords.com/{slug}' if 'https://swordsswords' not in slug else slug
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_products,
                    cookies=self.cookies,
                )


    def parse_categories(self, response):
        big_cats = response.css('.navPages-item')
        for category in big_cats:
            path = [category.css('a::text').get()]
            if menu := category.css('.navPages-item > div > .navPage-subMenu-list'):
                yield from self.parse_categories_tree(menu.css('li'), path)
            else:
                slug = category.css("a::attr(href)").get() 
                url =  f'https://swordsswords.com/{slug}' if 'https://swordsswords' not in slug else slug
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_products,
                    cookies=self.cookies,
                )

    def parse_products(self, response):
        
        products = response.css('.card-title a::attr(href)').getall()
        for product in products:
            yield scrapy.Request(
                url=product,
                callback=self.parse_pdp,
                cookies=self.cookies,
                meta={'path': ' > '.join(response.css('.breadcrumb a span::text').getall())}
            )
        
        if next_link := response.css('.pagination-item--next a::attr(href)').get():
            yield scrapy.Request(
                url=next_link,
                callback=self.parse_products,
                cookies=self.cookies,
            )

    def parse_pdp(self, response):
        description = remove_tags(response.css('#tab-description').get(''))
        description += remove_tags(response.css('#tab-features').get(''))
        
        item = Product()
        item['category'] = response.meta['path']
        item['url'] = response.url
        item['title'] = response.css('.productView-title::text').get()
        item['sku'] = response.css('span[data-product-sku]::text').get()
        item['description'] = description
        item['quantity'] = 0 if 'out of stock' in response.css('.alertBox-message::text').get('').lower() else 10
        item['coast'] = response.css('.productView-details .price--rrp::text').get()
        item['retail_coast'] = response.css('.productView-details .price--withoutTax::text').get()
        images = response.css('.productView-thumbnail img::attr(src)').getall()
        for i, image in enumerate(images):
            item[f'image_{i+1}'] = image.replace('50x50', '2560w')
        yield item