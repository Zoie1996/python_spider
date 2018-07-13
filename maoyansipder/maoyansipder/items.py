# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class MaoyansipderItem(scrapy.Item):
    pass


class MovieItem(scrapy.Item):
    collections = 'movie'
    id = Field()  # 电影ID
    describe = Field()  # 电影描述
    img = Field() # 宣传图片
    version = Field()  # 版本 3D IMAX 等
    name = Field()  # 电影名称
    cinemaScore = Field()  # 电影评分
    wish = Field()  # 想看数量
    star = Field()  # 参演明星
    dur = Field() # 时长
    releaseTime = Field()  # 上映时间
    globalReleased = Field() # 是否发布 True代表已发布可购买 False代表预售


class CinemasItem(scrapy.Item):
    collections = 'cinemas'
    id = Field()  # 影院id
    name = Field()  # 影院名字
    sellPrice = Field()  # 起价
    addr = Field()  # 地址
    distance = Field()  # 距离
    # tag = Field() # 标签 小吃/折扣卡
    # promotion = Field() # 促销 开卡特惠...
    city_id = Field()  # 城市id
    city_name = Field()  # 影院所在城市名称


