# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Product(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    url = scrapy.Field()
    image = scrapy.Field()
    ean = scrapy.Field()
    now_price = scrapy.Field()
    was_price = scrapy.Field()
    price_drop = scrapy.Field()
    promotion = scrapy.Field()

class Service(scrapy.Item):
    # define the fields for your item here like:
    business_name = scrapy.Field()
    abn = scrapy.Field()
    license_number = scrapy.Field()
    trade_type = scrapy.Field()
    description = scrapy.Field()
    phone_number = scrapy.Field()
    email = scrapy.Field()
    social_media = scrapy.Field()
    category = scrapy.Field()
    location = scrapy.Field()
    contact_information = scrapy.Field()
    reviews = scrapy.Field()
    rating_avg = scrapy.Field()
    primary_services = scrapy.Field()
    specializations = scrapy.Field()
    service_area = scrapy.Field()
    awards = scrapy.Field()
    response_time = scrapy.Field()
    availability = scrapy.Field()
    equipment_provided = scrapy.Field()
    experience = scrapy.Field()
    insurance_coverage = scrapy.Field()
    website = scrapy.Field()