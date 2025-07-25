import scrapy
from urllib.parse import urlencode
from furl import furl
PARAMS = [
    ['310125001', 'radiology-service'],
]


class HealthdirectSpider(scrapy.Spider):
    name = "healthdirect"
    custom_settings = {
        'HTTPCACHE_ENABLED': True
    }
    proxy='burp'

    def start_requests(self):
        import string
        alphabet = list(string.ascii_lowercase)
        for i in alphabet:
            yield scrapy.Request(
                url=f"https://auspost.com.au/postcode/suburb-index/{i}",
                callback=self.parse
            )

    def parse(self, response):
        for i in response.css('.pol-suburb-index-list-item a::text').getall():
            yield scrapy.Request(
                url=f'https://www.healthdirect.gov.au/australian-health-services/api/location?{urlencode({'q':i})}',
                callback=self.parse_locations,
            )
        if next_link := response.css('.next_link a::attr(href)').get():
            yield scrapy.Request(
                url=f'https://auspost.com.au{next_link}',
                callback=self.parse,
            )

    def parse_locations(self, response):
        for param in PARAMS:
            for location in response.json()['data']['suburbs']:
                l = f"{location['label'].replace(' ', '-')}-{location['code']}-{location['state']['label']}"
                yield scrapy.Request(
                    url=f"https://www.healthdirect.gov.au/australian-health-services/_next/data/ndf8NjWm2EehBnrL3Jum_/ar/search/{l.lower()}/{param[1]}/{param[0]}.json?offset=0&params={l.lower()}&params={param[1]}&params={param[0]}",
                    callback=self.parse_results
                )

    def parse_results(self, response):
        data = response.json()['pageProps']
        for doc in data['healthcareServices']['services']:
            email = None
            phone = ''
            for contact in doc['contacts']:
                if 'phone' in contact['valueType']['label'].lower() or 'fax' in contact['valueType']['label'].lower():
                    phone = f"{phone}\n{contact['value']}"
                if 'email' in contact['valueType']['label'].lower():
                    email = contact['value']
            yield {
                'name':doc['organisation']['name'],
                'email':email,
                'phone':phone,
            }

        if data['urlParams']['pageNumber'] * 10 < data['healthcareServices']['count']:
            f = furl(response.url)
            f.args['offset'] = int(f.args['offset']) + 10
            yield scrapy.Request(
                url=f.url,
                callback=self.parse_results
            )