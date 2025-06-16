import scrapy
import json

class LondonstockexchangeSpider(scrapy.Spider):
    name = "londonstockexchange"

    def start_requests(self):
        url = "https://api.londonstockexchange.com/api/v1/components/refresh"
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "fr-FR,fr;q=0.9,ar-DZ;q=0.8,ar;q=0.7,en-US;q=0.6,en;q=0.5",
            "cache-control": "no-cache",
            "content-type": "application/json",
            "dnt": "1",
            "origin": "https://www.londonstockexchange.com",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": "https://www.londonstockexchange.com/",
            "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Linux"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        }
        for i in range(162):
            payload = {
                "path": "news",
                "parameters": f"tab%3Dnews-explorer%26indices%3DNMX%26period%3Dcustom%26beforedate%3D20250520%26afterdate%3D20230601%26page%3D{i}%26headlinetypes%3D1%2C2%26tabId%3D58734a12-d97c-40cb-8047-df76e660f23f",
                "components": [
                    {
                        "componentId": "block_content%3A431d02ac-09b8-40c9-aba6-04a72a4f2e49",
                        "parameters": f"indices=NMX&period=custom&beforedate=20250520&afterdate=20230601&page={i}&size=500&sort=datetime,desc"
                    }
                ]
            }

            yield scrapy.Request(
                url=url,
                method="POST",
                headers=headers,
                body=json.dumps(payload),
                callback=self.parse
            )

    def parse(self, response):
        data = response.json()[0]['content']
        data = filter(lambda x: x['name'] == 'newsexplorersearch',data)
        data = list(data)[0]['value']['content']
        for item in data:
            date = item['datetime'].split('T')[0].split('-')
            yield {
                'Headline': f"{item['companyname']} - {item['companycode']}",
                'date': f"{date[0][2:]}.{date[1]}.{date[2]}",
                'price': item['lastprice'],
                'link': f"https://www.londonstockexchange.com/news-article/{item['companycode']}/transaction-in-own-shares/{item['id']}"
            }
