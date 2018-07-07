# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy import Selector, Request

from lianjiaspider.items import RedislianjiaItem


class LianjiaSpider(scrapy.Spider):
    name = 'lianjia'
    domains_url = 'https://cd.lianjia.com'
    start_urls = ['https://cd.lianjia.com/ershoufang/']

    def parse(self, response):
        res = Selector(response)
        ershoufang_area = res.xpath('//div[@data-role="ershoufang"]/div/a')
        for area in ershoufang_area:
            area_href = area.xpath('./@href').extract()[0]
            area_name = area.xpath('./text()').extract()[0]
            yield Request(self.domains_url + area_href,
                          callback=self.paging,
                          meta={'area': area_name})

    def paging(self, response):
        res = Selector(response)
        page = res.xpath('/html/body/div[4]/div[1]/div[8]/div[2]/div/@page-data').extract()[0]
        totalPage = json.loads(page).get('totalPage')
        for page in range(1, totalPage + 1):
            item = RedislianjiaItem()
            item['url'] = response.url + 'pg' + str(page)
            yield item
