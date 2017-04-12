#!/usr/bin/env python
# coding=utf-8

import pika
# ######################### 生产者 #########################
#credentials = pika.PlainCredentials('admin', 'admin')
#链接rabbit服务器（localhost是本机，如果是其他服务器请修改为ip地址）
connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1',5672))
#创建频道
channel = connection.channel()
#channel.basic_qos(prefetch_count=1)
# 声明消息队列，消息将在这个队列中进行传递。如果将消息发送到不存在的队列，rabbitmq将会自动清除这些消息。如果队列不存在，则创建
channel.queue_declare(queue='url_queue5',durable = True)
#channel.basicQos(1)
#exchange -- 它使我们能够确切地指定消息应该到哪个队列去。
#向队列插入数值 routing_key是队列名 body是要插入的内容

for i in range(0,40):
    channel.basic_publish(exchange='',
                  routing_key='url_queue',
                  body='Hello World!{}'.format(i),
#                  properties = pika.BasicProperties(
#                      delivery_mode = 2,)
    )
    
print("开始队列")
#缓冲区已经flush而且消息已经确认发送到了RabbitMQ中，关闭链接
connection.close()
