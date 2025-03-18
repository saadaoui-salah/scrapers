import scrapy


class CasinolistingsSpider(scrapy.Spider):
    name = "casinolistings"
    start_urls = ["https://www.casinolistings.com/casinos"]

    def parse(self, response):
        for casino in response.css('td.name a'):
            name = casino.css('::text').get()
            link = casino.css('::attr(href)').get()
            yield scrapy.Request(
                url=f"https://www.casinolistings.com{link}",
                callback=self.parse_details,
                meta={'name':name}
            )

    def parse_details(self, response):
        name = response.mtea['name']
        emails = response.css("//li/em[contains(text(), 'Email')]/../text()").get()
        website = response.css('.casino-actions a.play::attr(href)').get()
        print(emails)
        if all([name,emails,website]):
            item = {
                'name':name,
                'emails':emails,
            }
            yield scrapy.Request(
                url=website,
                callback=self.yield_item,
                meta={"item":item, 'handle_httpstatus_list': [403]}
            )

    def yield_item(self, response):
        item = response.meta['item']
        item['website'] = response.url
        yield item
