import scrapy


class VietnamtourismSpider(scrapy.Spider):
    name = "vietnamtourism"
    
    def start_requests(self):
        url = "https://www.vietnamtourism.org.vn/index.php?mod=agent&act=loadMore"
        headers = {
            "Accept": "*/*",
            "Accept-Language": "fr-FR,fr;q=0.9,ar-DZ;q=0.8,ar;q=0.7,en-US;q=0.6,en;q=0.5",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "DNT": "1",
            "Origin": "https://www.vietnamtourism.org.vn",
            "Pragma": "no-cache",
            "Referer": "https://www.vietnamtourism.org.vn/travel-guide/list-of-travel-agencies-in-vietnam/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Linux"',
        }
        for i in range(24):
            data = {
                "city_id": "",
                "page": str(i),
                "limit": "10"
            }

            yield scrapy.FormRequest(
                url=url,
                method="POST",
                headers=headers,
                formdata=data,
                callback=self.parse_result
            )

    def parse_result(self, response):
        for url in response.css('.title a::attr(href)').getall():
            yield scrapy.Request(
                url=f"https://www.vietnamtourism.org.vn{url}",
                callback=self.parse_details
            )
            
            
    def parse_details(self, response):
        yield {
            'name':response.css('h1.agentID::text').get(),
            'email':response.xpath("//div[@class='agentProfile']//p/strong[contains(text(), 'Email')]/../a/text()").get(),
            'website':response.xpath("//div[@class='agentProfile']//p/strong[contains(text(), 'Website')]/../a/text()").get(),
            'tel':response.xpath("//div[@class='agentProfile']//p/strong[contains(text(), 'Tel')]/../text()").get(),
            'Fax':response.xpath("//div[@class='agentProfile']//p/strong[contains(text(), 'Fax')]/../text()").get(),
        }
