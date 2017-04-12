#!/usr/bin/env python
# coding=utf-8

import requests

url = "http://hq.sinajs.cn/list=sh601006,sh601001"

r = requests.get(url)
#print r.content
r_json = r.content
r_json = r_json.decode("gbk")
print r_json
