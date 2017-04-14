#encoding=utf-8

import sys
sys.path.append("../queues")
import requests
import json
from bs4 import BeautifulSoup
from rb_product import RQProduct

class SinaSpiderUrl():
    def __init__(self):
        self.index = "http://feed.mix.sina.com.cn/api/roll/get?pageid=155&lid=1686&num={}&page={}&callback=feedCardJsonpCallback&_=1492089504614"

    def get_urls(self):
        s = requests.Session()
        url = self.index.format(10,1)
        r = s.get(self.index)
        html = r.content
        print html
        a = html.find("(")
        b = html.rfind(")")
        html = html[a:b]
        c = html.rfind(")")
#        print html[1:c-1]
        html = html[1:c-1]
#        print html
        a = "sdf"
        print a
        html = html.replace('\"',"'")
        html = json.loads(html)
        print html
        urls = []
        return urls

a = SinaSpiderUrl()
url = a.get_urls()
print url,"--"
