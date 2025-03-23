import scrapy
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder

class BathroomsalesdirectSpider(scrapy.Spider):
    name = "bathroomsalesdirect"
    start_urls = ["https://www.bathroomsalesdirect.com.au/wp-json/menus/v1/mega-menu/?menu_id=shop-products"]

    api_url = "https://www.bathroomsalesdirect.com.au/wp-admin/admin-ajax.php"
    headers = {
        "Accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "fr-FR,fr;q=0.9,ar-DZ;q=0.8,ar;q=0.7,en-US;q=0.6,en;q=0.5",
        "cache-control": "no-cache",
        "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryDBgPRLF0SxKBJmyJ",
        "Origin": "https://www.bathroomsalesdirect.com.au",
        "Referer": "https://www.bathroomsalesdirect.com.au/product-category/bathroom-accessories/",
        "dnt": "1",
        "origin": "https://www.bathroomsalesdirect.com.au",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://www.bathroomsalesdirect.com.au/product-category/federation-frenzy/",
        "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    }
    
    def start_requests(self):
        yield scrapy.Request(
            url="https://www.bathroomsalesdirect.com.au/wp-json/menus/v1/mega-menu/?menu_id=shop-products",
            headers={'content-type':'application/json'},
            callback=self.parse
        )


    def parse(self, response):
        data = response.json()['menu']
        sel = scrapy.Selector(text=data)
        links = sel.css('#menu-mega-menu a::attr(href)').getall()
        for link in links:
            if 'product-category' not in link:
                continue
            slugs = link.split('/')
            category = [slugs[-2] if link.endswith('/') else slugs[-1]]
            payload = MultipartEncoder(
            fields={
                "action": "shop_filters",
                "payload": json.dumps({
                    "page": 1,
                    "per_page": 12,
                    "filters": {"product_cat": category},
                    "orderby": "popularity",
                    "order": "desc",
                    "paginate": "more"
                }),
                "refresh_attributes": "true"
                }
            )

            yield scrapy.Request(
                self.api_url,
                method="POST",
                body=payload.to_string(),  # Convert to raw multipart data
                headers={
                    "Content-Type": payload.content_type,  # Set proper content type
                    "User-Agent": "Mozilla/5.0"
                },
                callback=self.parse_products,
                meta={'page':1, 'category': category}
            )


    def parse_products(self, response):
        sel = scrapy.Selector(text=response.json()['data']['products'])
        for product in sel.css('.product .border-gray-subtle >  a::attr(href)').getall():
            yield scrapy.Request(url=product, callback=self.parse_pdp)
        if response.json()['data']['header']['x-wp-totalpages'] < response.meta['page']:
            category = response.meta['category']
            page = response.meta['page'] + 1
            payload = MultipartEncoder(
            fields={
                "action": "shop_filters",
                "payload": json.dumps({
                    "page": page,
                    "per_page": 12,
                    "filters": {"product_cat": category},
                    "orderby": "popularity",
                    "order": "desc",
                    "paginate": "more"
                }),
                "refresh_attributes": "true"
                }
            )
            yield scrapy.Request(
                self.api_url,
                method="POST",
                body=payload.to_string(),  # Convert to raw multipart data
                headers={
                    "Content-Type": payload.content_type,  # Set proper content type
                    "User-Agent": "Mozilla/5.0"
                },
                callback=self.parse_products,
                meta={'page':page, 'category': category}
            )
    
    def parse_pdp(self, response):
        yield {
            'sku':response.xpath("//div[contains(@class, 'sku')]//span[2]/text()").get(),
            'title':response.css(".fs-xl-2.ff-secondary::text").get(),
            'RRP': ' - '.join(response.css('.pewc-main-price .small-dollar bdi::text').getall()),
            'price': response.css('.pewc-main-price .text-decoration-line-through bdi::text').get(),
            'brand':response.xpath("//div[@id='product-info']//div[contains(@class,'row')]"\
                "//div[contains(text(), 'Brand')]/../../following-sibling::*[1]/div/text()").get('').replace('\n','').strip(),
            'colour':response.xpath("//div[@id='product-info']//div[contains(@class,'row')]"\
                "//div[contains(text(), 'Colour')]/../../following-sibling::*[1]/div/text()").get('').replace('\n','').strip(),
        }
