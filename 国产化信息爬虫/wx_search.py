# coding=utf-8
from selenium import webdriver
import time
import json
import requests
import re
import random
import sys


#设置要爬取的公众号列表
#gzlist=['优麒麟开源操作系统','深度操作系统','统信软件']
#获取当前系统时间
'''
times=time.time()
timeArray=time.localtime(times)
LocalTime=time.strftime("%Y-%m-%d",timeArray)
'''
#LocalTime='2020-12-13'

class WX_search():

    def __init__(self, nowdate):
        self.url ='https://mp.weixin.qq.com'

        self.count = 0
        self.nowdate = nowdate
        self.gzlist=['优麒麟开源操作系统','深度操作系统','统信软件','自助可控新鲜事','信创纵横','工信智谷信创研究院','龙芯中科','特大号','晋江信创服务','信创产业发展']

    def weChat_login(self,url):
        #定义一个空的字典，存放cookies内容
        post={}

        #用webdriver启动谷歌浏览器
        print("启动浏览器，打开微信公众号登录界面")
        driver = webdriver.Edge(executable_path=r'E:\Python\Scripts\msedgedriver.exe')
        #打开微信公众号登录页面
        driver.get(url)
        # 获取账号输入框
        driver.find_element_by_xpath("//a[@class='login__type__container__select-type']").click()
        ID = driver.find_element_by_xpath("//input[@name='account']")
        # 获取密码输入框
        PW = driver.find_element_by_xpath("//input[@name='password']")
        # 输入账号
        id = 'vifereo1024@gmail.com'
        pw = 'Ssj05111217'
        # id = input('请输入账号:')
        # pw = input('请输入密码:')
        ID.send_keys(id)
        PW.send_keys(pw)
        # 获取登录button，点击登录
        driver.find_element_by_class_name('btn_login').click()
     

        # 拿手机扫二维码！
        print("请拿手机扫码二维码登录公众号")
        time.sleep(10)
        print("登录成功")
        #重新载入公众号登录页，登录之后会显示公众号后台首页，从这个返回内容中获取cookies信息
        driver.get(url)
        #获取cookies
        cookie_items = driver.get_cookies()

        #获取到的cookies是列表形式，将cookies转成json形式并存入本地名为cookie的文本中
        for cookie_item in cookie_items:
            post[cookie_item['name']] = cookie_item['value']
        cookie_str = json.dumps(post)
        with open('cookie.txt', 'w+') as f:
            f.write(cookie_str)
        print("cookies信息已保存到本地")

    #爬取微信公众号文章，并存在本地文本中
    def get_data(self):
        urladd=self.url
        datalists=[]
        login=self.weChat_login(urladd)
        cut=self.count
        print("-"*40)
        print("本次爬取今日： [" + self.nowdate + "] 的数据记录。")
 #       datalists=[]
        for query in self.gzlist:

            print("开始爬取公众号："+query)
            #query为要爬取的公众号名称
            #公众号主页
            self.url = 'https://mp.weixin.qq.com'
            #设置headers
            header = {
                "HOST": "mp.weixin.qq.com",
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
            }

            #读取上一步获取到的cookies
            with open('cookie.txt', 'r') as f:
                cookie = f.read()
            cookies = json.loads(cookie)

            #登录之后的微信公众号首页url变化为：https://mp.weixin.qq.com/cgi-bin/home?t=home/index&lang=zh_CN&token=1849751598，从这里获取token信息
            response = requests.get(url=self.url, cookies=cookies)
            token = re.findall(r'token=(\d+)', str(response.url))[0]

            #搜索微信公众号的接口地址
            search_url = 'https://mp.weixin.qq.com/cgi-bin/searchbiz?'
            #搜索微信公众号接口需要传入的参数，有三个变量：微信公众号token、随机数random、搜索的微信公众号名字
            query_id = {
                'action': 'search_biz',
                'token' : token,
                'lang': 'zh_CN',
                'f': 'json',
                'ajax': '1',
                'random': random.random(),
                'query': query,
                'begin': '0',
                'count': '5'
            }
            #打开搜索微信公众号接口地址，需要传入相关参数信息如：cookies、params、headers
            search_response = requests.get(search_url, cookies=cookies, headers=header, params=query_id)
            #取搜索结果中的第一个公众号
            lists = search_response.json().get('list')[0]
            #获取这个公众号的fakeid，后面爬取公众号文章需要此字段
            fakeid = lists.get('fakeid')

            #微信公众号文章接口地址
            appmsg_url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?'
            #搜索文章需要传入几个参数：登录的公众号token、要爬取文章的公众号fakeid、随机数random
            query_id_data = {
                'token': token,
                'lang': 'zh_CN',
                'f': 'json',
                'ajax': '1',
                'random': random.random(),
                'action': 'list_ex',
                'begin': '0',#不同页，此参数变化，变化规则为每页加5
                'count': '5',
                'query': '',
                'fakeid': fakeid,
                'type': '9'
            }
            #打开搜索的微信公众号文章列表页
            appmsg_response = requests.get(appmsg_url, cookies=cookies, headers=header, params=query_id_data)
            query_fakeid_response = requests.get(appmsg_url, cookies=cookies, headers=header, params=query_id_data)
            fakeid_list = query_fakeid_response.json().get('app_msg_list')
            #print(fakeid_list)


            cunt=self.count
            dls=[]
            for item in fakeid_list:
                
                content_link=(item.get('link')).replace('&','&amp;')
                content_title=('【{}】'.format(query)+item.get('title')).replace('&','&amp;')
                tm=item["update_time"]
                timeArray=time.localtime(tm)
                content_time=time.strftime("%Y-%m-%d",timeArray)
                fileName=query+'.txt'
                if content_time ==self.nowdate:
                    dls.append({'wdate':content_time,'title':content_title,'wurl':content_link})
                    cunt +=1
                    #print(content_title+":\n"+content_link+"\n"+content_time)
                elif content_time < self.nowdate:
                    break

            if cunt==0:
                print("\n今日无更新")
                print("*"*40)
            else:
                print("\n该站点共抓取到：" + str(cunt) + "条记录！")
                print(dls)
                print("*"*40)
            time.sleep(2)
            datalists+=dls
        
        print("爬取完成！")
        print("*"*40)
        return datalists
     
#WX_search.weChat_login()
#WX_search.get_data()
