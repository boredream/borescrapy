# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TTYSItem(scrapy.Item):
    date = scrapy.Field()
    name = scrapy.Field()
    link = scrapy.Field()
    link_page = scrapy.Field()
