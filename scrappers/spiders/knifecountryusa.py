import scrapy
from w3lib.html import remove_tags

class Product(scrapy.Item):
    # define the fields for your item here like:
    category = scrapy.Field()
    sub_category = scrapy.Field()
    title = scrapy.Field()
    manufactor = scrapy.Field()
    description = scrapy.Field()
    specefication = scrapy.Field()
    url = scrapy.Field()
    sku = scrapy.Field()
    ean = scrapy.Field()
    upc = scrapy.Field()
    stock = scrapy.Field()
    list_price = scrapy.Field()
    our_price = scrapy.Field()
    savings = scrapy.Field()
    weight = scrapy.Field()
    dimensions = scrapy.Field()
    country = scrapy.Field()
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

class KnifecountryusaSpider(scrapy.Spider):
    name = "knifecountryusa"
    allowed_domains = ["knifecountryusa.com"]
    start_urls = ["https://www.knifecountryusa.com/shop/categories/"]

    def parse(self, response):
        categories = response.css('.Categories > ul > li')
        for category in categories:
            item = Product()
            item['category'] = response.css('div > a::text').getall()[0]
            categories_lev2 = category.css('ul li div')
            for category_lev2 in categories_lev2:
                item['sub_category'] = category_lev2.css('a::text').get()
                slug = category_lev2.css('a::attr(href)').get().replace('/store/category/','/shop/category/view/')
                yield scrapy.Request(
                    url=f"https://www.knifecountryusa.com{slug}",
                    callback=self.parse_products,
                    meta={'item': item}
                )

    def parse_products(self, response):
        products = response.css('a[itemprop="url"]::attr(href)').getall()
        for product in products:
            yield scrapy.Request(
                url=f"https://www.knifecountryusa.com{product}",
                callback=self.parse_pdp,
                meta=response.meta
            )
        
        if next_link := response.css('.Next > a::attr(href)'):
            yield scrapy.Request(
                url=f"https://www.knifecountryusa.com{next_link}",
                callback=self.parse_products,
                meta=response.meta
            )


    def get_from_li(self, text, response):
        return remove_tags(response.xpath(f'//li[contains(text(), "{text}")]//text()').get('')).replace(text, '').replace(':','')

    def parse_pdp(self, response):
        item = response.meta['item']
        
        item['title'] = response.css('h2[itemprop="name"]::text').get()
        item['description'] = remove_tags(response.css('div.Description').get('')).strip()
        item['specefication'] = remove_tags(response.css('div.Specifications').get('')).strip()
        item['sku'] = response.css('[name="SKU"]::attr(value)').get()
        item['list_price'] = remove_tags(response.css('.PriceMSRP span').get('')).strip()
        item['our_price'] = response.css('.PriceRetail::attr(content)').get()
        item['savings'] = ''.join(response.css('.Savings span::text').getall())
        item['upc'] = response.css('[itemprop="gtin12"]::text').get()
        item['url'] = response.url
        item['stock'] = 5 if response.css('.Availability .InStock::text').get() else 0
        item['manufactor'] = response.css('[title="Manufacturer"] span::text').get()
        item['weight'] = remove_tags(response.css('[itemprop="weight"]').get('')).replace('Weight: ','').strip()
        item['dimensions'] = remove_tags(response.css('.Dimensions').get('')).replace('Dimensions: ', '')
        item['country'] = self.get_from_li('Made in', response)
        item['ean'] = self.get_from_li('Product Number', response)
        images = response.css('.Images img::attr(src)').getall()

        for i, image in enumerate(images):
            item[f'image_{i+1}'] = f'https://www.knifecountryusa.com{image}'
        
        yield item