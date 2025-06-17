import os
import random

class ProxyMiddleware(object):
    # overwrite process request
    def process_request(self, request, spider):
        if hasattr(spider,'proxy'):
            if spider.proxy == 'oxy_rs':
                request.meta['proxy'] = os.getenv('OXYLABS_RS')
            if spider.proxy == 'oxy_dc':
                request.meta['proxy'] = os.getenv('OXYLABS_DC')
            if spider.proxy == 'oxy_isp':
                request.meta['proxy'] = os.getenv('OXYLABS_ISP').replace('PORT', random.choice([8001,8002,8003,8004,8005,8006,8007,8008,8009,8010]))
            if spider.proxy == 'burp':
                request.meta['proxy'] = 'http://127.0.0.1:8080'