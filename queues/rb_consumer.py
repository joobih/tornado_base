#!/usr/bin/env python
# coding=utf-8
import pika
import time

#credentials = pika.PlainCredentials('admin', 'admin')
# 链接rabbit
#connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',5672))
# 创建频道
#channel = connection.channel()
#channel.basic_qos(prefetch_count=1)

# 如果生产者没有运行创建队列，那么消费者创建队列
#channel.queue_declare(queue='url_queue5',durable = True)
#channel.basic_qos(1)


#def callback(ch, method, properties, body):
#    print(" [x] Received %r" % body)
#    time.sleep(0.5)
#    ch.basic_ack(delivery_tag=method.delivery_tag)  # 主要使用此代码

#channel.basic_consume(callback,
#                      queue='url_queue')
#                      no_ack=False)

#print(' [*] Waiting for messages. To exit press CTRL+C')
#channel.start_consuming()

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
        print "recive the message"
        print(body)
#        time.sleep(0.5)
        ch.basic_ack(delivery_tag = method.delivery_tag)
    
    def start(self):
        def callback(ch,method,properties,body):
            print body
            ch.basic_ack(delivery_tag = method.delivery_tag)
        print "start consumer..."
        self.channel.basic_consume(callback,queue = self.queue)
        self.channel.start_consuming()

if __name__ == "__main__":
    consumer = RQConsumer("127.0.0.1",5672,"url_queue5")
    consumer.start()
