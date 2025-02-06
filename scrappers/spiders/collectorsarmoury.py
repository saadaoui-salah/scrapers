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
        
        yield scrapy.Request(
            url='https://collectorsarmoury.com/',
            callback=self.parse_categories  # Define a callback function
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
                    dont_filter=True,
                    meta={'path': f'{path_1} > {path_2}'}
                )

    def parse_products(self, response):
        for product in response.css('.card-title a::attr(href)'):
            yield Request(
                url=product.get(),
                meta=response.meta,
                callback=self.parse_pdp
            )

        if next_link := response.css('.pagination-link--next::attr(href)').get():
            yield Request(
                url=next_link,
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
        item['url'] = response.url
        item['category'] = response.meta['path']
        for i, image in enumerate(images):
            item[f'image_{i+1}'] = image
        response.meta['item'] = item
        item['MSRP'] = response.css('.productView-price [data-product-rrp-price-without-tax]::text').get().replace('\r','').replace('\n','').strip()
        item['price'] = response.css('.productView-price .price-primary::text').get()
        yield item