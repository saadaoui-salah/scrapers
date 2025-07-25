import os
import base64
import json
from scrapy import Request, Selector

class ZyteRequest(Request):
    def __init__(self, url, *args, http_response_body=True, meta={}, **kwargs):
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
        }

        # Override URL, method, body, headers
        super().__init__(
            url="https://api.zyte.com/v1/extract",
            method="POST",
            headers=headers,
            body=json.dumps(payload),
            meta={**meta,'url': url},
            dont_filter=True,  # Avoid duplicate filtering since it's proxied
            *args,
            **kwargs
        )


def load(response):
    response = base64.b64decode(response.json()['httpResponseBody'])
    try:
        response = json.loads(response)
    except Exception:
        response = Selector(text=response)
        
    return response