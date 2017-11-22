import scrapy
import redis
from wdjcomment.settings import *

url_redis = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

class WdjSpider(scrapy.Spider):
    name = "wandoujia_comment"
    allowed_domains = ["wandoujia.com"]
    start_urls = [
        "http://www.wandoujia.com/category/app",
        "http://www.wandoujia.com/category/game"
    ]

    def parse(self, response):
        print 'Preparing Starting'
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse_category)


    def parse_category(self,response):
        #category_big = response.xpath('//ul/li[@class="parent-cate"]/a/@href').extract()
        category_small = response.xpath('//ul/li[@class="child-cate"]/a/@href').extract()
        #category = category_big + category_small
        for url in category_small:
            yield scrapy.Request(url,self.parse_detail)


    def parse_detail(self,response):
        appid_list = response.xpath('//div[@class="col-left"]/ul/li/@data-pn').extract()
        url_str = "http://www.wandoujia.com/apps/"
        for i in appid_list:
            url  = url_str + i
            for ii in url_redis.lrange("wdj_comment:start_urls",0, -1):
                if ii == url:
                    print ii
                    continue
            url_redis.lpush("wdj_comment:start_urls", url)

        page_url = response.xpath('//div[@class="page-wp roboto"]/a[@class="page-item "]/@href').extract()
        for i in page_url:
            if i == "javascript:;":
                continue
            if len(i.split('/')) == 6:
                page_num = int(i.split('/')[-1])
                if page_num > 10:
                    for ii in range(10, page_num+1):
                        pages = '/'.join(i.split('/')[0:5]) +'/' + str(ii)
                        yield scrapy.Request(pages,self.parse_detail)
            else:
                yield scrapy.Request(i,self.parse_detail)

