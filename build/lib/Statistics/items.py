# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class StatisticsItem(scrapy.Item):
    # define the fields for your item here like:
    # # name = scrapy.Field()
    # capacity = scrapy.Field()
    # color = scrapy.Field()
    # logistics = scrapy.Field()
    infos = scrapy.Field()
    datetime = scrapy.Field()
    country = scrapy.Field()
    image_urls = scrapy.Field()  # 图片
    product_id = scrapy.Field()

    # CAPACITY = 'capacity'
    # COLOR = 'color'
    # LOGISTICS = 'logistics'
    INFOS = 'infos'
    DATETIME = 'datetime'
    COUNTRY = 'country'
    IMAGE_URLS = 'image_urls'
    PRODUCT_ID = 'product_id'
