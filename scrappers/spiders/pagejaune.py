from scrapy import Spider, Request, Item, Field
from urllib.parse import quote
from scrappers.utils import generate_cookies

class ServiceItem(Item):
    # Define fields to store scraped data
    name = Field()
    page = Field()
    url = Field()
    location = Field()
    address = Field()
    category = Field()
    phone_number = Field()

class PagejauneSpider(Spider):
    name = "pagejaune"
    allowed_domains = ["pagesjaunes.fr"]
    # 'Loiret (45)'
    locations = '14-61-27-76-62-80-59-02-60-08-51-55-54-57-67-88-68-52-10-70-21-89-58-71-39-18-41-28-45-03-42-69-01-63-43-77-95-78-91'
    categories = ['Restaurant', 'Electricien', 'Beauté', 'Pharmacie', 'Kiné', 'Taxi', 'Comptable', 'Notaire', 'Plombier',]
    
    def start_requests(self):
        self.cookies = {
            "cf_clearance": "B_H5s3Y3W0hrV39wFmO7MEd74gu_0wcp33C5eBdrmxc-1731089075-1.2.1.1-BxrtslHx3VPO7aBZG2cIMDb0._AUrZOC7RPRArmBX40pztDojQrtmezIAYMaEati7dtSTHu_.lkUR5T0ptyjMwSq.41HYwA..mvNOe74j6Dh2GWtHHykPxNdA7OlUKwncaeaaoyCT9KvbBfc449kcPQEDPt0H8EF3Zk7L0gE5hjr5CtRapgL_w1Iy66Nqh_cnLqYG3uWMKQ24_gbWGSbwfFqqiqwJ60e9ccYu5SUwxRfQusoFU2HzS0FxILptlWzh3kl245.ZzB2LU4iqjqpLM_dg19YD575zje.zDX3wcFI7T8quBP2MhFceesbypo4xMWnBEyTma51E5uCcZYlgwh2UkryN.kA3fSy.Bt_PsGkaq2IjnCMhK0jkI4pald4"
        }
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

    def parse_locations(self, response):
        data = response.json()
        location = response.meta['loc']
        for hit in data['hits']:
            if f"({location})" in hit['label']['value']:
                for category in self.categories:
                    yield Request(
                        url=f"https://www.pagesjaunes.fr/pagesblanches/recherche?quoiqui={quote(category)}&ou={quote(location)}&univers=pagesblanches&idOu=",
                        headers=self.headers,
                        cookies=self.cookies,
                        callback=self.parse,
                        meta={'keyword': hit['label']['value'], 'category':category}
                    )
                break

    def parse(self, response):
        for service in response.css('ul.bi-list > li'):
            item = ServiceItem()
            page = response.meta.get('page', 1)
            item['name'] = service.css('.bi-header-title a h3::text').get()
            item['page'] = page
            item['location'] = response.meta['keyword']
            item['category'] = response.meta['category']
            item['url'] = response.url
            item['phone_number'] = service.css('.number-contact > span::text').get()
            item['address'] = service.css('.bi-address a::text').get('').strip()
            yield item
        next_url = response.css('a.next').get()
        if next_url:
            quoiqui = quote(response.css("input[name='quoiqui']::attr('value')").get())
            ou = quote(response.css("input[name='ou']::attr('value')").get())
            quoiQuiInterprete = quote(response.css("input[name='quoiQuiInterprete']::attr('value')").get())
            contexte = quote(response.css("input[name='contexte']::attr('value')").get())
            idOu = response.css("input[name='idOu']::attr('value')").get()
            page += 1
            url = f"https://www.pagesjaunes.fr/pagesblanches/recherche?quoiqui={quoiqui}&ou={ou}&quoiQuiInterprete={quoiQuiInterprete}&contexte={contexte}&idOu={idOu}&page={page}"
            print(f'Movin To Page {page} Location: {response.meta["keyword"]} category: {response.meta["category"]}')
            response.meta['page'] = page
            yield Request(
                url=url,
                headers=self.headers,
                cookies=self.cookies,
                callback=self.parse,
                errback=self.errback,
                meta=response.meta
            )

    def errback(self, failure):
        self.cookies = generate_cookies(['https://www.pagesjaunes.fr/','https://www.pagesjaunes.fr/pagesblanches/',failure.request.url])
        retry = response.meta.get('errback_retry', 1)
        if retry > 15:
            response.meta['errback_retry'] = retry + 1
            yield failure.request.replace(cookies=self.cookies, meta=meta)
        else:
            self.logger.error(f'[Errback] Gave Up retry {failure.request.url}')
