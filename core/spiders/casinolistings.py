import scrapy
from core.utils.security import decode_cf_email
from core.utils.search import find_emails
from core.playwright.playwright_spider import PlaywrightSpider
import asyncio
from http.cookies import SimpleCookie


class CasinolistingsSpider(PlaywrightSpider):
    name = "casinolistings"
    start_urls = ["https://www.casinolistings.com/casinos"]
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "fr-FR,fr;q=0.9,ar-DZ;q=0.8,ar;q=0.7,en-US;q=0.6,en;q=0.5",
        "cache-control": "no-cache",
        "dnt": "1",
        "pragma": "no-cache",
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
    pages = 3
    context = 2

    def start_requests(self):
        for i in range(65):
            yield scrapy.Request(
                url=f"https://www.askgamblers.com/online-casinos/countries/bd/{i+1}",
                headers=self.headers,
                callback=self.parse,
            )
        for i in range(39):
            yield scrapy.Request(
                url=f"https://www.askgamblers.com/online-casinos/countries/be/{i+1}",
                headers=self.headers,
                callback=self.parse,
            )
        for i in range(44):
            yield scrapy.Request(
                url=f"https://www.askgamblers.com/online-casinos/countries/bg/{i+1}",
                headers=self.headers,
                callback=self.parse,
            )
        for i in range(69):
            yield scrapy.Request(
                url=f"https://www.askgamblers.com/online-casinos/countries/ca/{i+1}",
                headers=self.headers,
                callback=self.parse,
            )
        
    def parse(self, response):
        for casino in response.css('.ag-card > a'):
            name = casino.css('::attr(title)').get()
            link = casino.css('::attr(href)').get()
            link = f'https://www.askgamblers.com{link}' if not 'https://www.askgamblers.com' in link else link
            yield scrapy.Request(
                url=link,
                headers=self.headers,
                callback=self.parse_details,
                meta={'name': name}
            )

    def parse_details(self, response):
        name = response.meta['name']
        emails = response.xpath("//div[contains(text(), 'Email') and @class='review-details__text']/text()").getall()
        website = response.css('.review-details__text > a.js-ga-website::text').get()
        emails = ' '.join(emails)
        emails = find_emails(emails)
        print(name,emails,website)
        if all([name,emails,website]):
            item = {
                'name':name,
                'emails':emails,
            }
            yield scrapy.Request(
                url=website,
                callback=self.yield_item,
                meta={"item":item, 'playwright':False,'handle_httpstatus_list': [403]}
            )

    def yield_item(self, response):
        item = response.meta['item']
        item['website'] = response.url
        yield item
