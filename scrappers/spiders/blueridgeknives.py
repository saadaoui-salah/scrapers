import scrapy
from w3lib.html import remove_tags
import json

class Product(scrapy.Item):
    # define the fields for your item here like:
    brand = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
    sku = scrapy.Field()
    price = scrapy.Field()
    msrp = scrapy.Field()
    minimum_advertised_price = scrapy.Field()
    sales_restrictions = scrapy.Field()
    weight = scrapy.Field()
    country = scrapy.Field()
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


class BlueridgeknivesSpider(scrapy.Spider):
    name = "blueridgeknives"
    start_urls = ["https://store.blueridgeknives.com/brands"]
    cookies = {
        "form_key": "oLnGo21HYeexLwkQ",
        "mage-cache-storage": "{}",
        "mage-cache-storage-section-invalidation": "{}",
        "recently_viewed_product": "{}",
        "recently_viewed_product_previous": "{}",
        "recently_compared_product": "{}",
        "recently_compared_product_previous": "{}",
        "product_data_storage": "{}",
        "mage-messages": "",
        "persistent_shopping_cart": "ycEW8FIpvboteKmS4fSxumUDvKCaODWXRhIcNZ0Arkxh8oZyUK",
        "PHPSESSID": "d3a7b45c5f8c71ffd7ce3d9ff62e8349",
        "private_content_version": "1ae5634f6bba824aba570793696035c0",
        "X-Magento-Vary": "9b39552580316e1912d12b04cf050a794f7b10f23fb6ca31d2537804684eeb52",
        "mage-cache-sessid": "true",
        "section_data_ids": '{%22customer%22:1739553741%2C%22compare-products%22:1739553741%2C%22last-ordered-items%22:1739553741%2C%22cart%22:1739553741%2C%22directory-data%22:1739553741%2C%22captcha%22:1739553741%2C%22instant-purchase%22:1739553741%2C%22loggedAsCustomer%22:1739553741%2C%22persistent%22:1739553741%2C%22review%22:1739553741%2C%22payments%22:1739553741%2C%22wishlist%22:1739553741%2C%22recently_viewed_product%22:1739553741%2C%22recently_compared_product%22:1739553741%2C%22product_data_storage%22:1739553741%2C%22paypal-billing-agreement%22:1739553741}'
    }
    headers = {
        "dnt": "1",
        "pragma": "no-cache",
        "priority": "u=0, i",
        "referer": "https://store.blueridgeknives.com/shop-by-brand/12-survivors.html",
        "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
    }


    def start_requests(self):
        yield scrapy.Request(
                url=self.start_urls[0],
                cookies=self.cookies,
                headers=self.headers,
                callback=self.parse,
            )

    def parse(self, response):
        brands = response.css('.ambrands-brand-item')
        for brand in brands:
            yield scrapy.Request(
                url=f"{brand.css('a::attr(href)').get()}?product_list_limit=96",
                callback=self.parse_brands,
                cookies=self.cookies,
                headers=self.headers,
                meta={'brand':brand.css('a::attr(href)').get()}
            )

    def parse_brands(self, response):
        products = response.css('.product-item-photo::attr(href)').getall()
        for product in products:
            yield scrapy.Request(
                url=product,
                cookies=self.cookies,
                headers=self.headers,
                callback=self.parse_pdp,
                meta=response.meta
            )

        if next_link := response.css('.pages-item-next .next::attr(href)').get():
            yield scrapy.Request(
                url=next_link,
                callback=self.parse_brands,
                cookies=self.cookies,
                headers=self.headers,
                meta=response.meta
            )

    def clean_data(self, data, key):
        return data.strip().replace('\n','').replace(key, '').replace(' ', '')

    def parse_pdp(self, response):
        item = Product()
        item['brand'] = response.meta['brand']
        item['title'] = response.css('[data-ui-id="page-title-wrapper"]::text').get()
        item['description'] = remove_tags(response.css('.description').get('')) + remove_tags(response.css('#product-attribute-specs-table').get(''))
        item['url'] = response.url
        item['sku'] = response.css('[itemprop="sku"]::text').get()
        item['price'] = response.css('[data-price-type="finalPrice"] .price::text').get()
        for tr in response.css('.product-view-info-content tr'):
            if 'Retail Price' in tr.get():
                item['msrp'] = tr.css('.price::text').get()
            if 'Weight' in tr.get():
                item['weight'] = self.clean_data(remove_tags(tr.get()), 'Weight:')
            if 'Country of Origin' in tr.get():
                item['country'] = self.clean_data(remove_tags(tr.get()), 'Country of Origin:')
            if 'Stock Status' in tr.get():
                item['quantity'] = 5 if 'In stock' in tr.get().lower() else 0  
            if 'Minimum Advertised Price' in tr.get():
                item['minimum_advertised_price'] = tr.css('.price::text').get()

        item['sales_restrictions'] = response.css('[data-th="BRK Spotlight"]::text').get()
        images = json.loads(response.xpath('//script[contains(text(), "mage/gallery/gallery")]//text()').get())
        images = images["[data-gallery-role=gallery-placeholder]"]['mage/gallery/gallery']['data']
        for i, image in enumerate(images):
            item[f'image_{i+1}'] = image['full']
        yield item