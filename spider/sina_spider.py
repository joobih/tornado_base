#!/usr/bin/env python
# coding=utf-8

import requests
from bs4 import BeautifulSoup

class SinaSpider(object):
    def __init__(self,url):
        self.url = url

    def parser_content(self,html):
        bs = BeautifulSoup(html,"html.parser")
        title = bs.find_all(id = "artibodyTitle")
        if not title:
            return {}
        title = title[0]
        title = title.text
        print title 

        data = {
            "url":self.url,
            "title":title
        }
        return data

    def get_html(self):
        print self.url
        r = requests.get(self.url)
        html = r.content
        data = self.parser_content(html)
        return data
