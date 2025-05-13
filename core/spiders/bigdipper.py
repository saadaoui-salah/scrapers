import scrapy
import json
from furl import furl
from w3lib.html import remove_tags

class BigdipperSpider(scrapy.Spider):
    name = "bigdipper"
    domain = 'https://bigdipper.no'
    headers = {
        "pragma": "no-cache",
        "cache-control": "no-cache",
        "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-full-version": '"129.0.6668.58"',
        "sec-ch-ua-arch": '"x86"',
        "sec-ch-ua-platform": '"Linux"',
        "sec-ch-ua-platform-version": '"6.8.11"',
        "sec-ch-ua-model": '""',
        "sec-ch-ua-bitness": '"64"',
        "sec-ch-ua-full-version-list": '"Google Chrome";v="129.0.6668.58", "Not=A?Brand";v="8.0.0.0", "Chromium";v="129.0.6668.58"',
        "dnt": "1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "sec-fetch-site": "none",
        "sec-fetch-mode": "navigate",
        "sec-fetch-user": "?1",
        "sec-fetch-dest": "document",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "fr-FR,fr;q=0.9,ar-DZ;q=0.8,ar;q=0.7,en-US;q=0.6,en;q=0.5",
        "priority": "u=0, i" 
    }


    def start_requests(self):
        yield scrapy.Request(
            url='https://bigdipper.no/api/Menu/GetHtmlMenu?nodeId=2001589&screensize=sm&screensizePixels=768&width=1920&height=1080&showMobileMenuCollapsed=false&_=1746827350247',
            headers=self.headers,
            callback=self.parse,
        )

    def parse(self, response):
        categories = response.css('a[target="_self"]::attr(href)').getall()
        for category in categories[:38]:
            if self.domain not in category:
                yield scrapy.Request(
                    url=f'{self.domain}{category}',
                    callback=self.parse_pagination,
                    headers=self.headers,
                )

    def parse_pagination(self, response):
        total = len(response.css('.AddProductImage'))
        if total == response.meta.get('total', 0):
            yield from self.parse_products(response)
            return
        f = furl(response.url)
        f.args['pageID'] = int(f.args.get('pageID', 1)) + 1

        yield scrapy.Request(
            url=f.url,
            callback=self.parse_pagination,
            headers=self.headers,
            meta={'total': total}
        )

    def parse_products(self, response):
        slugs = response.css('.AddProductImage > a::attr(href)')
        for slug in slugs:
            yield scrapy.Request(
                url=f"{self.domain}{slug}",
                callback=self.parse_pdp,
                headers=self.headers,
            )   

    def parse_pdp(self, response):
        data = response.xpath("//script[contains(text(), 'EAN')]/text()").get('').replace('dataLayer.push(', '').replace(');', '')
        data = data.replace('\n', '').replace('\t', '').replace('\r', '').replace('"', '').strip()
        ean = data.split("EAN': '")[1].split("',")[0]
        category = data.split("BreadCrumb': '")[1].split("',")[0]
        images = response.css('img[data-rsBigImg]::attr(src)').getall()
        item = {
            'url': response.url,
            'name 1': response.css('.heading-container h1::text').get(),
            'name 2': response.css('.heading-container h2::text').get(),
            'release-date': response.css('.release-date::text').get('').replace('(Slippes ', '').replace(')', ''),
            'price': response.css('.PriceLabel::text').get(),
            'images': [f"{self.domain}{image}" for image in images],
            'status': response.css('.DynamicStockTooltipContainer > span:nth-child(2)::text').get(),
            'category': category,
            'ean': ean,
            'description': remove_tags(response.css('.prod-text-content').get('')),
        }
        for tr in response.css('.technical-info tr'):
            list_ = tr.css('td').getall()
            item[remove_tags(list_[0])] = remove_tags(list_[1])
        
        yield item
        
        