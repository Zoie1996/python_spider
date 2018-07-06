# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy import Selector, Request

from lianjiaspider.items import LianjiaspiderItem


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
            yield Request(response.url + 'pg' + str(page),
                          callback=self.parse_house_info,
                          meta={'area': response.meta.get('area')})


    def parse_house_info(self, response):
        res = Selector(response)
        lis = res.xpath('/html/body/div[4]/div[1]/ul/li[@class="clear"]')
        item = LianjiaspiderItem()
        for li in lis:
            if li.xpath('./a/img/@data-original'):
                item['img_src'] = li.xpath('./a/img/@data-original').extract()[0]
            item['title'] = li.xpath('./div[1]/div[@class="title"]/a/text()').extract()[0]
            item['house_code'] = li.xpath('./div[1]/div[@class="title"]/a/@data-housecode').extract()[0]  # 房屋编号
            item['address'] = li.xpath('./div[1]/div[@class="address"]/div/a/text()').extract()[0]
            infos = li.xpath('./div[1]/div[@class="address"]/div/text()').extract()[0]
            item['info'] = [i.strip() for i in infos.split('|')[1:]]  # ['2室1厅', '54.25平米', '北 东北', '精装', '无电梯']
            addr = li.xpath('./div[1]/div[@class="flood"]/div/a/text()').extract()[0]
            item['flood'] = li.xpath('./div[1]/div[@class="flood"]/div/text()').extract()[0] + addr
            tag = li.xpath('./div[1]/div[@class="tag"]')  # ['距离2号线东门大桥站461米', '房本满五年', '随时看房']
            if tag.xpath('./span[@class="subway"]/text()'):
                item['subway'] = tag.xpath('./span[@class="subway"]/text()').extract()[0]
            else:
                item['subway'] = None
            if tag.xpath('./span[@class="five"]/text()'):
                item['five'] = tag.xpath('./span[@class="five"]/text()').extract()[0]
            else:
                item['five'] = None
            if tag.xpath('./span[@class="haskey"]/text()'):
                item['haskey'] = tag.xpath('./span[@class="haskey"]/text()').extract()[0]
            else:
                item['haskey'] = None
            item['type'] = res.xpath('/html/body/div[1]/div/ul/li[@class="selected"]/a/text()').extract()[0]  # 新房/二手房
            item['city'] = '成都'  # 城市
            item['area'] = response.meta.get('area')  # 区域
            item['price'] = li.xpath('./div[1]/div[@class="priceInfo"]/div[@class="totalPrice"]/span/text()').extract()[0] + '万'  # 总价
            item['unitPrice'] = \
                li.xpath('./div[1]/div[@class="priceInfo"]/div[@class="unitPrice"]/span/text()').extract()[0]  # 单价
            yield item
