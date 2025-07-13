import scrapy
from core.utils.cleaning import clean
from w3lib.html import remove_tags

class WhichgunSpider(scrapy.Spider):
    name = "whichgun"
    start_urls = ["http://whichgun.com/pistols/limit:500", "http://whichgun.com/pistols/page:2/limit:500"]

    def parse(self, response):
        for product in response.css('.firearm_box'):
            yield {
                'name':product.css('.model_name a::text').get(),
                'name':f"http://whichgun.com{product.css('.model_name a::attr(href)').get()}",
                'MSRP':product.css('.msrp_value::text').get(),
                'image':f"http://whichgun.com{product.css('.firearm_box a img::attr(src)').get()}",
                'CCW Factor':product.css('.ccw_factor[align="right"]::text').get(),
                'Type':clean(remove_tags(product.xpath(".//td[contains(text(), 'Type')]/../td[2]").get(''))),
                'Caliber':clean(remove_tags(product.xpath(".//td[contains(text(), 'Caliber')]/../td[2]").get(''))),
                'Capacity':clean(remove_tags(product.xpath(".//td[contains(text(), 'Capacity')]/../td[2]").get(''))),
                'Weight':clean(remove_tags(product.xpath(".//td[contains(text(), 'Weight')]/../td[2]").get(''))),
                'Length':clean(remove_tags(product.xpath(".//td[contains(text(), 'Length')]/../td[2]").get(''))),
                'Height':clean(remove_tags(product.xpath(".//td[contains(text(), 'Height')]/../td[2]").get(''))),
                'Barrel':clean(remove_tags(product.xpath(".//td[contains(text(), 'Barrel')]/../td[2]").get(''))),
                'Trigger':clean(remove_tags(product.xpath(".//td[contains(text(), 'Trigger')]/../td[2]").get(''))),
                'Views':clean(remove_tags(product.xpath(".//td[contains(text(), 'Views')]/../td[2]").get(''))),
                'Photos':clean(remove_tags(product.xpath(".//td[contains(text(), 'Photos')]/../td[2]").get(''))),
                'ratings':clean(product.css('.statistics_ratings::text').get('')),
            }
