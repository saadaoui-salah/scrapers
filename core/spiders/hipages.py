import scrapy
from scrapy import Request
from core.items import Service
import json
from html import unescape
from w3lib.html import remove_tags


LOCATIONS = []

headers = {
    "dnt": "1",
    "if-none-match": 'W/"54e6f-S52/lgP+7jagdfZTWzjiOrt3smU"',
    "priority": "u=0, i",
    "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Linux"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
}

class HipagesSpider(scrapy.Spider):
    name = "hipages"
    allowed_domains = ["hipages.com.au"]
    start_urls = ["https://hipages.com.au/"]
    search_api = 'https://cerebro.k8s.hipages.com.au/suggest/fuzzimatch?keyword={}&size=5'
    location_api = 'https://cerebro.k8s.hipages.com.au/suggest/location?keyword={}'
    locations = []
    results_api = 'https://gateway.hipages.com.au/directory/v1/businesses?filter%5Bstate%5D=nsw&filter%5Bcategory%5D={}&filter%5Bsuburb%5D={}&page%5Blimit%5D={}&page%5Boffset%5D={}'
    phone_number_api = 'https://gateway.hipages.com.au/directory/v1/phones/{}?fields%5Bphone%5D=formatted%2Ctel'
    
    def parse(self, response):
        keywords = ['Fencer','Fencing','Landscaper','Handymen','Carpenter']
        for keyword in keywords:
            yield Request(
                url=self.search_api.format(keyword.lower()),
                callback=self.parse_suggestions,
                dont_filter=True,
                meta={'keyword': keyword}
            )

    def parse_suggestions(self, response):
        data = response.json()
        directories = list(filter(lambda x: x['title'] == 'Tradies', data))[0]['results']
        for directory in directories:
            for location in LOCATIONS:
                response.meta['dir'] = directory['practice_person_plural'] 
                yield Request(
                    url=self.results_api.format(directory['practice_seo_key'], location['suburb_seo_key'], 10, 0),
                    callback=self.parse_results,
                    dont_filter=True,
                    meta=response.meta
                )

    def parse_results(self, response):
        data = response.json()['data']
        for service in data:
            yield Request(
                url=service['attributes']['profilePageFullUrl'],
                callback=self.parse_details,
                meta=response.meta,
                headers=headers,
                dont_filter=True
            )
    
    def parse_details(self, response):
        data = response.xpath('//script[contains(text(), "__INITIAL_PROPS__")]//text()').get()
        data = data.replace(' window.__INITIAL_PROPS__=', '')
        data = json.loads(json.loads(data))
        data = list(data.values())
        pri_data = data[1]['site'] if 'page' not in list(data[1].keys()) else data[0]['site']
        sec_data = data[1] if 'page' in list(data[1].keys()) else data[0]
        item = Service()
        item['business_name'] = pri_data['name']
        item['abn'] = pri_data['abn']
        item['trade_type'] = response.meta['keyword']
        item['description'] = unescape(remove_tags(sec_data['page']['description']))
        item['email'] = sec_data['page']['email']
        item['category'] = response.meta['dir']
        item['location'] = pri_data['address']
        item['reviews'] = pri_data['rating']['ratings']
        item['rating_avg'] = pri_data['rating']['star_rating']
        item['website'] = response.css('a[data-ga-action="Click tradie website"]::attr(href)').get()
        item['current_url'] = response.url
        yield Request(
            url=self.phone_number_api.format(sec_data['page']['mobile']),
            callback=self.parse_phone,
            meta={'item': item},
        )

    def parse_phone(self, response):
        item = response.meta['item']
        item['phone_number'] = response.json()['data']['attributes']['formatted']
        yield item