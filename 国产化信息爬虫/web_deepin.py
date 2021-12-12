# coding=utf-8
import requests
import sys
from bs4 import BeautifulSoup

class Deepin():

    def __init__(self, nowdate):

        self.urladds = [
            'https://www.deepin.org/zh/community-news/'
        ]
        self.url_pre = 'https://www.deepin.org/zh/'

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

                        title = ('【深度】'+div.find("header",class_="entry-header").find("a").string).replace('&','&amp;')
                        wurl = (div.find("header",class_="entry-header").find("a").get('href')).replace('&','&amp;')
                        month = div.find("span",class_="hs-month").string
                        day = div.find("span",class_="hs-day").string
                        year = div.find("span",class_="hs-year").string
                        wdate = year+"-"+month.replace("月","-")+day
                      

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

