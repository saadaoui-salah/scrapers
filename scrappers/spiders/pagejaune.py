from scrapy import Spider, Request, Item, Field
from urllib.parse import quote
from scrappers.utils import generate_cookies
import os
import json
from w3lib.html import remove_tags
import pandas as pd



class ServiceItem(Item):
    # Define fields to store scraped data
    name = Field()
    page = Field()
    url = Field()
    location = Field()
    address = Field()
    category = Field()
    phone_number = Field()

logfile = ''.join(open('./page2.log', 'r').readlines()) + ''.join(open('./page.log', 'r').readlines())

class PagejauneSpider(Spider):
    name = "pagejaune"
    allowed_domains = ["pagesjaunes.fr"]
    # 'Loiret (45)'
    locations = '14-61-27-76-62-80-59-02-60-08-51-55-54-57-67-88-68-52-10-70-21-89-58-71-39-18-41-28-45-03-42-69-01-63-43-77-95-78-91'
    categories = ['Restaurant', 'Electricien', 'Beauté', 'Pharmacie', 'Kiné', 'Taxi', 'Comptable', 'Notaire', 'Plombier',]
    num = 0
    def parse_locations(self):
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
        self.keywords = 'Jean,Marie,Paul,Emma,Louise,Lucas,Hugo,Jade,Gabriel,Alice,Nathan,Chloé,Arthur,Léa,Manon,Raphaël,Camille,Juliette,Jules,Mila,Tom,Théo,Zoé,Sarah,Ethan,Mia,Noah,Sofia,Maxime,Clara,Léo,Léna,Eva,Adam,Enzo,Laura,Elena,Nora,Louis,Charles,Hélène,François,Sophie,Catherine,Anne,Claire,Michel,Henri,André,Jacqueline,Christine,Jeanne,Lucas,Matteo,Ryan,Dylan,Aaron'
        with open('./missing.json', 'r') as f:
            data = json.load(f)
            for keyword in self.keywords.split(','):
                url = f"https://www.pagesjaunes.fr/pagesblanches/recherche?quoiqui={quote(keyword)}&ou=&univers=pagesblanches&idOu="
                df = pd.read_csv("combined.csv")
                self.urls = df['url'].tolist()
                fy = url in urls
                yield Request(
                    url=url,
                    headers=self.headers,
                    cookies=self.cookies,
                    callback=self.parse,
                    meta={'category':keyword, 'page': page, 'fy':fy}
                )

    def parse(self, response):
        page = response.meta.get('page', 1)
        if response.meta['fy']:
            for service in response.css('ul.bi-list > li'):
                if service.css('.badge-particulier').get():
                    item = ServiceItem()
                    item['name'] = service.css('.bi-denomination h3::text').get()
                    item['page'] = page
                    item['category'] = response.meta['category']
                    item['url'] = response.url
                    item['phone_number'] = service.css('.number-contact > span::text').get()
                    item['address'] = service.css('.bi-address a::text').get('').strip()
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
                print(response.meta['category'], i)
                response.meta['page'] = i
                response.meta['fy'] = fy
                url = f"https://www.pagesjaunes.fr/pagesblanches/recherche?quoiqui={quoiqui}&quoiQuiInterprete={quoiQuiInterprete}&contexte={contexte}&page={i}"
                if f"Crawled (200) <GET {url}" in logfile or url in self.urls:
                    print(f'url {url} found')
                    continue
                else :
                    fy = True
                    self.num += 1
                yield Request(
                    url=url,
                    headers=self.headers,
                    cookies=self.cookies,
                    callback=self.parse,
                    errback=self.errback,
                    meta=response.meta
                )
            print(f"{self.num} url to be crawled")
            print(f"{len(self.keywords.split(','))} keyword to be crawled")

    def errback(self, failure):
        self.cookies = generate_cookies(['https://www.pagesjaunes.fr/'])
        retry = failure.value.response.meta.get('errback_retry', 1)
        if retry > 15:
            failure.value.response.meta['errback_retry'] = retry + 1
            yield failure.request.replace(cookies=self.cookies, meta=failure.value.response.meta['errback_retry'])
        else:
            self.logger.error(f'[Errback] Gave Up retry {failure.request.url}')
