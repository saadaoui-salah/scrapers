import scrapy
import json
from core.utils.utils import generate_cookies
import asyncio
from twisted.internet.defer import ensureDeferred

slugs = [
    ['dentistry/NSW/sydney-2000', 9],
    ['dentistry/VIC/melbourne-3000', 15],
    ['dentistry/WA/perth-6000', 15],
    ['dentistry/SA/adelaide-5000', 7],
    ['dentistry/WA/subiaco-6008', 14],
    ['dentistry/WA/nedlands-6009', 13],
    ['dentistry/VIC/richmond-3121', 16],
    ['dentistry/VIC/east-melbourne-3002', 16],
    ['dentistry/QLD/brisbane-4000', 7],
    ['dentistry/QLD/southport-4215', 2],
    ['dentistry/NSW/bondi-junction-2022', 7],
    ['dentistry/QLD/spring-hill-4000', 7],
    ['dentistry/NSW/chatswood-2067', 9],
    ['dentistry/WA/joondalup-6027', 6],
    ['dentistry/VIC/box-hill-3128', 15],
    ['dentistry/WA/murdoch-6150', 12],
    ['dentistry/VIC/frankston-3199', 2],
    ['dentistry/WA/west-perth-6005', 14],
    ['dentistry/TAS/hobart-7000', 0],
    ['dentistry/NSW/bankstown-2200', 7],
]

class HealthengineSpider(scrapy.Spider):
    custom_settings = {
        'RETRY_HTTP_CODES': [202],
        'DOWNLOAD_DELAY':15
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
        "s_ecid": "MCMID|37670092415842476713423419466475388671",
        "he_ga": "GA1.1.780785978.1746562001",
        "flagr-experiment-session": "27d0c4d0-0609-475a-b1a5-0e8fb8b0e7ec",
        "_fbp": "fb.2.1746562010854.185164377402343216",
        "he-tracking": "7caad080795ec346a926f1d9dc17ce082552a1e0",
        "_hjSessionUser_30103": "eyJpZCI6ImQ2MTY5ZjZhLWNkNDUtNTcxZi05NmJiLWI4MjU3MjBhOTFjYiIsImNyZWF0ZWQiOjE3NDY1NjIwMTE2ODcsImV4aXN0aW5nIjp0cnVlfQ==",
        "mbox": "session#6fb52a69a2264e2db61809eb183bef0a#1747771045|PC#00ad664ff61f4d578d1ef84e42f1974e.36_0#1811013985",
        "mboxEdgeCluster": "36",
        "ab.storage.deviceId.dc09be09-6294-4f5c-91e1-add0f02e9e38": '{"g":"8f941c9c-f4ee-c667-4c0e-cc6ea3be9836","c":1746559673371,"l":1747769189377}',
        "__Host-next-auth.csrf-token": "aafce8bb701dc05452671b2d0fc0db514fabd90f33c497ea8b9eea4d578abd3e|737c204365c93d8fe9b394e15a5824ec8481cd50e956dc4e3e1dece584d5259b",
        "__Secure-next-auth.callback-url": "https://bookings.terrywhitechemmart.com.au",
        "AMCVS_23ED7BAF56EBC7B07F000101@AdobeOrg": "1",
        "AMCV_23ED7BAF56EBC7B07F000101@AdobeOrg": "179643557|MCIDTS|20229|MCMID|37670092415842476713423419466475388671|MCAAMLH-1748373990|6|MCAAMB-1748373990|RKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y|MCOPTOUT-1747776390s|NONE|MCAID|NONE|vVersion|5.5.0",
        "HE-PATIENT-DATA-SESSION": "datasession.db049c4719182af8083106819afed0612b05d0e2",
        "s_cc": "true",
        "IR_gbd": "healthengine.com.au",
        "_hjSession_30103": "eyJpZCI6ImM4ZTdkNzgyLWVlYzUtNGE0NS1iOGViLWIzNzEzOTFlYmY1OCIsImMiOjE3NDc3NjkxOTI0OTQsInMiOjEsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowfQ==",
        "ab.storage.sessionId.dc09be09-6294-4f5c-91e1-add0f02e9e38": '{"g":"909c1981-aec6-e47b-d242-35d8c91a156b","e":1747770992555,"c":1747769189374,"l":1747769192555}',
        "SearchSpecialty": "Dentistry",
        "gpv_Pagepath": "healthengine.com.au/search/dentistry/NSW/bankstown-2200",
        "dtm_pv_pn": "AU:HE:Con:Appt:Res:Dentistry:NSW:2200",
        "s_sq": "[[B]]",
        "aws-waf-token": "725a3fef-42e1-4f54-9716-76e8c351a32e:BwoAdgqLCSzzAAAA:4JY+v9xYGcEEUHz+PHjfIYjOqugdAoC6XMgFp9HFW3DcAKaNEDpCMcHCcgPofZ0lxRq6XjEcbUMAEvh/K9bLV/cw7UGusnJBqbVWquVYIOMRZhoxL7sf9WDNT28BUiSG5OcoGtcUsH4TcUE5tWK9OMLDrSI6qO+OWJ5BJvVf14sbjM+Rh41QFE7PsfDbhtmbqeuDDHeZ1D0d35IxUChbVo1UEEumpZgOoLTJ/dJHCgte2+nfeFlgrz+ggiVmOJP4orYO7pk3FXyoVQ==",
        "__gads": "ID=c064de249727ec51:T=1746562868:RT=1747770459:S=ALNI_MY875gTOx_2zDIs3Smo4O31kufoow",
        "__gpi": "UID=000010bd0ee7a19f:T=1746562868:RT=1747770459:S=ALNI_MbVhGHUlT-bqjJ7fdF8sv_24_nRGg",
        "__eoi": "ID=268da73f7d12af77:T=1746562868:RT=1747770459:S=AA-Afja8pN9d-s4vVS3BnrqT63Jx",
        "IR_29590": "1747770500505|0|1747770500505||",
        "he_ga_ZVK7K6FDJP": "GS2.1.s1747769191$o1$g1$t1747770502$j55$l0$h0$d3LJF2-O4_9j0j-2GsulQ31s5e-yaYZcv2w"
    }
    proxy='burp'


    def start_requests(self):
        for page in range(13):
            yield scrapy.Request(
                url=f"https://healthengine.com.au/search?page={page}&q=Surgery&onlineAppts=true",
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