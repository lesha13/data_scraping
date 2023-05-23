# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Module2Item(scrapy.Item):
    model = scrapy.Field()
    img_url = scrapy.Field()
    config = scrapy.Field()
    price_low = scrapy.Field()
    price_high = scrapy.Field()
