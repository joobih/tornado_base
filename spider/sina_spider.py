#!/usr/bin/env python
# coding=utf-8

import sys,os
#sys.path.append(os.path.join(os.path.split(os.path.realpath(__file__))[0], '../queues'))
sys.path.append(os.path.join(os.path.split(os.path.realpath(__file__))[0], '../db'))
sys.path.append(os.path.join(os.path.split(os.path.realpath(__file__))[0], '../submodules'))
import requests
import json
import ConfigParser
from bs4 import BeautifulSoup
from datetime import datetime

from Common.queues.rb_consumer import RQConsumer
from orm_mongo import MyMongoDB

class MyRQConsumer(RQConsumer):

    def __init__(self,rq_queue,rq_host="127.0.0.1",rq_port=5672,kwags={}):
        try:
            print "myrqconsumer init"
            mongo_host = kwags["mongo_host"]
            mongo_port = kwags["mongo_port"]
            mongo_db = kwags["mongo_db"]
            mongo_collection = kwags["mongo_collection"]
            self.db = MyMongoDB(mongo_host,mongo_port,mongo_db,mongo_collection)
            RQConsumer.__init__(self,rq_queue,rq_host,rq_port,kwags)
        except Exception,e:
            print "MyRQConsumer __init__ occure a exception:{}".format(e)
            return

    """
        data里面存放url信息，这里接收到rabbitmq队列中的数据提取出url，抓取url中的信息并处理html，处理解析数据等
        该json数据格式为{"url":"http://www.baidu.com"}
    """
    def data_process(self,data):
        json_data = json.loads(data)
        url = json_data["url"]
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
            print "parser_content occure a Exception:e",e
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
    host = conf.get("rabbitmq","host")
    port = conf.getint("rabbitmq","port")
    queue = conf.get("rabbitmq","queue")
    mongo_host = conf.get("mongo","host")
    mongo_port = conf.getint("mongo","port")
    mongo_db = conf.get("mongo","db")
    mongo_collection = conf.get("mongo","collection")
    kwags = {
        "mongo_host":mongo_host,
        "mongo_port":mongo_port,
        "mongo_db":mongo_db,
        "mongo_collection":mongo_collection
    }

    from rb_consumer import TestConsumer
    TestConsumer(MyRQConsumer,queue,host,port,kwags)
#    from rb_consumer import multi_consumer
#    multi_consumer(MyRQConsumer,queue,host,port,kwags)
