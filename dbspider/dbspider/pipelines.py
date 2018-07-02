# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

from scrapy.conf import settings


class DbspiderPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        for i in range(len(item['name'])):
            data = {}
            data['name'] = item['name'][i]
            data['avator'] = item['avator'][i]
            data['director'] = item['director'][i]
            data['year'] = item['year'][i]
            data['country'] = item['country'][i]
            data['classify'] = item['classify'][i]
            data['rate'] = item['rate'][i]
            self.collection.insert(data)
            print(data)
        return item
