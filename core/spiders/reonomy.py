import scrapy
from core.utils.utils import read_json_files,  fake_request
from datetime import datetime
from core.proxy.zyte_api import ZyteRequest, load
import json
AUTH_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJUWkdOamN3TlVVMFJFTTJORGt6UlRNd1JVSTVSVGs1TlVZeE56UkRNVUUzUlVNd09UTkVOdyJ9.eyJpc3MiOiJodHRwczovL2F1dGgucmVvbm9teS5jb20vIiwic3ViIjoiYXV0aDB8NzZkNWJlMjAtYzk4Ni00YWY0LTg1ZGEtYmIyMjM2MmQzYmY0IiwiYXVkIjpbImh0dHBzOi8vYXBwLnJlb25vbXkuY29tL3YyLyIsImh0dHBzOi8vcmVvbm9teS1wcmQuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTc1NTk3ODcwOCwiZXhwIjoxNzU2MDY1MTA4LCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwiYXpwIjoiVVRxaklaZjVqcUUwUm9SQ0pQRDIxNmFUOUNXWnJxMkMifQ.Vr8GazuW10goXa5DiORTJirLrmV4dLBWaZSpVB4mw2Yi3KsDQhuQC_glU3udtTxj9DTUoDhlANJEnVd8AAulupHNvYEZjarAoLCyimINTtgpR_rt_TFLSiCNoFBjAK39Y6enmcr3xy_YGy1nzuyjh2c0yaUO0Rk4CwiS1Z_kuYJPy7uqKfCVqfxJCCkNPpL9c-LPx_NxIEQkqjRhJ-PbRYLRHAK22X_f2UceBXkXIcCp9NTIrqB6eD9uZuIMzmeFIjDnMPznhFv01oL8YHxu3jet1iPEIb6IAq6lTCagsCgFcSMbO4MKOOFXPq0LH6VmNT0BHnYKtUo-Eaoh_vUq8A'

