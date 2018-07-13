# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy import Request

from maoyansipder.items import MovieItem


class MoviesSpider(scrapy.Spider):
    name = 'movies'
    start_urls = ['http://m.maoyan.com/ajax/movieOnInfoList?token=']
    base_url = 'http://m.maoyan.com/ajax/detailmovie?movieId={movie_id}'

    """
    电影列表
    http://m.maoyan.com/ajax/moreComingList?token=&movieIds=1198178
    
    
    电影详情
    http://m.maoyan.com/ajax/detailmovie?movieId=1198178
    
    
    获取放映时间下的电影院：
    http://m.maoyan.com/ajax/movie?forceUpdate=1530667487934（时间戳带毫秒）
    http://m.maoyan.com/ajax/cinemaList?day=2018-07-11&cityId=20
   
    
    获取全城、品牌、特色：
    http://m.maoyan.com/ajax/filterCinemas?movieId=1198178&day=2018-07-04
    
    
    影院下的信息：
    http://m.maoyan.com/ajax/cinemaDetail?cinemaId=24569&movieId=1198178
    
    
    
    即将上映：
    http://m.maoyan.com/ajax/moreComingList?token=&movieIds=346096%2C343873%2C1221133%2C1211641%2C1220805%2C1227229%2C592271%2C1224953%2C1217513%2C1203528
    
    
    """


    def parse(self, response):
        res = json.loads(response.text)
        movieIds = res.get('movieIds')
        # movieIds = list(map(str,movieIds))
        for id in movieIds:

            yield Request(self.base_url.format(movie_id=id), callback=self.movie_info)

    def movie_info(self, response):

        res = json.loads(response.text)
        field_map = {
            'id': 'id',
            'describe':'dra',
            'img': 'albumImg',
            'version': 'version',
            'name': 'nm',
            'cinemaScore': 'sc',
            'wish': 'wish',
            'star': 'star',
            'dur':'dur',
            'releaseTime': 'rt',
            'globalReleased':'globalReleased'
            # 'showInfo': 'showInfo',
        }
        if res:
            movie = res.get('detailMovie')
            movie_item = MovieItem()
            for item,info in field_map.items():
                movie_item[item] = movie.get(info)
            yield movie_item



