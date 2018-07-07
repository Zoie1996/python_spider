# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class QunarspiderItem(scrapy.Item):
    pass


class PlaceItem(scrapy.Item):
    """
    所有地点 国际/国内
    """
    collections = 'place'
    id = Field()  # 目的地id
    name = Field()  # 目的地名称
    classify = Field()  # 目的地分类 国内/国际
    place_href = Field()  # 地点链接
    crawl_href = Field()  # 爬虫链接


class StrategyItem(scrapy.Item):
    """
    游记内容
    """
    collections = 'travels'
    id = Field()  # 游记id
    title = Field()  # 游记标题
    imageUrl = Field()  # 首页图片
    startTime = Field()  # 旅游开始时间
    routeDays = Field()  # 游玩天数
    travelRoute = Field()  # 行程地点 (1个或多个)
    destCities = Field()  # 途径地点
    create_time = Field()  # 保存数据的时间

    travelMethod = Field()  # 玩法 自驾游/周末游/跟团游等
    person = Field()  # 同行人物 好友/亲人等
    price = Field()  # 人均价格
    youji_note = Field()  # 游记内容
    youji_href = Field()


class YoujiItem(scrapy.Item):
    collections = 'travels'
    id = Field()  # 游记id
    travelMethod = Field() # 玩法 自驾游/周末游/跟团游等
    person = Field() # 同行人物 好友/亲人等
    price = Field() # 人均价格
    youji_note = Field()  # 游记内容
    youji_href = Field()  # 游记内容

