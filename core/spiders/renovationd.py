import scrapy


class RenovationdSpider(scrapy.Spider):
    name = "renovationd"
    start_urls = ["https://renovationd.com.au/sitemap/categories"]

    def parse(self, response):
        categories = response.css('.simple-list > li')

        def parse_tree(cats):
            for cat in cats:
                if elem:= cat.css('ul > li'):
                    yield from parse_tree(elem)
                else:
                    yield scrapy.Request(
                        url=cat.css('a::attr(href)').get(),
                        callback=self.parse_products,
                    )
        yield from parse_tree(categories)


    def parse_products(self, response):
        for link in response.css('.card-title a::attr(href)').getall():
            yield scrapy.Request(
                url=link,
                callback=self.parse_pdp,
            )

        if next_link := response.css('.pagination-item--next a::attr(href)').get():
            yield scrapy.Request(
                url=next_link,
                callback=self.parse_products,
            )


    def parse_pdp(self, response):
        yield {
            'title': response.css('.productView-title::text').get(),
            'sku': response.css('[data-product-sku]::text').get(),
            'brand': response.css('[data-product-brand] a span::text').get(),
            'colour': response.xpath("//dt[contains(text(), 'Color')]/following-sibling::*[1]/text()").get(),
            'price': response.css('.productView-details .price--withoutTax::text').get(),
            'RRP': response.css('.productView-details .price--rrp::text').get('').replace('\n','').strip(),
            'url': response.url,
        }