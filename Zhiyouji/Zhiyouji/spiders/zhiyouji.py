# -*- coding: utf-8 -*-
import scrapy


class ZhiyoujiSpider(scrapy.Spider):
    name = 'zhiyouji'
    allowed_domains = ['zhiyouji.com']
    start_urls = ['http://zhiyouji.com/']

    def parse(self, response):
        pass
