# -*- coding: utf-8 -*-
import json

import scrapy

from weibospider.items import UserItem, UserRelationItem, WeiboItem
from scrapy import Request


class WeiboSpider(scrapy.Spider):
    name = 'weibo'
    # 用户url
    user_url = 'https://m.weibo.cn/api/container/getIndex?uid={uid}&type=uid&value={uid}&containerid=100505{uid}'
    # 关注url
    follow_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_{uid}&page={page}'
    # 粉丝url
    fans_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_{uid}&page={page}'
    # 微博url
    weibo_url = 'https://m.weibo.cn/api/container/getIndex?uid={uid}&type=uid&value={uid}&containerid=107603{uid}&page={page}'

    # 开始爬取的用户id
    # start_user_uids = ['1642351362', '5796662600', '1192329374']
    start_user_uids = ['1642351362']

    def start_requests(self):
        for uid in self.start_user_uids:
            yield Request(self.user_url.format(uid=uid), callback=self.parse)

    def parse(self, response):
        res = json.loads(response.text)
        # 获取用户信息
        user_info = res.get('data').get('userInfo')
        # 将json字段与数据库字段一一对应
        field_map = {
            'id': 'id', 'name': 'screen_name', 'avatar': 'profile_image_url','cover': 'cover_image_phone',
            'gender': 'gender', 'description':'description', 'fans_count': 'followers_count',
            'follows_count': 'follow_count','weibos_count': 'statuses_count', 'verified': 'verified',
            'verified_reason': 'verified_reason', 'verified_type': 'verified_type'
        }
        user_item = UserItem()
        for item, info in field_map.items():
            user_item[item] = user_info.get(info)
        yield user_item

        # 博主id
        uid = user_info.get('id')
        # 关注
        yield Request(self.follow_url.format(uid=uid, page=1), callback=self.parse_follow,
                      meta={'uid': uid, 'page': 1})
        # 粉丝
        yield Request(self.fans_url.format(uid=uid, page=1), callback=self.parse_fans,
                      meta={'uid': uid, 'page': 1})
        # 微博
        yield Request(self.weibo_url.format(uid=uid, page=1), callback=self.parse_weibo,
                      meta={'uid': uid, 'page': 1})

    def parse_follow(self, response):
        """
        获取关注的用户的的信息
        """
        # 获取页面信息
        res = json.loads(response.text)
        if res['ok']:
            follows = res.get('data').get('cards')[-1].get('card_group')
            for follow in follows:
                # 循环得到所有关注的人的id
                uid = follow.get('user').get('id')
                yield Request(self.user_url.format(uid=uid), callback=self.parse)

            # 获取博主id
            uid = response.meta.get('uid')
            follows = [{'id': follow.get('user').get('id'),
                        'name': follow.get('user').get('screen_name')}
                       for follow in follows]

            # 解析用户的关注人的信息之间的关系
            user_relation_item = UserRelationItem()
            user_relation_item['id'] = uid
            user_relation_item['follows'] = follows
            user_relation_item['fans'] = []
            yield user_relation_item

            # 获取下一页关注
            # 获取上一页
            page = int(response.meta.get('page')) + 1

            # 实现翻页功能
            yield Request(self.follow_url.format(uid=uid, page=1), callback=self.parse_follow, meta={'uid': uid, 'page': page})

    def parse_fans(self, response):
        """
        获取粉丝的用户信息
        """
        res = json.loads(response.text)
        if res['ok']:
            fans = res.get('data').get('cards')[-1].get('card_group')
            for fan in fans:
                uid = fan.get('user').get('id')
                yield Request(self.user_url.format(uid=uid), callback=self.parse)

            # 获取博主id
            uid = response.meta.get('uid')
            fans = [{'id': fan.get('user').get('id'),
                     'name': fan.get('user').get('screen_name')}
                    for fan in fans]

            # 关注的人列表
            user_relation_item = UserRelationItem()
            user_relation_item['id'] = uid
            user_relation_item['fans'] = fans
            user_relation_item['follows'] = []
            yield user_relation_item

            # 获取下一页关注
            # 获取当前页页码
            page = int(response.meta.get('page')) + 1

            # 实现翻页功能
            yield Request(self.fans_url.format(uid=uid, page=1), callback=self.parse_follow, meta={'uid': uid, 'page': page})

    def parse_weibo(self, response):
        res = json.loads(response.text)
        if res['ok']:
            field_map = {
                'id': 'id', 'attitudes_count': 'attitudes_count', 'comments_count': 'comments_count',
                'reposts_count': 'reposts_count', 'picture': 'original_pic', 'pictures': 'pics',
                'created_at': 'created_at', 'source': 'source', 'text': 'text', 'raw_text': 'raw_text',
            }
            cards = res.get('data').get('cards')
            uid = response.meta.get('uid')
            for card in cards:
                mblog = card.get('mblog')
                if mblog:
                    weibo_item = WeiboItem()
                    for item, info in field_map.items():
                        weibo_item[item] = mblog.get(info)
                        weibo_item['user'] = uid
                    yield weibo_item

            # 获取下一页关注
            # 获取当前页页码
            page = int(response.meta.get('page')) + 1

            # 实现翻页功能
            yield Request(self.weibo_url.format(uid=uid, page=1), callback=self.parse_follow, meta={'uid': uid, 'page': page})
