# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BttiantangScrapyItem(scrapy.Item):
    # 电影名字
    name = scrapy.Field()
    # 豆瓣评分
    douban_score = scrapy.Field()
    # 更新时间
    update_time = scrapy.Field()
    # 国家
    contry = scrapy.Field()
