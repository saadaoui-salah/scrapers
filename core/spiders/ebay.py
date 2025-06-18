import scrapy
from w3lib.html import remove_tags
from core.utils.utils import read_json

class EbaySpider(scrapy.Spider):
    custom_settings = {
        'CONCURRENT_REQUESTS': 1,
        'COOKIES_ENABLED':False,
        'HTTPCACHE_ENABLED': False
    }
    name = "ebay"
    start_urls = [f"https://www.ebay.co.uk/str/automationplanetuk?_ipg=200&_pgn={i}&_tab=shop&_ajax=itemFilter&_tabName=shop" for i in [49]]
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "fr-FR,fr;q=0.9,ar-DZ;q=0.8,ar;q=0.7,en-US;q=0.6,en;q=0.5",
        "cache-control": "no-cache",
        "dnt": "1",
        "pragma": "no-cache",
        "priority": "u=0, i",
        "referer":"https://www.google.com",
        "sec-ch-ua": "\"Google Chrome\";v=\"134\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"134\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Linux\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
    }
    proxy = 'oxy_isp'
    data = read_json('ebay-2.json')
    done = []

    def start_requests(self):
        for i in range(20):
            for url in self.data:
                yield scrapy.Request(
                    url=url['url'],
                    dont_filter=True,
                    callback=self.parse_pdp,
                    headers=self.headers,
                    meta={'item': url,}
            ) 

    def parse(self, response):
        data = response.json()
        items = filter(lambda x: x['_type'] == 'CardContainer',data['modules']['LISTINGS_MODULE']['containers'])
        items = list(items)[0]
        for item in items['cards']:
            yield scrapy.Request(
                url=item['action']['URL'],
                headers=self.headers,
                callback=self.parse_pdp,
            )


    def parse_pdp(self, response):
        item = response.meta['item']
        if not remove_tags(response.css('.x-item-title__mainTitle').get('')) or response.url in self.done:
            return
        self.done += [response.url]
        item['sold'] = response.xpath("//div[@id='qtyAvailability']//span[contains(text(), 'sold')]/text()").get()
        item['item specifics'] = remove_tags(response.css('.ux-layout-section--features').get(''))
        item['Product Identifiers'] = remove_tags(response.css('.ux-layout-section-evo.ux-layout-section--productIdentifiers').get(''))
        yield item