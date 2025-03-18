from scrapy import Spider, Request, Item, Field
from urllib.parse import quote
from core.utils.utils import generate_cookies
import os
import json
from w3lib.html import remove_tags
import pandas as pd



class ServiceItem(Item):
    # Define fields to store scraped data
    name = Field()
    phone_number = Field()


class PagejauneSpider(Spider):
    logfile = ''
    name = "pagejaune"
    allowed_domains = ["pagesjaunes.fr"]
    # 'Loiret (45)'
    locations = '14-61-27-76-62-80-59-02-60-08-51-55-54-57-67-88-68-52-10-70-21-89-58-71-39-18-41-28-45-03-42-69-01-63-43-77-95-78-91'
    categories = ['Société de rénovation']#'Entreprise BTP', 'Société de rénovation', 'Entrepreneur en construction', 'Entreprise de construction', 'Architecte', 'Promoteur immobilier']
    num = 0
    def parse_locations(self):
        self.cookies = generate_cookies(['https://www.pagesjaunes.fr/','https://www.pagesjaunes.fr/pagesblanches/','https://www.pagesjaunes.fr/pagesblanches/recherche?quoiqui=Restaurant&ou=Eure-et-Loir+(28)&univers=pagesblanches&idOu='])
        for location in self.locations.split('-'):
            url = f"https://www.pagesjaunes.fr/autocomplete/search/where?query={location}&profile=BROWSING"
            yield Request(
                    url=url,
                    headers = {
                        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
                        "Accept": "application/json",
                        "Accept-Language": "en-US,en;q=0.5",
                        "Accept-Encoding": "identity",
                        'Referer': 'https://www.pagesjaunes.fr/pagesblanches/recherche?quoiqui=Restaurant&ou=Eure-et-Loir+(28)&univers=pagesblanches&idOu=',
                        "X-Requested-With": "XMLHttpRequest",
                        "Sec-Fetch-Dest": "empty",
                        "Sec-Fetch-Mode": "cors",
                        "Sec-Fetch-Site": "same-origin",
                        "Te": "trailers"
                    },
                    cookies=self.cookies,
                    callback=self.parse_locations,
                    meta={'loc': location}
                )

    def start_requests(self):
        self.cookies = generate_cookies(['https://www.pagesjaunes.fr/','https://www.pagesjaunes.fr/pagesblanches/','https://www.pagesjaunes.fr/pagesblanches/recherche?quoiqui=Restaurant&ou=Eure-et-Loir+(28)&univers=pagesblanches&idOu='])
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": "https://www.pagesjaunes.fr/",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Te": "trailers"
        }
        for keyword in self.categories:
            url = f"https://www.pagesjaunes.fr/annuaire/chercherlespros?quoiqui={quote(keyword)}"
            yield Request(
                url=url,
                headers=self.headers,
                cookies=self.cookies,
                callback=self.parse,
                meta={'category':keyword}
            )

    def parse(self, response):
        page = response.meta.get('page', 1)
        for service in response.css('ul.bi-list > li'):
            item = ServiceItem()
            item['name'] = service.css('.bi-denomination h3::text').get()
            item['phone_number'] = service.css('.number-contact > span::text').get()
            if item['phone_number']:
                yield item
        next_url = response.css('a.next').get()
        if next_url and not response.meta.get('pagination_done', False):
            quoiqui = quote(response.css("input[name='quoiqui']::attr('value')").get())
            quoiQuiInterprete = quote(response.css("input[name='quoiQuiInterprete']::attr('value')").get())
            contexte = quote(response.css("input[name='contexte']::attr('value')").get())
            page += 1
            response.meta['pagination_done'] = True
            response.meta['errback_retry'] = 0
            fy = True
            pages_count = int(remove_tags(response.css('#SEL-compteur').get('')).strip().split('/')[-1])
            for i in range(page, pages_count + 1):
                response.meta['page'] = i
                url = f"https://www.pagesjaunes.fr/pagesblanches/recherche?quoiqui={quoiqui}&quoiQuiInterprete={quoiQuiInterprete}&contexte={contexte}&page={i}"
                yield Request(
                    url=url,
                    headers=self.headers,
                    cookies=self.cookies,
                    callback=self.parse,
                    errback=self.errback,
                    meta=response.meta
                )

    def errback(self, failure):
        self.cookies = generate_cookies(['https://www.pagesjaunes.fr/'])
        retry = failure.value.response.meta.get('errback_retry', 1)
        if retry > 15:
            failure.value.response.meta['errback_retry'] = retry + 1
            yield failure.request.replace(cookies=self.cookies, meta=failure.value.response.meta['errback_retry'])
        else:
            self.logger.error(f'[Errback] Gave Up retry {failure.request.url}')
