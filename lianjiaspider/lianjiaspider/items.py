# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class LianjiaspiderItem(scrapy.Item):
    collection = 'ershoufang'

    img_src = Field() # 房屋图片
    title = Field() # 标题
    house_code = Field()  # 房屋编号
    address = Field() # 地址
    info = Field() # 房屋信息
    flood = Field() # 楼层
    # tag = Field()
    subway = Field() # 地铁位置
    five = Field() # 房本
    haskey = Field() # 看房时间
    type = Field()  # 新房/二手房
    city = Field()  # 区域
    area = Field()  # 区域
    price = Field() # 价格
    unitPrice = Field() # 单价

