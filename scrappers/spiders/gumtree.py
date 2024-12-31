import scrapy


class GumtreeSpider(scrapy.Spider):
    name = "gumtree"
    allowed_domains = ["gumtree.com.au"]
    start_urls = ["https://www.google.com/"]
    api_url = 'https://www.gumtree.com.au/ws/search.json?defaultRadius=10&keywords={}&locationId=0&locationStr=Australia&pageNum={}&pageSize=24&previousCategoryId=&radius=500&sortByName=date'
    headers = {
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "fr-FR,fr;q=0.9,ar-DZ;q=0.8,ar;q=0.7,en-US;q=0.6,en;q=0.5",
        "device-memory": "8",
        "dnt": "1",
        "downlink": "0.65",
        "dpr": "1",
        "ect": "4g",
        "priority": "u=1, i",
        "referer": "https://www.gumtree.com.au/s-fencer/page-1/k0r500",
        "rtt": "250",
        "sec-ch-ua": "\"Google Chrome\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
        "sec-ch-ua-arch": "\"x86\"",
        "sec-ch-ua-bitness": "\"64\"",
        "sec-ch-ua-full-version": "\"129.0.6668.58\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-model": "\"\"",
        "sec-ch-ua-platform": "\"Linux\"",
        "sec-ch-ua-platform-version": "\"6.8.11\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
        }
    def parse(self, response):
        keywords = ['Fencer','Fencing','Landscaper','Handymen','Carpenter']
        for keyword in keywords:
            yield scrapy.Request(
                url=self.api_url.format(keyword.lower(), 1),
                headers=self.headers,
                callback=self.parse_results
            )
            break

    def parse_results(self, response):
        print(response.json())
