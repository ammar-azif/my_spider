# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst

class CraiglistItem(scrapy.Item):
    country = scrapy.Field()
    area = scrapy.Field()
    category = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
