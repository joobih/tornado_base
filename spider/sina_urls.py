#encoding=utf-8

import sys
sys.path.append("../queues")
sys.path.append("../db")
import requests
import json
import re
import time
import multiprocessing
from bs4 import BeautifulSoup
from rb_product import RQProduct
from orm_mongo import MyMongoDB
import ConfigParser

class SinaSpiderUrl():
    def __init__(self,conf):
        host = conf.get("mongo","host")
        port = conf.getint("mongo","port")
        db_name = conf.get("mongo","db")
        collection = conf.get("mongo","collection")
        self.mongo = MyMongoDB(host,port,db_name,collection)
        self.index = "http://feed.mix.sina.com.cn/api/roll/get?pageid=155&lid=1686&num={}&page={}&callback=feedCardJsonpCallback&_={}"

    def get_urls(self,page):
        try:
            s = requests.Session()
            t = int(time.time())
            url = self.index.format(100,page,t)
            print url
            r = s.get(url)
            html = r.content
            a = html.find("(")
            b = html.rfind(")")
            html = html[a:b]
            c = html.rfind(")")
            html = html[1:c-1]
            html = html.replace('\/','/').replace('\\\/','/')
            urlParttern = r'https?://[\w\-\/]+[\.[\w\-\/]+]*'
            pattern = re.compile(urlParttern)
            match_url = re.findall(pattern,html,0)
            return match_url
        except Exception,e:
            print "occure a exception:{}".format(e)
            return []

    def get_all(self,s,e):
        for i in range(s,e):
            urls = self.get_urls(i)
#            print urls
            for u in urls:
                data = {
                    "url":u,
                    "is_over":-1
                }
                self.mongo.update({"url":u,"is_over":-1},{"$set":data})

def multi_p(s,e):
    file = "../queues/setting.conf"
    conf = ConfigParser.ConfigParser()
    conf.read(file)
    a = SinaSpiderUrl(conf)
    a.get_all(s,e)

def main():
    p = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes = p)
    for i in xrange(p):
        print i
        pool.apply_async(multi_p,(10*i,10*(i+1)))
    pool.close()
    pool.join()

if __name__ == "__main__":
    main()

#a = SinaSpiderUrl()
#a.get_all()
#print url,"--"
