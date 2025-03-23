import scrapy
from w3lib.html import remove_tags
from core.utils.search import find_emails


class LcbSpider(scrapy.Spider):
    name = "lcb"
    start_urls = [
        "https://lcb.org/partial/sites/list?&order%5Brating%5D=DESC&region=dz&page=2&show_hidden=true"
    ]

    def start_requests(self):
        headers = {
            "accept": "text/html, */*; q=0.01",
            "accept-language": "fr-FR,fr;q=0.9,ar-DZ;q=0.8,ar;q=0.7,en-US;q=0.6,en;q=0.5",
            "cache-control": "no-cache",
            "dnt": "1",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": "https://lcb.org/casinos",
            "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Linux"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
            "x-country-code": "dz",
            "x-requested-with": "XMLHttpRequest",
        }

        cookies = {
            "_ym_uid": "1742251330520680645",
            "_ym_d": "1742251330",
            "_ga": "GA1.1.1584365854.1742251337",
            "_fbp": "fb.1.1742251342383.239343300645232625",
            "_ym_isad": "2",
            "_ga_Y83LHXRVH2": "GS1.1.1742501574.3.1.1742501577.57.0.0",
            "_uetsid": "2eb42410058811f09ccfeb5acb839619",
            "_uetvid": "2eb95170058811f0a9e9e543283b3126",
        }
        for i in range(1, 64):
            yield scrapy.Request(
                url=f"https://lcb.org/partial/sites/list?&order%5Brating%5D=DESC&region=dz&page={i}&show_hidden=true",
                headers=headers,
                cookies=cookies,
                callback=self.parse,
            )

    def parse(self, response):
        links = response.css('.table-row.reviews-item div.hide-on-mobile > a::attr(href)').getall()
        for link in links:
            yield scrapy.Request(
                url=link,
                callback=self.parse_details,
            )

    def parse_details(self, response):
        email = response.xpath("//li/span[contains(text(),'Email')]/../div").get()
        email = remove_tags(email)
        email = find_emails(email)
        if email:
            name = response.css('.button.filled.cta-blue::attr(title)').get()
            link = response.css('.button.filled.cta-blue::attr(href)').get()
            yield {
                'name':name,
                'email': email,
                'website': link or email.split('@')[-1]
            }