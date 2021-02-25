# coding=utf-8
import requests
import sys
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta

class Xinch():

    def __init__(self, nowdate):

        self.count = 0

        self.nowdate = nowdate

    # request 库调用

    def get_data(self):


        print("本次爬取今日： [" + self.nowdate + "] 的数据记录。")
        session=requests.Session()
        headers={"User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) App leWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"}


        datalists=[]
        count=0
        url='https://www.baidu.com/s?tn=news&rtt=4&bsst=1&cl=2&wd=%E4%BF%A1%E5%88%9B&medium=0'
        response = session.get(url,headers=headers)
        soup = BeautifulSoup(response.text,'lxml')
        print('开始爬取【信创】！')

        print('正在爬取，请稍候')
        divs = soup.find_all("div",class_="result-op c-container xpath-log new-pmd")
        #print(divs)

        for div in divs:
            title = ('【信创】'+div.find('h3',class_='news-title_1YtI1').find('a').get_text()).replace('&','&amp;')
            wurl = (div.find('h3',class_='news-title_1YtI1').find('a').get('href')).replace('&','&amp;')
            creat_time=div.find('div',class_='news-source').find('span',class_='c-color-gray2 c-font-normal').get_text()
            if "刚刚" in creat_time:
                wdate=datetime.now().strftime("%Y-%m-%d")
                #print(wdate)

            elif "小时" in creat_time:
                hour=creat_time[:creat_time.find("小时")]
                hour=timedelta(hours=int(hour))
                wdate=(datetime.now()-hour).strftime("%Y-%m-%d")
               # print(wdate)

            elif "分钟" in creat_time:
                minute=creat_time[:creat_time.find("分钟")]
                minute=timedelta(hours=int(minute))
                wdate=(datetime.now()-minute).strftime("%Y-%m-%d")
               # print(wdate)

            elif "昨天" in creat_time:
                today=datetime.now()
                detday=timedelta(days=1)
                da_days=today-detday
                wdate=da_days.strftime("%Y-%m-%d")
               # print(wdate)

            else:
                wdate=creat_time.replace("年","-").replace("月","-").replace("日","").split(' ')[0]
               # print(wdate)

            if wdate==self.nowdate:
                datalists.append({'title': title, 'wurl': wurl, 'wdate': wdate})
                self.count+=1
        print("该站点共抓取到：{}条记录！".format(self.count))
        print(datalists)
        return datalists

