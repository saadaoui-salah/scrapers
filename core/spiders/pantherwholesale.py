import scrapy
from w3lib.html import remove_tags

class Product(scrapy.Item):
    category = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
    sku = scrapy.Field()
    cost = scrapy.Field()
    retail_cost = scrapy.Field()
    stock_status = scrapy.Field()
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

class PantherwholesaleSpider(scrapy.Spider):
    name = "pantherwholesale"
    allowed_domains = ["pantherwholesale.com"]
    start_urls = ["https://pantherwholesale.com"]
    cookies = {
        "localization": "US",
        "_shopify_y": "37A9E3BF-0e98-40EB-9172-95744b5f439f",
        "_tracking_consent": '{"con":{"CMP":{"a":"","m":"","p":"","s":""}},"v":"2.1","region":"DZ08","reg":"","purposes":{"a":true,"p":true,"m":true,"t":true},"display_banner":false,"sale_of_data_region":false,"consent_id":"15E8E3F9-ad99-4557-a3d0-711c3be89f5b"}',
        "_orig_referrer": "",
        "_landing_page": "/",
        "_ga": "GA1.2.531968785.1738427255",
        "receive-cookie-deprecation": "1",
        "snize-recommendation": "2fnajfeyc1r",
        "_ju_dn": "1",
        "_ju_dc": "c0e950c6-e558-11ef-8d61-876feaa1343c",
        "cart": "Z2NwLWV1cm9wZS13ZXN0MTowMUpLSDk5RjVQNTFDMEFOMkhITjQxV1Q2RQ?key=b6c78c64562a48c378fbc181a9888a1a",
        "cart_sig": "8521d9b8d0d83aa22b4b96c8ae5c7fb1",
        "_shopify_sa_p": "",
        "_gid": "GA1.2.1165689507.1739138889",
        "_ju_v": "4.1_6.09",
        "_ju_dm": "cookie",
        "auth_state_01JKPCRPNRJ46VD9VWH78M64RF": "a4c2921b52b8b4f51db2eceb23d94e87",
        "_shopify_essential": ":AZTszI0iAAH_NMoNGeIaaJV9iF_csxskZMs9HCMiyA0a1tDjjL7Qptxlxtuf8RPhKaA3eMOciaeOLeHgrlU5NQaG88ZwssU3P5jXayHkl9dyQs5G9NqcV6T6Lv5x:",
        "secure_customer_sig": "53b26852621f3f8a82b3fd1c5c7dc916",
        "keep_alive": "1a58ef5a-cd23-436c-9e12-d9301bde934a",
        "_shopify_s": "1352CE88-83c7-4C09-92e0-629d8a26f72c",
        "_shopify_sa_t": "2025-02-09T22:22:20.392Z",
        "_ga_DE9XHSNT7D": "GS1.2.1739138889.5.1.1739139743.0.0.0",
        "_ju_pn": "7"
    }


    def parse(self, response):
        categories_lev1 = response.css('.tier1 > ul > li')
        for category_lev1 in categories_lev1:
            path = [category_lev1.css('a::text').get()]
            if categories_lev2 := category_lev1.css('.tier2 ul li'):
                for category_lev2 in categories_lev2:
                    path_copy = path.copy() + [category_lev2.css('a::text').get()]
                    slug = category_lev2.css('a::attr(href)').get()
                    url = f"{self.start_urls[0]}{slug}" if 'http' not in slug else slug
                    yield scrapy.Request(
                        url=url,
                        callback=self.parse_products,
                        meta={'path': '>'.join(path_copy)}
                    )
            else:
                slug = category_lev1.css('a::attr(href)').get()
                url = f"{self.start_urls[0]}{slug}" if 'http' not in slug else slug
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_products,
                    meta={'path': path[0]}
                )

    def parse_products(self, response):
        products = response.css('.product .main a::attr(href)').getall()
        for product in products:
            yield scrapy.Request(
                url=f"{self.start_urls[0]}{product}",
                callback=self.parse_pdp,
                meta=response.meta,
                cookies=self.cookies
            )

        if next_link := response.css('a.next::attr(href)').get():
            print(next_link)
            yield scrapy.Request(
                url=f"{self.start_urls[0]}{next_link}",
                callback=self.parse_products,
                meta=response.meta
            )

    def parse_pdp(self, response):
        images = response.css('.swiper-wrapper img::attr(src)').getall()
        item = Product()
        item['category'] = response.meta['path']
        item['url'] = response.url
        item['title'] = response.css('.product-title::text').get('').strip()
        item['sku'] = response.css('.sku__value::text').get('')
        item['description'] = remove_tags(response.css('.descriptionunder').get(''))
        item['cost'] = response.css('.pricearea .price .hide-price-guest::text').get()
        item['retail_cost'] = response.css('.pricearea .was-price .hide-price-guest::text').get()
        item['stock_status'] = 5 if response.css('#quantity::attr(value)').get() else 0  
        for i, image in enumerate(images):
            item[f'image_{i+1}'] = f"https:{image}"
        yield item