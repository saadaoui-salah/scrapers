import scrapy

from w3lib.html import remove_tags

class RedfinSpider(scrapy.Spider):
    name = "redfin"
    start_urls = [f"https://www.redfin.com/stingray/api/gis?al=1&include_nearby_homes=true&market=socal&mpt=99&num_homes=350&ord=redfin-recommended-asc&page_number={i + 1}&region_id=11203&region_type=6&sf=1,2,3,5,6,7&start={350 * i}&status=9&uipt=1&v=8" for i in range(9)]
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "fr-FR,fr;q=0.9,ar-DZ;q=0.8,ar;q=0.7,en-US;q=0.6,en;q=0.5",
        "cache-control": "no-cache",
        "dnt": "1",
        "pragma": "no-cache",
        "priority": "u=0, i",
        "referer": "https://www.redfin.com/",
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
    proxy = 'burp'

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                headers=self.headers,
                callback=self.parse,
            )

    def parse(self, response):
        import json
        try:
            data = json.loads(response.text.replace('{}&&',''))
            homes = data['payload']['homes']
            for home in homes:
                yield scrapy.Request(
                    url=f"https://www.redfin.com{home['url']}",
                    headers=self.headers,
                    callback=self.parse_details,
                )
        except:
            print(response.text)

    def parse_details(self, response):
        location = response.css('[data-rf-test-id="abp-cityStateZip"]::text').getall()
        street_address = response.css('[data-rf-test-id="abp-streetLine"]::attr(title)').get()
        if location:
            city = location[0]
            state, zip_ = location[2], location[-1] 
        else:
            state, zip_, city = [None, None, None]
        yield {
            'Street Address':street_address,
            'City':city,
            'State':state,
            'Zip':zip_,
            'Price':response.css('[data-rf-test-id="abp-price"] .statsValue::text').get(),
            'Home Type':response.xpath("//span[contains(.,'Property Type') and @class='valueType']/../span[1]/text()").get(),
            'Days on Market':response.xpath("//span[contains(.,'On Redfin') and @class='valueType']/../span[1]/text()").get(),
            'Sqft':response.css('[data-rf-test-id="abp-sqFt"] .statsValue::text').get(),
            'Beds':response.css('[data-rf-test-id="abp-beds"] .statsValue::text').get(),
            'Baths':response.css('[data-rf-test-id="abp-baths"] .statsValue::text').get(),
            'Lot Size':response.xpath("//span[contains(.,'Lot Size') and @class='valueType']/../span[1]/text()").get(),
            'Year Built':response.xpath("//span[contains(.,'Year Built') and @class='valueType']/../span[1]/text()").get(),
            'Price Per Sqft':response.xpath("//span[contains(.,'Price/Sq.Ft.') and @class='valueType']/../span[1]/text()").get(),
            'Agent Name':response.css('.agent-basic-details--heading span::text').get(),
            'Agent License':''.join(response.css('.agentLicenseDisplay::text').getall()),
            'Agency':remove_tags(response.css('.agent-basic-details--broker').get('')),
            'Agent Phone':response.css('[data-rf-test-id="agentInfoItem-agentPhoneNumber"]::text').get(),
            'Agent Email':remove_tags(response.css('.email-addresses').get('')).replace('(agent)',''),
            'Full Address':f'{street_address} {"".join(location)}',
            'Taxes':response.xpath('//span[contains(.,"Property taxes")]/../span[2]//a/text()').get(),
            '3D Tour':True if response.xpath("//span[contains(@class, 'ButtonLabel') and contains(text(), '3D Tour')]").get() else False,
            'Description':remove_tags(response.css('[data-rf-test-id="listingRemarks"].remarks').get('')),
            'Listing URL':response.url
        }