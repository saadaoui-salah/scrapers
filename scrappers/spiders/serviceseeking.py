import scrapy
from w3lib.html import remove_tags
from scrappers.items import Service
import re
from scrapy import Request
from html import unescape

class ServiceseekingSpider(scrapy.Spider):
    name = "serviceseeking"
    allowed_domains = ["serviceseeking.com.au"]
    start_urls = ["https://www.serviceseeking.com.au/categories"]

    def parse(self, response):
        cats = response.css('.all-categories-container')
        keywords = {'Fenc':['Fencing', 'Fencer'],'Landscap':'Landscaper','Handym':'Handymen','Carpenter':'Carpenter'}
        for cat in cats:
            for keyword, val in keywords.items():
                if keyword.lower() in cat.css('a::text').get().lower():
                    slug = cat.css('a::attr(href)').get()
                    yield Request(
                        url=f'https://www.serviceseeking.com.au{slug}',
                        callback=self.parse_results,
                        meta={'category': cat.css('a::text').get(), 'trade': val, 'url': f'https://www.serviceseeking.com.au{slug}'}
                    )
            

    def parse_results(self, response):
        cards = response.css('.mbd-card')
        for card in cards:
            slug = card.css('.card-content.card-pad-md.visible-xs a::attr(href)').get()
            url = f"https://www.serviceseeking.com.au{slug}"
            yield Request(
                url=url,
                callback=self.parse_details,
                meta=response.meta
            )
        if response.css('#view-more-business-cards').get():
            page = response.meta.get('page', 1) + 1
            response.meta['page'] = page
            yield Request(
                url=f"{response.meta['url']}?page={page}",
                callback=self.parse_results,
                meta=response.meta
            )
        
            
    def parse_details(self, response):
            awards = []
            for badge in response.css('.bio-badge-description'):
                if 'award' in badge.css('div .bold::text').get('').lower():
                    awards = badge.css('div .pl4::text').get()
                    print(awards)
            response_time = ''
            for sel in response.css('#profile-about-us .col-xs-12'):
                if 'response' in sel.css('.bold::text').get('').lower():
                    response_time = sel.css('.pr8 .text-gray')

            services = []
            services += response.css('#profile-services .panel-body a::text').getall()
            services += response.css('#profile-services .panel-body div::text').getall()
            email_pattern = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'
            item = Service()
            item['business_name'] = response.css('div[itemprop="name"]::text').get()
            item['trade_type'] = response.meta['trade']
            item['description'] = remove_tags(response.css('#about-us').get(''))
            item['abn'] = response.css('.abn-number-link a::attr(href)').get('').split('SearchText=')[-1]
            item['license_number'] = ''
            emails = re.findall(email_pattern, item['description'])
            item['email'] = emails[0] if emails else ''
            item['social_media'] = ''
            item['category'] = response.meta['category']
            item['location'] = response.css('.row .text-copy-2.font-14::text').getall()[1]
            item['contact_information'] = ''
            item['reviews'] = response.css('.js-scroll-to-reviews::text').get()
            item['rating_avg'] = unescape(response.css('.star-rating-sm::text').get(''))
            item['primary_services'] = services
            item['specializations'] = response.meta['category']
            item['awards'] = awards
            item['website'] = response.css('a[itemprop="url"].flat-link::attr(href)').get()
            item['response_time'] = response_time
            item['availability'] = ''
            item['equipment_provided'] = ''
            item['experience'] = ''
            item['insurance_coverage'] = ''
            item['current_url'] = response.url
            yield item
