import scrapy
import json
from core.utils.utils import generate_cookies
import asyncio
from twisted.internet.defer import ensureDeferred

slugs = [
    ['chiropractic/NSW/sydney-2000', 2],
    ['chiropractic/VIC/melbourne-3000', 3],
    ['chiropractic/WA/perth-6000', 6],
    ['chiropractic/SA/adelaide-5000', 1],
    ['chiropractic/WA/subiaco-6008', 1],
    ['chiropractic/WA/nedlands-6009', 6],
    ['chiropractic/VIC/richmond-3121', 4],
    ['chiropractic/VIC/east-melbourne-3002', 3],
    ['chiropractic/QLD/brisbane-4000', 1],
    ['chiropractic/QLD/southport-4215', 1],
    ['chiropractic/NSW/bondi-junction-2022', 1],
    ['chiropractic/QLD/spring-hill-4000', 1],
    ['chiropractic/QLD/southport-4215', 1],
    ['chiropractic/NSW/bondi-junction-2022', 1],
    ['chiropractic/QLD/spring-hill-4000', 1],
    ['chiropractic/NSW/chatswood-2067', 2],
    ['chiropractic/WA/joondalup-6027', 2],
    ['chiropractic/VIC/box-hill-3128', 3],
    ['chiropractic/WA/murdoch-6150', 5],
    ['chiropractic/VIC/frankston-3199', 1],
    ['chiropractic/WA/west-perth-6005', 6],
    ['chiropractic/TAS/hobart-7000', 1],
    ['chiropractic/NSW/bankstown-2200', 1],
]

class HealthengineSpider(scrapy.Spider):
    custom_settings = {
        'RETRY_HTTP_CODES': [202],
    }
    name = "healthengine"
    headers = {
        "dnt": "1",
        "priority": "u=0, i",
        "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
    }
    cookies = {
        "_gcl_au": "1.1.1343959935.1746561985",
        "AMCVS_23ED7BAF56EBC7B07F000101@AdobeOrg": "1",
        "s_ecid": "MCMID|37670092415842476713423419466475388671",
        "he_ga": "GA1.1.780785978.1746562001",
        "flagr-experiment-session": "27d0c4d0-0609-475a-b1a5-0e8fb8b0e7ec",
        "IR_gbd": "healthengine.com.au",
        "__Host-next-auth.csrf-token": "d2f27d522661b0c637699b245bb7dbb1fd712e7d6c852e9264eb312e893220bf|98ea2b1dbe48ea14fad98f4063e4db39d3aa6336014b3f790fc0255a5ed99bed",
        "__Secure-next-auth.callback-url": "https://bookings.terrywhitechemmart.com.au",
        "_fbp": "fb.2.1746562010854.185164377402343216",
        "s_cc": "true",
        "he-tracking": "7caad080795ec346a926f1d9dc17ce082552a1e0",
        "_hjSessionUser_30103": "eyJpZCI6ImQ2MTY5ZjZhLWNkNDUtNTcxZi05NmJiLWI4MjU3MjBhOTFjYiIsImNyZWF0ZWQiOjE3NDY1NjIwMTE2ODcsImV4aXN0aW5nIjp0cnVlfQ==",
        "ab.storage.deviceId.dc09be09-6294-4f5c-91e1-add0f02e9e38": "{\"g\":\"8f941c9c-f4ee-c667-4c0e-cc6ea3be9836\",\"c\":1746559673371,\"l\":1746639847760}",
        "s_ips": "586",
        "s_tp": "1221",
        "s_ppv": "AU%3AHE%3ACon%3AAppointments%3APractice,103,48,1256,1,2",
        "ab.storage.sessionId.dc09be09-6294-4f5c-91e1-add0f02e9e38": "{\"g\":\"d74f59e5-02b9-6f51-2e91-7ff6bfa68527\",\"e\":1746642747146,\"c\":1746639847756,\"l\":1746640947146}",
        "AMCV_23ED7BAF56EBC7B07F000101@AdobeOrg": "179643557|MCIDTS|20219|MCMID|37670092415842476713423419466475388671|MCAAMLH-1747517180|6|MCAAMB-1747517180|RKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y|MCOPTOUT-1746919580s|NONE|MCAID|NONE|vVersion|5.5.0",
        "HE-PATIENT-DATA-SESSION": "datasession.bec594a89e678b18a5146ad5e7a807604660b604",
        "_hjSession_30103": "eyJpZCI6IjIwYWMwYzBlLWYxNWYtNDI4YS05YjhiLWE4NTIxMzJlMmIzMSIsImMiOjE3NDY5MTIzODgyOTAsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowfQ==",
        "SearchSpecialty": "Chiropractic",
        "aws-waf-token": "c3a65b77-686f-4893-848e-c04f5eb6cb35:BwoAh2eaMPBkAQAA:0b01EH3V/3r2POS+UBMloJTpmgjRjebcxJRtnjreIVgeAZ5vXzyxjmrLHLOgsZ1eah2uX0HRLVq+4DEoJ+TJr1cuNYkBkhEIxFfg+9Cas8Bgac3FPHomevDsktHcAKg3Yj5r7aorWmlFI0ocamZ2OFN6oAquQex2Z5ZfXCJLDt22bAnEdT4z5ShNJkzICcNS8MgL8Mr8TXWPIik=",
        "__gads": "ID=c064de249727ec51:T=1746562868:RT=1746915029:S=ALNI_MY875gTOx_2zDIs3Smo4O31kufoow",
        "__gpi": "UID=000010bd0ee7a19f:T=1746562868:RT=1746915029:S=ALNI_MbVhGHUlT-bqjJ7fdF8sv_24_nRGg",
        "__eoi": "ID=268da73f7d12af77:T=1746562868:RT=1746915029:S=AA-Afja8pN9d-s4vVS3BnrqT63Jx",
        "dtm_pv_pn": "AU:HE:Con:Appt:Res:Chiropractic:NSW:2200",
        "gpv_Pagepath": "healthengine.com.au/search/chiropractic/NSW/bankstown-2200",
        "s_sq": "[[B]]",
        "IR_29590": "1746915727513|0|1746915727513||",
        "he_ga_ZVK7K6FDJP": "GS2.1.s1746912385$o6$g1$t1746915728$j58$l0$h0"
    }
    proxy='burp'


    def start_requests(self):
        for i in slugs:
            for page in range(i[1]):
                yield scrapy.Request(
                    url=f"https://healthengine.com.au/search/{i[0]}?page={page+1}&onlineAppts=true",
                    callback=self.parse,
                    cookies=self.cookies,
                    headers=self.headers
                )

    def parse(self, response):
        data = response.css('#__NEXT_DATA__::text').get()
        data = json.loads(data)['props']['ssrData']['PRELOAD_CACHE']['HANNIBAL_CACHE']
        keys = data.keys()

        for key in keys:
            if not 'practice:' in key.lower():
                continue
            item = data[key]
            if not item['phoneNumber']:
                continue
            if not item['phoneNumber'].strip():
                continue
            lead = {}
            lead['phone'] = item['phoneNumber'] 
            lead['name'] = item['name']
            yield lead