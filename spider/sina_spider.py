#!/usr/bin/env python
# coding=utf-8

import sys,os
sys.path.append(os.path.join(os.path.split(os.path.realpath(__file__))[0], '../queues'))
sys.path.append(os.path.join(os.path.split(os.path.realpath(__file__))[0], '../db'))
import requests
import ConfigParser
from bs4 import BeautifulSoup

from rb_consumer import RQConsumer,multi_consumer,TestConsumer
from orm_mongo import MyMongoDB

class MyRQConsumer(RQConsumer):

    def __init__(self,conf):
        try:
            print "myrqconsumer init"
            mongo_host = conf.get("mongo","host")
            mongo_port = conf.getint("mongo","port")
            mongo_db = conf.get("mongo","db")
            mongo_collection = conf.get("mongo","collection")
            self.db = MyMongoDB(mongo_host,mongo_port,mongo_db,mongo_collection)
            RQConsumer.__init__(self,conf)
        except Exception,e:
            print "MyRQConsumer __init__ occure a exception:{}".format(e)
            return

    #抓取url，并处理html，处理解析数据等
    def spider(self,url):
        spider = SinaSpider(url)
        data = spider.get_data()
        data["date"] = datetime.now()
        self.db.update({"url":url},{"$set":data})#{"title":data["title"],"date":datetime.now()},"is_over":0})


class SinaSpider(object):

    def __init__(self,url):
        self.url = url

    def parser_content(self,html):
        try:
            bs = BeautifulSoup(html,"html.parser")
            title = bs.find_all(id = "artibodyTitle")
            if not title:
                return {}
            title = title[0]
            title = title.text
            print title 

            data = {
                "url":self.url,
                "title":title,
                "is_over":0
            }
            return data
        except Exception,e:
            data = {
                "url":self.url,
                "is_over":-2
            }
            return data

    def get_data(self):
        print self.url
        r = requests.get(self.url)
        html = r.content
        data = self.parser_content(html)
        return data

if __name__ == "__main__":         
    conf = ConfigParser.ConfigParser()
    conf.read("setting.conf")      
#    TestConsumer(conf,MyRQConsumer)
    multi_consumer(conf,MyRQConsumer)
