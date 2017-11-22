# encoding: utf-8
import scrapy
import datetime
from scrapy_redis.spiders import RedisCrawlSpider
from wdjcomment.items import WdjcommentItem

class WdjCommentSpider(RedisCrawlSpider):
    name = "comment"
    redis_key = 'wdj_comment:start_urls'

    def parse(self, response):
        appid = str(response).split("/")[-1].split(">")[0]
        comments = []
        for sel in response.xpath('//ul[@class="comments-list"]/li'):
            data = {}
            user = ''.join(sel.xpath('p[@class="first"]/span[@class="name"]/text()').extract())
            if user == "":
                continue
            data['username'] = user
            date = sel.xpath('p[@class="first"]/span/text()').extract()[1].encode('utf-8')
            data['date'] = datetime.datetime.strptime(date, '%Y年%m月%d日')
            data['comment'] = ''.join(sel.xpath('p[@class="cmt-content"]/span/text()').extract())
            comments.append(data)

        item = WdjcommentItem()
        item['appid'] = appid
        item['create'] = datetime.datetime.now()
        item['comments'] = comments
        yield item
