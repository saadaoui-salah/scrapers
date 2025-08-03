import scrapy
from urllib.parse import urlencode
from core.utils.utils import csv_to_dict
import json

class SocieteSpider(scrapy.Spider):
    name = "societe"
    headers = {
        'accept': '*/*',
        'accept-language': 'fr-FR,fr;q=0.9,ar-DZ;q=0.8,ar;q=0.7,en-US;q=0.6,en;q=0.5',
        'cache-control': 'no-cache',
        'dnt': '1',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
    }
    cookies = {
        "sib_cuid": "8f1f3135-f193-471d-a7f2-84699acd3e81",
        "didomi_token": "eyJ1c2VyX2lkIjoiMTk4NDk1MGMtZjRiZi02MTgyLWJjZjAtMWJlMDI1M2U3MmFlIiwiY3JlYXRlZCI6IjIwMjUtMDctMjdUMDA6Mzg6MDkuNDg0WiIsInVwZGF0ZWQiOiIyMDI1LTA3LTI3VDAwOjM4OjEyLjEzM1oiLCJ2ZW5kb3JzIjp7ImVuYWJsZWQiOlsiZ29vZ2xlIiwiYW1hem9uIiwic2FsZXNmb3JjZSJdLCJjb25zZW50cyI6eyJnaXZlbl9jb25zZW50cyI6eyJnb29nbGUiOnRydWUsImFtYXpvbiI6dHJ1ZSwic2FsZXNmb3JjZSI6dHJ1ZX0sImdsb2JhbF9jb25zZW50cyI6eyJnb29nbGUiOnRydWUsImFtYXpvbiI6dHJ1ZSwic2FsZXNmb3JjZSI6dHJ1ZX19fQ==",
        "euconsent-v2": "CQVNjgAQVNjgAAHABBENB0FsAP_gAEPgAAqILANR_X_fb2vj-_59953eF5_7_v-__zfj9fV399t0eY1fdt-8Nyd_X9_j-_9__59fTP59_1ftr3e3LBAQdlH4JYBFoIBgFoRkYVhmNMBiCRECoFAKAwIgAAgCIAEAwACACgAIAABAAIAAgAKACAEAAIAACAAAAIAIAAgAEACQAACIAABAAIAAAAAAIAAAAAAgAAAAAAAAAAAAAAAgAAAAAAIAAAACAAAAAgAAAAAAAAAAIAAAAEAAAEAAAAAAAAAAAAgAAAAAAgAAAAAAAAAAAAAAAAAAAAAAAACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
        "__uzma": "98ff2fa6-202b-4a9d-b6a1-0a236790f949",
        "__uzmb": "1725133574",
        "__uzmc": "753",
        "__uzmd": "1725133574",
        "__uzme": "1172",
        "__uzmf": "1725133574736",
        "sid": "66fce3965684260cdecc58b3c5d46302"
    }


    def fix_siren(self, company):
        missing = 9 - len(str(company['siren']))
        siren = f"{missing*'0'}{str(company['siren'])}"
        return siren

    def fix_siret(self, company):
        missing = 14 - len(str(company['siret']))
        siret = f"{missing*'0'}{str(company['siret'])}"
        return siret

    def start_requests(self):
        resources = csv_to_dict("./resources.csv")
        for company in resources: 
            base_url = 'https://www.societe.com/cgi-bin/finder-api?'
            
            params = {
                'q': self.fix_siren(company),
                'ftT': ['c', 'm']
            }

            url = base_url + urlencode(params, doseq=True)



            yield scrapy.Request(
                url=url,
                headers=self.headers,
                callback=self.parse,
                meta={'company': company}
            )

    def parse(self, response):
        company = response.meta['company']
        result = response.json()['hits']
        company['societ profile'] = f"https://www.societe.com{result[0]['url']}"
        base_url = "https://www.societe.com/cgi-bin/produit-api-aboutement"
        params = {
            "state": "getnum",
            "siret": self.fix_siret(company)
        }

        url = f"{base_url}?{urlencode(params)}"
        yield scrapy.Request(url=url, callback=self.parse_phone, headers=self.headers, meta={'company':company})
    
    def parse_phone(self, response):
        phone = response.json()['aboutement']['body']['phone']
        response.meta['company']['societe phone'] = phone
        yield response.meta['company']

        #url = "https://www.societe.com/cgi-bin/contacts-api"
        #payload = f"siren={self.fix_siren(response.meta['company'])}"
        #headers = self.headers.copy()
        #headers["content-type"] = "application/json"
        #headers["accept-encoding"] = "gzip, deflate, br, zstd"
        #yield scrapy.Request(
        #    url=url,
        #    method="POST",
        #    headers=headers,
        #    body=payload,
        #    callback=self.parse_email,
        #    meta=response.meta,
        #    errback=self.errback,
        #)

#    def errback(self, failure):
#        print(failure.value.request.body)
#
#    def parse_email(self, response):
#        response.meta['company']['societe email'] = response.json()['email']
#        yield response.meta['company']