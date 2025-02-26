import scrapy
import json
import ast
import os

class LeboncoinSpider(scrapy.Spider):

    name = "leboncoin"
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES':{
            'scrappers.proxy.oxylabs.ProxyMiddleware': 130, 
        }
    }
    api_url = "https://api.leboncoin.fr/finder/search"
    phone_number_url = 'https://api.leboncoin.fr/api/procontact/v1/online_stores_phone'
    categories_url = 'https://api.leboncoin.fr/api/frontend/v1/data/v7/fdata' 
    headers = {
        "accept": "*/*",
        "accept-language": "fr-FR,fr;q=0.9,ar-DZ;q=0.8,ar;q=0.7,en-US;q=0.6,en;q=0.5",
        "api_key": "ba0c2dad52b3ec",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "dnt": "1",
        "origin": "https://www.leboncoin.fr",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://www.leboncoin.fr/",
        "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
    }
    spider_id = 1
    RESULTS_PER_PRAGE = 35

   
    def start_requests(self):
        self.is_shelf = False
        yield scrapy.Request(
            self.categories_url,
            headers=self.headers,
            callback=self.parse_categories,
        ) 


    def parse_categories(self, response):
        categories = response.json()
        def parse_categories_tree(data, path=[]):
            for category in data:
                path_copy = path.copy() + [category['name']]
                if category.get('subcategories'):
                    yield from parse_categories_tree(category['subcategories'], path_copy)
                else:
                    if self.is_shelf:
                        item = CategoryItem()
                        item['path'] = path_copy
                        item['extra'] = {
                            'catID': category['catId']
                        }
                        yield item
                    else:
                        yield scrapy.Request(
                            self.api_url,
                            method='POST',
                            body=self.make_payload(category['catId'], 0),
                            headers=self.headers, callback=self.parse_item,
                            meta={'path': path_copy, 'category_id': category['catId']}
                        )

        yield from parse_categories_tree(categories['categories'])

    def make_payload(self, catId, page, listing='offer', min_price=None, max_price=None, owner=None, sort_by='time', order='desc',location=None, keyword=None, pivot=None, refer=None):
        payload = {
            "filters": {
                "category": {
                    "id": catId
                },
                "enums": {
                    "ad_type": [
                        listing
                    ],
                },
                "ranges": {}
            },
            "limit": self.RESULTS_PER_PRAGE,
            "limit_alu": 3,
            "offset": page*self.RESULTS_PER_PRAGE,
            "sort_by": sort_by,
            "sort_order": order
        }
        if pivot and refer:
            payload['pivot'] = pivot
            payload['referrer_id'] = refer
            payload['listing_source'] = "pagination"

        if keyword:
            payload['filters']['keywords'] = {"text": keyword}
        if min_price and max_price:
            payload['filters']['ranges'] = {
                "price": {
                        "min": min_price,
                        "max": max_price
                    }
            }
        if location:
            payload['filters']['location'] = {
                    "locations": [location]
            }
        if owner:
            payload['filter']['owner_type'] = owner
        return json.dumps(payload)

    def parse_item(self, response):
        data = response.json()
        ads = data.get('ads',[]) + data.get('ads_alu',[])
        for ad in data.get('ads_widget',[]):
            ads += ad['ads']
        for ad in ads:
            location = ad['location']
            item = DataItem()
            item['data'] = {
                'id': ad['list_id'],
                'title': ad['subject'],
                'description': ad['body'],
                'price': ad['price'][0] if ad.get('price') else None,
                'location': location,
                'publication_date': ad['first_publication_date'],
                'category': response.meta['path'], 
                'advertiser_name': ad['owner']['name'],
                'advertiser_email':None,
                'advertiser_phone':None,
                'advertiser_type':ad['owner']['type'],
                'detail_link': ad['url'],
                'reviews': None
            }
            item['path'] = response.meta['path']
            item['site_id'] = ad['list_id']
            feedback_url = f'https://feedback-api-leboncoin.trust.advgo.net/public/users/sdrn:leboncoin:user:{ad["owner"]["user_id"]}/feedback?'
            yield scrapy.Request(
                url=feedback_url,
                callback=self.parse_reviews,
                meta={'item': item, 'store': ad['owner']['store_id'], 'handle_httpstatus_all': True}
            )
        if not data['pivot']:
            return
        pivot_json = ast.literal_eval(data['pivot'])
        results = pivot_json['page_number'] * self.RESULTS_PER_PRAGE
        if results < data['total']:
            offset = (pivot_json['page_number'] + 1) * self.RESULTS_PER_PRAGE
            catId = response.meta['category_id']
            yield scrapy.Request(
                self.api_url,
                method='POST',
                body=self.make_payload(catId, offset, pivot=data['pivot'], refer=data['referrer_id']),
                headers=self.headers,
                callback=self.parse_item,
                meta=response.meta
            )
    
    def parse_reviews(self, response):
        if response.status == 200 and response.json().get('reputation', {}):
            item = response.meta['item']
            item['data']['reviews'] = response.json().get('reputation', {}).get('receivedCount')
            response.meta['item'] = item
        del response.meta['handle_httpstatus_all']
        yield scrapy.Request(
            self.phone_number_url,
            method='POST',
            body=json.dumps({"online_store_id": response.meta['store']}),
            headers=self.headers,
            callback=self.parse_phone_number,
            errback=self.errback,
            meta=response.meta
        )

    def parse_phone_number(self, response):
        item = response.meta['item']
        item['data']['advertiser_phone'] = response.json()['phone']
        yield item

    def errback(self, failure):
        yield failure.request.meta['item']

class DatadomCookieMiddleware:
    def __init__(self):
        # Storage for the datadom cookie
        self.datadom_cookie = None

    def process_response(self, request, response, spider):
        """
        Extract the 'datadom' cookie from the response and store it for future requests.
        """
        # Extract the 'datadom' cookie from the response headers
        cookie_jar = response.headers.getlist('Set-Cookie')
        for cookie in cookie_jar:
            if b'datadome=' in cookie:
                # Extract the cookie value
                self.datadom_cookie = cookie.decode().split(';')[0].split('=')[1]
                spider.logger.info(f"Captured 'datadome' cookie: {self.datadom_cookie}")
                break

        return response

    def process_request(self, request, spider):
        """
        Attach the 'datadom' cookie to the request if it's available.
        """
        if self.datadom_cookie:
            # Add the cookie to the request headers
            request.cookies['datadome'] = self.datadom_cookie
            spider.logger.info(f"Added 'datadome' cookie to request: {self.datadom_cookie}")

        return request


