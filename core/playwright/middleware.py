import os

class PlaywrightMiddleware(object):
    # overwrite process request
    def process_request(self, request, spider):
        request.meta['playwright'] = request.meta.get('playwright', True)