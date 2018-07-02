# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector


class WeiboSpider(scrapy.Spider):
    name = 'weibo'
    start_urls = ['https://weibo.com/p/1006051642351362/follow']

    def parse(self, response):
        res = Selector(response)
        name = res.xpath('//*[@id="Pl_Official_HisRelation__60"]/div/div/div/div[2]/div[1]/ul/li/dl/dd[1]/div[1]/a[1]')
        print(name)



