import os

class ProxyMiddleware(object):
    # overwrite process request
    def process_request(self, request, spider):
        # Set the location of the proxy
        request.meta['proxy'] = 'http://dcscraphub_RDKQ4:Zehzeh0809+=@dc.oxylabs.io:8001'