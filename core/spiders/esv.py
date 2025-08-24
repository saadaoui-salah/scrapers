import scrapy
from w3lib.html import remove_tags



class EsvSpider(scrapy.Spider):
    name = "esv"

    def start_requests(self):
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "fr-FR,fr;q=0.9,ar-DZ;q=0.8,ar;q=0.7,en-US;q=0.6,en;q=0.5",
            "cache-control": "no-cache",
            "dnt": "1",
            "pragma": "no-cache",
            "priority": "u=0, i",
            "referer": "https://esv.deimos.ch/web/Results?page=1&freeText=&lang=FR&keyWord=&sortField=nameDe&sortDirection=",
            "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Linux"',
            "sec-fetch-dest": "iframe",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        }

        for page in range(0, 268):  # inclusive 0 → 267
            url = f"https://esv.deimos.ch/web/Results?page={page}&freeText=&lang=FR&keyWord=&sortField=nameFr&sortDirection="
            yield scrapy.Request(url, headers=headers, callback=self.parse)

    def parse(self, response):
        # Example: extract titles or rows
        for row in response.css("tbody tr"):  # adjust selector
            data = {
                "Nom": row.xpath(".//td[1]/a/text()").get(),
                "Ville": row.xpath(".//td[2]/text()").get(),
                "lien": f"https://esv.deimos.ch{row.xpath(".//td[1]/a/@href").get()}",
            }
            yield scrapy.Request(data['lien'], callback=self.parse_details, meta={'data': data})

    def parse_details(self, response):
        data = response.meta['data']
        data['address'] = remove_tags(response.css('address').get('')).strip()
        data['site internet'] = response.css('a.detail-link::attr(href)').get('')
        data['But'] = response.xpath("//h4[contains(., 'But')]/following-sibling::p[1]/text()").get('')
        data['Mots clés'] = remove_tags(response.xpath("//h4[contains(., 'Mots clés')]/following-sibling::ul[1]").get(''))
        yield data