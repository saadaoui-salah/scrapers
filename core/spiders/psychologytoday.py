import scrapy
from core.utils.cleaning import clean
from core.spiders.contacts_finder import ContactsFinderSpider

class PsychologytodaySpider(ContactsFinderSpider):
    name = "psychologytoday"
    start_urls = ["https://www.psychologytoday.com/us/psychiatrists/new-york"]
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "fr-FR,fr;q=0.9,ar-DZ;q=0.8,ar;q=0.7,en-US;q=0.6,en;q=0.5",
        "cache-control": "no-cache",
        "dnt": "1",
        "pragma": "no-cache",
        "priority": "u=0, i",
        "referer": "https://www.psychologytoday.com/us/psychiatrists/new-york",
        "sec-ch-ua": "\"Google Chrome\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Linux\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
    }
    cookies = {
        "summary_id": "684f43611ec1d",
        "optimizelyEndUserId": "oeu1750025062256r0.19689620559158638",
        "optimizelySession": "1750025064166",
        "_ga": "GA1.1.883888455.1750025070",
        "_ga_5EMHF6S1M6": "GS2.1.s1750025068$o1$g0$t1750025068$j60$l0$h0",
        "cookieyes-consent": "consentid:QkpCZUxBRmFEUm1rMXNMeVhLVlQ0U256Qno1S2tlOFo,consent:no,action:,necessary:yes,functional:yes,analytics:yes,performance:yes,advertisement:yes",
        "_dd_s": "logs=1&id=6a9e1abd-0977-427f-b59d-c7e18f53be29&created=1750025064328&expire=1750026027844"
    }



    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                headers=self.headers,
                callback=self.parse
            )

    def parse(self, response):
        for profile in response.css('.results-row'):
            item = {
                'link': profile.css('.results-row-cta-view::attr(href)').get(),
                'first name': ''.join(clean(profile.css('.profile-title').get('')).split(' ')[0:-1]),
                'last name': clean(profile.css('.profile-title').get('')).split(' ')[-1],
                'Role': profile.css('.profile-subtitle-credentials::text').get(),
                'psychologytoday phone number': profile.css('.results-row-phone::text').get(),
                'website': '',
                'email': [],
                'phone number': [],
            }
            yield scrapy.Request(
                url=f'https://out.psychologytoday.com/us/profile/{item['link'].split('/')[-1]}/website-redirect',
                headers=self.headers,
                dont_filter=True,
                callback=self.parse_website, 
                errback=self.errback,
                meta={'item': item}
            )
        if next_link := response.xpath("//a[contains(@class,'previous-next-btn') and contains(@title, 'Next')]/@href").get():
            yield scrapy.Request(
                url=next_link,
                headers=self.headers,
                callback=self.parse
            )
    
    def parse_website(self, response):
        item = response.meta['item']
        item['website'] = response.url
        item = response.meta['item']
        item['email'] = self.get_emails(response)
        item['phone number'] = self.get_numbers(response)
        
        contact_page = response.xpath('//*[contains(@href, "contact")]/@href').getall()
        if not contact_page :
            yield item
            return
        contact_page = list(filter(lambda x: 'whatsapp.com' not in x ,contact_page))
        if len(contact_page):
            contact_page = contact_page[0]
        if contact_page.startswith('/'):
            contact_page = f"{response.url}{contact_page}"
        url = contact_page if 'http' in contact_page else f"https://{contact_page}"
        yield scrapy.Request(
            url=url,
            headers=self.headers,
            callback=self.parse_contact,
            errback=self.errback,
            meta={'item': item}
        )


    def errback(self, failure):
        item = failure.request.meta['item']
        if not item['website']:
            item['website'] = failure.request.url 
        yield item

    def parse_contact(self, response):
        item = response.meta['item']
        item['email'] +=  self.get_emails(response)
        item['phone number'] += self.get_numbers(response)
        
        about_page = response.xpath('//*[contains(@href, "about")]/@href').get()
        if not about_page:
            yield item
            return
        if about_page.startswith('/'):
            about_page = f"{response.url}{about_page}"
        url = about_page if 'http' in about_page else f"https://{about_page}"
        yield scrapy.Request(
            url=url,
            errback=self.errback,
            headers=self.headers,
            callback=self.parse_about,
            meta={'item': item}
        )
    
    def parse_about(self, response):
        item = response.meta['item']
        item['email'] +=  self.get_emails(response)
        item['phone number'] += self.get_numbers(response)
        yield item