import scrapy
from w3lib.html import remove_tags
from core.utils.utils import csv_to_dict
from core.proxy.zyte_api import ZyteRequest, load

class EbaySpider(scrapy.Spider):
    custom_settings = {
        'CONCURRENT_REQUESTS': 40,
        'DOWNLOAD_DELAY':0.3,
        'COOKIES_ENABLED':False,
        'HTTPCACHE_ENABLED': False
    }
    name = "ebay"
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "fr-FR,fr;q=0.9,ar-DZ;q=0.8,ar;q=0.7,en-US;q=0.6,en;q=0.5",
        "cache-control": "no-cache",
        "dnt": "1",
        "pragma": "no-cache",
        "priority": "u=0, i",
        "referer":"https://www.bing.com",
        "sec-ch-ua": "\"Google Chrome\";v=\"134\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"134\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Linux\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
    }
    done = []

    def start_requests(self):
        self.done = [p['url'] for p in csv_to_dict('./client-data/ebay.csv')]
        for i in range(400):
            yield ZyteRequest(
                url=f'https://www.ebay.co.uk/sch/i.html?_dkr=1&iconV2Request=true&_blrs=recall_filtering&_ssn=deals*heng&store_cat=0&store_name=dealsheng&_oac=1&rt=nc&_ipg=240&_pgn={i+1}',
                callback=self.parse,
            ) 

    def parse(self, response):
        response = load(response)
        products = response.css('.srp-results li .s-item__image')
        for link in products:  
            link = link.css('a::attr(href)').get()
            if link not in self.done: 
                self.done += [link]
                yield ZyteRequest(
                    url=link,
                    callback=self.parse_pdp,
                )

    def parse_pdp(self, response):
        url = response.meta['url']
        response = load(response)
        if not remove_tags(response.css('.x-item-title__mainTitle').get('')):
            print('error ', url)
            return
        item = {}
        image = response.css('.img-transition-medium img::attr(src)').get()
        item['url'] = url
        item['image'] = image
        item['quantity'] = response.css('.x-quantity__availability  span::text').get()
        item['name'] = remove_tags(response.css('.x-item-title__mainTitle').get())
        item['price'] = response.css('.x-price-primary span::text').get()
        item['condition'] = response.css('.x-item-condition-text .clipped::text').get()
        item['sold'] = response.xpath("//div[@id='qtyAvailability']//span[contains(text(), 'sold')]/text()").get()
        item['item specifics'] = remove_tags(response.css('.ux-layout-section--features').get(''))
        item['Product Identifiers'] = remove_tags(response.css('.ux-layout-section-evo.ux-layout-section--productIdentifiers').get(''))
        yield item