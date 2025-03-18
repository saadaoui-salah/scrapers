import scrapy
from core.utils.search import find_emails


class CasinolistingsSpider(scrapy.Spider):
    name = "casinolistings"
    start_urls = ["https://www.casinolistings.com/casinos"]
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "fr-FR,fr;q=0.9,ar-DZ;q=0.8,ar;q=0.7,en-US;q=0.6,en;q=0.5",
        "cache-control": "no-cache",
        "dnt": "1",
        "pragma": "no-cache",
        "priority": "u=0, i",
        "referer": "https://www.casinolistings.com/casinos",
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
    cookies = {
        "_ga": "GA1.1.611698300.1742251557",
        "VARYclprefs": "USD_DZ_",
        "cf_clearance": "LOKMKmHHMSCNtpnqCnPwVkg21yOW4VrdUevD1aiO77w-1742314036-1.2.1.1-nCePBn.GHhIbj75K_MYfOBcUH09ikSqg6Q0eH5yIaK5W6ktMiwU9LL.XOK4Ip5Ux8JhNsMxiMqVllTJzVpXAu249s0aKGatEFcI5kU2Ka4xUfGMezqY3y3IU9oQlAVKfaukzuYCxS.oLS6Yi5PH6tBVoN.X7d67Zo8fuxik7hVeFcXdvCfSQQmSviVCnooTnD0b7PQKct3XM4amyMYlALYrRZ5BTCTFmnDQW0gUKsaRfhM9bXfV6V9JK6kUpgYGnEP61fhJ7nvEhoA7M0B1iiUx7uW1.7_c.ugAC6oW7P9q_JXU78t66C7A46StEYje.Ghod9pFcpVGGU4X6DhFyF192glog8lj0TVKMscDk9PM",
        "_ga_GXDRKL1LX9": "GS1.1.1742312747.3.1.1742314576.60.0.0"
    }

    def start_requests(self):
        yield scrapy.Request(
            url="https://www.casinolistings.com/casinos",
            headers=self.headers,
            cookies=self.cookies,
            callback=self.parse,
            meta={'playwright':True}
        )
        
    def parse(self, response):
        for casino in response.css('td.name a'):
            name = casino.css('::text').get()
            link = casino.css('::attr(href)').get()
            yield scrapy.Request(
                url=f"https://www.casinolistings.com{link}",
                headers=self.headers,
                cookies=self.cookies,
                callback=self.parse_details,
                meta={'name':name, 'playwright':True}
            )

    def parse_details(self, response):
        name = response.meta['name']
        emails = response.xpath("//li/em[contains(text(), 'Email')]/../text()").getall()
        website = response.css('.casino-actions a.play::attr(href)').get()
        emails = ' '.join(emails)
        emails = find_emails(emails)
        if all([name,emails,website]):
            item = {
                'name':name,
                'emails':emails,
            }
            yield scrapy.Request(
                url=f"https://www.casinolistings.com{website}",
                callback=self.yield_item,
                meta={"item":item, 'handle_httpstatus_list': [403], 'playwright':True}
            )

    def yield_item(self, response):
        item = response.meta['item']
        item['website'] = response.url
        yield item
