# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from scrapy.conf import settings
from pymongo import MongoClient

class ZhiyoujiPipelinepro(object):
    def open_spider(self,spider):
        self.f = open('zhiyouji1.json','a')


    def process_item(self, item, spider):
        data_str = json.dumps(dict(item),ensure_ascii=False) + ',\n'
        self.f.write(data_str)
        return item

    def close(self,item):
        self.f.close()


class ZhiyoujiPipeline(object):
    def open_spider(self, spider):
        host = settings['MONGO_HOST']
        port = settings['MONGO_PORT']
        db_name = settings['MONGO_DBNAME']
        col_name = settings['MONGO_COLNAME']
        self.client = MongoClient(host, port)
        self.db = self.client[db_name]
        self.col = self.db[col_name]


    def process_item(self, item, spider):
        data_str = dict(item)
        self.col.insert(data_str)
        return item

    def close_spider(self):
        pass


