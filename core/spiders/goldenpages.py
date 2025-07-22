import scrapy
from core.proxy.zyte_api import  ZyteRequest 
import base64
import json

class GoldenpagesSpider(scrapy.Spider):
    name = "goldenpages"
    proxy = 'zyte_api'
    emails = []

    def start_requests(self):
        for i in range(4000, 8000):
            yield ZyteRequest(
                url=f'https://www.goldenpages.be/search/roofers/1/?Where={i}',
                callback=self.parse
            )

    def load(self, response):
        response = base64.b64decode(response.json()['httpResponseBody'])
        try:
            response = json.loads(response)
        except Exception:
            response = scrapy.Selector(text=response)
            
        return response

    def parse(self, response):
        response = self.load(response)
        for url in response.css('.result-item [itemprop="url"]::attr(content)').getall():
            yield ZyteRequest(
                url=url,
                callback=self.parse_details,
                meta={'url': url}
            )
        if next_link := response.xpath('//svg[contains(@class, "-rotate-90")]/ancestor::a[1]/@href').get():
            yield ZyteRequest(
                url=next_link,
                callback=self.parse
            )


    def parse_details(self, response):
        url = response.meta['url']
        response = self.load(response)
        phone = response.css('#phoneNumber a::attr(data-phone-number)').get()
        if not phone:
            phone = response.css('[itemprop="telephone"]::attr(content)').get()
        email = response.css('[data-ta="EmailBtnClick"]::attr(href)').get('').replace('mailto:','').split('?')[0]
        company = response.css('#listing-title span::text').get()
        if not email:
            print(url)
        data = {
            'website':response.css('[data-label="Website"] a::attr(href)').get(),
            'phone': phone,
            'email': email or None,
            'city/post code': f"{response.css('[data-yext="address"] [data-yext="postal-code"]::text').get()} {response.css('[data-yext="address"] [data-yext="city"]::text').get()}",
            'company': company,
            'kbo': response.xpath("//a[contains(text(), 'Link to KBO')]/@href").get(),
        }
        if email:
            if email not in self.emails:
                self.emails += [email]
                yield data
        else:
            if data['website']:
                yield data