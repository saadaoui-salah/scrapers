import scrapy


class WorldcasinodirectorySpider(scrapy.Spider):
    name = "worldcasinodirectory"
    custom_headers = {
        "accept": "*/*",
        "accept-language": "fr-FR,fr;q=0.9,ar-DZ;q=0.8,ar;q=0.7,en-US;q=0.6,en;q=0.5",
        "cache-control": "no-cache",
        "cookie": "s=q11eggp0c1a9tsdh39kup1ch7o; wcd_last_visit=1742173640; _ga=GA1.1.1121548463.1742173657; __smVID=6fe30f700cff65e535c950ad2b4b5224aa8f67681235a927e2f9d4b4e6ccd62c; _ga_3S8HDH7G9C=GS1.1.1742175708.2.1.1742175933.0.0.0; _ga_Z64ZKND9VZ=GS1.1.1742175708.2.1.1742176211.0.0.0",
        "dnt": "1",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://www.worldcasinodirectory.com/region/north-america",
        "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest",
    }

    def start_requests(self):
        for i in range(1,8):
            yield scrapy.Request(
                url=f'https://sbcdirectory.com/?page={i}&pageSize=100', 
                headers=self.custom_headers,
                callback=self.parse_contries,
            )
        
    def parse_contries(self, response):
        data = response.css('.company-card-btn::attr(href)')
        for link in data:
            url = f'https://sbcdirectory.com{link}'
            yield scrapy.Request(
                url=url,
                callback=self.parse_details,
            )



    def parse_details(self,response):
        mail = response.xpath("//a[contains(@href, 'mailto')]/@href").get('').replace('mailto:', '')
        website = response.css(".row .links a.c-7[target='_blank']::attr(href)").get('')
        name = response.css('.company-name::text').get()
        if mail and website and name:
            yield {
                'email': mail,
                'name': name.replace('\r','').replace('\n','').strip(),
                'website': website
            }