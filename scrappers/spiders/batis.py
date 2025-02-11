import scrapy

class Service(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    location = scrapy.Field()
    fax = scrapy.Field()
    mobile = scrapy.Field()
    email = scrapy.Field()
    website = scrapy.Field()
    url = scrapy.Field()
    category = scrapy.Field()


class BatisSpider(scrapy.Spider):
    name = "batis"
    allowed_domains = ["batis.dz"]
    start_urls = ["https://batis.dz/entreprise", "https://batis.dz/immobilier", "https://batis.dz/produit"]

    def parse(self, response):
        if 'produit' in response.url: 
            url = 'https://batis.dz/produit?k={}&wilaya=&q='
            categories = response.css('[name="k"] option::attr(value)').getall()
            names = response.css('[name="k"] option::text').getall()
            parent = 'Produits BTPH'
            slug = '/produit'
        elif 'entreprise' in response.url:
            url = 'https://batis.dz/entreprise?k={}&wilaya=&q='
            categories = response.css('[name="k"] option::attr(value)').getall()
            names = response.css('[name="k"] option::text').getall()
            parent = 'Entreprises BTPH'
            slug = '/entreprise'
        else:
            url = 'https://batis.dz/immobilier?k={}&wilaya=&q='
            categories = response.css('[name="wilaya"] option::attr(value)').getall()
            names = response.css('[name="wilaya"] option::text').getall()
            parent = 'Projets immobiliers'
            slug = '/immobilier'


        for category, name in zip(categories, names):
            if category:
                yield scrapy.Request(
                    url=url.format(category),
                    callback=self.parse_results,
                    meta={'category': f"{parent} > {name}", 'slug': slug}
                )

    def parse_results(self, response):
        results = response.css('.fi a[rel="bookmark"]::attr(href)').getall()
        for result in results:
            yield scrapy.Request(
                url=result,
                callback=self.parse_pdp,
                meta=response.meta
            )

        if next_link := response.css('a[rel="next"]::attr(href)').get():
            yield scrapy.Request(
                url=f'https://batis.dz{response.meta["slug"]}{next_link}',
                callback=self.parse_results,
                meta=response.meta
            )

    def parse_pdp(self,response):
        item = Service()
        item['name'] = response.css('.large-12 h1::text').get()
        item['location'] = response.css('.large-12 p::text').getall()[0]
        item['fax'] = response.xpath("//p[contains(text(), 'Fax')]//text()").get()
        item['mobile'] = response.xpath("//p[contains(text(), 'Mob')]//text()").get()
        item['email'] = response.xpath("//p[contains(text(), 'Email')]//text()").get()
        item['website'] = ''.join(response.xpath("//p[contains(text(), 'Site web')]//text()").getall()).strip()
        item['url'] = response.url
        item['category'] = response.meta['category']
        yield item