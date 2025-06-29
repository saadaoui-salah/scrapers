import scrapy
from core.playwright.playwright_spider import PlaywrightSpider

class TestSpider(scrapy.Spider):
    name = "test"
    url = "https://clutch.co/seo-films"
    cookies = {
        "at_check": "true",
        "usprivacy": "1---",
        "AMCVS_5C64123F5245AF950A490D45%40AdobeOrg": "1",
        "AMCV_5C64123F5245AF950A490D45%40AdobeOrg": "179643557|MCIDTS|20260|MCMID|67012844075724011631804626419558050369|MCAAMLH-1750986079|6|MCAAMB-1750986079|RKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y|MCOPTOUT-1750388479s|NONE|vVersion|5.5.0",
        "s_vnc365": "1781917279952&vn=1",
        "s_ivc": "true",
        "s_inv": "0",
        "__cf_bm": "P9lAvshOZaS1.ItashYaswD9III5it_xHa2VE4O9Inc-1750382403-1.0.1.1-rOnMAx2jggpfwi9M1ixy5u7DE7GU5z61JtOel6AaIAiRMhrLL9_D5AY0tl5qo_jKut.UjM6eQMS1Uxa3h61U9IOcneITSo.51qBN5Y4NEus",
        "_ga": "GA1.1.1574282205.1750382408",
        "_clck": "1ehutgr|2|fwx|0|1997",
        "_gcl_au": "1.1.1473500840.1750382411",
        "IP_LOC": "Chlef|Chlef|",
        "BROWSE_ISSUE": "Airplane, Bus & Helicopter Accidents",
        "LDIR_ISSUE": "Airplane, Bus & Helicopter Accidents",
        "BROWSE_PA_META": "FL3911|2551",
        "gpv_v22": "https://lawyers.findlaw.com/aviation-mass-transit-accidents/alabama/",
        "refer_url": "https://lawyers.findlaw.com/aviation-mass-transit-accidents/alabama/alabaster/",
        "_ga_2JETTHX7WE": "GS2.1.s1750382407$o1$g1$t1750382498$j44$l0$h0",
        "mbox": "session#7d38dfb0a91040fdb4e735a5ca4a52a6#1750384359|PC#7d38dfb0a91040fdb4e735a5ca4a52a6.37_0#1813627299",
        "fl_last_page_view_id": "9527734e82314e23",
        "BROWSE_LOC": "Alabaster|AL|62|",
        "BROWSE_GEO_TYPE": "city",
        "fl-location": "Alabaster|AL|62|",
        "LDIR_LOC": "Alabaster|AL|62|",
        "OptanonAlertBoxClosed": "2025-06-20T01:21:39.684Z",
        "OptanonConsent": "isGpcEnabled=0&datestamp=Fri+Jun+20+2025+02%3A21%3A40+GMT%2B0100+(Central+European+Standard+Time)&version=202504.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=f3d80741-799d-4222-a52f-fb34e0ba5403&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&AwaitingReconsent=false&geolocation=DZ%3B02",
        "_clsk": "zxzyzf|1750382500400|6|1|b.clarity.ms/collect",
        "s_nr30": "1750382502669-New",
        "s_tslv": "1750382502682",
        "gpv_v12": "FL.com:Directory:LawyerDirectory:SearchResults",
        "s_sess": " s_sq=; s_cc=true;",
        "_rdt_uuid": "1750382411717.a7d5337b-586b-4c1f-92e3-b66aba3cbab2",
        "invoca_session": '{"ttl":"2025-07-20T01:29:13.108Z","session":{"invoca_id":"i-fa72c50d-b1d3-45b8-93d8-8f406df3e412"},"config":{"ce":true,"fv":false,"rn":false}}',
        "_dd_s": "rum=2&id=9a84957d-afb6-4871-ab10-cf93d20ab8bf&created=1750382408200&expire=1750383860366"
    }
    visible = True
    proxy = 'oxy_isp'


    def start_requests(self):
        yield scrapy.Request(
            url=self.url,
            headers=self.headers,
            callback=self.parse,
        )


    @property
    def headers(self):
        headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "fr-FR,fr;q=0.9,ar-DZ;q=0.8,ar;q=0.7,en-US;q=0.6,en;q=0.5",
            "cache-control": "no-cache",
            "dnt": "1",
            "pragma": "no-cache",
            "priority": "u=0, i",
            "referer": "https://clutch.co/",
            "sec-ch-ua": "\"Google Chrome\";v=\"135\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"135\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Linux\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "user-agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
        }
        return headers


    def parse(self, response):
        print(response.text)