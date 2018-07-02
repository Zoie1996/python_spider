# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DbspiderItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    avator = scrapy.Field()
    director = scrapy.Field()
    year = scrapy.Field()
    country = scrapy.Field()
    classify = scrapy.Field()
    rate = scrapy.Field()
