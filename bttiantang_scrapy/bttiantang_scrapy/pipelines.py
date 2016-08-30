# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
import json

from scrapy.exceptions import DropItem
from scrapy.mail import MailSender


class BttiantangScrapyPipeline(object):
    def process_item(self, item, spider):
        return item


class BttiantangScrapyDoubanscorePipeline(object):
    MIN_DOUBAN_SCORE = 80

    def process_item(self, item, spider):
        if item['douban_score'] and item['douban_score'] >= self.MIN_DOUBAN_SCORE:
            return item
        else:
            raise DropItem("score [%d], too low!" % item['douban_score'])


class BttiantangScrapyEmailPipeline(object):
    EMAIL_ADDR_LS = ['845094708@qq.com']
    MOVIE_LS = []

    def process_item(self, item, spider):
        self.MOVIE_LS.append(item)
        return item

    def close_spider(self, spider):
        movie_body = u'\n'.join(
            [
                json.dumps(
                    dict(movie),
                    indent=4,
                    encoding='utf-8'
                )
             for movie in self.MOVIE_LS]
        )

        mail = MailSender()
        mail.send(
            self.EMAIL_ADDR_LS,
            subject = u'bt天堂电影爬虫推送(%s)' % datetime.datetime.now(),
            body = movie_body,
        )
