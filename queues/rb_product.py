#!/usr/bin/env python
# coding=utf-8

import sys
sys.path.append("../db")
import pika
import ConfigParser
import json
from orm_mongo import MyMongoDB
#rabbitmq 生产者
class RQProduct():
    def __init__(self,host,port,queue):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host,int(port)))
        self.channel = connection.channel()
        self.channel.queue_declare(queue = queue,durable = True)
        self.queue = queue

    def product(self,message):
        self.channel.basic_publish(exchange = '',routing_key = self.queue,body = message)

    def close(self):
        self.channel.close()


if __name__ == "__main__":
    conf = ConfigParser.ConfigParser()
    conf.read("setting.conf")
    host = conf.get("rabbitmq","host")
    port = conf.getint("rabbitmq","port")
    queue = conf.get("rabbitmq","queue")
#    product = MyProduct("127.0.0.1",5672,"url_queue5")
    product = RQProduct(host,port,queue)
    message = {"url":"http://finance.sina.com.cn/china/gncj/2017-04-13/doc-ifyeimqc3353066.shtml"}
    message = json.dumps(message)
    product.product(message)
#    for i in range(0,100*100*10):
#        message = {"id":i,"name":"cuijun","org":"org1"}
#        message = json.dumps(message)
#        message = "I send a msg:int{}".format(i)
#        product.product(message)
#    product.close()
