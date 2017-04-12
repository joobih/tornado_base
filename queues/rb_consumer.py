#!/usr/bin/env python
# coding=utf-8

import os
import pika
import time
import multiprocessing
import ConfigParser

#rabbitmq 消费者
class RQConsumer():
    def __init__(self,host,port,queue):
        #连接rabbit
        connection = pika.BlockingConnection(pika.ConnectionParameters(host,int(port)))
        self.channel = connection.channel()
        self.channel.basic_qos(prefetch_count = 1)
        #如果没有队列就创建
        self.channel.queue_declare(queue = queue,durable = True)
        self.queue = queue

    #接收消息的回调函数
    def callback(self,ch,method,properties,body):
        print("Process is running at pid %s" % os.getpid())
        print(body)
        time.sleep(1)
        ch.basic_ack(delivery_tag = method.delivery_tag)
        #在此处理每条消息
    
    def start(self):
        print "start consumer..."
        self.channel.basic_consume(self.callback,queue = self.queue)
        self.channel.start_consuming()

def TestConsumer(conf):
    host = conf.get("rabbitmq","host")
    port = conf.getint("rabbitmq","port")
    queue = conf.get("rabbitmq","queue")
    consumer = RQConsumer(host,port,queue)
    consumer.start()

def multi_consumer(conf,process_num = 0):
    p = multiprocessing.cpu_count()
    if process_num != 0:
        p = process_num
    pool = multiprocessing.Pool(processes = p)
    for i in xrange(p):
        pool.apply_async(TestConsumer,(conf,))
    pool.close()
    pool.join()
    print "done"

if __name__ == "__main__":
#    p = multiprocessing.cpu_count()
#    print "CPU is:",p
#    pool = multiprocessing.Pool(processes = p)
    conf = ConfigParser.ConfigParser()
    conf.read("setting.conf")
    multi_consumer(conf)
#    for i in xrange(p):
#        pool.apply_async(TestConsumer,(conf,))
#    pool.close()
#    pool.join()
#    print "done"
