# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class StatisticsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    capacity = scrapy.Field()
    color = scrapy.Field()
    logistics = scrapy.Field()
    datetime = scrapy.Field()
    country = scrapy.Field()

    CAPACITY = 'capacity'
    COLOR = 'color'
    LOGISTICS = 'logistics'
    DATETIME = 'datetime'
    COUNTRY = 'country'
