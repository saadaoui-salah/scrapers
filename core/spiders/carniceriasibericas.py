import scrapy
from core.utils.cleaning import clean

class CarniceriasibericasSpider(scrapy.Spider):
    name = "carniceriasibericas"
    start_urls = ["https://carniceriasibericas.com/todas-las-carnicerias/?localizacion=alcala-de-guadaira"]
    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'HTTPCACHE_ENABLED':True
    }
    urls = []
    headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "fr-FR,fr;q=0.9,ar-DZ;q=0.8,ar;q=0.7,en-US;q=0.6,en;q=0.5",
            "cache-control": "no-cache",
            "dnt": "1",
            "pragma": "no-cache",
            "priority": "u=0, i",
            "referer": "https://www.google.com",
            "sec-ch-ua": "\"Google Chrome\";v=\"130\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"130\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Linux\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "user-agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
        }

    def start_requests(self):
        yield scrapy.Request(
                url="https://carniceriasibericas.com/todas-las-carnicerias/?localizacion=alcala-de-guadaira",
                callback=self.parse,
                headers=self.headers
            ) 


    def parse(self, response):
        for cat in response.css('[data-fid="12873"] .wpc-filters-ul-list > li'):
            if sub_cats := cat.css('.children > li'):
                for sub_cat in sub_cats:
                    if last_levs := response.css('.children > li'):
                        for last_lev in last_levs:
                            self.urls +=[{
                                    'pro':sub_cat.css('a::text').get(),
                                    'mun':last_lev.css('.wpc-term-item-content-wrapper a::text').get(),
                                    'url':last_lev.css('a::attr(href)').get()
                                }]
                            continue
                            yield scrapy.Request(
                                url=last_lev.css('a::attr(href)').get(),
                                callback=self.parse_products,
                                headers=self.headers
                            )
                    else:
                        print('hey')
            else:
                print('hey2')
        from random import shufle
        urls = shufle(self.urls)
        for url in urls:
            yield scrapy.Request(
                url=url['url'],
                callback=self.parse_products,
                headers=self.headers,
                meta=url
            )


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

        if next_page := response.css('.next.page-link::attr(href)').get():
            yield scrapy.Request(
                url=next_page.css('::attr(href)').get(),
                callback=self.parse_products,
                meta=response.meta,
                headers=self.headers
            )