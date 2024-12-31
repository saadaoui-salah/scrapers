import scrapy
from scrapy import Request

class HipagesSpider(scrapy.Spider):
    name = "hipages"
    allowed_domains = ["hipages.com.au"]
    start_urls = ["https://hipages.com.au/"]
    search_api = 'https://cerebro.k8s.hipages.com.au/suggest/fuzzimatch?keyword={}&size=5'
    location_api = 'https://cerebro.k8s.hipages.com.au/suggest/location?keyword={}'
    locations = []
    results_api = 'https://gateway.hipages.com.au/directory/v1/businesses?filter%5Bstate%5D=nsw&filter%5Bcategory%5D={}&filter%5Bsuburb%5D={}&page%5Blimit%5D={}&page%5Boffset%5D={}'
    def parse(self, response):
        numbers = [1,2,3,4,5,6,7,8,9,0]
        for i in numbers:

            yield Request(
                url=self.location_api.format(i),
                callback=self.parse_locations,
                meta={'last_num': i == 0},
                priority=i if i != 0 else 10
            )

    def parse_locations(self, response):
        data = response.json()
        self.locations += data
        keywords = ['Fencer','Fencing','Landscaper','Handymen','Carpenter']
        if response.meta['last_num']:
            for keyword in keywords:
                yield Request(
                    url=self.search_api.format(keyword.lower()),
                    callback=self.parse_suggestions,
                )

    def parse_suggestions(self, response):
        data = response.json()
        directories = list(filter(lambda x: x['title'] == 'Tradies', data))[0]['results']
        for directory in directories:
            for location in self.locations:
                params = {
                    'filter[state]': 'nsw',
                    'filter[category]': directory['practice_seo_key'],
                    'filter[suburb]': location['suburb_seo_key'],
                    'page[limit]': 10,
                    'page[offset]': 0,
                }
                yield Request(
                    url=self.results_api.format(directory['practice_seo_key'], location['suburb_seo_key'], 10, 0),
                    callback=self.parse_results,
                    meta={'location': location['suburb_seo_key'], 'directory': directory['practice_seo_key']}
                )

    def parse_results(self, response):
        print(response.json())