# coding=utf-8
import requests
import sys,time
from bs4 import BeautifulSoup

class Cnblog():

    def __init__(self, nowdate):

        self.urladds = [
            'http://www.cnblogs.com/cate/testing/',
            'http://www.cnblogs.com/cate/linux/',
            'http://www.cnblogs.com/cate/codelife/',
            'http://www.cnblogs.com/cate/php/'
        ]
        self.url_pre = 'http://www.cnblogs.com/'

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
                try:

                    soup = self.get_page(urladd + str(page))
                    divs = soup.find_all('div', class_='post_item_body')

                except:
                    print(sys.exc_info())

                do = False

                for div in divs:

                    do = True

                    # 日期判断
                    try:

                        title = div.find('a').text
                        wurl = div.find('a').get('href')
                        wdate = div.find('div', class_='post_item_foot').find('a').next_sibling.strip()[4:14]

                        # print(title)
                        # print(wurl)
                        # print(wdate)

                        if wdate == self.nowdate:

                            # 如果日期相同则保存
                            self.datalists.append({'wdate': wdate, 'title': title, 'wurl': wurl})

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
                    print(wdate)
                    time.sleep(1)
                    sys.stdout.write('.')
                    sys.stdout.flush()
                else:
                    # 下一个地址池
                    print("\n已抓取：" + str(self.count) + "条记录，继续抓取中...\n")
                    break


        if self.count == 0:
            print("\n今日无更新")
        else:
            print("\n该站点共抓取到：" + str(self.count) + "条记录！")
            print(self.datalists)

        return self.datalists