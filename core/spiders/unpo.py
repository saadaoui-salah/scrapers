import scrapy


class UnpoSpider(scrapy.Spider):
    name = "unpo"
    start_urls = ["https://unpo.org/members/"]

    def parse(self, response):
        orgs  = response.css('.elementor-image-box-title a::attr(href)').getall()
        for org in orgs:
            yield scrapy.Request(
                url=f"https://unpo.org{org}" if 'http' not in org else org,
                callback=self.parse_details
            )


    def parse_details(self,response):
        data = {}
        data['name'] = response.css('.elementor-widget-container h4.elementor-heading-title::text').get()
        data['website'] = response.css('[aria-labelledby="bluesea"] a::attr(href)').get()
        data['email'] =  ''
        yield data