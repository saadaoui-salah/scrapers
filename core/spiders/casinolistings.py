import scrapy
from core.utils.security import decode_cf_email
from core.utils.search import find_emails


class CasinolistingsSpider(scrapy.Spider):
    name = "casinolistings"
    start_urls = ["https://www.casinolistings.com/casinos"]
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "fr-FR,fr;q=0.9,ar-DZ;q=0.8,ar;q=0.7,en-US;q=0.6,en;q=0.5",
        "cache-control": "no-cache",
        "dnt": "1",
        "pragma": "no-cache",
        "priority": "u=0, i",
        "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
    }
    cookies = {
        "_ga": "GA1.1.2088439758.1742251795",
        "_omappvp": "8Bpcsn0KXQaTduW4pnRUg4n7oYY9rMNyInIesA8ZeXUl1drnq4pMHeYds7ERLaQV3g3o5qML3TqPsRAU3ocTu6TsNFOAkGuE",
        "cookiePolicy_accepted": "1",
        "omSeen-lbpmk6lafq3py27of8k1": "1742251846986",
        "_fbp": "fb.1.1742309544949.73585409399747916",
        "_cfuvid": "jjVppAEWouabwHgyzBfS31p2eqeMrWoFDiyH_S6t7zU-1742316791424-0.0.1.1-604800000",
        "__cf_bm": "QbK.3nHbyOIsm2sS8DQoxUUSFdjQ6HNZIP.w2auha8U-1742327155-1.0.1.1-7OdyQ3sjz0LdcEQ68FPw25DGqYoQ_qDDkpEHkakvcd64lFOimB_HNmxtRh6GA2ZvChZDJBpE6QuC91SZFI6Yt6oD7a3xLrBtFO0eDln.ztA",
        "omSeen-w7bhqpmgb5t73nqnldfx": "1742327237396",
        "om-w7bhqpmgb5t73nqnldfx": "1742327255468",
        "_ga_PWQZ79LZK1": "GS1.1.1742327159.3.1.1742327294.60.0.0"
    }

    def start_requests(self):
        for i in range(65):
            yield scrapy.Request(
                url=f"https://www.askgamblers.com/online-casinos/countries/at/{i+1}",
                headers=self.headers,
                callback=self.parse,
                meta={'playwright':True, "playwright_request": self.block_images_and_svgs,}
            )
            break
        
    def parse(self, response):
        for casino in response.css('.ag-card > a'):
            name = casino.css('::attr(title)').get()
            print(name)
            link = casino.css('::attr(href)').get()
            link = f'https://www.askgamblers.com{link}' if not 'https://www.askgamblers.com' in link else link
            yield scrapy.Request(
                url=link,
                headers=self.headers,
                callback=self.parse_details,
                meta={'playwright':True, 'name':name, "playwright_request": self.block_images_and_svgs}
            )

    async def block_images_and_svgs(self, request):
        """Blocks images and SVG requests."""
        if request.resource_type in ["image"]:
            return request.abort()
        if request.url.endswith(".svg"):  # Block SVGs specifically
            return request.abort()
        if 'google.com' in request.url:
            return request.abort()
        if 'facebook.net' in request.url:
            return request.abort()
        return request.continue_()

    def parse_details(self, response):
        name = response.meta['name']
        emails = response.xpath("//div[contains(text(), 'Email') and @class='review-details__text']/text()").getall()
        website = response.css('.review-details__text > a.js-ga-website::text').get()
        emails = ' '.join(emails)
        emails = find_emails(emails)
        print(name,emails,website)
        if all([name,emails,website]):
            item = {
                'name':name,
                'emails':emails,
            }
            yield scrapy.Request(
                url=website,
                callback=self.yield_item,
                meta={"item":item, 'handle_httpstatus_list': [403]}
            )

    def yield_item(self, response):
        item = response.meta['item']
        item['website'] = response.url
        yield item
