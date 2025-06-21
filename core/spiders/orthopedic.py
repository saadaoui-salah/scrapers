import scrapy


class OrthopedicSpider(scrapy.Spider):
    name = "orthopedic"
    start_urls = ["https://orthopedic.io/physio-therapists/ga/"]

    def parse(self, response):
        for city in response.css('.col-md-3 .mynav a'):
            yield scrapy.Request(
                url=f"https:{city.css('::attr(href)').get()}",
                callback=self.parse_doctors,
                meta={'city': city.css('::text').get()}
            )

    def parse_doctors(self, response):
        for doc in response.css('.doclist'):
            yield {
                'name': doc.css('.inline a::text').get(),
                'phone': doc.xpath("./small/span[contains(@class, 'glyphicon-phone')]/following-sibling::text()[1]").get('').replace('\xa0', ''),
                'fax': doc.xpath("./small/span[contains(@class, 'glyphicon-print')]/following-sibling::text()[1]").get(),
                'city': response.meta['city']
            }
        
        if next_page := response.css('[rel="next"]::attr(href)').get():
            yield scrapy.Request(
                url=f"https:{next_page}",
                callback=self.parse_doctors,
                meta=response.meta
            )