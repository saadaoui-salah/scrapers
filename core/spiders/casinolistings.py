import scrapy


class CasinolistingsSpider(scrapy.Spider):
    name = "casinolistings"
    allowed_domains = ["casinolistings.com"]
    start_urls = ["https://casinolistings.com"]

    def parse(self, response):
        pass
