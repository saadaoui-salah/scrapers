import scrapy
from w3lib.html import remove_tags
from core.utils.cleaning import clean



class AreeindustrialiSpider(scrapy.Spider):
    name = "areeindustriali"
    allowed_domains = ["areeindustriali.it"]
    start_urls = ["https://www.areeindustriali.it/it-IT/insediamenti-produttivi.aspx?prov=bo"]
    cookies = {
        "CMSCsrfCookie": "XKDHFILyvzuDPB9Q4S0JdS81M0RWiMvNtkbruFjd",
        "ASP.NET_SessionId": "u0p51jmor5slarmfbespdstx",
        ".ASPXFORMSAUTH": "500E62118B0499F39B495B5DE25214181A44D39C00745C0B94409ABDF0E0D19AEFE8C611021A30A8CBCD36DB564A772E6F995F934831495B134595B9F443744EBB545B96916AD62F629669DFB07B334B2C3393C857B5346F18B0892DBC29A9394060C91ADC68708BEE8955FFCF9FE2B22ADD4014"
    }


    def parse(self, response):
        for value in response.css('#p_lt_ctl06_pageplaceholder_p_lt_ctl02_ZoneRicerca_ZoneRicerca_zone_AreeIndustrialiSearchBox_ddlArea option::attr(value)').getall():
            if value:
                yield scrapy.Request(
                    url=f'https://www.areeindustriali.it/it-IT{value}',
                    cookies=self.cookies,
                    callback=self.parse_details
                )

    def parse_details(self, response):
        data = {
            'nome area':response.css('h2.pageSubtitle::text').get(),
            'descrizione informazioni':clean(remove_tags(response.css('.rowAreeIndIntro').get('')))
        }
        for item in response.css('.infoTerritoriali .infoItem'):
            if 'Comuni interessati' in item.get():
                data['Comuni interessati'] = clean(remove_tags(item.get())).replace('Comuni interessati', '').replace(':', '')
            if 'Superficie territoriale ambito' in item.get():
                data['Superficie territoriale ambito (ha)'] = clean(remove_tags(item.get())).replace('Superficie territoriale ambito', '').replace(':', '')
            if 'Superficie territoriale disponibile' in item.get():
                data['Superficie territoriale disponibile (ha)'] = clean(remove_tags(item.get())).replace('Superficie territoriale disponibile', '').replace(':', '')
            if 'Superficie territoriale edificabile' in item.get():
                data['Superficie territoriale edificabile (mq)'] = clean(remove_tags(item.get())).replace('Superficie territoriale edificabile', '').replace(':', '')
            if 'Lotti disponibili (minima superficie)' in item.get():
                data['Lotti disponibili (minima superficie)'] = clean(remove_tags(item.get())).replace('Lotti disponibili (minima superficie)', '').replace(':', '')
            if 'Rete gas disponibile' in item.get():
                data['Rete gas disponibile'] = clean(remove_tags(item.get())).lower().replace('rete gas disponibile', '').replace(':', '')
            if 'Funzioni insediabili' in item.get():
                data['Funzioni insediabili'] = clean(remove_tags(item.get())).replace('Funzioni insediabili', '').replace(':', '')
            if 'Accessibilità viabilistica' in item.get():
                data['Accessibilità viabilistica'] = clean(remove_tags(item.get())).replace('Accessibilità viabilistica', '').replace(':', '')
            if 'Distanza dal casello autostradale' in item.get():
                data['Distanza dal casello autostradale (km)'] = clean(remove_tags(item.get())).replace('Distanza dal casello autostradale', '').replace(':', '')
            if "Distanza dall'aeroporto" in item.get():
                data["Distanza dall'aeroporto (km)"] = clean(remove_tags(item.get())).split(':')[-1]

            if "Distanza dalla stazione ferroviaria" in item.get():
                data["Distanza dalla stazione ferroviaria (km)"] = clean(remove_tags(item.get())).split(':')[-1]
            if "Distanza dall'interporto" in item.get():
                data["Distanza dall'interporto (km)"] = clean(remove_tags(item.get())).split(':')[-1]
            if "Distanza dalla fiera di Bologna" in item.get():
                data["Distanza dalla fiera di Bologna (km)"] = clean(remove_tags(item.get())).split(':')[-1]
            if "Distanza dal centro di Bologna" in item.get():
                data["Distanza dal centro di Bologna (km)"] = clean(remove_tags(item.get())).split(':')[-1]
            
            if "Distanza dal centro di Ferrara" in item.get():
                data["Distanza dal centro di Ferrara (km)"] = clean(remove_tags(item.get())).split(':')[-1]
            if "Distanza dal porto di Ravenna" in item.get():
                data["Distanza dal porto di Ravenna (km)"] = clean(remove_tags(item.get())).split(':')[-1]
        for card in response.css('.boxComparti .mainListItem'):
            data["Comparto"] = card.css('.listaCompartoNome::text').get('').replace('Comparto: ','')
            data["Area (ha)"] = card.css('.area::text').get('').replace('Comparto: ','')
            yield data