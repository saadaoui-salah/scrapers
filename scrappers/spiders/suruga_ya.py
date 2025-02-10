import scrapy
from w3lib.html import remove_tags


class Product(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    quantity = scrapy.Field()
    price = scrapy.Field()
    original_price = scrapy.Field()
    images = scrapy.Field()
    page = scrapy.Field()

class SurugaYaSpider(scrapy.Spider):
    name = "suruga-ya"
    allowed_domains = ["suruga-ya.jp"]
    start_urls = ["https://www.suruga-ya.jp/search?category=5010401&search_word=&grade=HG&is_marketplace=1&scale=1/144"]

    def parse(self, response):
        products = response.css('.item')
        for product in products:
            item = Product()
            item['title'] = remove_tags(product.css('.product-name').get(''))
            item['page'] = response.url
            item['quantity'] = remove_tags(product.css('.text-blue-light::text').get('')).replace('(', '').replace('点の中古品)','')
            item['price'] = remove_tags(product.css('.item_price .highlight-box .text-red').get('')).replace('\n','').strip().replace('￥','')
            item['original_price'] = product.xpath(".//p[contains(text(),'定価')]//text()").get('').replace('定価：', '').replace('￥','')
            yield scrapy.Request(
                url=f'https://www.suruga-ya.jp{response.css(".title > a::attr(href)").get()}',
                callback=self.parse_pdp,
                meta={'item': item}
            )
        if next_link := response.css('.next a::attr(href)').get():
            yield scrapy.Request(
                url=f'https://www.suruga-ya.jp{next_link}',
                callback=self.parse,
            )
    def parse_pdp(self, response):
        item = response.meta['item']
        item['url'] = response.url
        images = response.xpath('//img[contains(@src,"ya.jp/pics_webp/boxart_m")]//@src').getall()
        images = [image.replace('boxart_m','boxart_a').replace('m.jpg.webp','.jpg.webp').split('?')[0] for image in images]
        item['images'] = "|".join(images)
        yield item