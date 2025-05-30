import scrapy


class CarsSpider(scrapy.Spider):
    name = "cars"
    start_urls = ["https://www.cars.ie/dealers"]

    def parse(self, response):
        dealers = response.css('.car-listing-inner a::attr(href)').getall()
        for dealer in dealers:
            yield scrapy.Request(
                url=f"https://www.cars.ie{dealer}",
                callback=self.parse_dealers
            )

    def parse_dealers(self, response):
        for dealer in response.css('#dealer-search a::attr(href)').getall():
            yield scrapy.Request(
                url=f"https://www.cars.ie{dealer}",
                callback=self.parse_details
            )

    def parse_details(self, response):
        if response.xpath("//div[@class='row']/div[contains(text(), 'Dealer')]/following-sibling::*[1]/a/text()").get():
            yield {
                'name': response.xpath("//div[@class='row']/div[contains(text(), 'Dealer')]/following-sibling::*[1]/a/text()").get(),
                'phone number': response.xpath("//div[@class='row']/div[contains(text(), 'Phone')]/following-sibling::*[1]/a/text()").get(),
                'website': response.xpath("//div[@class='row']/div[contains(text(), 'Website')]/following-sibling::*[1]/a/text()").get(),
                'link': response.url
            }
