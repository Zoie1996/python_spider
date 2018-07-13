# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import HtmlResponse


class RequestsChrometmiddware(object):  # 浏览器访问中间件

    def process_request(self, request, spider):  # 重写process_request请求方法
        if spider.name == 'cinemas' and request.url == 'http://m.maoyan.com/#city-list':  # 判断爬虫名称为pach时执行
            spider.browser.get(request.url)  # 用谷歌浏览器访问url
            import time
            time.sleep(3)
            print('访问：{0}'.format(request.url))  # 打印访问网址
            # 设置响应信息，由浏览器响应信息返回
            return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source, encoding='utf-8',
                                request=request)
