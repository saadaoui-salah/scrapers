import scrapy
from w3lib.html import remove_tags

class AlbertslundSpider(scrapy.Spider):
    name = "albertslund"
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "fr-FR,fr;q=0.9,ar-DZ;q=0.8,ar;q=0.7,en-US;q=0.6,en;q=0.5",
        "cache-control": "no-cache",
        "dnt": "1",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://dagsordner.albertslund.dk/?request.kriterie.udvalgId=&request.kriterie.moedeDato=2020",
        "sec-ch-ua": "\"Google Chrome\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Linux\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }

    def start_requests(self):
        for year in range(2008, 2025):
            yield scrapy.Request(
                url=f'https://dagsordner.albertslund.dk/api/agenda/soeg/?request.kriterie.udvalgId=&request.kriterie.moedeDato={year}&request.paging.startIndex=0&request.paging.limit=200',
                callback=self.parse,
                headers=self.headers,
                dont_filter=True
            )

    def parse(self, response):
        for row in response.json()['Dagsordner']:
            item = {
                'date':row['Moede']['MeetingBeginUtc'].split('T')[0],
                'meeting':row['Udvalg']['Navn'],
                'url':f"https://dagsordner.albertslund.dk/vis?id={row['Id']}",
            }
            yield scrapy.Request(
                url=f'https://dagsordner.albertslund.dk/api/agenda/dagsorden/{row["Id"]}?fritekst=undefined',
                callback=self.parse_details,
                headers={'accept':'application/json'},
                meta={'item': item}
            )
    
    def parse_details(self, response):
        item = response.meta['item']
        for row in response.json()['Dagsordenpunkter']:
            item['collapse title'] = row['Navn']
            item['collapse content'] = remove_tags(row['Felter'][0]['Html'])
            item['pdf urls'] = [f'https://dagsordner.albertslund.dk/vis/pdf/bilag/{pdf_id["Id"]}/?redirectDirectlyToPdf=false' for pdf_id in row['Bilag']] + [f'https://dagsordner.albertslund.dk/vis/pdf/bilag/{row['Id']}/?redirectDirectlyToPdf=false']
            item['Hent hele referatet'] = f'https://dagsordner.albertslund.dk/vis/pdf/dagsorden/{row["AgendaUid"]}/?redirectDirectlyToPdf=false'
            yield item