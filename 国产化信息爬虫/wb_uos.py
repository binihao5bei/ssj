# -*- coding: utf-8 -*-

 
from urllib.parse import urlencode
import requests
import json
import random 
import datetime
#from datetime import datetime
from datetime import timedelta
 
# 请求的url
base_url = "https://m.weibo.cn/api/container/getIndex?";

# 构造请求头
headers = {
    'Host' : 'm.weibo.cn',
    'Referer' : 'https://m.weibo.cn/u/7370155840',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.57',
    'X-Requested-With' : 'XMLHttpRequest'
}
class Wb_uos:
    def __init__(self, nowdate):

        self.count = 0
        self.nowdate = nowdate

# 获取每一页的请求数据返回的是json格式
    def get_page(page):
        params = {
            'type' : 'uid',
            'value' : '7370155840',
            'containerid' : '1076037370155840',
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
        print("开始爬取【统信UOS】的内容！")
        print("本次爬取今日： [" +self.nowdate + "] 的数据记录。")
        
        datalists=[]
        data=Wb_uos.get_page(1).get('data').get('cards')
        items =[i for i in data if "itemid" in i]
        for item in items:
            if "page_info" in item.get("mblog"):
            #print("正在爬取第{}条内容。请稍后......".format(items.index))
                dzc=item.get("mblog").get("attitudes_count")
                plc=item.get("mblog").get("comments_count")
                zfc=item.get("mblog").get("reposts_count")                    
                wurl=(item.get("mblog").get("page_info").get("page_url")).replace('&','&amp;')
                title=('【麒麟软件】'+item.get("mblog").get("page_info").get("page_title")).replace('&','&amp;')
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
                    time_format=datetime.datetime.strptime(creat_time,'%a %b %d %H:%M:%S %z %Y')
                    time_format=str(time_format)
                    time=time_format[0:10]
                    print(time)


                if time==self.nowdate:
                    self.count+=1
                    datalists.append({"wurl":wurl,"title":title,"dzc":dzc,"plc":plc,"zfc":zfc,"time":time})
                    print(datalists)
                elif time<self.nowdate:
                    break
        if self.count==0:
            print("\n今日无更新")
            print("*"*40)
        else:
            print(datalists)
            print("\n该站点共抓取到：" + str(self.count) + "条记录！")
            print("爬取完成！")
            print("*"*40)
            print(datalists)
            return datalists
            time.sleep(2)
        return datalists
                        
#Wb_neokylin.get_data()


