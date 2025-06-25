import scrapy
from core.utils.cleaning import clean

class CarniceriasibericasSpider(scrapy.Spider):
    name = "carniceriasibericas"
    start_urls = ["https://carniceriasibericas.com/todas-las-carnicerias/"]
    custom_settings = {
        'DOWNLOAD_DELAY': 0.1,
        'HTTPCACHE_ENABLED':False
    }

    def parse(self, response):
        for cat in response.css('[data-fid="12873"] .wpc-filters-ul-list > li'):
            if sub_cats := cat.css('.children > li'):
                for sub_cat in sub_cats:
                    if last_levs := response.css('.children > li'):
                        for last_lev in last_levs:
                            yield scrapy.Request(
                                url=last_lev.css('a::attr(href)').get(),
                                callback=self.parse_products,
                                meta={
                                    'pro':sub_cat.css('a::text').get(),
                                    'mun':last_lev.css('.wpc-term-item-content-wrapper a::text').get(),
                                }
                            )
                    else:
                        print('hey')
            else:
                print('hey2')

    def parse_products(self, response):
        for product in response.css('.item-container'):
            address = clean(product.xpath(".//strong[contains(text(), 'Dirección')]/../text()[2]").get(''))
            yield {
                'RAZÓN SOCIAL':product.css('.card-title h3::text').get(),
                'DIRECCIÓN':address,
                'PROVINCIA ':address.split(',')[-1],
                'MUNICIPIO':response.meta['mun'],
                'CODIGO POSTAL':clean(product.xpath(".//strong[contains(text(), 'Código postal')]/../text()[2]").get('')),
                'TELEFONO':product.xpath('.//a[contains(@href,"tel:")]/@href').get('').replace('tel:',''),
            } 