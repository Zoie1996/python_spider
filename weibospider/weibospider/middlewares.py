import random

import requests
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware

from weibospider import settings


class RandomUserAgent(UserAgentMiddleware):
    """
    设置user-Agent方法
    """
    def process_request(self, request, spider):
        user_agent = random.choice(settings.agents)
        request.headers.setdefault(b'User-Agent', user_agent)


class RandomProxy(object):
    """
    设置代理IP
    """
    def process_request(self, request, spider):
        proxy = requests.get('http://10.7.152.151:5555/random').text
        uri = 'https://{proxy}'.format(proxy=proxy)
        request.meta['proxy'] = uri
