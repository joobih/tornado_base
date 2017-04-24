#!/usr/bin/env python
# coding=utf-8

import os
import sys
import pika
import time
import multiprocessing
import ConfigParser
import json
from datetime import datetime

"""
    rabbitmq 消费者,接受指定topic中的json数据,该json数据格式为{"url":"http://www.baidu.com"}
"""
class RQConsumer():
    def __init__(self,conf):
        try:
            host = conf.get("rabbitmq","host")
            port = conf.getint("rabbitmq","port")
            queue = conf.get("rabbitmq","queue")
            #连接rabbit
            connection = pika.BlockingConnection(pika.ConnectionParameters(host,int(port)))
            self.channel = connection.channel()
            self.channel.basic_qos(prefetch_count = 1)
            #如果没有队列就创建
            self.channel.queue_declare(queue = queue,durable = True)
            self.queue = queue
        except Exception,e:
            print "RQConsumer __init__ occure a Exception:{}".format(e)
            return

    #抓取url，并处理html，处理解析数据等
    def spider(self,url):
        raise NotImplementedError()

    #接收消息的回调函数
    def callback(self,ch,method,properties,body):
        try:
            print("Process is running at pid %s;data:%s" % (os.getpid(),body))
            urls = json.loads(body)
            url = urls["url"]
            self.spider(url)
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
    try:
        p = multiprocessing.cpu_count()
        if process_num != 0:
            p = process_num
        pool = multiprocessing.Pool(processes = p)
        for i in xrange(p):
            pool.apply_async(TestConsumer,(conf,Consumer))
        pool.close()
        pool.join()
        print "done"
    except e:
        print "Caught KeyboardInterrupt, terminating workers",e
        return
