import scrapy
from w3lib.html import remove_tags
import re
from core.utils.utils import fetch_sheet

class Product(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    quantity = scrapy.Field()
    price = scrapy.Field()
    original_price = scrapy.Field()
    images = scrapy.Field()

class SurugaYaSpider(scrapy.Spider):
    name = "suruga-ya"
    sheet = fetch_sheet("1vR51PgCcuP3RuQStxw2QdYlBH5c5KImjgA5fBsggR7M", "surugaya")
    #custom_settings = {
    #    'ITEM_PIPELINES': {
    #        'core.pipelines.google_sheets.GoogleSheetsPipeline': 300,
    #    }
    #}
    sheet_id = '1ZONuwTx2U10HvAcVLGYdij5Y-qWm1bxzr9d_1wOj2uY'
    keywords = [
        "https://www.suruga-ya.jp/search?category=50103&search_word=&brand=%E3%83%90%E3%83%B3%E3%83%80%E3%82%A4",
        "https://www.suruga-ya.jp/search?category=50103&search_word=&brand=%E3%82%BF%E3%82%AB%E3%83%A9%E3%83%88%E3%83%9F%E3%83%BC%E3%82%A2%E3%83%BC%E3%83%84",
        "https://www.suruga-ya.jp/search?category=50103&search_word=&brand=%E3%83%AA%E3%83%BC%E3%83%A1%E3%83%B3%E3%83%88",
        "https://www.suruga-ya.jp/search?category=50103&search_word=&brand=POPMART",
        "https://www.suruga-ya.jp/search?category=50103&search_word=&brand=%E3%83%A1%E3%82%AC%E3%83%8F%E3%82%A6%E3%82%B9",
        "https://www.suruga-ya.jp/search?category=50103&search_word=&brand=%E3%83%90%E3%83%B3%E3%83%97%E3%83%AC%E3%82%B9%E3%83%88",
        "https://www.suruga-ya.jp/search?category=50103&search_word=&brand=%E3%83%A6%E3%83%BC%E3%82%B8%E3%83%B3"]
    
    def start_requests(self):
        if not self.keywords:
            for row in self.sheet:
                yield scrapy.Request(
                    url=row['url'],
                    callback=self.parse_price,
                    meta={'item': row}
                )
        for url in self.keywords:
            yield scrapy.Request(
                url=url,
                callback=self.parse,
            )
    
    def parse_price(self, response):
        item = response.meta['item']
        item['price'] = remove_tags(response.xpath('//div[@id="tabs-all"]//tr[@class="item"][4]/td[1]//strong[contains(@class,"text-red text-bold mgnL10")]/text()').get("xxx"))
        ignore_chars = ['\n', '\t', ',', '円']
        for char in ignore_chars:
            item['price'] = item['price'].replace(char,"").strip()
        yield item

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
