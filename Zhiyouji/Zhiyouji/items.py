# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhiyoujiItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    eval_rand = scrapy.Field()
    wiew_num = scrapy.Field()
    eval_num = scrapy.Field()
    focur_num = scrapy.Field()
    intro = scrapy.Field()
    admire_num = scrapy.Field()
    negative_num = scrapy.Field()
    property = scrapy.Field()
    industry = scrapy.Field()
    full_name = scrapy.Field()
    detail_intro = scrapy.Field()
    pass
