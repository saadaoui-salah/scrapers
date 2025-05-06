import scrapy
from requests_toolbelt.multipart.encoder import MultipartEncoder

class MedicalregisterSpider(scrapy.Spider):
    name = "medicalregister"
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'fr-FR,fr;q=0.9,ar-DZ;q=0.8,ar;q=0.7,en-US;q=0.6,en;q=0.5',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Origin': 'https://medicalregister.com.au',
        'Pragma': 'no-cache',
        'Referer': 'https://medicalregister.com.au/Advanced-Search.aspx',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
    }


    def start_requests(self):
        import string
        alphabet = list(string.ascii_lowercase)
        for i in alphabet:
            yield scrapy.Request(
                url=f'https://medicalregister.com.au/Advanced-Search.aspx?&TxtDoctorName={i}',
                headers=self.headers,
                callback=self.parse,
            )

    def parse(self, response):
        for slug in response.css('.search-result-full-name a::attr(href)').getall():
            yield scrapy.Request(
                url=f'https://medicalregister.com.au{slug}',
                headers=self.headers,
                callback=self.parse_details,
            )

        pages = response.xpath("//span[contains(text(), 'Total')]/text()").get('').lower().replace('total ', '').replace('pages ', '')
        if not response.meta.get('paginated') and pages:
            for i in range(int(pages)):
                yield scrapy.Request(
                    url=f'{response.url}&page={i}',
                    headers=self.headers,
                    callback=self.parse,
                    meta={'paginated': True}
                )

    def parse_details(self, response):
        yield {
            'profile title':  response.css('.profile-title::text').get(),
            'email':response.xpath("//p[contains(text(), 'Email')]/a/@href").get(),
            'phone':''.join(response.xpath("//p[contains(text(), 'Phone')]//text()").getall() +\
                response.xpath("//p[contains(text(), 'Fax')]//text()").getall()),
        }