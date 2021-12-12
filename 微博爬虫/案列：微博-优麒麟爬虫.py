# -*- coding: utf-8 -*-
# @Time    : 2019-07-12 21:47
# @Author  : xudong
# @email   : dongxu222mk@163.com
# @Site    : 
# @File    : ajaxTest.py
# @Software: PyCharm
 
from urllib.parse import urlencode
import requests
import json
import random 
from datetime import datetime
from datetime import timedelta
 
# 请求的url
base_url = "https://m.weibo.cn/api/container/getIndex?";

# 构造请求头
headers = {
    'Host' : 'm.weibo.cn',
    'Referer' : 'https://m.weibo.cn/u/3265288504',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.57',
    'X-Requested-With' : 'XMLHttpRequest'
}
class Wb_ukylin:

    def __init__(self, nowdate):

        self.count = 0
        self.nowdate = nowdate
# 获取每一页的请求数据返回的是json格式
    def get_page(page):
        params = {
            'type' : 'uid',
            'value' : '3265288504',
            'containerid' : '1076033265288504',
            'page' : page
        }
        url = base_url + urlencode(params)
        try:
            response = requests.get(url, headers=headers)
            print(type(response))
            if response.status_code == 200:
                return response.json()
        except requests.ConnectionError as e:
            print('Error', e.args)
     


    # 解析每一页的json数据，并返回一个weibo的字典类型数据
    def get_data(self):
       # nowdate="2020-12-25"
        print("开始爬取【优麒麟社区微博】的内容！")
        print("本次爬取今日： [" +self.nowdate + "] 的数据记录。")
        datalists=[]
        data=Wb_ukylin.get_page(1).get('data').get('cards')
        items =[i for i in data if "itemid" in i]
        for item in items:
            if "page_info" in item.get("mblog"):
            #print("正在爬取第{}条内容。请稍后......".format(items.index))
                dzc=item.get("mblog").get("attitudes_count")
                plc=item.get("mblog").get("comments_count")
                zfc=item.get("mblog").get("reposts_count")                    
                wurl=item.get("mblog").get("page_info").get("page_url")
                title=item.get("mblog").get("page_info").get("page_title")
                creat_time= item.get("mblog").get("created_at")
                if "刚刚" in creat_time:
                    time=datetime.now().strftime("%Y-%m-%d")
                elif "小时" in creat_time:
                    hour=creat_time[:creat_time.find("小时")]
                    hour=timedelta(hours=int(hour))
                    time=(datetime.now()-hour).strftime("%Y-%m-%d")
                elif "分钟" in creat_time:
                    minute=creat_time[:creat_time.find("分钟")]
                    minute=timedelta(hours=int(minute))
                    time=(datetime.now()-minute).strftime("%Y-%m-%d")
                elif "昨天" in creat_time:
                    today=datetime.now()
                    detday=timedelta(days=1)
                    da_days=today-detday
                    time=da_days.strftime("%Y-%m-%d")
                else:
                    time="2020-"+creat_time
                if time==self.nowdate:
                    self.count+=1
                    datalists.append({"wurl":wurl,"title":title,"dzc":dzc,"plc":plc,"zfc":zfc,"time":time})
                elif time<self.nowdate:
                    break
        if self.count==0:
            print("\n今日无更新")
            print("*"*40)
        else:
            print("\n该站点共抓取到：" + str(self.count) + "条记录！")
            print("爬取完成！")
            print("*"*40)
            return datalists
            time.sleep(2)

        return datalists
#Wb_ukylin.get_data()


