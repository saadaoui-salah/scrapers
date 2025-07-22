import os
import base64
import json
from scrapy import Request

class ZyteRequest(Request):
    def __init__(self, url, *args, http_response_body=True, **kwargs):
        api_key = os.getenv("ZYTE_API")
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
            dont_filter=True,  # Avoid duplicate filtering since it's proxied
            *args,
            **kwargs
        )
