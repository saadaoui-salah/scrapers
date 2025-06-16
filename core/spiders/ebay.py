import scrapy
from w3lib.html import remove_tags

class EbaySpider(scrapy.Spider):
    custom_settings = {
        'CONCURRENT_REQUESTS': 1
    }
    name = "ebay"
    start_urls = [f"https://www.ebay.co.uk/str/automationplanetuk?_ipg=72&_pgn={i+1}&_tab=shop&_ajax=itemFilter&_tabName=shop" for i in range(237)]
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "fr-FR,fr;q=0.9,ar-DZ;q=0.8,ar;q=0.7,en-US;q=0.6,en;q=0.5",
        "cache-control": "no-cache",
        "dnt": "1",
        "pragma": "no-cache",
        "priority": "u=0, i",
        "referer": "https://www.ebay.co.uk/str/automationplanetuk",
        "sec-ch-ua": "\"Google Chrome\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Linux\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
    }
    cookies = {
        "__uzma": "4d93c8c8-2278-4b34-a0be-62814666eab0",
        "__uzmb": "1749760746",
        "__uzme": "9070",
        "__ssds": "3",
        "__ssuzjsr3": "a9be0cd8e",
        "__uzmaj3": "b686f386-6359-4572-89e5-cb55f3da37c4",
        "__uzmbj3": "1749760756",
        "ak_bmsc": "E86EC1FA436A8E7AF4871AEE6D42DFE5~000000000000000000000000000000~YAAQF7sUAteO81+XAQAAwShWdhxAEgdWI9n7QyhlaLE5TFUiC5SDD/aICEiVwu+uoWU8OmhNGFQqNAsFMOwCqlIX5q+VfJXGVXJlZBLpdGPzTIgXlSd2USBtj98l8SB1k1WayuPvB7lhFL6BH0WWAKTxBchkZecUo4+jW0goHwnfdMxZa1xxJ0pOwhjqDDjZB/KwBS+NxGWwbbDx6OFogwBUMh+2WvPvwP/LDUkapnbd5ell3fsodhjFacQkao+TN+/vzRfCWggXOr4M4iRFA/2pWtdQEULcH3IKiT0chhhNINh7njDQr7LZu6o+BnND+gnD8ufhCaYDDAXpuPHNmZgGRAkk84mPvFVhuKtuhgGpr/CSgRwIjyp4zdYXJeU8PnHW6Xc1vgc3wJk=",
        "utag_main__sn": "1",
        "utag_main_ses_id": "1750037154867%3Bexp-session",
        "_scid": "Gzg06Vz6gyhpaSPgLTRLLSpN8Gjfj6aL",
        "_gcl_au": "1.1.943539896.1750037157",
        "_pin_unauth": "dWlkPU5qRTVPVGxqT0RVdE5EQXhZaTAwT1RjekxUazBNVEF0WVRZek9ETm1aamMwTURNeQ",
        "_ScCbts": "[]",
        "_fbp": "fb.2.1750037160656.699887057891464093",
        "utag_main__ss": "0%3Bexp-session",
        "bm_sv": "8A50A20FE6BEF4C370B4004928F92298~YAAQbNXdWLZc3liXAQAAAXBkdhzT5ezJb0cYNu56M0Bn8vcTZmjMYop6aSITpUYnbCUY/O7ge6BLZ0SvKAfh7H5XAzK5jMh0qgYmwiJrAbWr2uHVqcVdyyIDDsrvprayREYvaG9zqZnfaVrkFp49gbZqWT1kYJm3fLPHaL8qkwsePhyc6IFJv7n20me9gkPALotXSh3kWDUo5cQco2gU71EDJPP5t4+BCjL8xI2EKpG+QYENsdwMYacxHXkcDr3O~1",
        "__uzmlj3": "Zfx2sss65dhmqFXLJDmqDtnKAHNyPUZuP0w15whnxdo=",
        "__gads": "ID=720e2cfcb080dd23:T=1750037985:RT=1750039758:S=ALNI_MafQe-4OsKSUD-zqNj0TInE7VNTPQ",
        "__gpi": "UID=0000113694f8adeb:T=1750037985:RT=1750039758:S=ALNI_MY709AuZ4e_F26os4FW8Dtj7Te2uQ",
        "__gsas": "ID=d80f0606e444ac7c:T=1750039794:RT=1750039794:S=ALNI_MZeDbe6xyTBTWC2OYzOXt9cnzaz_Q",
        "_uetsid": "cd6f01f04a5211f083615da6f9b40101",
        "_uetvid": "cd70f0e04a5211f08916973290bf5e71",
        "utag_main__se": "5%3Bexp-session",
        "utag_main__st": "1750041660812%3Bexp-session",
        "utag_main__pn": "5%3Bexp-session",
        "_rdt_uuid": "1750037155698.b5c3da1f-638b-4a0f-b329-99c155088019",
        "_scid_r": "J7g06Vz6gyhpaSPgLTRLLSpN8Gjfj6aL6CxYbw",
        "_derived_epik": "dj0yJnU9NF9zcFlnd2tsTkYwNEtxZ0hQeDhSVXZHWS0xWWZuS1Ambj1IaE5mMkF1SzU0N2pEdTJyeExGSGVBJm09MSZ0PUFBQUFBR2hQZlRZJnJtPTEmcnQ9QUFBQUFHaFBmVFkmc3A9Mg",
        "cto_bundle": "7npac18wJTJGNG1YampRemkxa01NOU5lQ09saEkxYWRwaUZ2dVNkUWhCVlVMdVoxSlBCTHoyM0l2TXJIR2tXZE5aRG9sYW9jaUFVNjBlY1pFWkIxNFZyNWVlbloweGhBWjVZTzFPaENhenQ0ZFU4bk1wYUFpUU9RbTRiYSUyRlFYc0xCdXUxcFlMdDF1R1NEbHBZZ0IzcyUyRkllaFVlYWFoS01jMGpiNkpodm1rTlppM0d2MGpyNW1ETCUyQnBydiUyQk5IcU9Db2FqT2I3RWx4bDFGQlpxbzQ5VWpsaXo3d2pzZyUzRCUzRA",
        "s": "CgADuAFBoUM7AMTQGaHR0cHM6Ly93d3cuZWJheS5jby51ay9zdHIvYXV0b21hdGlvbnBsYW5ldHVrP19pcGc9NzImcnQ9bmMmX3Bnbj0xJl90YWI9c2hvcAcA+AAgaFDDtjY1ZGUyNTc2MTk3MGE2MGRiNWZkZDg3NGZmZmY3Zjg2x9E5tg**",
        "ebay": "^js=1^sbf=#000200^",
        "__deba": "4sv7_QlnsG8Jj5QiS-ndWiUjq1iqItzRQyU5Iswbp4M07fU8ALbZFL2udoPGa1bEXR8UW1J2_XMwSXzXGqPFGJF5nXJcUVYN0ZInJxYc2huP8JMUhvX_ek6GSm8rEkYfn4mhBGs4WOp8Jg8Od--SGQ==",
        "__uzmc": "8909920575109",
        "__uzmd": "1750040421",
        "__uzmf": "7f60006c0cbcaa-91b5-43ee-9030-b5d46f286a2c1749760746847279674349-5154b784a345a055205",
        "ns1": "BAQAAAZZay1gcAAaAANgAU2owsuljNjl8NjAxXjE3NTAwMzcxNDU4MTVeXjFeM3wyfDV8NHw3fDEwfDQyfDQzfDExXl5eNF4zXjEyXjEyXjJeMV4xXjBeMV4wXjFeNjQ0MjQ1OTA3NSV0m0TwxjRcAkKLBGNZoZ1NXNdK",
        "nonsession": "BAQAAAZZay1gcAAaAADMABWowsukwODAwMADKACBsEeZpNjVkZTI1NzYxOTcwYTYwZGI1ZmRkODc0ZmZmZjdmODYAywADaE+GcTE0NVkocKlK+Kj+tnPYiqBbVraFhUP/",
        "dp1": "bpbf/#0002000000000000000006a30b2e9^bl/DZ6c11e669^",
        "__uzmcj3": "589727379626",
        "__uzmdj3": "1750040426",
        "__uzmfj3": "7f60006c0cbcaa-91b5-43ee-9030-b5d46f286a2c1749760756734279669739-3fedce2709d8ce7273"
    }


    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                headers=self.headers,
                cookies=self.cookies,
        ) 
    def parse(self, response):
        data = response.json()
        items = filter(lambda x: x['_type'] == 'CardContainer',data['modules']['LISTINGS_MODULE']['containers'])
        items = list(items)[0]
        for item in items['cards']:
            yield scrapy.Request(
                url=item['action']['URL'],
                headers=self.headers,
                cookies=self.cookies,
                callback=self.parse_pdp,
            )


    def parse_pdp(self, response):
        yield {
            'name':remove_tags(response.css('.x-item-title__mainTitle').get('')),
            'condition':remove_tags(response.css('.x-item-condition-text .ux-textspans::text').get('')),
            'price':response.css('.x-price-primary .ux-textspans::text').get(''),
            'availability':response.xpath("//div[@id='qtyAvailability']//span[contains(text(), 'available')]/text()").get() or 'Last one',
            'sold':response.xpath("//div[@id='qtyAvailability']//span[contains(text(), 'sold')]/text()").get(),
            'item specifics':remove_tags(response.css('.ux-layout-section--features').get('')),
            'Product Identifiers':remove_tags(response.css('.ux-layout-section-evo.ux-layout-section--productIdentifiers').get('')),
        }