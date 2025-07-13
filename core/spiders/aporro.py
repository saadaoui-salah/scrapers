import scrapy
from w3lib.html import remove_tags


class AporroSpider(scrapy.Spider):
    name = "aporro"
    start_urls = ["https://www.aporro.com/search?options%5Bprefix%5D=last&page=1&q=moissanite"]

    def parse(self, response):
        for product in response.css('.product-card__title::attr(href)').getall():
            yield scrapy.Request(
                url=f"https://www.aporro.com{product}",
                callback=self.parse_pdp
            )

        if next_link := response.css('a.next::attr(href)').get():
            yield scrapy.Request(
                url=f"https://www.aporro.com{next_link}",
                callback=self.parse
            )

    
    def parse_pdp(self, response):
        yield {
            'url': response.url,
            'name': response.css('[property="og:title"]::attr(content)').get(),
            'description': remove_tags(response.xpath("//span[contains(text(), 'Product Details')]/../../div").get('')),
            'price': response.css('.price__regular::text').get(),
            'colors': list(set(response.css('input[name="Color"]::attr(value)').getall())),
            'sizes': list(set(response.css('input[name="Size"]::attr(value)').getall())),
        }
