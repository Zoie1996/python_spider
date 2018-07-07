# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime

import pymongo
from scrapy.conf import settings

from qunarspider.items import PlaceItem, StrategyItem, YoujiItem


class CreateTimePipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, StrategyItem):
            item['create_time'] = datetime.now().strftime('%Y-%m-%d %H:%m')
        return item


class QunarspiderPipeline(object):
    def __init__(self):
        self.MONGODB_HOST = settings['MONGODB_SERVER']
        self.MONGODB_PORT = settings['MONGODB_PORT']
        self.MONGODB_DB = settings['MONGODB_DB']
        connection = pymongo.MongoClient(host=self.MONGODB_HOST, port=self.MONGODB_PORT)
        self.db = connection[self.MONGODB_DB]

    def process_item(self, item, spider):
        if isinstance(item, PlaceItem):
            """保存地点"""
            self.db[item.collections].update({'id': item['id']}, {'$set': item}, True)
            return item
        if isinstance(item, StrategyItem):
            """保存攻略首页信息"""
            self.db[item.collections].update({'id': item['id']}, {'$set': item}, True)
            return item
        if isinstance(item, YoujiItem):
            """保存游记详情信息"""
            tmp_item = StrategyItem()
            tmp_item['id'] = item.get('id')
            tmp_item['travelMethod'] = item.get('travelMethod')
            tmp_item['person'] = item.get('person')
            tmp_item['price'] = item.get('price')
            tmp_item['youji_note'] = item.get('youji_note')
            tmp_item['youji_href'] = item.get('youji_href')
            self.db[tmp_item.collections].update({'id': item['id']}, {'$set': tmp_item}, True)
            return item
