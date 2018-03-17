# -*- coding=utf-8 -*-

from pyquery import PyQuery
import json
import requests
import re


def parse(url):
    response = requests.get(url,headers=headers)
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
    html = requests.get(url,headers=headers).text
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
    html = requests.get(url,headers=headers).text
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
    html = requests.get(url,headers=headers).text
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
    html = requests.get(url,headers=headers).text
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
headers = {
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36"
}


for things in select1():
    li1.append(things)
    print(things["id"],things["txt"])
typ = int(input("输入代号选择榜单："))
typ = li1[typ]["type"]
print("\n")

if typ == "bangumi":
    choices = [
        {
            "id": 0,
            "type":"global",
            "txt":"番剧"
        },{
            "id": 1,
            "type": "cn",
            "txt": "国产动画"
        }
    ]
    for choice in choices:
        print(choice["id"],choice["txt"])
    tab = int(input("输入代号选择标签："))
    tab = choices[tab]["type"]
    print("\n")
    dates = [
        {
            "id": 0,
            "type": "3",
            "txt": "三日排行"
        },{
            "id": 1,
            "type": "7",
            "txt": "七日排行"
        }
    ]
    for date in dates:
        print(date["id"],date["txt"])
    rang = int(input("输入代号选择日期："))
    rang = dates[rang]["type"]
    print("\n")
    url = "https://bangumi.bilibili.com/jsonp/season_rank_list/%s/%s.ver" %(tab,rang)
    response = requests.get(url, headers=headers)
    txt = re.search("\((.*?)\);", response.text).group(1)
    doc = json.loads(txt)
    items = doc.get("result").get("list")
    i = 0
    for item in items:
        data = {
            '排名': i,
            '名称': item.get("title"),
            '播放量': item.get("play_count"),
            '弹幕': item.get("dm_count"),
            '收藏': item.get("fav"),
            '综合评分': item.get("pts"),
        }
        i = i + 1
        with open('data.json', 'a', encoding='utf-8') as file:
            file.write(json.dumps(data, indent=2, ensure_ascii=False))

elif typ == "cinema":
    choices = [
        {
            "id": 0,
            "tid": "177",
            "txt": "纪录片"
        },{
            "id": 1,
            "tid": "23",
            "txt": "电影"
        },{
            "id": 2,
            "tid": "11",
            "txt": "电视剧"
        },
    ]
    for choice in choices:
        print(choice["id"],choice["txt"])
    tab = int(input("输入代号选择标签："))
    tab = choices[tab]["tid"]
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
    parse(url)

else:
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
    parse(url)