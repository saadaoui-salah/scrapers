import os

class ProxyMiddleware(object):
    # overwrite process request
    def process_request(self, request, spider):
        if hasattr(spider,'proxy'):
            print(os.getenv('OXYLABS_RS'))
            if spider.proxy == 'oxy_rs':
                request.meta['proxy'] = os.getenv('OXYLABS_RS')
            if spider.proxy == 'oxy_dc':
                request.meta['proxy'] = os.getenv('OXYLABS_DC')
            if spider.proxy == 'burp':
                request.meta['proxy'] = 'http://127.0.0.1:8080'