import scrapy
import json
from core.utils.utils import generate_cookies
import asyncio
from twisted.internet.defer import ensureDeferred

loop = asyncio.get_event_loop()
class HealthengineSpider(scrapy.Spider):
    custom_settings = {
        'RETRY_HTTP_CODES': [202],
    }
    name = "healthengine"
    headers = {
        "dnt": "1",
        "priority": "u=0, i",
        "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
    }

    def start_requests(self):
        for i in range(468):
            yield scrapy.Request(
                url=f"https://healthengine.com.au/search?page={i+1}&onlineAppts=true",
                callback=self.parse
            )

    def parse(self, response):
        data = response.css('#__NEXT_DATA__::text').get()
        data = json.loads(data)['props']['ssrData']['PRELOAD_CACHE']['HANNIBAL_CACHE']
        keys = data.keys()

        for key in keys:
            if not 'practice:' in key.lower():
                continue
            item = data[key]
            if not item['phoneNumber']:
                continue
            if not item['phoneNumber'].strip():
                continue
            lead = {}
            lead['phone'] = item['phoneNumber'] 
            lead['name'] = item['name']
            yield lead