# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WdjcommentItem(scrapy.Item):
    # define the fields for your item here like:
    appid = scrapy.Field()
    create = scrapy.Field()
    comments = scrapy.Field()
