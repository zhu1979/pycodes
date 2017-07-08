#-*-coding=utf-8-*-

import requests
import os
import json
from bs4 import BeautifulSoup
import datetime

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
}

url = 'https://toutiao.io/prev/2017-07-07'

crawl_url = 'https://toutiao.io/'
cpev_url = 'https://toutiao.io/prev/'
csub_url = 'https://toutiao.io'


def CrawlPage(url):
    return requests.get(url, headers=headers)

def Extractpage(html):    
    soup = BeautifulSoup(html.content, 'lxml')
    posts = soup.find_all('div', {'class': 'post'})
    dd =[]
    for post in posts:
        z = post.find_all('a')[0].text  # 点赞
        s = post.find_all('a')[1].text  # 收藏
        title = post.find_all('a')[2].text  # 标题
        thref = csub_url + post.find_all('a')[2].get('href')  # 调整链接
        meta=post.find('div', {'class': 'meta'}).text.strip()  # 原始数据
        sharer=post.find_all('a')[-1].text  # 分享者
        shareurl=csub_url + post.find_all('a')[-1].get('href')  # 分享者的url

        yield {
            "dz":z,
            "sc":s,
            "title":title,
            "turl":thref,
            "meta":meta,
            "sharer":sharer,
            "shareurl":shareurl
        }

def save(jsons):
    with open('toujson.json','a') as t:
        for j in jsons:
            t.write(json.dumps(j)+'\n')


def GenUrl():
    today = datetime.datetime.now()
    oneday = datetime.timedelta(days =1)
    for i in range(1000):
        td = today - oneday
        today = td
        surl = cpev_url+td.strftime('%Y-%m-%d')
        print(surl)
        yield  surl

def main():
    for url in GenUrl():
        h=CrawlPage(url)
        save(Extractpage(h))
        

if __name__ == '__main__':
    main()
