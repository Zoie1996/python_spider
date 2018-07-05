# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime

import pymongo

from scrapy.conf import settings

from weibospider.items import UserItem, UserRelationItem, WeiboItem


class UserCreateTimePipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, UserItem) or isinstance(item, WeiboItem):
            item['create_time'] = datetime.now().strftime('%Y-%m-%d %H:%m')
        return item


class WeibospiderPipeline(object):

    def process_item(self, item, spider):
        return item


class WeiboPymongoPipeline(object):
    def __init__(self):
        self.MONGODB_HOST = settings['MONGODB_SERVER']
        self.MONGODB_PORT = settings['MONGODB_PORT']
        self.MONGODB_DB = settings['MONGODB_DB']
        connection = pymongo.MongoClient(host=self.MONGODB_HOST,
                                         port=self.MONGODB_PORT)
        self.db = connection[self.MONGODB_DB]

    def process_item(self, item, spider):
        # 保存用户信息和微博信息
        if isinstance(item, UserItem) or isinstance(item, WeiboItem):
            self.db[item.collection].update({'id': item['id']}, {'$set': item}, True)

        # 给微博用户添加粉丝,关注字段
        if isinstance(item, UserRelationItem):
            self.db[item.collection].update({'id': item['id']},
                                   {'$addToSet':
                                       {
                                           'follows': {'$each': item['follows']},
                                           'fans': {'$each': item['fans']}
                                       }

                                   }, True)
        return item

