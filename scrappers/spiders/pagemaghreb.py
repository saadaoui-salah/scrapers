import scrapy
import ast

class Service(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    phone_number = scrapy.Field()
    emails = scrapy.Field()
    location = scrapy.Field()
    website = scrapy.Field()
    other_contact = scrapy.Field()
    current_url = scrapy.Field()


class PagemaghrebSpider(scrapy.Spider):
    name = "pagemaghreb"
    start_urls = ["https://www.pagesmaghreb.com/"]

    def start_requests(self):
        yield scrapy.Request(
            url='https://www.pagesmaghreb.com/secteurs/services-aux-entreprises',
            callback=self.parse_categories
        )
    
    def parse_categories(self, response):
        data = response.css('sectors-show').get()
        data = self.clean_data(data, """sector="JSON.parse('""", """')"> </sectors-show>""")
        categories = ast.literal_eval(data)
        for category in categories['categories']:
            url = f'https://www.pagesmaghreb.com/entreprises/services-aux-entreprises/{category["slug"]}/algerie'
            yield scrapy.Request(
                url=url,
                callback=self.parse_pages
            )

    def parse_pages(self, response):
        pages = response.css('p.text-sm.text-gray-700.leading-5 span::text').getall() or [1]
        for i in range(int(pages[-1])):
            url = f'{response.url}?&page={i+1}'
            yield scrapy.Request(
                url=url,
                callback=self.parse_page
            )

    def parse_page(self, response):
        links = response.css('firm-card::attr(link)').getall()
        for link in links:
            yield scrapy.Request(
                url=link,
                callback=self.parse_item
            )

    def clean_data(sellf, data, s, l):
        return data.split(s)[1].split(l)[0].replace(r'\u0022','"').replace('true','True').replace('false','False').replace('null', 'None')


    def parse_item(self, response):
        name = response.css('index-show::attr(usual)').get()
        data = response.css('index-show').get()
        location = self.clean_data(data, """:addresses=" JSON.parse('""", '''\') " :breadcrumbs''')
        location = ast.literal_eval(location)
        contact_data = self.clean_data(data,""":contacts=" JSON.parse('""",'''\') " :premium=''')
        contact_data = ast.literal_eval(contact_data)
        location = f"{location[0]['city']['name']}, {location[0]['name']}"
        emails = []
        phone = []
        web = []
        other = []
        for contacts in contact_data:
            if contacts.get('contactmethods'):
                for contact in contacts['contactmethods']:
                    if contact['method_type'] == 'email':
                        emails += [contact['value']]
                    elif 'phone' in contact['method_type']:
                        phone += [contact['value']]
                    if contact['method_type'] == 'Site web':
                        web += [contact['value']]
                    else:
                        other += [contact['value']]
        item = Service()
        item['name'] = name
        item['phone_number'] = phone
        item['emails'] = emails
        item['location'] = location
        item['website'] = web
        item['other_contact'] = other
        item['current_url'] = response.url
        yield item
