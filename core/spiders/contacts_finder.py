import scrapy
from core.utils.utils import read_csv
from core.utils.search import find_emails


class ContactsFinderSpider(scrapy.Spider):
    name = "contacts_finder"

    df = read_csv("./leads.csv")
    
    def start_requests(self):
        data = self.df.to_dict(orient='records')
        for item in data:
            url = item['Website'] if 'http' in item['Website'] else f"http://{item['Website']}"
            item['whatsapp'] = []
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                errback=self.errback,
                meta={'item': item}
            )

    def add_social_media(self, key, keyword, item, response):
        links = response.xpath(f'//*[contains(@href, "{keyword}.com")]/@href').getall()
        if not item[key]:
            item[key] = links
        else:
            for link in links:
                    if isinstance(item[key], str):
                        item[key] = [item[key], link]
                    if isinstance(item[key], list):
                        if link not in item[key]: 
                            item[key] += [link]
                    else:
                        item[key] = [link]
        return item[key]

    def get_emails(self, response, item):
        emails = response.xpath('//*[contains(@href, "mailto:")]/@href').getall()
        emails_regex = find_emails(response.text)
        if isinstance(emails_regex, str) and emails_regex not in emails:
            emails += [emails_regex]
        if isinstance(emails_regex, list):
            for e in emails_regex:
                if e not in emails:
                    emails += [e]
        for e in emails:
            if isinstance(item['Primary email'], str) and item['Primary email'] not in emails:
                item['Primary email'] = emails + [item['Primary email']]
            elif isinstance(item['Primary email'], list):
                if e not in item['Primary email']:
                    item['Primary email'] += [e]
            else:
                item['Primary email'] = [e]
        return item['Primary email']

    def get_numbers(self, response, item):
        phone_numbers = response.xpath('//*[contains(@href, "tel:")]/@href').getall()
        for e in phone_numbers:
            if isinstance(item.get('Phone numbers'), list):
                if e not in item['Phone numbers']:
                    item['Phone numbers'] += [e]
            else:
                item['Phone numbers'] = [e]

        return item.get('Phone numbers')

    def add_data(self, response):
        
        item = response.meta['item']
        item['LinkedIn'] = self.add_social_media('LinkedIn', 'linkedin', item, response)
        item['YouTube'] = self.add_social_media('YouTube', 'youTube', item, response)
        item['Instagram'] = self.add_social_media('Instagram', 'instagram', item, response)
        item['TikTok'] = self.add_social_media('TikTok', 'tikTok', item, response)
        item['Facebook'] = self.add_social_media('Facebook', 'facebook', item, response)
        item['whatsapp'] = self.add_social_media('whatsapp', 'https://api.whatsapp.com/', item, response)
        item['Primary email'] = self.get_emails(response, item)
        item['Phone numbers'] = self.get_numbers(response, item)
        return item
    
    def parse(self, response):
        item = self.add_data(response)
        
        contact_page = response.xpath('//*[contains(@href, "contact")]/@href').getall()
        if not contact_page :
            yield item
            return
        contact_page = list(filter(lambda x: 'whatsapp.com' not in x ,contact_page))
        if len(contact_page):
            contact_page = contact_page[0]
        if contact_page.startswith('/'):
            contact_page = f"{response.url}{contact_page}"
        url = contact_page if 'http' in contact_page else f"http://{contact_page}"
        yield scrapy.Request(
            url=url,
            callback=self.parse_contact,
            errback=self.errback,
            meta={'item': item}
        )
    
    def parse_contact(self, response):
        item = self.add_data(response)
        
        about_page = response.xpath('//*[contains(@href, "about")]/@href').get()
        if not about_page:
            yield item
            return
        if about_page.startswith('/'):
            about_page = f"{response.url}{about_page}"
        url = about_page if 'http' in about_page else f"http://{about_page}"
        yield scrapy.Request(
            url=url,
            errback=self.errback,
            callback=self.parse_about,
            meta={'item': item}
        )
    
    def parse_about(self, response):
        item = self.add_data(response)
        yield item

    def errback(self, failure):
        yield failure.request.meta['item']