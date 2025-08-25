import scrapy
from core.proxy.zyte_api import ZyteRequest, load
from w3lib.html import remove_tags
from core.utils.utils import csv_to_dict

class PokemonSpider(scrapy.Spider):
    name = "pokemon"
    url = "https://www.pokemon.com/fr/jcc-pokemon/cartes-pokemon?cardName=&cardText=&evolvesFrom=&zsv10pt5=on&rsv10pt5=on&sv10=on&sv09=on&sv8pt5=on&sv08=on&sv07=on&sv6pt5=on&sv06=on&sv05=on&sv4pt5=on&sv04=on&sv3pt5=on&sv03=on&sv02=on&sv01=on&svp=on&swsh12pt5gg=on&swsh12pt5=on&swsh12tg=on&swsh12=on&swsh11tg=on&swsh11=on&pgo=on&swsh10tg=on&swsh10=on&swsh9tg=on&swsh9=on&swsh8=on&cel25=on&cel25c=on&swsh7=on&swsh6=on&swsh5=on&swsh45sv=on&swsh45=on&swsh4=on&swsh35=on&swsh3=on&swsh2=on&swsh1=on&swshp=on&sm12=on&sm115=on&sm11=on&sm10=on&det=on&sm9=on&sm8=on&sm75=on&sm7=on&sm6=on&sm5=on&sm4=on&sm35=on&sm3=on&sm2=on&sm1=on&sma=on&smp=on&xy12=on&xy11=on&xy10=on&g1=on&xy9=on&xy8=on&xy7=on&xy6=on&dc1=on&xy5=on&xy4=on&xy3=on&xy2=on&xy1=on&xy0=on&xya=on&xyp=on&bw10=on&bw9=on&bw8=on&bw7=on&dv1=on&bw6=on&bw5=on&bw4=on&bw3=on&bw2=on&bw1=on&bwp=on&col1=on&hgss4=on&hgss3=on&hgss2=on&hgss1=on&hsp=on&pl4=on&pl3=on&pl2=on&pl1=on&dp7=on&dp6=on&dp5=on&dp4=on&dp3=on&dp2=on&dp1=on&ex16=on&ex15=on&ex14=on&ex13=on&ex12=on&ex11=on&ex10=on&ex9=on&ex8=on&ex7=on&ex6=on&ex5=on&ex4=on&ex2=on&ex3=on&ex1=on&hitPointsMin=0&hitPointsMax=340&retreatCostMin=0&retreatCostMax=5&total"
    
    
    def start_requests(self):
        missing = [item['Link'] for item in csv_to_dict('./client-data/pokemon.csv') if not item['Number']]
        #for i in range(1232):
        #    yield ZyteRequest(
        #        url=f"{self.url}&page={i+1}",
        #        callback=self.parse_details,
        #    )
        for card in missing:
            yield ZyteRequest(
                url=card,
                callback=self.parse_details,
            )


    def parse(self, response):
        response = load(response)
        cards = response.css('#cardResults li a::attr(href)').getall()
        for card in cards:
            yield ZyteRequest(
                url=f"https://www.pokemon.com{card}",
                callback=self.parse_details,
            )
        
    def parse_details(self, response):
        meta = response.meta
        response = load(response)    
        yield {
            'Number':response.css('.stats-footer span::text').get('').split(' ')[0],
            'Label':remove_tags(response.css('.card-description h1').get('')),
            'Bloc':'',
            'Expansion':response.css('.stats-footer a::text').get(),
            'Pokemon':response.css('#pokedex-find span::text').get('').replace('Chercher ', '').replace(' dans le Pokédex', '').strip(),
            'Rarity':response.css('.stats-footer span::text').get('').split(' ')[-1],
            'Card Type':response.css('.card-type h2::text').get(),
            'Pokemon Type':response.css('.card-basic-info .right i::attr(title)').get(),
            'Link': meta['url']
        }