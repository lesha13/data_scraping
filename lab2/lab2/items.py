import scrapy


class News(scrapy.Item):
    date = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