class ReonomySpider(scrapy.Spider):
    name = "reonomy"
    proxy = 'burp'    
    headers = {
        "accept": "*/*",
        "accept-language": "fr-FR,fr;q=0.9,ar-DZ;q=0.8,ar;q=0.7,en-US;q=0.6,en;q=0.5",
        "authorization": f"Bearer {AUTH_TOKEN}",
        "cache-control": "no-cache",
        "content-type": "application/json",
    }
    
    def start_requests(self):
        url = "https://api.reonomy.com/v2/search/pins?offset=0&limit=10000"
        body = {
            "settings": {
                "land_use_code": ["136", "1109"],
                "locations": [
                    {"kind": "state", "state": "NY", "text": "New York"},
                    {"kind": "state", "state": "NJ", "text": "New Jersey"},
                    {"kind": "state", "state": "OH", "text": "Ohio"},
                    {"kind": "state", "state": "WV", "text": "West Virginia"},
                    {"kind": "state", "state": "DE", "text": "Delaware"},
                    {"kind": "state", "state": "CT", "text": "Connecticut"},
                    {"kind": "state", "state": "MD", "text": "Maryland"},
                    {"kind": "state", "state": "VA", "text": "Virginia"},
                    {"kind": "state", "state": "MI", "text": "Michigan"},
                    {"kind": "state", "state": "KY", "text": "Kentucky"}
                ],
                "sort": [{"name": "year_renovated", "order": "desc"}]
            },
            "aggregations": [{"name": "geo_bounds"}]
        }
        yield ZyteRequest(
            url=url,
            method="POST",
            headers=self.headers,
            body=json.dumps(body),
            callback=self.parse_search
        )
        url = "https://api.reonomy.com/v2/search/pins?offset=10000&limit=10000"
        yield ZyteRequest(
            url=url,
            method="POST",
            headers=self.headers,
            body=json.dumps(body),
            callback=self.parse_search
        )

    def parse_search(self, response):
        data = load(response)
        ids = [item["id"] for item in data.get("items", [])]
        self.logger.info(f"Got {len(ids)} IDs")

        for i in range(0, len(ids), 50):
            batch = ids[i:i+50]
            yield ZyteRequest(
                url="https://api.reonomy.com/v2/property/summaries",
                method="POST",
                headers=self.headers,
                body=json.dumps({"property_ids": batch}),
                callback=self.parse_details,
            )
    
    def format_date(self, date):
        dt = datetime.strptime(date, "%Y-%m-%d")
        return dt.strftime("%b %d, %Y")

    def parse_details(self, response):
        response = load(response)

        for item in response:
            in_preforeclosure = item['in_preforeclosure']  if isinstance(item.get('in_preforeclosure'), bool) else  '-'
            in_preforeclosure = 'Yes' if in_preforeclosure else 'No'
            data = {
                'Address': f"{item.get('house_nbr','')} {item.get('street')} {item.get('mode','').title()}, {item.get('city','').title()}, {item.get('state')} {item.get('zip5')}",
                'APN': item['formatted_apn'],
                'County':item['fips_county'],
                'Lot Size (Acreage)':round(item['lot_size_acres'], 2) if item.get('lot_size_acres') else '--',
                'Last Sale': self.format_date(item['sales_date'])  if item.get('sales_date') else  '--',
                'Zoning': item['zoning']  if item.get('zoning') else  '--',
                'Year Built': item['year_built']  if item.get('year_built') else  '--',
                'Sale Price': f"${item['sales_price']}"  if item.get('sales_price') else  '--',
                'Last Mortgage': self.format_date(item['mortgage_recording_date'])  if item.get('mortgage_recording_date') else  '--',
                'Mortgage Amount': f"${item['mortgage_amount']}"  if item.get('mortgage_amount') else  '--',
                'In Preforeclosure': in_preforeclosure,
                'On CMBS Watchlist': item['on_watchlist']  if item.get('on_watchlist') else  '--',
                'Building Area': f"{round(item['building_area'])} SF"  if item.get('building_area') else  '--',
                'Recorded Lender': item['mortgage_recorded_name']  if item.get('mortgage_recorded_name') else  '--',
                'Standardized Lender': item['mortgage_standardized_name']  if item.get('mortgage_standardized_name') else  '--',
                'Seller': item['seller_name']  if item.get('seller_name') else  '--',
                'Tax Amount': f"${round(item['tax_amount'])}"  if item.get('tax_amount') else  '--',
                'Total Assessed Value': f"${round(item['total_assessed_value'])}"  if item.get('total_assessed_value') else  '--',
                'Units': item['total_units']  if item.get('total_units') else  '--',
                'Property Type': f"{item['asset_category']} | {item['std_land_use_code_description']}"  if item.get('asset_category') else  '--',
                'Reported Owner': ', '.join([owner['name'] for owner in item['reported_owners']])  if item.get('reported_owners') else  '--',
                'Sale Price/Acre': f"${round(item['price_per_acre_lot_area'])}"  if item.get('price_per_acre_lot_area') else  '--',
                'Reported Owner Address': item['reported_owner_address']  if item.get('reported_owner_address') else  '--',
                'Link': f"https://app.reonomy.com/!/search/467ce1b7-0ab8-4b3e-9c43-2c678011b56d/property/{item['id']}/ownership"
            }


            url = f"https://api.reonomy.com/v3/property-contacts/{item['id']}"
     

            yield ZyteRequest(
                url=url,
                method="GET",
                headers=self.headers,
                callback=self.parse_contacts_ids,
                meta={'data':data}
            )


    def fetch_owners(self, owners, extra, meta):
        batch_size = 50
        headers = {
            "accept": "*/*",
            "accept-language": "fr-FR,fr;q=0.9,ar-DZ;q=0.8,ar;q=0.7,en-US;q=0.6,en;q=0.5",
            "authorization": f"Bearer {AUTH_TOKEN}",
            "cache-control": "no-cache",
            "content-type": "application/json",
            "dnt": "1",
            "origin": "https://app.reonomy.com",
            "pragma": "no-cache",
            "referer": "https://app.reonomy.com/",
            "sec-ch-ua": "\"Google Chrome\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Linux\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
        }
        if owners:
            for i in range(0, len(owners), batch_size):
                batch = owners[i:i + batch_size]
                body = json.dumps({"ids": batch})

                yield ZyteRequest(
                    url="https://api.reonomy.com/v3/people/bulk",
                    method="POST",
                    headers=self.headers,
                    body=body,
                    callback=self.parse_contacts,
                    meta={
                        "extra": extra,
                        "data":meta['data']
                    }
                )
        else:
            for i in range(0, len(extra), batch_size):
                batch = extra[i:i + batch_size]
                body = json.dumps({"ids": batch})

                yield ZyteRequest(
                    url="https://api.reonomy.com/v3/people/bulk",
                    method="POST",
                    headers=self.headers,
                    body=body,
                    callback=self.parse_contacts,
                    meta=meta
                )


    def parse_contacts_ids(self, response):
        meta = response.meta
        data = load(response)
        owners_ids = [] 
        extra = []
        if "owners" in data and isinstance(data["owners"], list):
            owners_ids = [o["id"] for o in data["owners"]]

        if "contacts" in data and isinstance(data["contacts"], list):
            extra = [c["id"] for c in data["contacts"]]
        
        yield from self.fetch_owners(owners_ids, extra, meta)
        
        
    def parse_contacts(self, response):
        meta = response.meta
        data = meta['data']
        response = load(response)
        if extra := meta.get('extra'):
            for i in range(4):
                data[f'Owner {i} Name'] = '--'
                data[f'Owner {i} Emails'] = '--'
                data[f'Owner {i} Phone Numbers'] = '--'
                data[f'Owner {i} Addresses'] = '--'
            if response['count'] > 4:
                print('>>>>>>>>>>>>>>>>>>>>>', response['count'])
            for contact in response['items']:
                try:
                    data[f'Owner {i} Name'] = contact['name']['full']
                    data[f'Owner {i} Emails'] = ', '.join([info['address'] for info in contact['emails']])
                    data[f'Owner {i} Phone Numbers'] = ', '.join([info['number'] for info in contact['phones']])
                    data[f'Owner {i} Addresses'] = '| '.join([f"{info['line1']}, {info['city'].title()}, {info['state']} {info['postal_code']}" for info in contact['addresses']])
                except IndexError:
                    data[f'Owner {i} Name'] = '--'
                    data[f'Owner {i} Emails'] = '--'
                    data[f'Owner {i} Phone Numbers'] = '--'
                    data[f'Owner {i} Addresses'] = '--'
            yield from self.fetch_owners([], extra, {'data':data})
        else:
            for i in range(50):
                data[f'Additional Contacts {i} Name'] = '--'
                data[f'Additional Contacts {i} Emails'] = '--'
                data[f'Additional Contacts {i} Phone Numbers'] = '--'
                data[f'Additional Contacts {i} Addresses'] = '--'
            for contact in response['items']:
                try:
                    data[f'Additional Contacts {i} Name'] = contact['name']['full']
                    data[f'Additional Contacts {i} Emails'] = ', '.join([info['address'] for info in contact['emails']])
                    data[f'Additional Contacts {i} Phone Numbers'] = ', '.join([info['number'] for info in contact['phones']])
                    data[f'Additional Contacts {i} Addresses'] = '| '.join([f"{info['line1']}, {info['city'].title()}, {info['state']} {info['postal_code']}" for info in contact['addresses']])
                except IndexError:
                    data[f'Additional Contacts {i} Name'] = '--'
                    data[f'Additional Contacts {i} Emails'] = '--'
                    data[f'Additional Contacts {i} Phone Numbers'] = '--'
                    data[f'Additional Contacts {i} Addresses'] = '--'
            yield data
