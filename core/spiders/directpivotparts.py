import scrapy
from w3lib.html import remove_tags

class DirectpivotpartsSpider(scrapy.Spider):
    name = "directpivotparts"
    start_urls = ["https://directpivotparts.com"]

    def parse(self, response):
        for slug in response.xpath('//div[contains(@id,"menu-main-root-")]//a[contains(@href, "/products/")]/@href').getall():
            yield scrapy.Request(
                url=f"https://directpivotparts.com{slug}",
                callback=self.parse_products
            )


    def parse_products(self, response):
        for slug in response.css('div.gap-4 [itemprop="itemListElement"] a[itemprop="url"]::attr(href)').getall():
            yield scrapy.Request(
                url=f"https://directpivotparts.com{slug}",
                callback=self.parse_pdp
            )
        
        if next_page := response.xpath("//div[text()='Next']/../../../a/@href").get():
            yield scrapy.Request(
                url=next_page,
                callback=self.parse_products
            )

    def parse_pdp(self, response):
        cat = ' > '.join(response.css('[itemtype="https://schema.org/BreadcrumbList"] a span::text').getall()[1:])
        variants = response.css('[class="flex flex-wrap gap-2 items-center"] a::attr(href)').getall()
        if not variants:
            response.meta['cat'] = cat
            yield from self.parse_variant(response)
        for slug in variants:
            yield scrapy.Request(
                url=f"https://directpivotparts.com{slug}",
                callback=self.parse_variant,
                meta={'cat':cat}
            )

    def parse_variant(self, response):
        yield {
            'title': response.css('h1[itemprop="name"]::text').get(),
            'SKU':response.css('span[itemprop="sku"]::text').get(),
            'brand':response.css('[itemprop="brand"] [itemprop="name"]::text').get(),
            'short description':remove_tags(response.css('[class="w-full"]').get('')).replace('\n','').replace('\t','').strip(),
            'long description':remove_tags(response.xpath("//h3[contains(text(), 'Description')]/../div").get('')).replace('\n','').replace('\t','').strip(),
            'category path':response.meta['cat'],
            'price':response.css('[itemprop="price"]::text').get(),
            'images':[f"  https://directpivotparts.com{image}  " for image in response.css('[data-client--page--products--photo-swipe-target="item"] img::attr(src)').getall()],
            'MPN':response.css('[itemprop="mpn"]::text').get(),
            'product url':response.url,
        }