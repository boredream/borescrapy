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


class XueItem(scrapy.Item):
    # 名称
    name = scrapy.Field()

    # 所属经络
    jingLuo = scrapy.Field()

    # 所属经络方向（从胸到手，从足到腹等）
    jingLuoIndexDirection = scrapy.Field()

    # 所属经络方向上的顺序索引，从0开始
    jingLuoIndex = scrapy.Field()

    # 功能类型（清肺热、解表等）
    functionType = scrapy.Field()

    # 所属身体部位（头、面、胸、足等）
    bodyArea = scrapy.Field()

    # 五输穴类型（井、荥、输、经、合），非五腧穴为空
    wuShuType = scrapy.Field()

    # 五输穴五行属性（注意阴阳经不同）
    wuShuWuXing = scrapy.Field()

