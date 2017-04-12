#!/usr/bin/env python
# coding=utf-8

import pika
import ConfigParser

#rabbitmq 生产者
class MyProduct():
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
    product = MyProduct(host,port,queue)
    for i in range(0,100):
        message = "I send a msg:int{}".format(i)
        product.product(message)
    product.close()
