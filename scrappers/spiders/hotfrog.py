import scrapy
from scrapy import Request
from scrappers.items import Service
from w3lib.html import remove_tags 

class HotfrogSpider(scrapy.Spider):
    name = "hotfrog"
    allowed_domains = ["www.hotfrog.com.au"]
    start_urls = ["https://www.hotfrog.com.au"]
    keywords = ['fencer','landscapers','handymen','carpenters','fencing','gate','timber']

    def start_requests(self):
        for keyword in self.keywords:
            url = f"https://www.hotfrog.com.au/search/au/{keyword.lower()}"
            yield Request(
                url=url,
                callback=self.parse_search,
                meta={'keyword':keyword, 'url': url, 'page': 1}
            )

    def parse_search(self, response):
        for box in response.css('.hf-box'):
            slug = box.css('h3 a[data-yext-click="name"]::attr(href)').get()
            item = Service()
            item['location'] = response.css('.col-8 > span.small::text').get()
            item['business_name'] = remove_tags(response.css('a[data-yext-click="name"]').get())
            item['phone_number'] = remove_tags(response.css('a[data-yext-click="phone"]').get())
            item['trade_type'] = response.meta['keyword']
            yield Request(
                url=f"https://www.hotfrog.com.au{slug}",
                callback=self.parse_results,
                meta={'item': item}
            )
        
        not_found = 'no results found' in response.css('.text-center h1::text').get('').lower()
        if not not_found:
            page = response.meta['page'] + 1
            url = f"{response.meta['url']}/{page}"
            response.meta['page'] = page
            yield Request(
                url=url,
                callback=self.parse_search,
                meta=response.meta
            ) 




    def parse_results(seelf, response):
        item = response.meta['item']
        item['description'] = remove_tags(response.css('#description').get(''))
        for key, val in zip(response.css('dl dt'), response.css('dl dd.col-8')):
            row = key.get().lower()
            if 'opening hours' in row:
                item['availability'] = remove_tags(val.get())
            elif 'social' in row:
                item['social_media'] = val.css('a::attr(href)').getall()
            elif 'address' in row:
                item['location'] = remove_tags(val.get())
                
        item['reviews'] = remove_tags(response.css('.business-reviews').get('')).replace('\n','').strip()
        item['primary_services'] = response.css('p > span.serp-tag::text').getall()
        item['specializations'] = response.css('em .serp-tag::text').getall()
        item['website'] = response.css('a[data-click="website"]::attr(href)').get()
        item['category'] = response.css('.breadcrumb a span.text-capitalize::text').get()
        item['current_url'] = response.url
        yield item
