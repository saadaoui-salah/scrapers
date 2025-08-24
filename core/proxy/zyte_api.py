import os
import base64
import json
from scrapy import Request, Selector

class ZyteRequest(Request):
    def __init__(self, url, http_response_body=True, meta={}, *args, **kwargs):
        api_key = os.getenv("ZYTE_API")
        api_key = '2f1f7213b2ec4f98922a854b64b363f8'
        if not api_key:
            raise ValueError("ZYTE_API environment variable not set")

        # Prepare auth header
        auth_str = f"{api_key}:".encode()
        auth_header = base64.b64encode(auth_str).decode()

        # Headers and JSON payload
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {auth_header}",
        }

        payload = {
            "url": url,
            "httpResponseBody": http_response_body,
            "geolocation": "US",
            "httpRequestMethod": kwargs.get("method", "GET"),
        }
        custom_headers = kwargs.pop("headers", None)
        if custom_headers:
            header_list = []
            for k, v in custom_headers.items():
                key = k.decode() if isinstance(k, bytes) else k
                val = v.decode() if isinstance(v, bytes) else v
                header_list.append({"name": key, "value": val})
            payload["customHttpRequestHeaders"] = header_list
        
        if body := kwargs.get('body'):
            if isinstance(body, (bytes, bytearray)):
                body = body.decode("utf-8")
            payload['httpRequestText'] = body 

        super().__init__(
            url="https://api.zyte.com/v1/extract",
            method="POST",
            headers=headers,
            body=json.dumps(payload),
            meta={**meta,'url': url},
            dont_filter=True,
            callback=kwargs.get('callback')  # Avoid duplicate filtering since it's proxied
        )


def load(response):
    response = base64.b64decode(response.json()['httpResponseBody'])
    try:
        response = json.loads(response)
    except Exception:
        response = Selector(text=response)
        
    return response