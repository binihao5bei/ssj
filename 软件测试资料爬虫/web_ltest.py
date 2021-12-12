# coding=utf-8
import requests
import sys
from bs4 import BeautifulSoup

class Ltest():

    def __init__(self, nowdate):

        # 子地址池
        self.urladds = [
            'http://www.ltesting.net/ceshi/ceshijishu/list_1_',
            'http://www.ltesting.net/ceshi/open/list_3_'
        ]
        # 网站头地址
        self.url_pre = 'http://www.ltesting.net'

        # 计数
        self.count = 0
        # 存放抓取记录
        self.datalists = []
        # 日期
        self.nowdate = nowdate

    # request 库调用
    def get_page(self, url):

        response = requests.get(url)
        response.encoding = 'gbk2312'
        soup = BeautifulSoup(response.text, 'lxml')
        return soup

    # 获取网站信息函数
    def get_data(self):

        print("本次爬取今日： [" + self.nowdate + "] 的数据记录。")

        # 遍历地址池
        for urladd in self.urladds:

            # 地址池遍历变量初始化
            do = True
            page = 1
            print("\n")
            print(urladd)
            sys.stdout.write('正在爬取，请稍候.')
            sys.stdout.flush()

            # 如果文章日期不比需要的日期小，则往下翻页选文章
            while (do):

                # 爬虫
                soup = self.get_page(urladd + str(page) + ".html")
                try:
                    divs = soup.find('ul', class_='lt_sec_list').find_all('li')
                except:
                    print(sys.exc_info())

                do = False

                for div in divs:

                    do = True

                    # 日期判断
                    try:

                        title = div.find('a').next_sibling.text
                        wurl = self.url_pre + div.find('a').next_sibling.get('href')
                        wdate = div.find('small').text[4:]

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