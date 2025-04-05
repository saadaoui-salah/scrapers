import scrapy
from core.spiders.myhomeware import MyhomewareSpider
import json

class HdrenoSpider(MyhomewareSpider):
    name = "hdreno"
    start_urls = ["https://hdreno.com.au/sitemap_collections_1.xml?from=470121349143&to=472018419735"]

    def parse_products(self, response):
        for link in response.css('.productitem--title > a::attr(href)').getall():
            yield scrapy.Request(
                url=f"https://hdreno.com.au{link}",
                callback=self.parse_pdp
            )

        if next_url := response.css('.pagination--next > a::attr(href)').get():
            yield scrapy.Request(
                url=f"https://hdreno.com.au{next_url}",
                callback=self.parse_products
            )

    def parse_pdp(self, response):
        data = response.css('#bss-po-store-data[type="application/json"]::text').get()
        data = json.loads(data)
        product = data['product']
        if product['option'] == ['Color']:
            for variant in product['variants']:
                yield {
                    'title': variant['name'],
                    'brand': product['vendor'],
                    'sku': variant['sku'],
                    'price': variant['price']/100,
                    'colour': variant['title'],
                    'url': response.url,
                }
            return
        color = response.xpath("//span[contains(@data-variant-option-name, 'Colour')]/../following-sibling"\
            "::*[1]/div[contains(@class, 'options-selection__option-value--selected')]//input/@value").get()
        if not color:
            color = response.xpath("//div[contains(@class, 'product-description')]//li[contains(text(), 'Color')]/text()").get('')
            color = color.lower().removeprefix('color : ').removeprefix('color: ')
        yield {
            'title': response.css('h1.product-title::text').get('').removeprefix('\n').removeprefix('\t').strip(),
            'brand': response.css('.product-vendor a::text').get(),
            'sku': response.css('[data-product-sku]::text').get('').removeprefix('\n').removeprefix('\t').strip(),
            'price': response.css('.product__price [data-price]::text').get('').removeprefix('\n').removeprefix('\t').strip(),
            'RRP': response.css('.product__price [data-price-compare]::text').get('').removeprefix('\n').removeprefix('\t').strip(),
            'colour': color,
            'url': response.url,
        }