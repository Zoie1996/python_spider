# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector


class QidianSpider(scrapy.Spider):
    name = 'qidian'
    allowed_domains = ['qidian.com']
    start_urls = ['http://qidian.com/']

    # 回调函数
    def parse(self, response):
        # 爬取时请求的url
        current_url = response.url

        # 返回的html 页面源码
        body = response.body

        # 返回的html unicode编码
        unicode_body = response.body_as_unicode()
        res = Selector(response)

        # 获取小说的分类信息
        xiaoshuo_type = res.xpath('//*[@id="classify-list"]/dl/dd/a/cite/span/i/text()').extract()

        xiaoshuo_href = res.xpath('//*[@id="classify-list"]/dl/dd/a/@href').extract()
        print(current_url)
        # print(body)
        # print(unicode_body)
        # print(xiaoshuo_type)
        # print(xiaoshuo_href)
