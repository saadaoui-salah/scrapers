import scrapy
from requests_toolbelt.multipart.encoder import MultipartEncoder

class MedicalregisterSpider(scrapy.Spider):
    name = "medicalregister"
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'fr-FR,fr;q=0.9,ar-DZ;q=0.8,ar;q=0.7,en-US;q=0.6,en;q=0.5',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Origin': 'https://medicalregister.com.au',
        'Pragma': 'no-cache',
        'Referer': 'https://medicalregister.com.au/Advanced-Search.aspx',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
    }


    def start_requests(self):
        for i in ['Ophthalmic%20Surgeon', 'Ophthalmology%20(see%20also%20Surgery%20-%20Ophthalmic)', 'Orthopaedics%20(see%20also%20Surgery%20-%20Orthopaedic)', 
        'Surgery%20-%20Abdominal', 'Surgery%20-%20Breast', 'Surgery%20-%20Cardiothoracic', 'Surgery%20-%20Colorectal', 'Surgery%20-%20Cosmetic', 'Surgery%20-%20Cosmetic%20and%20Hair%20Transplantation',
        'Surgery%20-%20Cosmetic,%20Plastic%20&%20Reconstructive', 'Surgery%20-%20Cranio%20Facial', 'Surgery%20-%20Cranio%20Facial', 'Surgery%20-%20Endocrine',
        'Surgery%20-%20Endovascular', 'Surgery%20-%20Facial%20Nerve%20Reconstruction', 'Surgery%20-%20Foot%20&%20Ankle', 'Surgery%20-%20General', 'Surgery%20-%20General/Endoscopy',
        'Surgery%20-%20Hand', 'Surgery%20-%20Hand%20&%20Upper%20Limb', 'Surgery%20-%20Hand,%20Wrist%20&%20Upper%20Limb', 'Surgery%20-%20Head%20and%20Neck', 'Surgery%20-%20Knee',
        'Surgery%20-%20Laparoscopic', 'Surgery%20-%20Microsurgery', 'Surgery%20-%20Neurosurgery', 'Surgery%20-%20Obesity', 'Surgery%20-%20Oesophageal', 'Surgery%20-%20Oncology',
        'Surgery%20-%20Ophthalmic%20(see%20also%20Ophthalmology/Ophthalmic%20Surgery)', 'Surgery%20-%20Oral/Maxillofacial', 'Surgery%20-%20Orthopaedic', 'Surgery%20-%20Orthopaedic%20(see%20also%20Orthopaedics%20&%20Medico/Legal)',
        'Surgery%20-%20Paediatric', 'Surgery%20-%20Paediatric%20Orthopaedic', 'Surgery%20-%20Spinal', 'Surgery%20-%20Transplantation', 'Surgery%20-%20Vascular', 'Surgery%20-%20Venous']:
            yield scrapy.Request(
                url=f'https://medicalregister.com.au/Advanced-Search.aspx?&TxtSpecialty={i}',
                headers=self.headers,
                callback=self.parse,
            )

    def parse(self, response):
        for slug in response.css('.search-result-full-name a::attr(href)').getall():
            yield scrapy.Request(
                url=f'https://medicalregister.com.au{slug}',
                headers=self.headers,
                callback=self.parse_details,
            )

        pages = response.xpath("//span[contains(text(), 'Total')]/text()").get('').lower().replace('total ', '').replace(' pages', '')
        if not response.meta.get('paginated') and pages:
            for i in range(int(pages)):
                yield scrapy.Request(
                    url=f'{response.url}&page={i}',
                    headers=self.headers,
                    callback=self.parse,
                    meta={'paginated': True}
                )

    def parse_details(self, response):
        yield {
            'profile title':  response.css('.profile-title::text').get(),
            'email':response.xpath("//p[contains(text(), 'Email')]/a/@href").get('').replace('mailto:',''),
            'phone':''.join(response.xpath("//p[contains(text(), 'Phone')]//text()").getall() +\
                response.xpath("//p[contains(text(), 'Fax')]//text()").getall()),
        }