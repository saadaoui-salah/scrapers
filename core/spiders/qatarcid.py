import scrapy
from furl import furl


class QatarcidSpider(scrapy.Spider):
    name = "qatarcid"
    start_urls = ["https://qatarcid.com/"]
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "fr-FR,fr;q=0.9,ar-DZ;q=0.8,ar;q=0.7,en-US;q=0.6,en;q=0.5",
        "cache-control": "no-cache",
        "cookie": "PHPSESSID=fb367b2468388634f958729bb4a15376",
        "dnt": "1",
        "pragma": "no-cache",
        "priority": "u=0, i",
        "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    }
    data = 'action=pfget_listitems&act=&dt=&dtx%5B0%5D%5Bname%5D=post_tags&dtx%5B0%5D%5Bvalue%5D=&dtx%5B1%5D%5Bname%5D=pointfinderltypes&dtx%5B1%5D%5Bvalue%5D={}&dtx%5B2%5D%5Bname%5D=pointfinderlocations&dtx%5B2%5D%5Bvalue%5D=&dtx%5B3%5D%5Bname%5D=pointfinderconditions&dtx%5B3%5D%5Bvalue%5D=&dtx%5B4%5D%5Bname%5D=pointfinderitypes&dtx%5B4%5D%5Bvalue%5D=&dtx%5B5%5D%5Bname%5D=pointfinderfeatures&dtx%5B5%5D%5Bvalue%5D=&ne=&sw=&ne2=&sw2=&cl=&grid=grid2&pfg_orderby=&pfg_order=&pfg_number=&pfcontainerdiv=.pfsearchresults&pfcontainershow=.pfsearchgridview&page={}&from=halfmap&security=006bcd06cf&pflat=undefined&pflng=undefined&ohours=undefined'
    proxy = 'burp'

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls[0],
            callback=self.parse,
            headers=self.headers
        )
    def parse(self, response):
        values = response.css('option.pfoptheader::attr(value)').getall()
        links = response.css('.pointfinder-terms-archive > li > a::attr(href)').getall()
        for link, value in zip(links, values):
            yield scrapy.Request(
                url=link,
                callback=self.parse_link,
                headers=self.headers,
                meta={'value':value}
            )

    def parse_link(self, response):

        self.url = 'https://qatarcid.com/wp-content/plugins/pointfindercoreelements/includes/pfajaxhandler.php'
        self.api_headers = {
            'accept': 'text/html, */*; q=0.01',
            'accept-language': 'fr-FR,fr;q=0.9,ar-DZ;q=0.8,ar;q=0.7,en-US;q=0.6,en;q=0.5',
            'cache-control': 'no-cache',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'dnt': '1',
            'origin': 'https://qatarcid.com',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': response.url,
            'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }
        yield scrapy.Request(
            url=self.url,
            method='POST',
            headers=self.api_headers,
            body=self.data.format(response.meta['value'],''),
            dont_filter=True,
            callback=self.parse_chambres,
            meta=response.meta
        )

    def parse_chambres(self, response):
        detail_links = response.css('.pflineclamp-title > a::attr(href)').getall()
        for link in detail_links:
            yield scrapy.Request(
                url=link,
                callback=self.parse_details,
                headers=self.headers
            )
        
        if next_page := response.css('.next.page-numbers::attr(href)').get():
            link = furl(next_page)
            yield scrapy.Request(
                url=self.url,
                method='POST',
                headers=self.api_headers,
                body=self.data.format(response.meta['value'],link.args['page']),
                callback=self.parse_chambres,
                meta=response.meta
            )

    def parse_details(self, response):
        yield {
            'Company name': response.css('.pf-item-title-text::text').get(),
            'Company email': response.xpath("//span[contains(.,'Email :')]/../span[2]//text()").get(),
            'Company phone number': response.xpath("//span[contains(.,'Phone :')]/../span[2]//text()").get(),
            'Contact person name': response.xpath("//span[contains(.,'Contact Person :')]/../span[2]//text()").get(),
            'Contact person email': ''.join([response.xpath("//i[contains(@class,'fa-envelope')]/../text()").get(''), response.xpath("//i[contains(@class,'fa-envelope')]/../@data-mx").get('')]),
            'Website': response.xpath("//span[contains(.,'Website :')]/../span[2]//text()").get(),
        }