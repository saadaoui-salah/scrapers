import scrapy
import json

class Lead(scrapy.Item):
    profile_link = scrapy.Field()
    first_name = scrapy.Field()
    last_name = scrapy.Field()
    title = scrapy.Field()
    company = scrapy.Field()
    mobile = scrapy.Field()
    phone = scrapy.Field()
    email = scrapy.Field()
    country = scrapy.Field()
    linkedin = scrapy.Field()

class ArabHealthSpider(scrapy.Spider):
    name = "arab_health"
    start_urls = ["https://connections.arabhealthonline.com/api/graphql"]

    url = "https://connections.arabhealthonline.com/api/graphql"
    
    headers = {
        "accept": "*/*",
        "accept-language": "fr-FR,fr;q=0.9,ar-DZ;q=0.8,ar;q=0.7,en-US;q=0.6,en;q=0.5",
        "authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb3JlQXBpVXNlcklkIjoiVlhObGNsOHlNalEwT0RreU1nPT0iLCJwZXJtaXNzaW9ucyI6WyJhcHBsaWNhdGlvbjpRWEJ3YkdsallYUnBiMjVmTlRJeCIsInNjaGVtYTp1c2VyIl0sInNlc3Npb25JZCI6IjY3YTYwNjU1NTg0ZjFiYTgxMzNhNWI1NyIsInR5cGUiOiJhY2Nlc3MtdG9rZW4iLCJ1c2VySWQiOiI2NzQ5YmIwYTczMWY2OWUwZjc4M2NlZmMiLCJlbWFpbFZlcmlmaWVkIjp0cnVlLCJpYXQiOjE3NDAxMjg5ODYsImV4cCI6MTc0MDIxNTM4NiwiaXNzIjoiYXV0aC1hcGkifQ.pQYxvGjcx-jSbTSEXdnz3tZdSgDK7fl40cKj2G6RjWyzs9QfvjVMBOEattoHOg8bjGy4at5v-rl2NEHpeWrQNzPg2rBJ2MlVpIwFJQNPYoIPN1ySf8uOM93wrQXHiCDGWQZ8pQiIZI8_k1QhpHcOxMQ6e-d3a4j32E6725Skqw6yLXmzOnTSQxooUKOvlVLru5ptYTgCxWJRMXtSPLjjESevcTajdgBupvWngf_2rN2jf1_lBPxfAzHRvmwmy1U098khC_JvXKQ4N-GsdZ45krubIjue00jHxuw7ZtDBStKDvMhv2cnydOKnOAANLKvMlO6lhr49Rb6eFvr8h60PUyF_nIZNHRE56k6BBNWqHKxF_aCDX1_hC7wEw3i2NHuO1f7Qy2NLIxPTRXIDyEGX6hJ3hK9jQ4HpUVLfvkwfe5Tw5Sr1xsQ9Eh-7f7SbUQ4PB-B-G2PinFEXX-G1XzFRW1qyr1XxlmdiZGN3Xmw3ROLZEul-LoI794BPOQvfIHg10tHwqAu1HGRVDtqSzhWIrLCiyspPSPrBu50ZJK8hqph9IfpbkgQwviMJ3OfN_KfRWt3R3WWRLF6f-jy6eI4I-u90eeT4EfbxIqAdLpuHYCVxN5FbagqEvBPB7hG2cZqF_rwV0mLG4xiUmo11ifxcy3F2UJYvbxU5XFRQ3LiMDSo",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "dnt": "1",
        "origin": "https://connections.arabhealthonline.com",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://connections.arabhealthonline.com/",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "x-client-origin": "connections.arabhealthonline.com",
        "x-client-platform": "Event App",
        "x-client-version": "2.309.108",
        "x-feature-flags": "fixBackwardPaginationOrder"
    }
    def start_requests(self):
        yield scrapy.Request(
            url='https://connections.arabhealthonline.com/',
            headers=self.headers,
            callback=self.start_crawling,
            meta={
                "playwright": True,
            },
        )

    def start_crawling(self):
        keywords = ['Quality','Operation','Regulatory']
        for keyword in keywords:
            data = [{"operationName":"EventPeopleListViewConnectionQuery","variables":{"viewId":"RXZlbnRWaWV3Xzk2MDU5OQ==","search":keyword},"extensions":{"persistedQuery":{"version":1,"sha256Hash":"7f6aeac87634ef772c93d5b0b2e89c9e7ed810a19868180507be401b9ab18214"}}}]
            yield scrapy.Request(
                url=self.url,
                method="POST",
                headers=self.headers,
                body=json.dumps(data),
                callback=self.send_request,
                meta={
                    "playwright": True,
                },
            )   
    
    
    def send_request(self, response):
        print(response.text)
        data = json.loads(response.css('pre::text').get())[0]
        poeples = data['data']['view']['people']['nodes']
        for person in poeples:
            payload = [
                {
                    "operationName": "EventPersonDetailsQuery",
                    "variables": {
                        "skipMeetings": True,
                        "withEvent": True,
                        "personId": person['id'],
                        "userId": "",
                        "eventId": "RXZlbnRfMjE0ODk4OA=="
                    },
                    "extensions": {
                        "persistedQuery": {
                            "version": 1,
                            "sha256Hash": "03e6ab3182b93582753b79d92ee01125bd74c7164986e7870be9dcad9080f048"
                        }
                    }
                },
                {
                    "operationName": "PersonUserId",
                    "variables": {
                        "personId": person['id']
                    },
                    "extensions": {
                        "persistedQuery": {
                            "version": 1,
                            "sha256Hash": "109137c30f77f624ffa4263a20e90a0a4fc9e9e7ddade6a7a5039a935b69e1b0"
                        }
                    }
                }
            ]

            yield scrapy.Request(
                url=self.url,
                method="POST",
                headers=self.headers,
                body=json.dumps(payload),
                callback=self.parse,
                meta={'playwright': True}
            )

    def parse(self, response):
        data = json.loads(response.css('pre::text').get())[0]['data']['person']
        linkedin = list(filter(lambda x: 'LINKEDIN' == x['type'] ,data['socialNetworks']))
        item = Lead()
        item['profile_link'] = f"https://connections.arabhealthonline.com/event/arab-health-2025-1/person/{data['id']}"
        item['first_name'] = data['firstName']
        item['last_name'] = data['lastName']
        item['title'] = data['jobTitle']
        item['company'] = data['organization']
        item['mobile'] = data['mobilePhone']['formattedNumber'] if data['mobilePhone'] else None 
        item['phone'] = data['landlinePhone']['formattedNumber'] if data['landlinePhone'] else None
        item['email'] = data['email']
        item['country'] = list(filter(lambda x: 'country' == x['name'].lower(), data['withEvent']['fields']))[0]['value']['text']
        item['linkedin'] = linkedin[0]['profile'] if linkedin else None
        #if any([item['email'], item['phone'], item['mobile'], item['linkedin']]):
        yield item