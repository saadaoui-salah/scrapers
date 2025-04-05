import scrapy


class PbcgovSpider(scrapy.Spider):
    name = "pbcgov"
    us_cities = [
    "New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
    "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose",
    "Austin", "Jacksonville", "Fort Worth", "Columbus", "San Francisco",
    "Charlotte", "Indianapolis", "Seattle", "Denver", "Washington"
    ]

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'fr-FR,fr;q=0.9,ar-DZ;q=0.8,ar;q=0.7,en-US;q=0.6,en;q=0.5',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'dtCookie=v_4_srv_2_sn_46B9CC8C5C2464D2C223D1F503A07F38_perc_100000_ol_0_mul_1_app-3Ad7582e25f5d159c6_1_rcs-3Acss_0; rxVisitor=17435991038416FOMG5MC54H8GEPMIQ6SN0UE7NHPDH6M; dtSa=-; _ga=GA1.1.417770196.1743600860; _ga_RJ2TTY6D6N=GS1.1.1743604567.2.0.1743604567.60.0.0; _ga_RVRSB1X61C=GS1.1.1743604567.2.0.1743604567.0.0.0; BIGipServer~external~www.pbcgov.org_pbcvendors=!ZQ5AjcATBSHod10NGDOj/Bt0WeV+sungoDjNaa3JhE3pkXuYSMISiNnXFCuRq2o878tbs5If+9lEu+wVKj+38nckGwOZzb/9p9y0biiZhw==; rxvt=1743809442509|1743807629029; dtPC=2$207628916_192h-vCFPJUJMIJQHQMMPRMIKBKWKQFBLQRTAA-0e0',
        'DNT': '1',
        'Origin': 'https://www.pbcgov.org',
        'Pragma': 'no-cache',
        'Referer': 'https://www.pbcgov.org/pbcvendors',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
    }
    ids = []

    def start_requests(self):
        for city in self.us_cities:

            data = {
                'advSearch': 'true',
                'Cities': city.upper()
            }

            yield scrapy.FormRequest(
                url="https://www.pbcgov.org/pbcvendors/Vendor/GetVendors",
                headers=self.headers,
                formdata=data,
                callback=self.parse
            )

    def parse(self, response):
        vendors = response.json()
        for vendor in vendors:
            if vendor['VendorCode'] in self.ids:
                continue
            self.ids += [vendor['VendorCode']]
            addresses = vendor['Addresses'].split('\u003cBR\u003e')
            phone_numbers = vendor['ContactNamePhone'].split('\u003cBR\u003e') if vendor['ContactNamePhone'] else [None]
            emails = vendor['Emails'].split(',') if vendor['Emails'] else [None]
            item = {
                'name':vendor['CompanyName'],
                'address':addresses[0],
                'email':emails[0],
                'phone_number':phone_numbers[0],
                'alias_dba':vendor['DbaName'],
                'website':vendor['WebAddress'],
            }
            if len(addresses) > 1:
                item['additional_addresses'] = addresses[1:]
            if len(phone_numbers) > 1:
                item['additional_phone_numbers'] = phone_numbers[1:]
            if len(emails) > 1:
                item['additional_email'] = emails[1:]
            yield item