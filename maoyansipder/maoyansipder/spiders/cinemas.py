import json
from datetime import datetime

import scrapy
from scrapy.xlib.pydispatch import dispatcher  # 信号分发器
from scrapy import Request, Selector, signals
from selenium import webdriver

from maoyansipder.items import CinemasItem


class CinemasSpider(scrapy.Spider):
    name = 'cinemas'
    # 城市url
    city_url = 'http://m.maoyan.com/#city-list'
    # 影院url
    cinema_url = 'http://m.maoyan.com/ajax/cinemaList?day={day}&offset=0&limit={pages}&cityId={cityId}'  #

    def __init__(self):  # 初始化
        self.browser = webdriver.Chrome()  # 创建谷歌浏览器对象
        super(CinemasSpider, self).__init__()  # 设置可以获取上一级父类基类的，__init__方法里的对象封装值
        # dispatcher.connect()信号分发器，第一个参数信号触发函数，
        # 第二个参数是触发信号，signals.spider_closed是爬虫结束信号
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        # 运行到此处时，就会去中间件执行，RequestsChrometmiddware中间件了

    def spider_closed(self, spider):  # 信号触发函数
        # print('爬虫结束 停止爬虫')
        self.browser.quit()

    def start_requests(self):
        yield Request(self.city_url, callback=self.parse)

    def parse(self, response):
        """
        获取城市id,
        """
        result = Selector(response)
        city_list = result.xpath('/html/body/div[1]/div/div[1]/div[2]/ul/li')
        day = datetime.now().strftime('%Y-%m-%d')
        for citys in city_list:
            city_div = citys.xpath('./div/a')
            for city in city_div:
                city_id = city.xpath('./@data-ci').extract()[0]
                city_name = city.xpath('./text()').extract()[0]
                yield Request(self.cinema_url.format(day=day, pages=0, cityId=city_id),
                              callback=self.start_crawl,
                              meta={'city_id': city_id, 'city_name': city_name})

    def start_crawl(self, response):
        res = json.loads(response.text)
        # 获取总的url条数, 组装url
        pages = res.get('paging').get('total')
        city_id = response.meta.get('city_id')
        city_name = response.meta.get('city_name')
        day = datetime.now().strftime('%Y-%m-%d')
        yield Request(self.cinema_url.format(day=day, pages=pages, cityId=city_id),
                      callback=self.cinemas_info,
                      meta={'city_id': city_id, 'city_name': city_name})

    def cinemas_info(self, response):
        res = json.loads(response.text)
        city_id = response.meta.get('city_id')
        city_name = response.meta.get('city_name')
        if res.get('cinemas'):
            field_map = {
                'id': 'id',
                'name': 'nm',
                'sellPrice': 'sellPrice',
                'addr': 'addr',
                'distance': 'distance',
            }
            cinemas = res.get('cinemas')
            if cinemas:
                for cinema in cinemas:
                    cinemas_item = CinemasItem()
                    for item, info in field_map.items():
                        cinemas_item[item] = cinema.get(info)
                        cinemas_item['city_id'] = city_id
                        cinemas_item['city_name'] = city_name
                    # yield cinemas_item
