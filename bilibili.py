# -*- coding=utf-8 -*-

from pyquery import PyQuery
from selenium import webdriver
import re
import json
import requests


def parse(url):
    browser = webdriver.Chrome()
    browser.get(url)
    html = browser.page_source
    doc = PyQuery(html)
    items = doc('.rank-item').items()
    fp = open('data.json', 'w', encoding='utf-8')
    fp.close()
    for item in items:
        data = {
            '排名': item.find('.num').text(),
            '名称': item.find('.title').text(),
            '播放量': item.find('.play').text(),
            '弹幕': item.find('.dm').text(),
            'up主': item.find('.author').text(),
            '综合评分': re.match('\d*', item.find('.pts').text()).group(),
        }
        with open('data.json', 'a', encoding='utf-8') as file:
            file.write(json.dumps(data, indent=2, ensure_ascii=False))
    browser.close()
    print("Succeed!")


def select1():
    url = "https://www.bilibili.com/ranking"
    html = requests.get(url).text
    doc = PyQuery(html)
    items = doc(".rank-menu li").items()
    i = 0
    for item in items:
        thing = {
            "id": i,
            "type": item.attr("type"),
            "txt": item(".txt").text()
        }
        i = i + 1
        yield thing


def select2(typ):
    url = "https://www.bilibili.com/ranking#!/%s" % typ
    html = requests.get(url).text
    doc = PyQuery(html)
    items = doc(".rank-tab li").items()
    i = 0
    for item in items:
        thing = {
            "id": i,
            "tid": item.attr("tid"),
            "txt": item.text()
        }
        i = i + 1
        yield thing


def select3():
    url = "https://www.bilibili.com/ranking"
    html = requests.get(url).text
    doc = PyQuery(html)
    items = doc("#rank_newv_tab ul li").items()
    i = 0
    for item in items:
        thing = {
            "id": i,
            "type": item.attr("type"),
            "txt": item.text()
        }
        i = i + 1
        yield thing


def select4():
    url = "https://www.bilibili.com/ranking"
    html = requests.get(url).text
    doc = PyQuery(html)
    items = doc("#rank_range_tab ul li").items()
    i = 0
    for item in items:
        thing = {
            "id": i,
            "range": item.attr("range"),
            "txt": item.text()
        }
        i = i + 1
        yield thing


def make_url(typ,tid,typ2,rang):
    return "https://www.bilibili.com/ranking#!/%s/%s/%s/%s/" % (typ,tid,typ2,rang)


li1 = []
li2 = []
li3 = []
li4 = []

for things in select1():
    li1.append(things)
    print(things["id"],things["txt"])
menu = int(input("输入代号选择榜单："))
print("\n")

for things in select2(li1[menu]["type"]):
    li2.append(things)
    print(things["id"],things["txt"])
tab = int(input("输入代号选择标签："))
print("\n")

for things in select3():
    li3.append(things)
    print(things["id"],things["txt"])
newv = int(input("输入代号选择检索投稿："))
print("\n")

for things in select4():
    li4.append(things)
    print(things["id"],things["txt"])
rang = int(input("输入代号选择检索时长："))
print("\n")

parse(make_url(li1[menu]["type"],li2[tab]["tid"],li3[newv]["type"],li4[rang]["range"]))