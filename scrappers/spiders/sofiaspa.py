import scrapy
import json

class SofiaSpaSpider(scrapy.Spider):
    name = "sofiaspa"
    start_urls = ["https://www.sofiaspa.it/catalogo/?reload=true"]
    headers = {
        "Accept": "*/*",
        "Accept-Language": "fr-FR,fr;q=0.9,ar-DZ;q=0.8,ar;q=0.7,en-US;q=0.6,en;q=0.5",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "DNT": "1",
        "Origin": "https://www.sofiaspa.it",
        "Pragma": "no-cache",
        "Referer": "https://www.sofiaspa.it/catalogo/?reload=true",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Linux",
    }

    def parse(self, response):
        """Extract categories and start parsing them."""
        categories = response.css('#menu-main-menu-mobile-1 .qodef-drop-down-second-inner > ul > li')
        def parse_tree(cats, path=[]):
            for cat in cats:
                category_name = cat.css('a > span::text, label::text').get()
                category_name = category_name.strip() if category_name else "Unknown"
                new_path = path + [category_name] 
                if cat.css('ul'):
                    yield from parse_tree(cat.css('ul > li'), new_path)
                else:
                    category_url = cat.css('button[data-url]::attr(data-url)').get()
                    category_slug = category_url.split("/")[-2]
                    yield response.follow(
                        url=f"https://www.sofiaspa.it/catalogo/?swoof=1&reload=true&paged=1&product_cat={category_slug}",
                        callback=self.parse_category_pages,
                        dont_filter=True,
                        meta={'category': " > ".join(new_path), 'slug': category_slug}
                    )

        yield from parse_tree(categories)

    def parse_category_pages(self, response):
        """Extract pagination and loop through product pages."""
        category_name = response.meta['category']
        category_slug = response.meta['slug']
        last_page = len(response.css('a.page-numbers')) - 1

        for page in range(1, last_page + 1):
            url = f"https://www.sofiaspa.it/wp-admin/admin-ajax.php"
            data = {
                "action": "woof_draw_products",
                "link": f"https://www.sofiaspa.it/catalogo/?swoof=1&reload=true&product_cat={category_slug}&paged={page}",
                "page": str(page),
                "shortcode": f"woof_products is_ajax=1 page={page}",
                "woof_shortcode": "woof sections='product_cat+product_cat^Categorie prodotti,pa_colore+pa_colore^Colore,pa_pietra+pa_pietra^Pietra' sections_type='tabs_checkbox'",
            }

            yield scrapy.FormRequest(
                url=url,
                formdata=data,
                headers=self.headers,
                dont_filter=True,
                callback=self.parse_products,
                meta={'category': category_name}
            )

    def parse_products(self, response):
        """Extract product links from AJAX response."""
        category_name = response.meta['category']

        try:
            data = json.loads(response.text)
            products_html = data.get("products", "")
            product_links = scrapy.Selector(text=products_html).css(
                'a.woocommerce-LoopProduct-link.woocommerce-loop-product__link::attr(href)'
            ).getall()

            for product_url in product_links:
                yield response.follow(
                    product_url,
                    dont_filter=True,
                    callback=self.parse_product_details,
                    meta={'category': category_name}
                )

        except json.JSONDecodeError:
            self.logger.error("Failed to decode JSON response")

    def parse_product_details(self, response):
        """Extract product details."""
        category_name = response.meta['category']

        riferimento = response.css('span.sku.qodef-woo-meta-value::text').get(default="N/A")
        peso = response.css('tr.woocommerce-product-attributes-item--weight td.woocommerce-product-attributes-item__value::text').get(default="N/A")

        yield {
            'Riferimento': riferimento.strip(),
            'Peso': peso.strip(),
            'Category': category_name
        }
