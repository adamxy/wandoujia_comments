# -*- coding: utf-8 -*-
import pymongo
import redis
import json

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

conn = pymongo.MongoClient('127.0.0.1',27017)
db = conn['pg_crawler']
r = redis.Redis('127.0.0.1', 6379, db=0)

def process_item():
    while True:
        source, data = r.blpop(["comment:items"])
        item = json.loads(data)
        print item
        db.wdj_comment.insert(item)
    return item


if __name__ == "__main__":
    process_item()
