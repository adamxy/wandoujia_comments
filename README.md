#把豌豆荚的单个App页面的URL链接Push到Redis 
scrapy runspider wdjcomment/spiders/category.py

#抓取每个页面的评论信息存入Redis 
scrapy runspider wdjcomment/spiders/comment.py

#从Redis里面把数据插入到Mongodb 
python wdjcomment/pipelines.py
