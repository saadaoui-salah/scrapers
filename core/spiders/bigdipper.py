import scrapy
import json
from furl import furl
from w3lib.html import remove_tags

class BigdipperSpider(scrapy.Spider):
    name = "bigdipper"
    domain = 'https://bigdipper.no'
    global_headers = {
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

    black_list = [
        'https://bigdipper.no/gavekort'
    ]


    def start_requests(self):
        yield scrapy.Request(
            url='https://bigdipper.no/api/Menu/GetHtmlMenu?nodeId=2001589&screensize=sm&screensizePixels=768&width=1920&height=1080&showMobileMenuCollapsed=false&_=1746827350247',
            headers=self.global_headers,
            callback=self.parse_categories,
        )


    def parse_categories(self, response):
        for cat in response.css('#navbar-collapse-grid .dropdown.mcm-fw'):
            if not cat.css('ul'):
                category = cat.css('a::attr(href)').get()
                url = f"{self.domain}{category}" if self.domain not in category else category
                if url in self.black_list:
                    continue
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_results,
                    headers=self.global_headers,
                    meta={'category': category}
                )
            else:
                for category in cat.css('.MegaMenuNotPublished .menu-items-container a::attr(href)').getall():
                    url = f"{self.domain}{category}" if self.domain not in category else category
                    if url in self.black_list:
                        continue
                    yield scrapy.Request(
                        url=url,
                        callback=self.parse,
                        headers=self.global_headers,
                        meta={'category': category}
                    )

    def parse(self, response):
        categories = response.css('.karuselloverskrift a::attr(href)').getall()
        if categories:
            for category in categories:
                url = f"{self.domain}/{category}" if self.domain not in category else category
                if url in self.black_list:
                    continue
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_results,
                    headers=self.global_headers,
                    meta={'category': category}
                )
        else:
            yield from self.parse_results(response)

    def parse_results(self, response):
        slugs = response.css('.AddProductImage > a::attr(href)')
        for slug in slugs:
            yield scrapy.Request(
                url=f"{self.domain}{slug}",
                callback=self.parse_pdp,
                headers=self.global_headers,
            )
        category = response.meta['category']
        self.url = 'https://bigdipper.no/api/AreaRenderer/RenderFields'
        self.headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'fr-FR,fr;q=0.9,ar-DZ;q=0.8,ar;q=0.7,en-US;q=0.6,en;q=0.5',
            'cache-control': 'no-cache',
            'content-type': 'application/x-www-form-urlencoded',
            'dnt': '1',
            'origin': 'https://bigdipper.no',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }

        self.formdata = {
            "Data[0][Width]": "727.5",
            "Data[0][AreaName]": "CenterContentDynamicAdList",
            "Data[0][FieldId]": response.css('[data-area-id="CenterContentDynamicAdList"]::attr(data-field-id)').get(),
            "Data[0][NodeId]": response.css('[data-area-id="CenterContentDynamicAdList"]::attr(data-node-id)').get(),
            "Data[0][ClientId]": response.css('[data-area-id="CenterContentDynamicAdList"]::attr(id)').get(),
            "Data[0][UseSpecificLayoutId]": "False",
            "Data[0][LayoutId]": response.css('[data-area-id="CenterContentDynamicAdList"]::attr(data-layoutid)').get(),
            "Data[0][ManufacturerId]": "0",
            "Data[0][Plid]": response.css('[data-area-id="CenterContentDynamicAdList"]::attr(data-plid)').get(),
            "Data[0][SendFilterOnly]": "false",
            "RequestFilter[NodeId]": response.css('[data-area-id="CenterContentDynamicAdList"]::attr(data-node-id)').get(),
            "RequestFilter[Url]": f"{category}?pageID=1",
            "RequestFilter[ClientId]": "AttributeListBox",
            "RequestFilter[PageIndex]": "1",
        }

        yield scrapy.FormRequest(
            url=self.url,
            method='POST',
            headers=self.headers,
            formdata=self.formdata,
            meta={'category':category, 'data':self.formdata},
            callback=self.parse_pagination
        )
    def parse_pagination(self, response):
        data = response.json()
        sel = scrapy.Selector(text=data['Data'][0]['Response'])
        slugs = sel.css('.AddProductImage > a::attr(href)')
        for slug in slugs:
            yield scrapy.Request(
                url=f"{self.domain}{slug}",
                callback=self.parse_pdp,
                headers=self.global_headers,
            )
        if not response.meta.get('pagination'):
            for page in range(data['PagesRemaining']):
                response.meta['pagination'] = True
                data = response.meta['data']
                data['RequestFilter[PageIndex]'] = str(page) 
                data['RequestFilter[Url]'] = f"{response.meta['category']}?pageID={page}" 
                yield scrapy.FormRequest(
                    url=self.url,
                    method='POST',
                    headers=self.headers,
                    meta=response.meta,
                    formdata=self.formdata,
                    callback=self.parse_pagination
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
        
        