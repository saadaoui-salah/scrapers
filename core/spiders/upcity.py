import scrapy
from selenieum import email


class UpcitySpider(scrapy.Spider):
    name = "upcity"
    start_urls = [
        "https://upcity.com/cybersecurity.json?list_sort_by=review_score&list_sort_order=desc&spotlight_profile=&page={}"
    ]
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "fr-FR,fr;q=0.9,ar-DZ;q=0.8,ar;q=0.7,en-US;q=0.6,en;q=0.5",
        "cache-control": "no-cache",
        "dnt": "1",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
    }

    def start_requests(self):
        for i in range(1,36):
            url = self.start_urls[0].format(i)
            yield scrapy.Request(url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        data = response.json()
        for company in data['profiles']:
            name = company['business_name']
            url = f"https://upcity.com{company['profile_url']}"
            yield scrapy.Request(url, 
            meta={'name':name},
            headers=self.headers, callback=self.parse_details)

    def parse_details(self, response):
        data = response.css('[data-react-class="containers/Profile"]::attr(data-react-props)').get()
        import json 
        data = json.loads(data)
        email = data['profile']['locations'][0]['contact_email']
        print(data['profile']['locations'][0]['contact_email'])
        if email:
            yield {
                'name': response.meta['name'],
                'email':email
            }