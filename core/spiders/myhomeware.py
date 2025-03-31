import scrapy
import xmltodict


class MyhomewareSpider(scrapy.Spider):
    name = "myhomeware"
    allowed_domains = ["myhomeware.com.au"]
    start_urls = ["https://www.myhomeware.com.au/sitemap_collections_1.xml?from=287293112492&to=314326810796"]

    def parse(self, response):
        cats = xmltodict.parse(response.text)
        cats = cats['urlset']['url']
        for cat in cats:
            yield scrapy.Request(
                url=cat['loc'],
                callback=self.parse_products
            )

    
    def parse_products(self, response):
        for link in response.css('.card-link::attr(href)').getall():
            yield scrapy.Request(
                url=f"https://www.myhomeware.com.au{link}",
                callback=self.parse_pdp
            )

        if next_url := response.css('a.js-pagination-load-more::attr(href)').get():
            yield scrapy.Request(
                url=f"https://www.myhomeware.com.au{next_url}",
                callback=self.parse_products
            )

    def parse_pdp(self, response):
        yield {
            'price': response.css('.product-info__sticky .price__default .price__current::text').get(),
            'RRP': response.css('.product-info__sticky .price__default .price__was::text').get(),
            'title': response.css('h1.product-title::text').get('').replace('\n','').replace('\t','').strip(),
            'sku': response.css('.product-sku__value::text').get(),
            'colour': response.xpath("//td[contains(text(), 'Colour')]/following-sibling::*[1]/text()").get(),
            'brand': response.css('.product-vendor a::text').get(),
            'url': response.url,
        }