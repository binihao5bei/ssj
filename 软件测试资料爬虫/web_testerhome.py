# coding=utf-8
import requests
import lxml
import sys
from bs4 import BeautifulSoup

class Testerhome():

    def __init__(self, nowdate):

        self.urladds = [
            'https://testerhome.com/topics/excellent'
        ]
        self.url_pre = 'https://testerhome.com'

        self.count = 0
        self.datalists = []

        self.nowdate = nowdate

    # request 库调用
    def get_page(self, url):

        response = requests.get(url)
        response.encoding = 'utf-8'
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

                soup = self.get_page(urladd + "?page=" + str(page) + ".html")

                try:
                    divs = soup.find_all('div', class_='infos media-body')
                except:
                    print(sys.exc_info())

                do = False

                for div in divs:

                    do = True

                    # 日期判断
                    try:

                        title = div.find('a').get('title')
                        wurl = self.url_pre + div.find('a').get('href')
                        wdate = div.find('abbr',class_='timeago').text
                        wdate = wdate.replace('年','-')
                        wdate = wdate.replace('月', '-')
                        wdate = wdate.replace('日', '')

                        # print(title)
                        # print(wurl)
                        # print(wdate)

                        if wdate == self.nowdate:

                            # 如果日期相同则保存
                            self.datalists.append({'wdate': wdate, 'title': title, 'wurl': wurl})

                            self.count += 1
                            sys.stdout.write('.')
                            sys.stdout.flush()

                        # 如果日期比目标小，说明爬取结束
                        #elif wdate < self.nowdate:

                        # 翻页（适用于帖子不按日期排序按回复日期排序的情况）
                        elif page > 3 :

                            do = False
                            break

                    except:
                        # 如果有异常，则爬下一条
                        #print(sys.exc_info())
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