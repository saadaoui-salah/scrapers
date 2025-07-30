import scrapy


class OodoSpider(scrapy.Spider):
    name = "oodo"
    start_urls = [("https://www.odoo.com/partners/country/united-states-224", 'united states'),("https://www.odoo.com/partners/country/ireland-99", 'ireland'), ("https://www.odoo.com/partners/country/united-kingdom-222", 'united kingdom')]


    def start_requests(self):
        for url,  country in self.start_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                meta={'country': country}
            )


    def parse(self, response):
        for url in response.css('.h-100.text-decoration-none a::attr(href)').getall():
            yield scrapy.Request(
                url=f"https://www.odoo.com{url}",
                callback=self.parse_details,
                meta=response.meta
            )

        if next_page := response.xpath('//span[@aria-label="Next"]/../@href').get():
            yield scrapy.Request(
                url=f"https://www.odoo.com{next_page}",
                callback=self.parse,
                meta=response.meta
                
            )


    def parse_details(self,response):
        
        for company in response.css('#right_column .card-body'):
            item = {
                'Company Name': company.css('a span::text').get(),
                'Company Url': f"https://www.odoo.com{company.css('a::attr(href)').get()}",
                'Partner':response.css('#partner_name span::text').get(),
                'Country': response.meta['country']
            }
            yield item

