# -*- coding=utf-8 -*-

from pyquery import PyQuery
from selenium import webdriver
import re
import json

url = input('请输入B站排行榜的url:\n')
print(url)
browser = webdriver.Chrome()
browser.get(url)
html = browser.page_source
doc = PyQuery(html)
items = doc('.rank-item').items()
fp = open('data.json','w',encoding='utf-8')
fp.close()
for item in items:
    data = {
        '排名' : item.find('.num').text(),
        '名称' : item.find('.title').text(),
        '播放量' : item.find('.play').text(),
        '弹幕' : item.find('.dm').text(),
        'up主' : item.find('.author').text(),
        '综合评分' : re.match('\d*',item.find('.pts').text()).group(),
    }
    with open('data.json','a',encoding='utf-8') as file:
        file.write(json.dumps(data,indent=2,ensure_ascii=False))
browser.close()