#!/usr/bin/env python
# coding=utf-8

from pymongo import MongoClient
from datetime import datetime
import time

"""
    table urls:

    {
        url             String,         --url网页地址
        is_over         Integer,        --是否抓去过的url ,-1 -- 未被抓取； 0 -- 已经抓取完成
        content         String,         --新闻内容
        title           String,         --新闻标题
        submit_time     String,         --发表日期
        date            Date            --存库日期或则更新库日期
        source          String          --新闻来源
        author          string          --新闻作者
        participate_num Integer         --新闻参与人数量
        comment_num     Integer         --评论数量
        comments        Arrays          --所有的评论组成的数组
            {
                comment_time        Date        --评论日期
                comment_user        String      --评论者
                comment_content     String      --评论内容
                comment_address     String      --评论地点
                concur_num          Integer     --评论支持数
            }
    }

    

"""

class MyMongoDB():
    def __init__(self,host,port,db_name,collection):
        self.client = MongoClient(host,port)
        self.db = self.client[db_name]
        self.collection = self.db[collection]

    #插入可以批量插入也可以单条插入 批量插入使用list
    def insert(self,data):
        if isinstance(data,dict):
            d = []
            d.append(data)
            data = d
        if not isinstance(data,list):
            return -1
        try:
            print data
            self.collection.insert_many(data)
            return 0
        except Exception,e:
            print "insert occure a Exception :{}".format(e)
            return -2

    """
        update({age: 25}, {$set: {name: 'changeName'}}, false, true);
        相当于:update users set name = ‘changeName’ where age = 25;
        update({name: 'Lisi'}, {$inc: {age: 50}}, false, true);
        相当于:update users set age = age + 50 where name = ‘Lisi’;
    """
    #更新操作，通过满足某些条件更新
    def update(self,condition,sets):
        try:
            #upsert表示没找到就插入，multi 表示匹配了多条就多条更改
            self.collection.update(condition,sets,upsert=True,multi=True)
            return 0
        except Exception,e:
            print "update occure a Exception:{}".format(e)
            return -1001

#mongo = MyMongoDB("127.0.0.1",27017,"test","urls")
#for i in range(0,1000):
#    id = i
#    name = "cuijun"
#    data = {"id":id,"name":name,"date":datetime.now(),"time_stamp":time.time()}
#    mongo.insert(data)

