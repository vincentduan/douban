# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class GirlItem(scrapy.Item):
    
    title = scrapy.Field() # 标题
    author = scrapy.Field() # 作者
    url = scrapy.Field() # url
    lastTime = scrapy.Field() # 最近回应时间
    detail_time = scrapy.Field() # 发帖时间
    detail_report = scrapy.Field() # 发帖内容

    def __str__(self):
       return '{"title": "%s", "author": "%s", "url": "%s", "lastTime": "%s", "detail_time": "%s", "detail_report": "%s"}\n' %(self['title'], self['author'], self['url'], self['lastTime'], self['detail_time'], self['detail_report'])
