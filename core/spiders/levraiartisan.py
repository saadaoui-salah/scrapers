import scrapy
from w3lib.html import remove_tags

franceDepartments = [
  "Ain",
  "Aisne",
  "Allier",
  "Alpes-de-Haute-Provence",
  "Hautes-Alpes",
  "Alpes-Maritimes",
  "Ardèche",
  "Ardennes",
  "Ariège",
  "Aube",
  "Aude",
  "Aveyron",
  "Bouches-du-Rhône",
  "Calvados",
  "Cantal",
  "Charente",
  "Charente-Maritime",
  "Cher",
  "Corrèze",
  "Corse-du-Sud",
  "Haute-Corse",
  "Côte-d'Or",
  "Côtes-d'Armor",
  "Creuse",
  "Dordogne",
  "Doubs",
  "Drôme",
  "Eure",
  "Eure-et-Loir",
  "Finistère",
  "Gard",
  "Haute-Garonne",
  "Gers",
  "Gironde",
  "Hérault",
  "Ille-et-Vilaine",
  "Indre",
  "Indre-et-Loire",
  "Isère",
  "Jura",
  "Landes",
  "Loir-et-Cher",
  "Loire",
  "Haute-Loire",
  "Loire-Atlantique",
  "Loiret",
  "Lot",
  "Lot-et-Garonne",
  "Lozère",
  "Maine-et-Loire",
  "Manche",
  "Marne",
  "Haute-Marne",
  "Mayenne",
  "Meurthe-et-Moselle",
  "Meuse",
  "Morbihan",
  "Moselle",
  "Nièvre",
  "Nord",
  "Oise",
  "Orne",
  "Pas-de-Calais",
  "Puy-de-Dôme",
  "Pyrénées-Atlantiques",
  "Hautes-Pyrénées",
  "Pyrénées-Orientales",
  "Bas-Rhin",
  "Haut-Rhin",
  "Rhône",
  "Haute-Saône",
  "Saône-et-Loire",
  "Sarthe",
  "Savoie",
  "Haute-Savoie",
  "Paris",
  "Seine-Maritime",
  "Seine-et-Marne",
  "Yvelines",
  "Deux-Sèvres",
  "Somme",
  "Tarn",
  "Tarn-et-Garonne",
  "Var",
  "Vaucluse",
  "Vendée",
  "Vienne",
  "Haute-Vienne",
  "Vosges",
  "Yonne",
  "Territoire de Belfort",
  "Essonne",
  "Hauts-de-Seine",
  "Seine-Saint-Denis",
  "Val-de-Marne",
  "Val-d'Oise",
  "Guadeloupe",
  "Martinique",
  "Guyane",
  "La Réunion",
  "Mayotte"
]



class LevraiartisanSpider(scrapy.Spider):
    name = "levraiartisan"
    start_urls = [
    "https://levraiartisan.fr/page-de-recherche/?post%5B0%5D=artisan&tax%5Blocal_business_category%5D%5B0%5D=5&address%5B0%5D={}&distance=250&units=metric&per_page=150&lat=47.921701&lng=0.165580&country&form=1&action=fs"]

    def start_requests(self):
        for department in franceDepartments: 
            yield scrapy.Request(
                url=self.start_urls[0].format(department),
                callback=self.parse,
                meta={'department': department}
            )

    def parse(self, response):
        posts = response.css('article article[id]')
        for post in posts:
            yield {
                'phone_number': post.xpath('.//a[contains(@href, "tel:")]/@href').get().removeprefix('tel:'),
                'email':post.xpath('.//a[contains(@href, "mailto:")]/@href').get().removeprefix('mailto:').split('?')[0],
                'name': remove_tags(post.css('a.group.text-gray-800').get()).strip(),
                'address':remove_tags(post.css('div.text-xs.text-gray-500').get()).strip(),
                'link': post.css('a.group.text-gray-800::attr(href)').get(),
                'department': response.meta['department']
            }