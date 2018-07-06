# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

from scrapy.conf import settings


class LianjiaspiderPipeline(object):
    def process_item(self, item, spider):

        return item

class PymongoLianjiaPipeline(object):
    def __init__(self):
        self.MONGODB_HOST = settings['MONGODB_SERVER']
        self.MONGODB_PORT = settings['MONGODB_PORT']
        self.MONGODB_DB = settings['MONGODB_DB']
        connection = pymongo.MongoClient(host=self.MONGODB_HOST, port=self.MONGODB_PORT)
        self.db = connection[self.MONGODB_DB]


    def process_item(self, item, spider):
        self.db[item.collection].update({'id': item['house_code']}, {'$set': item}, True)


