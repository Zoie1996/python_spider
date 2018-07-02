# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from scrapy.http import Request

from dbspider.items import DbspiderItem


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    start_urls = ['https://movie.douban.com/top250']
    url = 'https://movie.douban.com/top250'

    def parse(self, response):
        res = Selector(response)
        items = DbspiderItem()
        # 电影名称
        items['name'] = res.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[1]/a/span[1]/text()').extract()

        # 电影的图片
        items['avator'] = res.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[1]/a/img/@src').extract()

        # 电影导演
        director_info = res.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[2]/p[1]/text()[1]').extract()
        items['director'] = [info.strip().replace('\xa0', '') for info in director_info]
        # 年份 / 国家 / 分类
        movie_info = res.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[2]/p[1]/text()[2]').extract()
        movie_info = [info.strip().replace('\xa0', '') for info in movie_info]

        items['year'], items['country'], items['classify'] = [], [], []
        for info in movie_info:
            temp = info.split('/')
            items['year'].append(temp[0])
            items['country'].append(temp[1])
            items['classify'].append(temp[2])

        # 电影评分
        items['rate'] = res.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[2]/div/span[2]/text()').extract()
        yield items

        nextlink = res.xpath('//*[@id="content"]/div/div[1]/div[2]/span[3]/a/@href').extract()
        nextlink = self.url + nextlink[0]
        if nextlink:
            yield Request(nextlink, callback=self.parse)


