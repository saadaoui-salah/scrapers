import scrapy
from urllib.parse import urlencode


class DmSpider(scrapy.Spider):
    name = "dm"
    PRODUCTS_PER_PAGE = 20
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'fr-FR,fr;q=0.9,ar-DZ;q=0.8,ar;q=0.7,en-US;q=0.6,en;q=0.5',
        'cache-control': 'no-cache',
        'dnt': '1',
        'origin': 'https://www.dm.de',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.dm.de/',
        'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'x-dm-product-search-tags': 'presentation:grid;search-type:editorial;channel:web;editorial-type:brand',
        'x-dm-product-search-token': '47325045207780'
    }
    base_url = 'https://product-search.services.dmtech.com/de/search/static'
    params = [
        #('?query=trend%20it%20up&brandName=trend%20IT%20UP&brandName=trend%20!t%20up&pageSize=432&searchType=editorial-search&sort=editorial_relevance&type=search-static&currentPage=0', 'Trend it up'),
        ('?brandName=alverde%20NATURKOSMETIK&brandName=alverde%20MEN&brandName=alverde%20BABY&pageSize=151&searchType=editorial-search&sort=editorial_relevance&type=search-static&categoryNames=Augen%20Make-up&categoryNames=Lippen%20Make-up&categoryNames=Make-up%20Entferner&categoryNames=Make-up%20Primer&categoryNames=Make-up%20Zubeh%C3%B6r&currentPage=0','Alverde Naturkosmetik'),
        #('?brandName=essence&pageSize=732&searchType=editorial-search&sort=editorial_relevance&type=search-static&currentPage=0','essence'),
        #('?brandName=ebelin&pageSize=638&searchType=editorial-search&sort=editorial_relevance&type=search-static&currentPage=0','ebelin'),
        #('?brandName=catrice&pageSize=632&searchType=editorial-search&sort=new&type=search-static&currentPage=0','catrice'),
        ]

    def start_requests(self):
        for param in self.params:
            #params = {
            #    'brandName': 'Balea',
            #    'pageSize': self.PRODUCTS_PER_PAGE,
            #    'searchType': 'editorial-search',
            #    'sort': 'editorial_relevance',
            #    'type': 'search-static',
            #    'currentPage': 0
            #}
            full_url = f"{self.base_url}{param[0]}"

            yield scrapy.Request(url=full_url, headers=self.headers, callback=self.parse, meta={'page': 0, 'brand':param[1]})

    def parse(self, response):
        data = response.json()
        current_page = response.meta['page']
        products = data['products']
        for i, product in enumerate(products, 1):
            price = float(product['price']['formattedValue'].replace('€','').replace(',','.'))
            net = price/1.19
            try:
                yield {
                    'Position number': current_page * self.PRODUCTS_PER_PAGE + i,
                    'Product name (German)': product['title'],
                    'Product name (English)':'',
                    'Package unit':f"{product['basePriceRelNetQuantity']} {product['basePriceUnit']}" if product.get('basePriceUnit') else None,
                    'Gross price':f"{str(price).replace('.',',')} €",
                    'Net price':f"{str(round(net, 2)).replace('.',',')} €",
                    'Customer price':f"{str(round(net*1.4, 2)).replace('.',',')} €",
                    'Order quantity':0,
                    'Total amount':0,
                    'brand':response.meta['brand'],
                    'Product URL':f"https://www.dm.de{product['relativeProductUrl']}",
                    'Page url':f"https://www.dm.de/marken/balea?currentPage={current_page}&brandName0=Balea&pageSize0=20&sort0=editorial_relevance&currentPage0={current_page}",
                }
            except :
                import pdb;pdb.set_trace()

        #if response.meta['page'] < data['totalPages']:
        #    params = {
        #    'brandName': 'Balea',
        #    'pageSize': self.PRODUCTS_PER_PAGE,
        #    'searchType': 'editorial-search',
        #    'sort': 'editorial_relevance',
        #    'type': 'search-static',
        #    'currentPage': response.meta['page'] + 1
        #    }
        #    full_url = f"{self.base_url}?{urlencode(params)}"
        #    response.meta['page'] += 1 
        #    yield scrapy.Request(url=full_url, headers=self.headers, callback=self.parse, meta=response.meta)
