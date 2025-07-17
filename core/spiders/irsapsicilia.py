import scrapy
import mapbox_vector_tile


class IrsapsiciliaSpider(scrapy.Spider):
    name = "irsapsicilia"
    start = ["https://irsit.irsapsicilia.it/api/lotto/agglomerati"]
    url = 'https://irsit.irsapsicilia.it/api/map/mvt/{}/9/{}/{}.pbf'
    filters = ['lotti-edificati', 'terreni-propieta-consorzio-asi', 'terreni-propieta-privata', 'terreni-privati-zona-non-attuata',  'terreni-da-verificare', 'terreni-assegnati', 'terreni-altri-enti-pubblici', 'terreni-con-impiato-fotovoltaici']
    agglomerati = [
        "MILAZZO-GIAMMORO",
        "VILLAFRANCA TIRRENA",
        "TORREGROTTA-VALDINA-VENETICO",
        "BARCELLONA POZZO DI GOTTO",
        "MESSINA-LARDERIA",
        "PALERMO",
        "TERMINI IMERESE",
        "CATANIA",
        "BELPASSO",
        "PATERNO"
    ]
    codes = []
    
    def start_requests(self):
        for x in range(274,279):
            for y in range(196, 201):
                for f in self.filters:
                    yield scrapy.Request(
                        url=self.url.format(f, x, y),
                        callback=self.parse
                    )

    def parse(self, response):
        decoded = mapbox_vector_tile.decode(response.body)
        for layer_name, layer_data in decoded.items():
            for feature in layer_data['features']:
                feature = feature["properties"]
                data = {
                    "citta": feature.get("citta"),
                    "codice": feature.get("codice"),
                    "nome": feature.get("denominaz"),
                    "tipo lotto": ' '.join(feature.get("layer_type").split('-')).title(),
                    "area m2": feature.get("area"),
                    "numero": feature.get("numero"),
                    "Agglomerato": feature.get("agglom"),
                    "zona": feature.get("zona"),
                    "valore dell'area": feature.get("valore_cessione") if feature.get("valore_cessione") > 0 else None,
                    "valore m2": feature.get("prezzo_mq") if feature.get("prezzo_mq") > 0 else None,
                    "Dati catastali": feature.get("intestaz_"),
                }
                if feature.get("agglom") in self.agglomerati and feature.get("codice") not in self.codes:
                    self.codes += [data]
                    yield data