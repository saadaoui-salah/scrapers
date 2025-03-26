import scrapy


class AcquabathroomsSpider(scrapy.Spider):
    name = "acquabathrooms"
    start_urls = ["https://www.acquabathrooms.com.au"]

    def parse(self, response):
        categories = response.css('li.navmenu-item a::attr(href)').getall()
        for category in categories:
            yield scrapy.Request(
                url=f'https://www.acquabathrooms.com.au{category}',
                callback=self.parse_products
            )


    def parse_products(self, response):
        products = response.css('.productitem--title a::attr(href)').getall()
        colors = response.css('[data-filter-group="Colour"] .filter-text::text').getall()
        for product in products:
            yield scrapy.Request(
                url=f'https://www.acquabathrooms.com.au{product}',
                callback=self.parse_pdp,
                meta={'colors': colors}
            )
        
        if next_link := response.css('.pagination--next a::attr(href)').get():
            yield scrapy.Request(
                url=f'https://www.acquabathrooms.com.au{next_link}',
                callback=self.parse_products
            )

    def parse_pdp(self, response):
        colors = response.meta['colors']
        description = response.css('.pxu-tabs li::text').getall()
        color = None
        for color in colors:
            for li in description:
                if color.lower().replace('\n','').strip() in li.lower().replace('\n','').strip():
                    color = color.replace('\n','').strip()
                    break
            if color:
                break

        price = response.css('.product-pricing .price__compare-at.visible .money::text').get('').replace('\n','').strip()
        if not price:
            price = response.css('.product-pricing .price__current .money::text').get('').replace('\n','').strip()


        yield {
            'title': response.css('.product-title::text').get(),
            'sku': response.css('span[data-product-sku]::text').get(),
            'RRP': response.css('.product-pricing .price__current--on-sale .money::text').get('').replace('\n','').strip(),
            'price': price,
            'brand': response.css('.product-vendor a::text').get(),
            'url': response.url,
            'colour': color.replace('\n','').strip(),
        }