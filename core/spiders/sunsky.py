import scrapy


class SunskySpider(scrapy.Spider):
    name = "sunsky"
    start_urls = ["https://www.sunsky-online.com/product/default!search.do?keyword=&categoryId=3&priceRange=&brandIds=&colorIds=&certs=&brandModelIds=&propOptions=&closedFilters=&orderBy=rank&desc=true"]
    api_url = "https://www.sunsky-online.com/product/default!search.do?keyword=&categoryId={}&priceRange=&brandIds=&colorIds=&certs=&brandModelIds=&propOptions=&closedFilters=&orderBy=rank&desc=true"

    def parse(self, response):
        cats = response.css('.dcat2 > a::attr(rel)').getall()
        cat_id = response.meta.get('catId')
        pages = response.css('.productInfoDisplay .page_tag::text').getall()

        if cat_id in cats:
            for page in pages:
                if '1' in page:
                    yield from self.parse_products(response)
                else:
                    yield scrapy.Request(
                        url=f"{self.api_url.format(cat_id)}&page={int(page)}",
                        callback=self.parse_products,
                    )    
        else:
            for cat in cats:
                yield scrapy.Request(
                    url=self.api_url.format(cat),
                    callback=self.parse,
                    meta={'catId': cat}
                )

    def parse_products(self, response):
        category = response.css('.catpath > a::text').getall()
        category = ' >> '.join(category)
        for product in response.css('.shopcart_cont ul.clearfix li'):
            if product.css('.itemNo::attr(value)').get():
                yield {
                    'sku': product.css('.itemNo::attr(value)').get(),
                    'name':product.css('.product-main-img::attr(title)').get(),
                    'category': category
                }