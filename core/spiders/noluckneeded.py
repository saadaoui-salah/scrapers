import scrapy
from core.utils.security import decode_cf_email


class NoluckneededSpider(scrapy.Spider):
    name = "noluckneeded"
    start_urls = ["https://www.noluckneeded.com/casino-directory"]

    def start_requests(self):
        for i in range(1, 70):
            yield scrapy.Request(
                url=f"https://www.noluckneeded.com/casino-directory/page-{i}",
                callback=self.parse
            )

    def parse(self, response):
        for casino in response.css('.results .casino_title a::attr(href)').getall():
            yield scrapy.Request(
                url=casino,
                callback=self.parse_details
            )
    
    def parse_details(self, response):
        name = response.css('.page_fancy_title a::text').get('').lower().split('review')[0]
        emails = response.css(".__cf_email__::attr(data-cfemail)").getall()
        emails = [decode_cf_email(mail) for mail in emails]
        website = response.xpath("//a[contains(text(), 'Review by NoLuckNeeded.com')]/@href").get()
        if all([name, emails, website]):
            yield scrapy.Request(
                url=website,
                callback=self.yield_item,
                meta={'item':{'name':name, 'emails':emails},  'handle_httpstatus_list': [403]}
            ) 
    
    def yield_item(self, response):
        item = response.meta['item']
        item['website'] = response.url
        yield item