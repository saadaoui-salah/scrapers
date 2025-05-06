import scrapy
from core.utils.security import decode_cf_email 

class UnrepresentedunitednationsSpider(scrapy.Spider):
    name = "unrepresentedunitednations"
    start_urls = ["https://www.unrepresentedunitednations.org/en/unrepresented-united-nations-directory/"]

    def parse(self, response):
        for cart in response.css('.card-body > a[title]::attr(href)').getall():
            yield scrapy.Request(
                url=f'https://www.unrepresentedunitednations.org{cart}',
                callback=self.parse_details
            )

    def parse_details(self, response):
        data = {}
        data['name'] = response.css('h2.text-center::text').get()
        if mail := response.css("span > a.__cf_email__::attr(data-cfemail)").get():
            data['email'] = decode_cf_email(mail) 
        data['website'] = response.css('.tooltips::attr(title)').get()
        data['url'] = response.url
        yield data