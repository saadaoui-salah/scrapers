import scrapy
from fake_useragent import UserAgent

class AmazonSpider(scrapy.Spider):
    name = "amazon"
    ua = UserAgent()
    custom_settings = {
        'CONCURRENT_REQUESTS': 100,
        'REFERER_ENABLED': False,
        'COOKIES_ENABLED': False,
        'DOWNLOAD_DELAY': 0,
        'RETRY_TIMES': 5
    }
    visited_urls = []
    cookies = {
        "session-id": "258-0309807-8035564",
        "i18n-prefs": "EUR",
        "lc-acbnl": "en_GB",
        "ubid-acbnl": "258-1726622-9781405",
        "session-id-time": "2082787201l",
        "csm-hit": "tb:F90AHJVXAS77SWAQXX8C+s-F90AHJVXAS77SWAQXX8C|1750127422666&t:1750127422666&adb:adblk_no",
        "session-token": "fkk7GkNpc9Ww5gQJ8XREHhXgRXVXwJ0dyitjCHTGL4fLwaEATVlO7FP1NRMflXhJPDizOig7dDZnkGHtMaytk3KyYHM0SDCdM1YL0+t6g7XGuBk2s8IqZSgwUQOp2IcbR0CcSfZbRFClGfIZecDhHhE2f456xmChROqPBshvRD7jSYa5LG6XxYk09ocC62OeCJZ5tsUv3lIge1RWdj3Gqb30V3MrRcVxVjuy5+vyzfbomS6NdZpUT/462l2+dp2L1tgBMVXQLgHYUSoLKnZPQ+jT41ZcXpzXlQAKm905Oed7dnRAo8GGyUl+wY8irXWaV/sX4nDhapf1Q2YqMiYFZXAT5tYs1LTr",
        "rxc": "AMs1bWEhIT5sSB92WWQ"
    }
    proxy = 'burp'


    @property
    def headers(self):
        headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "fr-FR,fr;q=0.9,ar-DZ;q=0.8,ar;q=0.7,en-US;q=0.6,en;q=0.5",
            "cache-control": "no-cache",
            "dnt": "1",
            "pragma": "no-cache",
            "priority": "u=0, i",
            "sec-ch-ua": "\"Google Chrome\";v=\"134\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"134\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Linux\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "user-agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
        }
        return headers

    def start_requests(self):
        yield scrapy.Request(
            url="https://www.amazon.nl/s?i=electronics&rh=n%3A16269066031&s=popularity-rank&fs=true&language=en&qid=1750115631&rnid=16365235031&xpid=VCVepzxZn09dG&ref=sr_nr_p_36_0_0&low-price=41&high-price=",
            cookies=self.cookies,
            callback=self.parse_categories,
            headers=self.headers,
            errback=self.errback
        )

    def errback(self, failure):
        req  = failure.request
        retry = failure.request.meta.get('retry', 0) +1
        if retry < 15:
            meta = {'retry': retry}
            yield req.replace(meta=meta, headers=self.headers)

    def parse_categories(self, response):
        slugs = response.css('#departments .a-link-normal.s-navigation-item::attr(href)').getall()
        slugs = list(filter(lambda x: x not in self.visited_urls, slugs))
        if len(slugs):
            for slug in slugs:
                self.visited_urls += [slug]
                yield scrapy.Request(
                    url=f"https://www.amazon.nl{slug}",
                    cookies=self.cookies,
                    callback=self.parse_categories,
                    headers=self.headers
                )
        else:
            if not len(response.css('[data-component-type="s-product-image"] a::attr(href)')):
                print(response.url)
                return
            yield {'url': response.url}
            #yield from self.parse_products(response)

    def parse_products(self, response):
        for product in response.css('[data-component-type="s-product-image"] a::attr(href)').getall():
            yield scrapy.Request(
                url=f"https://www.amazon.nl{product}",
                cookies=self.cookies,
                callback=self.parse_pdp,
                headers=self.headers
            )
        if next_link := response.css('.s-pagination-next::attr(href)').get():
            yield scrapy.Request(
                url=f"https://www.amazon.nl{next_link}",
                cookies=self.cookies,
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