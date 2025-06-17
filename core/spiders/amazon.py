import scrapy
from fake_useragent import UserAgent

class AmazonSpider(scrapy.Spider):
    name = "amazon"
    ua = UserAgent()
    custom_settings = {
        'CONCURRENT_REQUESTS': 1,
        'REFERER_ENABLED': False,
        'COOKIES_ENABLED': False,
        'DOWNLOAD_DELAY': 0.3
    }
    visited_urls = []
    cookies = {
        "session-id": "258-0309807-8035564",
        "i18n-prefs": "EUR",
        "lc-acbnl": "en_GB",
        "ubid-acbnl": "258-1726622-9781405",
        "session-id-time": "2082787201l",
        "csm-hit": "tb:s-AM3SGJFXH0440P3QNDGN|1750119727302&t:1750119729303&adb:adblk_no",
        "session-token": "wXz1kg03d6u9JCx9Dcai+VVkie9t9nx7Ci0g+CDnoWh87sj2ycdJCJYCgqJ7zxr5LIk+1ciCs3d/mQ93rIC6yBBU5WhQrp35+UumYd/soVTtYHaFRpPi1/h9Bp3FI97dm5UyZLHH0VkMihFXErWMU9QeD9fOJEXpO1BGOD5H8hXL20nXTgF4U2dCOM2/kE6MtUKlTDule2+EEFaxsstr0/Zr24flpW5UnsWyCEBKwxDOmZ40zTlZ1DgRmYksjkOvtoAEf78VcwHoodBACyEkbZTnbVwFYVzT/ozcuZw0cwReWrIgeAHVHY5NbFPOvamFyA0di8cydrflnOtZwdRgcw4Fv2/XS2t+",
        "rxc": "AMs1bWHyRD5sSB92o2U"
    }

    @property
    def headers(self):
        headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "fr-FR,fr;q=0.9,ar-DZ;q=0.8,ar;q=0.7,en-US;q=0.6,en;q=0.5",
            "cache-control": "no-cache",
            "dnt": "1",
            "pragma": "no-caclshe",
            "priority": "u=0, i",
            "sec-ch-ua": "\"Google Chrome\";v=\"134\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"134\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Linux\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": self.ua.random
        }


    def start_requests(self):
        yield scrapy.Request(
            url="https://www.amazon.nl/s?i=electronics&rh=n%3A16269066031&s=popularity-rank&fs=true&language=en&qid=1750115631&rnid=16365235031&xpid=VCVepzxZn09dG&ref=sr_nr_p_36_0_0&low-price=41&high-price=",
            callback=self.parse_categories,
            headers=self.headers
        )

    def parse_categories(self, response):
        slugs = response.css('#departments .a-link-normal.s-navigation-item::attr(href)').getall()
        slugs = list(filter(lambda x: x not in self.visited_urls, slugs))
        if len(slugs):
            for slug in slugs:
                self.visited_urls += [slug]
                yield scrapy.Request(
                    url=f"https://www.amazon.nl{slug}",
                    callback=self.parse_categories,
                    headers=self.headers
                )
        else:
            yield from self.parse_products(response)

    def parse_products(self, response):
        for product in response.css('[data-component-type="s-product-image"] a::attr(href)').getall():
            yield scrapy.Request(
                url=f"https://www.amazon.nl{product}",
                callback=self.parse_pdp,
                headers=self.headers
            )
        if next_link := response.css('.s-pagination-next::attr(href)').get():
            yield scrapy.Request(
                url=f"https://www.amazon.nl{next_link}",
                callback=self.parse_products,
                headers=self.headers
            )


    def parse_pdp(self, response):
        yield {
            'name': response.css('#productTitle::text').get().strip(),
            'price': response.css('#corePrice_feature_div .a-price .a-offscreen::text').get('').replace('€', ''),
            'url': response.url,
            'dispatch': response.css('[data-csa-c-content-id="fulfillerInfoFeature"] .offer-display-feature-text-message::text').get('').lower(),
            'return': response.css('[data-csa-c-content-id="odf-desktop-return-info"] .offer-display-feature-text-message::text').get()
        }
        if not response.css('#productTitle::text').get():
            print(response.text)