# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Card(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    fees = scrapy.Field()
    reward = scrapy.Field()
    lounge = scrapy.Field()
    milestone = scrapy.Field()
    reversal = scrapy.Field()
