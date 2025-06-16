import scrapy
import json
from core.utils.utils import read_json_files
import json
from datetime import datetime
from dateutil import parser
import re
regions = [
  "Baden-Württemberg",
  "Bavaria",
  "Berlin",
  "Brandenburg",
  "Bremen",
  "Hamburg",
  "Hesse",
  "Lower Saxony",
  "Mecklenburg-Vorpommern",
  "North Rhine-Westphalia",
  "Rhineland-Palatinate",
  "Saarland",
  "Saxony",
  "Saxony-Anhalt",
  "Schleswig-Holstein",
  "Thuringia"
]

class StepstoneSpider(scrapy.Spider):
    name = "stepstone"
    start_urls = ['https://www.google.com/']
    ignore = []

    
    def parse(self, res):
        for items in read_json_files('json/*.json'): 
            for item in items:
                item['script'] = json.loads(item['script'].strip().split('props: ')[-1][:-1])
                yield from self.parse_details(item)

    def parse_details(self, data):
        if f"https://www.stepstone.de{data['url']}" in self.ignore:
            return 
        self.ignore += [f"https://www.stepstone.de{data['url']}"]
        text = ''.join([i['content'] for i in data['script']['textSections']])
        postcodes = re.findall(r'\b\d{5}\b', text)
        target_date = parser.parse(data['datePosted'])
        now = datetime.now(target_date.tzinfo)
        delta_days = (now.date() - target_date.date()).days
        item = {
            'Job Postion':data['title'],
            'Company Name':data['companyName'],
            'Postcode':postcodes,
            'Cityname':data['location'],
            'Publish Date':data['datePosted'],
            'Publish in Dates':f"vor {delta_days} Tagen",
            'Link': f"https://www.stepstone.de{data['url']}",
        }
        if len(data['script']['companyCard']['sectors']) > 1:
            item['First Categorie'] = data['script']['companyCard']['sectors'][1]['name']
            item['Second Categorie'] = data['script']['companyCard']['sectors'][0]['name']
        if len(data['script']['companyCard']['sectors']) == 1:
            item['First Categorie'] = data['script']['companyCard']['sectors'][0]['name']
 
        for html in data['script']['textSections']:
            sel = scrapy.Selector(text=html['content'])
            if email := sel.xpath('//a[contains(@href, "mailto:")]/@href').get('').replace('mailto:', '') and not data.get('Email'):
                email = sel.xpath('//a[contains(@href, "mailto:")]/@href').get('').replace('mailto:', '')
                item['Email'] = email
            if email := sel.xpath('//strong[contains(text(), "@")]/text()').get('') and not data.get('Email'):
                email = sel.xpath('//strong[contains(text(), "@")]/text()').get('')
                item['Email'] = email
            if tel := sel.xpath('//a[contains(@href, "tel:")]/@href').get('').replace('tel:', '') and not data.get('Telefon'):
                item['Telefon'] = sel.xpath('//a[contains(@href, "tel:")]/@href').get('').replace('tel:', '')
            if tel := ''.join(sel.xpath('//*[contains(text(), "Telefon")]//text()').getall()) and not data.get('Telefon') :
                item['Telefon'] = ''.join(sel.xpath('//*[contains(text(), "Telefon")]//text()').getall())
            if name := sel.xpath('//*[contains(text(),"Dr.")]/text()').getall() and not data.get('Full Name'):
                item['Full Name'] = sel.xpath('//*[contains(text(),"Dr.")]/text()').getall()
            for i in regions:
                if item.get('Bundesland'):
                    break
                if i in html:
                    item['Bundesland'] = i
            yield item
            