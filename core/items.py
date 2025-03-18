# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Product(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    url = scrapy.Field()
    image = scrapy.Field()
    upc = scrapy.Field()
    price = scrapy.Field()
    brand = scrapy.Field()
    description = scrapy.Field()

class Service(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    phone_number = scrapy.Field()
    email = scrapy.Field()
    social_media = scrapy.Field()
    location = scrapy.Field()