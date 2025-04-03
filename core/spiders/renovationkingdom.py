import scrapy
import json


class RenovationkingdomSpider(scrapy.Spider):
    name = "renovationkingdom"
    start_urls = ["https://www.renovationkingdom.com.au/sitemap"]

    def parse(self, response):
        cats = response.css('.column.main .col-bss-2 ul a::attr(href)').getall()
        for cat in cats:
            yield scrapy.Request(
                url=cat,
                callback=self.parse_products
            )

    def parse_products(self, response):
        for link in response.css('.product-item-link::attr(href)').getall():
            yield scrapy.Request(
                url=link,
                callback=self.parse_pdp
            )

        if next_url := response.css('a.js-pagination-load-more::attr(href)').get():
            yield scrapy.Request(
                url=f"https://www.myhomeware.com.au{next_url}",
                callback=self.parse_products
            )

    def parse_pdp(self, response):
        data = response.css('[type="application/ld+json"]::text').get()
        data = json.loads(data)
        color = data.get('mainEntity',{}).get('color')
        if not color:
            color = response.xpath("//label[@class='amprot-label' and contains(text(), 'Colour')]/..//ul/li/span[@class='amprot-name']/text()").get()

        yield {
            'title': data['mainEntity']['name'],
            'sku': data['mainEntity']['sku'].split(',')[0],
            'price': response.css('[data-price-type="finalPrice"] .price::text').get() or f"${data['mainEntity']['offers']['price']}",
            'RRP': response.css('[data-price-type="oldPrice"] .price::text').get(),
            'colour': color,
            'brand': data['mainEntity'].get('brand',{}).get('name'),
            'url': response.url,
        }


