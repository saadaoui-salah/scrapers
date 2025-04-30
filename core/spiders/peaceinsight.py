import scrapy


class PeaceinsightSpider(scrapy.Spider):
    name = "peaceinsight"
    start_urls = ["https://www.peaceinsight.org/api/v1/organisation-search/?format=json&limit=990999&location=&theme="]

    def parse(self, response):
        results = response.json()['results']
        for result in results:
            yield scrapy.Request(
                url=f"https://www.peaceinsight.org{result['url']}",
                callback=self.parse_details,
            )

    def parse_details(self, response):
        data = {}
        data['website'] = response.xpath("//h4[contains(text(), 'Website')]/../div/a/@href").get()
        data['phone_number'] = response.xpath("//h4[contains(text(), 'Phone')]/../div/a/@href").get('').replace('tel:', '')
        data['email'] = response.xpath("//h4[contains(text(), 'Email')]/../div/a/@href").get('').replace('mailto:', '')
        data['name'] = response.css(".text-XXL::text").get('')
        data['url'] = response.url
        yield data