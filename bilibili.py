# -*- coding=utf-8 -*-

from pyquery import PyQuery
import json
import requests


def parse(url):
    response = requests.get(url)
    items = response.json().get("rank").get("list")
    i = 1
    for item in items:
        data = {
            '排名': i,
            '名称': item.get("title"),
            '播放量': item.get("play"),
            '弹幕': item.get("video_review"),
            'up主': item.get("author"),
            '综合评分': item.get("pts"),
        }
        i = i + 1
        with open('data.json', 'a', encoding='utf-8') as file:
            file.write(json.dumps(data, indent=2, ensure_ascii=False))
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
    # 由于B站番剧榜和影视榜的URL与其他不同，所以特殊处理
    if typ == "bangumi":
        typ = "bangumi/13/0/3/"
    if typ == "cinema":
        typ = "cinema/177/0/3/"
    url = "https://www.bilibili.com/ranking#!/%s" % typ
    print(url)
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


def make_url(typ,rang,tid,newv):
    # 由于影视榜的ajax用的名称是all而不是cinema，所以特殊处理
    if typ == "cinema":
        typ = "all"
    if newv == "1":
        return "https://www.bilibili.com/index/rank/%s-0%s-%s.json" % (typ,rang,tid)
    else:
        return "https://www.bilibili.com/index/rank/%s-%s-%s.json" % (typ,rang,tid)


li1 = []
li2 = []
li3 = []
li4 = []
open('data.json', 'w', encoding='utf-8').close()


for things in select1():
    li1.append(things)
    print(things["id"],things["txt"])
typ = int(input("输入代号选择榜单："))
typ = li1[typ]["type"]
print("\n")

for things in select2(typ):
    li2.append(things)
    print(things["id"],things["txt"])
tab = int(input("输入代号选择标签："))
tab = li2[tab]["tid"]
print("\n")

for things in select3():
    li3.append(things)
    print(things["id"],things["txt"])
newv = int(input("输入代号选择检索投稿："))
newv = li3[newv]["type"]
print("\n")

for things in select4():
    li4.append(things)
    print(things["id"],things["txt"])
rang = int(input("输入代号选择检索时长："))
rang = li4[rang]["range"]
print("\n")

url = make_url(typ,rang,tab,newv)
print(url)
parse(url)