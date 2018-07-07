# -*- coding: utf-8 -*-
import time
import json
import re

import scrapy
from scrapy import Selector, Request

from qunarspider.items import PlaceItem, StrategyItem, YoujiItem


class QunarSpider(scrapy.Spider):
    name = 'qunar'
    start_urls = ['http://travel.qunar.com/place/']  # 网页版所有目的地
    search_url = 'https://touch.go.qunar.com/search?_json&searchDistId={place_id}&page={page}'  # 攻略接口
    youji_url = 'https://touch.travel.qunar.com/youji/' # 游记

    def parse(self, response):
        """
        通过网页版获取所有目的地的链接, ID和名字
        """
        res = Selector(response)
        # 国内全部目的地
        guolei_listboxs = res.xpath('//*[@id="js_destination_recommend"]/div[2]/div[1]/div[2]/dl')
        # 国际全部目的地
        guoji_listboxs = res.xpath('//*[@id="js_destination_recommend"]/div[2]/div[2]/div[2]/dl')
        # 将国际和国内目的地放入字典循环的到所有地点的id和链接
        listboxall = {'guolei': guolei_listboxs, 'guoji': guoji_listboxs}
        for classify, listboxs in listboxall.items():
            for listbox in listboxs[:2]:
                guonei_lis = listbox.xpath('./dd/div/ul/li')
                guoji_lis = listbox.xpath('./dd/ul/li')
                lis = guonei_lis if classify == 'guolei' else guoji_lis
                for li in lis:
                    # 目的地链接
                    place_href = li.xpath('./a/@href').extract()[0] # 网页链接
                    # 目的地id
                    place_id = re.sub("\D", "", place_href)
                    # 目的地名称
                    place_name = li.xpath('./a/text()').extract()[0]
                    # 保存弟弟是你信息到数据库
                    """
                    place_item = PlaceItem()
                    place_item['id'] = place_id
                    place_item['name'] = place_name
                    place_item['place_href'] = place_href
                    # 目的地分类
                    place_item['classify'] = '国内' if classify == 'guolei' else '国际·港澳台'
                    place_item['crawl_href'] = response.url
                    yield place_item
                    """
                    # 将攻略url放入调度器
                    yield Request(self.search_url.format(place_id=place_id, page=0),
                                  callback=self.pagging,
                                  meta={'place_id':place_id, 'page':0})

    def pagging(self, response):
        """
        实现攻略翻页功能
        """
        place_id = response.meta.get('place_id')
        page = response.meta.get('page') + 1
        yield Request(self.search_url.format(place_id=place_id, page=page),
                      callback=self.parse_strategy)

    def parse_strategy(self, response):
        """
        获取所有攻略
        """
        res = json.loads(response.text)
        booklist = res.get('data').get('bookList')
        field_map = {
            'id': 'id',
            'title': 'title',
            'imageUrl': 'imageUrl',
            'routeDays': 'routeDays',
            'travelRoute': 'travelRoute',
            'destCities': 'destCities',
        }
        if booklist:
            for book in booklist[:1]:
                # 获取的游记开始时间是时间戳格式,并且末尾多3个0
                t = time.localtime(book.get('startTime') / 1000)
                startTime = time.strftime("%Y-%m-%d", t) # 出游开始时间
                id = book.get('id') # 游记文章id
                strategy_item = StrategyItem()
                for item, info in field_map.items():
                    strategy_item[item] = book.get(info)
                    strategy_item['startTime'] = startTime
                # 将游记url放入调度器
                yield Request(self.youji_url + str(id), callback=self.parse_youji, meta={'id': id})
                # 返回攻略页面数据
                yield strategy_item

    def parse_youji(self, response):
        """
        获取游记页面数据, 游记内容
        """
        id = response.meta.get('id') # 游记文章id
        res = Selector(response)

        travel_info = res.xpath('/html/body/div[2]/div[2]/div/div[2]/ul/li')
        # 人物,方式,价格不是每一篇游记上都有, 通过以下方式进行处理
        person, travelMethod, price = None, None, None
        if travel_info:
            for info in travel_info:
                span_class = info.xpath('./span[1]/@class').extract()[0]
                if span_class == 'info-bar-icon':
                    if info.xpath('./span[3]/text()'):
                        person = info.xpath('./span[3]/text()').extract()[0]
                if span_class == 'info-bar-icon info-bar-icon1':
                    if info.xpath('./span[3]/text()'):
                        travelMethod = info.xpath('./span[3]/text()').extract()[0]
                if span_class == 'info-bar-icon info-bar-icon2':
                    if info.xpath('./span[3]/text()'):
                        price = info.xpath('./span[3]/text()').extract()[0]

        youji_item = YoujiItem()
        youji_item['id'] = id # 游记文章id
        youji_item['person'] = person # 同行人物分类
        youji_item['travelMethod'] = travelMethod # 出游方式
        youji_item['price'] = price # 人均价格

        content = res.xpath('/html/body/div[2]/div[2]/div/div[@class="date-content"]').extract()
        youji_note = ''
        for c in content:
            youji_note += c
        youji_item['youji_note'] = youji_note
        youji_item['youji_href'] = response.url
        yield youji_item
