import scrapy
from core.utils.utils import generate_cookies
import json
from core.items import Service
from w3lib.html import remove_tags
from scrapy import Request

class YellowpagesSpider(scrapy.Spider):
    name = "yellowpages"
    allowed_domains = ["www.yellowpages.com.au"]
    start_urls = ["https://www.yellowpages.com.au"]
    keywords = []
    def start_requests(self):
        ########################
        self.cookies = {
        'cf_clearance':'RIf2cC_.AnXy5POP4vEIAN0NY4QLIZDQ8xCIOy1V4CA-1736802557-1.2.1.1-sMmGNDKLSyjZldVwwaTdiL6x6gD777VzittVVeH.gnZSDQygul46JoINOAQEzl.lAM7O1ZrNiUrGuFsANy3ewfAvOgzhsfbH9mjEIf9lqgAF3rrVaA7LDxeZVMEgqRbklUlMAN.xsKVx8uc6fhHfNpRufKWp2trVAswha2OdEPsPgRSoIWjQN48oilVp6Ov_YUP6WZCTGgkQE1BepVwZVGpwqVR5DXDSr3L.TlIHm4OdDLBWPjdD7PrQrSSuEsNJFa895TirFSdjOT_BiRwndAytiSzCsRBSVG6JCi9rZ9x96Admfyivkqk9Y_OzpQnPWu9LHV5Faww70Jt58AuF.A'}
        start_page = 28
        keyword = 'handyman'
        #### UPDATE FILE NAME
        ########################

        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": "https://www.yellowpages.com.au",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Te": "trailers"
        }
        self.base_url = 'https://www.yellowpages.com.au/search/listings?clue={}&pageNumber={}'
        yield scrapy.Request(
            url=self.base_url.format(keyword, start_page),
            cookies=self.cookies,
            headers=self.headers,
            callback=self.parse_results,
            meta={'keyword': 'fencing'}
        )
        yield scrapy.Request(
            url=self.base_url.format(keyword, start_page + 1),
            cookies=self.cookies,
            headers=self.headers,
            callback=self.parse_results,
            meta={'keyword': 'fencing'}
        ) 
        yield scrapy.Request(
            url=self.base_url.format(keyword, start_page + 2),
            cookies=self.cookies,
            headers=self.headers,
            callback=self.parse_results,
            meta={'keyword': 'timber'}
        )
        print(f'Your Next Page start_page = {start_page + 3}')
        
    def parse_results(self, response):
        data = response.xpath('//script[contains(text(), "window.__INITIAL_STATE__")]/text()').get()
        if data:
            data = data.split('window.__INITIAL_STATE__ =')[1].strip().replace(';', '')
            data = json.loads(data)
            services = data['model']['inAreaResultViews']
            for service in services:
                item = Service()
                address = service['primaryAddress']
                rating = service['averageRatings']['yellowReviewSummary']
                item['business_name'] = service['name']
                item['email'] = service['primaryEmail']
                if address:
                    item['location'] = f"{address['addressLine']}, {address['suburb']}, {address['state']}, {address['postCode']}"
                item['availability'] = service['openingHoursView']
                item['website'] = service['website']
                item['phone_number'] = service['callContactNumber']['displayValue']
                item['current_url'] = f"https://www.yellowpages.com.au{service['relativeDetailsLink']}"
                item['category'] = service['category']['name']
                item['rating_avg'] = rating['displayRating'] if rating else None
                item['reviews'] = rating['reviewCount'] if rating else None
                item['trade_type'] = response.meta['keyword']

                response.meta['item'] = item
                yield Request(
                    url=item['current_url'],
                    callback=self.parse_details,
                    cookies=self.cookies,
                    headers=self.headers,
                    meta=response.meta
                )
        else:
            address = response.css('.search-contact-card')
            for service in services:
                item['trade_type'] = response.meta['keyword']
                item['business_name'] = service.css('.listing-name::text').get()
                item['email'] = service.css('.contact-email::attr(title)').get('').replace('Send Email','')
                item['website'] = service.css('.contact-email::attr(title)').get('')
                item['current_url'] = f"https://www.yellowpages.com.au{service.css('.listing-name::attr(href)').get()}"
                item['phone_number'] = service.css('a[title="Phone"] .contact-text::text').get()
                item['location'] = remove_tags(service.css('.listing-address').get(''))
                item['availability'] = remove_tags(services.css('.opening-hours-all-days').get(''))
                item['category'] = remove_tags(services.css('.listing-heading').get(''))
                item['rating_avg'] = remove_tags(service.css('.rating').get(''))
                item['reviews'] = service.css('.de-emphasis.count::text').get()
                response.meta['item'] = item
                yield Request(
                    url=item['current_url'],
                    callback=self.parse_details,
                    cookies=self.cookies,
                    headers=self.headers,
                    meta=response.meta
                )
            
    def parse_details(self, response):
        item = response.meta['item']
        item['description'] = remove_tags(response.css('.listing-descriptors').get(''))
        item['specializations'] = remove_tags(response.css('.product-keywords').get(''))
        item['abn'] = response.css('dd.abn::text').get()
        yield item