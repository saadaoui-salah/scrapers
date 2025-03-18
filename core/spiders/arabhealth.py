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
        "authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb3JlQXBpVXNlcklkIjoiVlhObGNsOHlNalEwT0RreU1nPT0iLCJwZXJtaXNzaW9ucyI6WyJhcHBsaWNhdGlvbjpRWEJ3YkdsallYUnBiMjVmTlRJeCIsInNjaGVtYTp1c2VyIl0sInNlc3Npb25JZCI6IjY3YTYwNjU1NTg0ZjFiYTgxMzNhNWI1NyIsInR5cGUiOiJhY2Nlc3MtdG9rZW4iLCJ1c2VySWQiOiI2NzQ5YmIwYTczMWY2OWUwZjc4M2NlZmMiLCJlbWFpbFZlcmlmaWVkIjp0cnVlLCJpYXQiOjE3NDAyNTMxMjAsImV4cCI6MTc0MDMzOTUyMCwiaXNzIjoiYXV0aC1hcGkifQ.UVYPmLbUc5xwdOmWmYrDTOkTuO0MmzGtYjU3p9nomRL2dwWkfkjVcY7_1JB46FXjQslEbWDWIapgz3AiYm78PUiUvteLX252X1uGtO0FeClvfz7n9RJIHCE73l4voNj5pQpfPsuP13Nx0nVWehm0yF61opex7QRoMTiPEZREgDVIZ7Bih3kVH9wsFSBh4aUe3pRVwRqm8lClEg53KOYpYcUSMzPEqcm1R_wMme6h-o6HX3vFpS3Ok3n3D88WBf8pv6ignJ2xm1RB-3u56_Fja3_x0lz1bjsjSQIfTNPJtfigQMeAz58v9rE49IvXfnhppP65pzjUFGzPtvsRGadwsR3TflHo2hkvD6UG6ITZkKurNjkByHPpsg-Z3W1iysoqy8PFuMLIC1EPFOxPOBsAn8ZJLN_HPApHC4nGtjFUB21l2eaEBiHIQlf32TrZqToLBXHkXVQ1hnUj2HHZg9dO1Qxw8JY8yL0oDU9JgH3Qlym-MGurJxCTyBKRFzRY9zUG6oBYjqNFpEbTIRqKNjcKkmON23PTtSjlTdc-cYz68CYENTHtURCiVMMdZb5vMW1I6dQBPqkwn5Aem5pRaNpIvdNE6e_G1gFgOZ5vzEt2VMWI-fn4vplcSrTMVtex3H7_nET_UUdbRYWnIUcL_9kaYUd38x15fHhQqgQV6-YV8Ys",
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
                "proxy": 'http://127.0.0.1:8080',
            },
        )

    def start_crawling(self, response, end_cursor=None):
        keywords = ['Regulatory']
        for keyword in keywords:
            data = [{"operationName":"EventPeopleListViewConnectionQuery","variables":{"viewId":"RXZlbnRWaWV3Xzk2MDU5OQ==","search":keyword},"extensions":{"persistedQuery":{"version":1,"sha256Hash":"7f6aeac87634ef772c93d5b0b2e89c9e7ed810a19868180507be401b9ab18214"}}}]
            if end_cursor:
                data[0]['variables']["endCursor"] = end_cursor
            yield scrapy.Request(
                url=self.url,
                method="POST",
                headers=self.headers,
                body=json.dumps(data),
                callback=self.send_request,
                meta={
                    "proxy": 'http://127.0.0.1:8080',
                },
            )   
    
    
    def send_request(self, response):
        data = response.json()
        data = list(filter(lambda x: x.get('data'), data))[0]
        if data['data']['view']['people']['pageInfo']['hasNextPage']:
            yield from self.start_crawling('', data['data']['view']['people']['pageInfo']['endCursor'])
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
                meta={'proxy': 'http://127.0.0.1:8080'}
            )

    def parse(self, response):
        data = response.json()[0]['data']['person']
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