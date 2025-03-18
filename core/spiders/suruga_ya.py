import scrapy
from w3lib.html import remove_tags
import re

class Product(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    quantity = scrapy.Field()
    price = scrapy.Field()
    original_price = scrapy.Field()
    images = scrapy.Field()

class SurugaYaSpider(scrapy.Spider):
    name = "suruga-ya"
    allowed_domains = ["suruga-ya.jp"]
    start_urls = ["https://www.suruga-ya.jp/search?category=50104&search_word=&brand=%E3%82%A4%E3%83%9E%E3%82%A4&is_marketplace=1"]

    def parse(self, response):
        products = response.css('.item')
        for product in products:
            item = Product()
            cleaned_text = re.sub(r"\[\d+\]", "", remove_tags(product.css('.product-name').get('')))
            item['title'] = cleaned_text
            item['quantity'] = remove_tags(product.css('.text-blue-light::text').get('')).replace('(', '').replace('点の中古品)','')
            item['price'] = remove_tags(product.css('.item_price .highlight-box .text-red').get('')).replace('\n','').strip().replace('￥','')
            item['original_price'] = product.xpath(".//p[contains(text(),'定価')]//text()").get('').replace('定価：', '').replace('￥','')
            slug = product.css(".title > a::attr(href)").get('')
            url= slug if slug.startswith('http') else f'https://www.suruga-ya.jp{slug}'
            yield scrapy.Request(
                url=url,
                callback=self.parse_pdp,
                meta={'item': item}
            )
        if next_link := response.css('.next a::attr(href)').get():
            next_link = next_link if next_link.startswith('http') else f'https://www.suruga-ya.jp{next_link}'
            yield scrapy.Request(
                url=next_link,
                callback=self.parse,
            )
    def get_bigger_image(self, image):
        if not image:
            return ''
        image = image.replace('/pics_webp/boxart_ss/','/database/pics_webp/game/').replace('ss.gif.webp','.jpg.webp').split('?')[0]
        image = image.replace('/pics_webp/boxart_m/','/database/pics_webp/game/').replace('m.jpg.webp','.jpg.webp')
        return image
    
    def parse_pdp(self, response):
        item = response.meta['item']
        item['url'] = response.url
        images = response.xpath('//img[contains(@src,"https://www.suruga-ya.jp/pics_webp/boxart_ss")]//@src').getall()
        images = [self.get_bigger_image(image) for image in images]
        images += [self.get_bigger_image(response.xpath('//img[contains(@src,"ya.jp/pics_webp/boxart_m")]//@src').get())]
        item['images'] = "|".join(images)
        yield item