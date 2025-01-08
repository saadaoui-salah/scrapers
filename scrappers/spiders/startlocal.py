import json
import scrapy
from scrapy import Request
from scrappers.items import Service


class StartlocalSpider(scrapy.Spider):
    name = "startlocal"
    allowed_domains = ["startlocal.com.au"]
    start_urls = ["https://startlocal.com.au"]
    keywords = ['fencer','landscapers','handymen','carpenters','fencing','gate','timber']
    
    def parse(self, response):
        for url in response.css('ul.horizontal-category li a::attr(href)').getall():
            body = json.dumps({
                "operationName": None,
                "variables": {
                    "category": url.replace('/','')
                },
                "query": "query ($category: String) {\n  category(buildDirectoryName: $category) {\n    id\n    name\n    buildDirectoryName\n    userGuide\n    childCategories(take: 1000) {\n      edges {\n        name\n        buildDirectoryName\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"
            }) 
            self.headers = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
                "Accept": "application/json",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "identity",
                "Content-Type": "application/json",
                "X-Requested-With": "XMLHttpRequest",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "Te": "trailers"
            }
            yield Request(
                url=f'https://api.startlocal.com.au/',
                method='POST',
                body=body,
                dont_filter=True,
                headers=self.headers,
                callback=self.parse_first
            )

    def parse_first(self, response):
        data = response.json()['data']['category']
        for keyword in self.keywords:
            for cat in data['childCategories']['edges']:
                if keyword in cat['name'].lower():
                    body = json.dumps({
                        "operationName": None,
                        "variables": {
                            "category": cat['buildDirectoryName']
                        },
                        "query": "query ($category: String) {\n  category(buildDirectoryName: $category) {\n    id\n    name\n    buildDirectoryName\n    userGuide\n    parentCategory {\n      name\n      buildDirectoryName\n      __typename\n    }\n    childCategories(where: {numberOfLinks_gt: 0}, take: 1000) {\n      edges {\n        id\n        name\n        fullName\n        buildDirectoryName\n        __typename\n      }\n      __typename\n    }\n    businesses(take: 7) {\n      edges {\n        id\n        name\n        address\n        state\n        suburb\n        postcode\n        fileLogoThumbnail\n        presenceOnlineOnly\n        slug\n        about\n        phone\n        email\n        categories {\n          edges {\n            id\n            name\n            buildDirectoryName\n            parentCategory {\n              id\n              name\n              buildDirectoryName\n              parentCategory {\n                id\n                name\n                buildDirectoryName\n                __typename\n              }\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    articles {\n      name\n      brief\n      slug\n      __typename\n    }\n    __typename\n  }\n}\n"
                    })
                    yield Request(
                        url=f'https://api.startlocal.com.au/',
                        method='POST',
                        body=body,
                        dont_filter=True,
                        headers=self.headers,
                        meta={'trade': keyword},
                        callback=self.parse_second
                    )


    def parse_second(self, response):
        data = response.json()['data']['category']['childCategories']['edges']
        for location in data:
            body = json.dumps({
                "operationName": None,
                "variables": {
                    "category": location['buildDirectoryName']
                },
                "query": "query ($category: String) {\n  category(buildDirectoryName: $category) {\n    id\n    name\n    buildDirectoryName\n    userGuide\n    parentCategory {\n      name\n      buildDirectoryName\n      __typename\n    }\n    childCategories(where: {numberOfLinks_gt: 0}, take: 1000) {\n      edges {\n        id\n        name\n        fullName\n        buildDirectoryName\n        __typename\n      }\n      __typename\n    }\n    businesses(take: 7) {\n      edges {\n        id\n        name\n        address\n        state\n        suburb\n        postcode\n        fileLogoThumbnail\n        presenceOnlineOnly\n        slug\n        about\n        phone\n        email\n        categories {\n          edges {\n            id\n            name\n            buildDirectoryName\n            parentCategory {\n              id\n              name\n              buildDirectoryName\n              parentCategory {\n                id\n                name\n                buildDirectoryName\n                __typename\n              }\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    articles {\n      name\n      brief\n      slug\n      __typename\n    }\n    __typename\n  }\n}\n"
            })
            yield Request(
                url=f'https://api.startlocal.com.au/',
                method='POST',
                body=body,
                dont_filter=True,
                headers=self.headers,
                meta=response.meta,
                callback=self.parse_location,
            )


    def parse_location(self, response):
        data = response.json()['data']['category']['businesses']['edges']
        for service in data:
            body = json.dumps({
                "operationName": None,
                "variables": {
                    "id": int(service['id'])
                },
                "query": "query ($id: Int!) {\n  business(id: $id) {\n    id\n    name\n    about\n    url\n    email\n    phone\n    address\n    suburb\n    state\n    postcode\n    hoursMonOpen\n    hoursMonClose\n    hoursTueOpen\n    hoursTueClose\n    hoursWedOpen\n    hoursWedClose\n    hoursThuOpen\n    hoursThuClose\n    hoursFriOpen\n    hoursFriClose\n    hoursSatOpen\n    hoursSatClose\n    hoursSunOpen\n    hoursSunClose\n    hoursHolidayOpen\n    hoursHolidayClose\n    fileLogoThumbnail\n    fileImg1Thumbnail\n    fileImg1Large\n    fileImg2Thumbnail\n    fileImg2Large\n    fileImg3Thumbnail\n    fileImg3Large\n    fileImg4Thumbnail\n    fileImg4Large\n    fileImg5Thumbnail\n    fileImg5Large\n    fileImg1Description\n    fileImg2Description\n    fileImg3Description\n    fileImg4Description\n    fileImg5Description\n    rating\n    votes\n    categories {\n      edges {\n        name\n        buildDirectoryName\n        parentCategory {\n          name\n          buildDirectoryName\n          parentCategory {\n            name\n            buildDirectoryName\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    slug\n    specialties\n    __typename\n  }\n}\n"
            })
            yield Request(
                url=f'https://api.startlocal.com.au/',
                method='POST',
                body=body,
                dont_filter=True,
                meta=response.meta,
                headers=self.headers,
                callback=self.parse_results,
            )
    
    def parse_results(self, response):
        data = response.json()['data']['business']
        item = Service()
        item['business_name'] = data['name']
        item['phone_number'] = data['phone']
        item['location'] = f"{data['address']}, {data['suburb']}, {data['state']}, {data['postcode']}"
        item['reviews'] = data['votes']
        item['rating_avg'] = data['rating']
        item['category'] = data['categories']['edges'][0]['parentCategory']['parentCategory']['name']
        item['email'] = data['email']
        item['current_url'] = f"https://startlocal.com.au{data['slug']}"
        item['website'] = data['url']
        item['trade_type'] = response.meta['trade']
        item['description'] = data['about']
        item['availability'] ={ "hoursMonOpen": data['hoursMonOpen'],
                                "hoursMonClose": data['hoursMonClose'],
                                "hoursTueOpen": data['hoursTueOpen'],
                                "hoursTueClose": data['hoursTueClose'],
                                "hoursWedOpen": data['hoursWedOpen'],
                                "hoursWedClose": data['hoursWedClose'],
                                "hoursThuOpen": data['hoursThuOpen'],
                                "hoursThuClose": data['hoursThuClose'],
                                "hoursFriOpen": data['hoursFriOpen'],
                                "hoursFriClose": data['hoursFriClose'],
                                "hoursSatOpen": data['hoursSatOpen'],
                                "hoursSatClose": data['hoursSatClose'],
                                "hoursSunOpen": data['hoursSunOpen'],
                                "hoursSunClose": data['hoursSunClose'],
                                "hoursHolidayOpen": data['hoursHolidayOpen'],
                                "hoursHolidayClose": data['hoursHolidayClose']}
        yield item