#!/usr/bin/env python
# coding=utf-8

import requests
from bs4 import BeautifulSoup

class SinaSpider(object):
    def __init__(self,url):
        self.url = url

    def parser_content(self,html):
        try:
            bs = BeautifulSoup(html,"html.parser")
            title = bs.find_all(id = "artibodyTitle")
            if not title:
                return {}
            title = title[0]
            title = title.text
            print title 

            data = {
                "url":self.url,
                "title":title,
                "is_over":0
            }
            return data
        except Exception,e:
            data = {
                "url":self.url,
                "is_over":-2
            }
            return data

    def get_html(self):
        print self.url
        r = requests.get(self.url)
        html = r.content
        data = self.parser_content(html)
        return data
