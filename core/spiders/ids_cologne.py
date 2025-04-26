import scrapy
import json
from urllib.parse import urlencode


class IdsCologneSpider(scrapy.Spider):
    name = "ids-cologne"
    cookies = {
        "OptanonAlertBoxClosed": "2025-04-05T21:39:16.318Z",
        "gig_bootstrap_3_pOCT7i_ztOpYc32Iu7DN5ntr76tsHpgFj9kS8MVTABgbcjerfiWfTD41wBsDc0NF": "sso_ver4",
        "_ga": "GA1.1.576878167.1743889077",
        "_gcl_au": "1.1.1649425392.1743889077",
        "FPID": "FPID2.2.pPSP6%2FmqobQ5z0I%2FTG17V81u1i0f1v807afizqMHr3Q%3D.1743889077",
        "glt_3_pOCT7i_ztOpYc32Iu7DN5ntr76tsHpgFj9kS8MVTABgbcjerfiWfTD41wBsDc0NF": "st2.s.AtLti3BApw.fEQ4fW_t-Mp4lRozuenbKUqRkWuo1y-e2CjRkU06TH25OHE14yYQwn3L7Hd9tshRX4t-H4dOstnCoySr73STpxXBJJdeO08DPg3-Q39dLT_9BPkKObfaxyGypi8hFBsT.W0MG-El3KowLzKqFBMRdce4BtE5ouuqzqLiw0-TEed8qqxOGZv62vJfxC_cFt55bn64A4W0AmcGQJjhtaj7J-A.sc3",
        "gig_bootstrap_4_rEOxG2rRH43GkREwFgcG4A": "sso_ver4",
        "glt_4_rEOxG2rRH43GkREwFgcG4A": "st2.s.AtLti3BApw.fEQ4fW_t-Mp4lRozuenbKUqRkWuo1y-e2CjRkU06TH25OHE14yYQwn3L7Hd9tshRX4t-H4dOstnCoySr73STpxXBJJdeO08DPg3-Q39dLT_9BPkKObfaxyGypi8hFBsT.W0MG-El3KowLzKqFBMRdce4BtE5ouuqzqLiw0-TEed8qqxOGZv62vJfxC_cFt55bn64A4W0AmcGQJjhtaj7J-A.sc3",
        "OptanonConsent": "isGpcEnabled=0&datestamp=Sat+Apr+12+2025+12%3A05%3A16+GMT%2B0100+(Central+European+Standard+Time)&version=202402.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=7e608f94-04be-446a-8a2e-d06066f32c6c&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&geolocation=DZ%3B08&AwaitingReconsent=false",
        "PHPSESSID": "r5cnmf79s9ngm53341gvts9j7d",
        "FPLC": "ebldqK3MAVTH09FjLyHSuXesqs1m7JhvIxwXFWHrfUIGiUmkVUc5ltyFrQM%2Fnhtc9lbbkqt3fizHxrGRnv3qZ4X0XtTQLIiKVCHQ8HEMafPPzFIJDsDLt08p4jraBg%3D%3D",
        "_ga_F5WGQ8B9S7": "GS1.1.1744455789.3.1.1744455917.51.0.0",
        "_ga_91CK38R0CW": "GS1.1.1744455789.3.1.1744455917.0.0.2056663910"
    }
    url = "https://live.messebackend.aws.corussoft.de/rest/seriesoftopicsuser/topic/2025_ids/profile/Jlk8WoqwHiWUyYelVzNWcJqJC9SEoFjMJ3LN06sl70GZgmRdmY8kbzSAtWluU4Lg/profiles/relevant?topic=2025_ids&os=web&appUrl=https%3A%2F%2Fconnect.ids-cologne.de&lang=en&apiVersion=52&timezoneOffset=0&searchString={}&itemsPerPage=35&page={}&filterlist=0"


    def start_requests(self):
        for keyword in ['quality', 'operation']:
            url = f"https://live.messebackend.aws.corussoft.de/rest/seriesoftopicsuser/topic/2025_ids/profile/Jlk8WoqwHiWUyYelVzNWcJqJC9SEoFjMJ3LN06sl70GZgmRdmY8kbzSAtWluU4Lg/profiles/relevant?topic=2025_ids&os=web&appUrl=https%3A%2F%2Fconnect.ids-cologne.de&lang=en&apiVersion=52&timezoneOffset=0&searchString={keyword}&itemsPerPage=35&page=0&filterlist=0"
            
            self.headers = {
                "accept": "application/json",
                "accept-language": "fr-FR,fr;q=0.9,ar-DZ;q=0.8,ar;q=0.7,en-US;q=0.6,en;q=0.5",
                "beconnectiontoken": "eyJhbGciOiJIUzUxMiJ9.eyJzb3RVc2VySWQiOiJKbGs4V29xd0hpV1V5WWVsVnpOV2NKcUpDOVNFb0ZqTUozTE4wNnNsNzBHWmdtUmRtWThrYnpTQXRXbHVVNExnIiwidXNlclBvb2xJZCI6IklEUyIsImlhdCI6MTc0NDY3MTIxMCwiaXNzIjoiZXZlbnQtY2xvdWQuY29tIiwic3ViIjoiNzkwNzY3OSIsInR5cGUiOiJiZUNvbm5lY3Rpb24ifQ.leA8UhgQjG9hKaAA1le2-O_cAfkO-EtkVGvEgIvElXQnMCmwcs9sQiCjgmep8lTW8TGtZgkg4i3d3P6_58gXSw",
                "cache-control": "no-cache",
                "content-type": "application/json",
                "dnt": "1",
                "ec-client": "EventGuide/2.14.0-9570[52]",
                "ec-client-branding": "2025_ids",
                "origin": "https://connect.ids-cologne.de",
                "pragma": "no-cache",
                "priority": "u=1, i",
                "referer": "https://connect.ids-cologne.de/",
                "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Linux"',
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "cross-site",
                "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
            }

            yield scrapy.Request(
                url=url,
                method="GET",
                headers=self.headers,
                callback=self.parse,
                meta={'page': 0, 'keyword': keyword}
            )

    def parse(self, response):
        # Handle the JSON data here
        data = response.json()
        for item in data['items']:
            yield from self.send_request(item['sotUser']['id'], response.meta)

        if data['hasNextPage']:
            response.meta['page'] += 1
            yield scrapy.Request(
                url=self.url.format(response.meta['keyword'], response.meta['page']),
                headers=self.headers,
                callback=self.parse,
                meta=response.meta
            )


    def send_request(self, profile, meta):
        url = (
            "https://live.messebackend.aws.corussoft.de/rest/seriesoftopicsuser/topic/2025_ids/profile/"
            "Jlk8WoqwHiWUyYelVzNWcJqJC9SEoFjMJ3LN06sl70GZgmRdmY8kbzSAtWluU4Lg/"
            f"targetProfile/{profile}"
            "?topic=2025_ids&os=web&appUrl=https%3A%2F%2Fconnect.ids-cologne.de&lang=en&apiVersion=52&timezoneOffset=0"
        )

        headers = {
            "accept": "application/json",
            "accept-language": "fr-FR,fr;q=0.9,ar-DZ;q=0.8,ar;q=0.7,en-US;q=0.6,en;q=0.5",
            "beconnectiontoken": "eyJhbGciOiJIUzUxMiJ9.eyJzb3RVc2VySWQiOiJKbGs4V29xd0hpV1V5WWVsVnpOV2NKcUpDOVNFb0ZqTUozTE4wNnNsNzBHWmdtUmRtWThrYnpTQXRXbHVVNExnIiwidXNlclBvb2xJZCI6IklEUyIsImlhdCI6MTc0NDY3MTIxMCwiaXNzIjoiZXZlbnQtY2xvdWQuY29tIiwic3ViIjoiNzkwNzY3OSIsInR5cGUiOiJiZUNvbm5lY3Rpb24ifQ.leA8UhgQjG9hKaAA1le2-O_cAfkO-EtkVGvEgIvElXQnMCmwcs9sQiCjgmep8lTW8TGtZgkg4i3d3P6_58gXSw",
            "cache-control": "no-cache",
            "content-type": "application/json",
            "dnt": "1",
            "ec-client": "EventGuide/2.14.0-9570[52]",
            "ec-client-branding": "2025_ids",
            "origin": "https://connect.ids-cologne.de",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": "https://connect.ids-cologne.de/",
            "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Linux"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
        }

        yield scrapy.Request(
            url=url,
            headers=headers,
            callback=self.parse_details,
            meta=meta
        )


    def parse_details(self, response):
        data = response.json()['profile']
        item = {
            'keyword': response.meta['keyword'],
            'name': f"{data['firstName']} {data['lastName']}",
            'linkedin': data.get('linkedIn'),
            'position': data.get('position'),
            'email':data.get('email'),
            'phone_number':data.get('phone'),
            'country_code':data.get('countrycode'),
        }
        if data.get('organizations') and len(data.get('organizations')):
            item['company'] = data['organizations'][0].get('name')
            item['company_email'] = data['organizations'][0].get('email')
            item['company_phone'] = data['organizations'][0].get('phone')
        yield item