#!/usr/bin/env python
# coding=utf-8

import os
import sys
sys.path.append("../spider")
sys.path.append("../db")
import pika
import time
import multiprocessing
import ConfigParser
from sina_spider import SinaSpider
from orm_mongo import MyMongoDB
import json
from datetime import datetime

#rabbitmq 消费者
class RQConsumer():
    def __init__(self,conf):
        host = conf.get("rabbitmq","host")
        port = conf.getint("rabbitmq","port")
        queue = conf.get("rabbitmq","queue")
        mongo_host = conf.get("mongo","host")
        mongo_port = conf.getint("mongo","port")
        mongo_db = conf.get("mongo","db")
        mongo_collection = conf.get("mongo","collection")
        #连接rabbit
        connection = pika.BlockingConnection(pika.ConnectionParameters(host,int(port)))
        self.channel = connection.channel()
        self.channel.basic_qos(prefetch_count = 1)
        #如果没有队列就创建
        self.channel.queue_declare(queue = queue,durable = True)
        self.queue = queue
        self.db = MyMongoDB(mongo_host,mongo_port,mongo_db,mongo_collection)

    #接收消息的回调函数
    def callback(self,ch,method,properties,body):
        try:
            print("Process is running at pid %s;data:%s" % (os.getpid(),body))
            urls = json.loads(body)
            url = urls["url"]
            spider = SinaSpider(url)
            data = spider.get_html()
            data["date"] = datetime.now()
            self.db.update({"url":url},{"$set":data})#{"title":data["title"],"date":datetime.now()},"is_over":0})
            print data
            #消息处理完成可以通知到队列完成了处理
            ch.basic_ack(delivery_tag = method.delivery_tag)
            #在此处理每条消息

        except Exception,e:
            print "occure a Exception:{}".format(e)
    
    def start(self,_call_back):
        print "start consumer..."
        self.channel.basic_consume(_call_back,queue = self.queue)
        self.channel.start_consuming()

def TestConsumer(conf,Consumer):
    consumer = Consumer(conf)
    consumer.start(consumer.callback)

def multi_consumer(conf,Consumer,process_num = 0):
    p = multiprocessing.cpu_count()
    if process_num != 0:
        p = process_num
    pool = multiprocessing.Pool(processes = p)
    for i in xrange(p):
        pool.apply_async(TestConsumer,(conf,Consumer))
    pool.close()
    pool.join()
    print "done"

if __name__ == "__main__":
    conf = ConfigParser.ConfigParser()
    conf.read("setting.conf")
    multi_consumer(conf,RQConsumer)
