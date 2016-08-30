#encoding=utf8
import scrapy

from bttiantang_scrapy.items import BttiantangScrapyItem


class BttiantangSpider(scrapy.spiders.Spider):
    """
    爬取 bt天堂 首页 的电影
    """
    name = "bttiantang"
    allowed_domains = ['bttiantang.com']
    start_urls = [
        'http://www.bttiantang.com/',
    ]

    def parse(self, response):
        for movie in response.xpath('//div[@class="item cl"]'):
            title = movie.xpath('div[@class="title"]/p[@class="tt cl"]')
            # 空的
            if not title.extract_first():
                continue

            # 电影名
            movie_name_ls = title.xpath('a/b/text()|a/b/font/text()').extract()

            # 更新时间
            update_date = title.xpath('span/text()').extract_first()

            # 国家
            contry_ls = movie.xpath('div[@class="title"]/p[@class="des"]/text()').extract()
            contry = ''
            flag = True
            for key in contry_ls:
                if '(' in key:
                    contry = key
                elif flag:
                    contry += key
                if ')' in key:
                    flag = False
            contry = contry[contry.find('(') + 1: contry.find(')')]

            # 豆瓣评分
            big_score = movie.xpath('div[@class="title"]/p[@class="rt"]/strong/text()').extract()
            small_score = movie.xpath('div[@class="title"]/p[@class="rt"]/em[@class="fm"]/text()').extract()
            score = int(big_score[0]) * 10 + int(small_score[0])

            item = BttiantangScrapyItem()
            item['name'] = movie_name_ls[0].encode('utf-8')
            item['update_time'] = update_date
            item['contry'] = contry
            item['douban_score'] = score
            yield item
