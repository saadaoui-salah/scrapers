import scrapy


class ArchitectsSpider(scrapy.Spider):
    name = "architects"

    def start_requests(self):
        for i in range(50):
            url = f'https://www.architectes.org/recherche?created=&created_1=&search_api_fulltext=architect&f%5B0%5D=search_facet_type_de_contenu%3Aannonce&page={i}'
            yield scrapy.Request(
                url=url,
                callback=self.parse_results
            ) 

    def parse_results(self, response):
        for slug in response.css('.views-row a::attr(href)').getall():
            url = f"https://www.architectes.org{slug}"
            yield scrapy.Request(
                url=url,
                callback=self.parse_details
            )
    
    def parse_details(self, response):
        email = response.css('.field--type-email a::text').get()
        if email:
            yield {
                'email':email,
                'name': response.css('.organization::text').get()
            }