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
        filtred_cats = []
        for cat in categories:
            if list(filter(lambda x: cat in x and x != cat, categories)):
                continue
            if self.domain in cat:
                continue
            filtred_cats += [cat]

        for category in categories:
            if self.domain not in category:
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
                    'referer': 'https://bigdipper.no/vinyl/nyheter?pageID=3',
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
                    "Data[0][FieldId]": "1546",
                    "Data[0][NodeId]": "2002500",
                    "Data[0][ClientId]": "A100416F1546N2002500",
                    "Data[0][UseSpecificLayoutId]": "False",
                    "Data[0][LayoutId]": "120032",
                    "Data[0][ManufacturerId]": "0",
                    "Data[0][Plid]": "0",
                    "Data[0][PlidList]": "",
                    "Data[0][SendFilterOnly]": "false",
                    "RequestFilter[NodeId]": "2002500",
                    "RequestFilter[Url]": f"{category}?pageID=1",
                    "RequestFilter[Filter]": "",
                    "RequestFilter[MinPrice]": "",
                    "RequestFilter[MaxPrice]": "",
                    "RequestFilter[SearchString]": "",
                    "RequestFilter[ClientId]": "AttributeListBox",
                    "RequestFilter[PageIndex]": "1",
                    "RequestFilter[FilterCacheKey]": "",
                    "RequestFilter[FilterIsJson]": "false",
                    "RequestFilter[OtherContactId]": "",
                    "SkipFilterRendering": "true",
                    "UseDummyData": "false",
                    "DeviceSize": "md",
                    "GetElementsOnly": "true",
                    "SkipSorter": "false",
                    "CurrentArticle": "0",
                    "PopupFilter": "0"
                }

                yield scrapy.FormRequest(
                    url=self.url,
                    method='POST',
                    headers=self.headers,
                    formdata=self.formdata,
                    meta={'category':category},
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
                headers=self.headers,
            )   
        if data['PagesRemaining'] > 0:
            f = furl(response.url)
            page = int(f.args.get('pageID', 1)) + 1
            data = self.formdata.copy()
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
        
        