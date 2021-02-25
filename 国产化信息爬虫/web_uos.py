# coding=utf-8
import requests
import sys
from bs4 import BeautifulSoup
import datetime

class UOS():

    def __init__(self, nowdate):

        self.urladds = [
            'https://www.7uos.com/category/uos-news/'
        ]
        self.url_pre = 'https://www.7uos.com/'

        self.count = 0
        self.datalists = []

        self.nowdate = nowdate

    # request 库调用
    def get_page(self, url):

        response = requests.get(url)
#        response.encoding = 'gbk'
        soup = BeautifulSoup(response.text, 'lxml')
        return soup

    def get_data(self):


        print("本次爬取今日： [" + self.nowdate + "] 的数据记录。")

        for urladd in self.urladds:

            # 地址池遍历变量初始化
            do = True
            page = 1
            print("\n")
            print(urladd)
            sys.stdout.write('正在爬取，请稍候.')
            sys.stdout.flush()

            while (do):
                if page > 1:
                    soup = self.get_page(urladd+"page/" + str(page)+"/")
                else:
                    soup = self.get_page(urladd)

                try:
                    divs = soup.find_all("article")
                except:
                    print(sys.exc_info())

                do = False

                for div in divs:

                    do = True
                    # 日期判断
                    try:

                        title = ('【统信UOS】'+div.find("header",class_="entry-header").find("a").string).replace('&','&amp;')
                        wurl = (div.find("header",class_="entry-header").find("a").get('href')).replace('&','&amp;')
                        month = div.find("span",class_="date-month").string
                        day = div.find("span",class_="date-day").string
                        year = div.find("span",class_="date-year").string
                        wdate1 = year+"年"+ month + day+ "日"
                        wdate = datetime.datetime.strptime(wdate1,"%Y年%m月%d日").strftime("%Y-%m-%d")

                      

                        if wdate == self.nowdate:

                            # 如果日期相同则保存
                            self.datalists.append({'wdate': wdate, 'title': title, 'wurl': wurl.replace("..","https://www.ubuntukylin.com")})

                            self.count += 1
                            sys.stdout.write('.')
                            sys.stdout.flush()

                        elif wdate < self.nowdate:

                            # 如果日期比目标小，说明爬取结束
                            do = False
                            break

                    except:
                        # 如果有异常，则爬下一条
                        print(sys.exc_info())
                        pass

                if do:
                    # 下一页
                    page += 1
                    sys.stdout.write('.')
                    sys.stdout.flush()
                else:
                    # 下一个地址池
                    break


        if self.count == 0:
            print("\n今日无更新")
        else:
            print("\n该站点共抓取到：" + str(self.count) + "条记录！")
            print(self.datalists)

        return self.datalists
