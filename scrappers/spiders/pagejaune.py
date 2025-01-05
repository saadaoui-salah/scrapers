from scrapy import Spider, Request, Item, Field
from urllib.parse import quote
import ssl

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
    locations = ['Eure-et-Loir (28)', 'Yonne (89)', 'Aube (10)', 'Marne (51)', 'Ille-et-Vilaine (35)', 'Mayenne (53)']
    categories = ['Restaurant', 'Electricien', 'Beauté', 'Pharmacie', 'Kiné', 'Taxi', 'Comptable', 'Notaire', 'Plombier',]
    
    def start_requests(self):
        self.cookies = {
            "cf_clearance": "eZACHT.TQb9LAT1RnkHFa7iBUEqI1qWQrfKVtD7HFmo-1731094418-1.2.1.1-n8z.5yjBFJY7VjOygRlRp98IOks71_alCkK2MYCU5imaQ5nuhSsNm4MsWNwkuV3Qp_gp1Zd0UAFtz6uKjf9LLbrMnGnHcRCARcxSXXA3VFSBK4Sx.fYnBmV2m2PYz9l4Hj.fTSKpDEIUzak6mx6Vsc6xAThddHYV9qN24LUTPOFecnOi6i029vdXAuL.fDsH8bL390CniJRLMbn4cS0GSY7AcALkjzDdhyCZawBrmo5KySfK8fLPKQpu6enjC1DdRnoCNCe9p9JIcA60bRjSk6PMhOJI8bG17itb7I_rhDd9o8vdHRgZT8MpEswMG5S0qPh0gALM2v9qyjk5ETkRLyNUC953u6jlKQGLgYXcDySx31ml3dR4x1XF4HIo8EBJKDEM.mEPwshkeff3eOAcYDu6C19xxVnBYsOpjzu34QQ"
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
        for location in self.locations:
            for category in self.categories:
                yield Request(
                    url=f"https://www.pagesjaunes.fr/annuaire/chercherlespros?quoiqui={quote(category)}&ou={quote(location)}&univers=pagesjaunes&idOu=",
                    headers=self.headers,
                    cookies=self.cookies,
                    callback=self.parse,
                    meta={'keyword': self.locations[0], 'category':category}
                )

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
            item['address'] = service.css('.bi-address a::text').get().strip()
            yield item
        next_url = response.css('a.next').get()
        if next_url:
            quoiqui = quote(response.css("input[name='quoiqui']::attr('value')").get())
            ou = quote(response.css("input[name='ou']::attr('value')").get())
            quoiQuiInterprete = quote(response.css("input[name='quoiQuiInterprete']::attr('value')").get())
            contexte = quote(response.css("input[name='contexte']::attr('value')").get())
            idOu = response.css("input[name='idOu']::attr('value')").get()
            page += 1
            url = f"https://www.pagesjaunes.fr/annuaire/chercherlespros?quoiqui={quoiqui}&ou={ou}&quoiQuiInterprete={quoiQuiInterprete}&contexte={contexte}&idOu={idOu}&page={page}"
            print(f'Movin To Page {page} URL: {url}')
            response.meta['page'] = page
            yield Request(
                url=url,
                headers=self.headers,
                cookies=self.cookies,
                callback=self.parse,
                meta=response.meta
            )