import scrapy
from w3lib.html import remove_tags
from scrapy_playwright.page import PageMethod

class Item(scrapy.Item):
    marque = scrapy.Field()
    modèle = scrapy.Field()
    année = scrapy.Field()
    motorisation = scrapy.Field()
    puissance_fiscale = scrapy.Field()
    emission_de_co2 = scrapy.Field()
    poids_du_véhicule = scrapy.Field() 

class LargusSpider(scrapy.Spider):
    name = "largus"
    start_urls = [
        "https://www.largus.fr/fiche-technique.html", 
        "https://www.largus.fr/fiche-technique/utilitaires-legers.html",
        "https://www.largus.fr/fiche-technique/motos-cyclos.html",
        "https://www.largus.fr/fiche-technique/autocars.html",
        "https://www.largus.fr/fiche-technique/voiturettes-tourisme.html",

    ]

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES':{
            'scrappers.proxy.oxylabs.ProxyMiddleware': 130, 
        }
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse
            )


    def parse(self, response):
        marks = response.css(".liste-marques li")
        for mark in marks:
            yield scrapy.Request(
                url=f'https://www.largus.fr{mark.css("a::attr(href)").get()}',
                callback=self.parse_marks,
                meta={'mark': mark.css('a::attr(title)').get()},
            ) 


    def parse_marks(self, response):
        models = response.css(".liste-modeles li")
        for model in models:
            response.meta['model'] = model.css('a::attr(title)').get()
            yield scrapy.Request(
                url=f'https://www.largus.fr{model.css("a::attr(href)").get()}',
                callback=self.parse_years,
                meta=response.meta
            ) 

    def parse_years(self, response):
        years = response.css(".liste-millesimes li")
        for year in years:
            response.meta['year'] = year.css('.libelle::text').get().replace('\t','').replace('\n', '').replace('\r', '')
            yield scrapy.Request(
                url=f'https://www.largus.fr{year.css("a::attr(href)").get()}',
                callback=self.parse_cars,
                meta=response.meta
            ) 

    def parse_cars(self, response):
        years = response.css("td")
        for year in years:
            yield scrapy.Request(
                url=f'https://www.largus.fr{year.css("a::attr(href)").get()}',
                callback=self.parse_details,
                meta=response.meta
            )

    def parse_details(self, response):
        item = Item()
        poids = []
        for div in response.xpath("//h3[contains(text(), 'Poids')]/../div/div"):
            poids += [{div.css('.labelInfo::text').get(): div.css('.valeur::text').get()}]
        motor = []
        for div in response.xpath("//h3[contains(text(), 'Moteur')]/../div/div"):
            motor += [{div.css('.labelInfo::text').get(): div.css('.valeur::text').get()}]
        item['marque'] = response.meta['mark'].replace('Fiches techniques ', '')
        item['modèle'] = response.meta['model'].replace('Fiches techniques ', '').split('-')[0]
        item['année'] = response.meta['year'].replace('Fiche technique ', '').replace(item['modèle'], '')
        item['motorisation'] = motor
        item['puissance_fiscale'] = response.xpath("//div[@class='ligneInfo']/span[contains(text(),'Puissance fiscale')]/../span[@class='valeur']//text()").get('').replace('\t','').replace('\n', '').replace('\r', '')
        item['emission_de_co2'] = remove_tags(response.css('.CO2').get('')).replace('\t','').replace('\n', '').replace('\r', '')
        item['poids_du_véhicule'] = poids
        yield item
