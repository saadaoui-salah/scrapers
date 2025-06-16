import scrapy
from core.utils.utils import read_glob_files 
from core.utils.security import decode_cf_email 

class BandejaShopSpider(scrapy.Spider):
    name = "bandeja-shop"

    def start_requests(self):
        yield scrapy.Request(
            url='https://google.com/',
            callback=self.parse
        )

    def parse(self, res):
        selectors = {
            'Email address':[
                "//strong[contains(text(), 'mail :')]/../*[contains(text(), '@')]/text()",
                "//strong[contains(text(), 'mail:')]/../*[contains(text(), '@')]/text()", 
                "//strong[contains(text(), 'mail:')]/../a/*[contains(text(), '@')]/text()", 
                "//li[contains(text(), 'mail:')]/*[contains(text(), '@')]/text()", 
                "//li[contains(text(), 'mail :')]/*[contains(text(), '@')]/text()"
            ],
            'Phone number':[
                "//strong[contains(text(), 'téléphone')]/..//text()", 
                "//b[contains(text(), 'téléphone')]/..//text()", 
                "//strong[contains(text(), 'Téléphone')]/..//text()", 
                "//b[contains(text(), 'Téléphone')]/..//text()", 
                "//li[contains(text(), 'téléphone')]//text()", 
                "//p[contains(text(), 'téléphone')]//text()", 
                "//p[contains(text(), 'Téléphone')]/..//text()", 
                "//li[contains(text(), 'Téléphone')]//text()"],
            'Physical address':["//strong[contains(text(), 'Adresse :')]/../text()", "//li[contains(text(), 'Adresse du Club :')]/text()"],
            'Website':[
                "//b[contains(text(), 'nternet :')]/..//@href", 
                "//b[contains(text(), 'nternet:')]/..//@href",
                "//strong[contains(text(), 'nternet :')]/..//@href", 
                "//strong[contains(text(), 'nternet:')]/..//@href", 
                "//p[contains(text(), 'nternet:')]/..//@href", 
                "//p[contains(text(), 'nternet :')]/..//@href", 
                "//li[contains(text(), 'nternet :')]//@href",
                "//li[contains(text(), 'nternet:')]//@href",
                "//strong[contains(text(), 'site web')]/..//@href", 
                "//strong[contains(text(), 'Site web')]/..//@href", 
                "//p[contains(text(), 'Site web')]/..//@href", 
                "//p[contains(text(), 'site web')]/..//@href", 
                "//li[contains(text(), 'site web')]//@href",
                "//li[contains(text(), 'Site web')]//@href",
                ],
        }
        for response in read_glob_files('*.html'):
            data =  {
                'Club name':response.css("[property='og:title']::attr(content)").get('').replace('Club De Padel ',  '').split('-')[0],
                'Link':response.css('link[rel="canonical"]::attr(href)').get(),
                'description':''.join(response.css('.inner-post-entry p::text').getall()),
            }
            for key, vals in selectors.items():
                for val in vals:
                    if res := ''.join(response.xpath(val).getall()):
                        data[key] = res.split(':')[-1]
                        break
            
            if not data.get('Email address','').replace(' ', ''):
                if coded := response.css('.__cf_email__::attr(data-cfemail)').get():
                    data['Email address'] = decode_cf_email(coded)
            if  not data.get('Website','') and data['Link']:
                print(data['Link'])
            yield data