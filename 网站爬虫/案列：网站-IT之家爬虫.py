# coding=utf-8
import requests
import sys
from bs4 import BeautifulSoup

session=requests.Session()
headers={"User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) App leWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"}

class IThome():

    def __init__(self, nowdate):

        self.urladds = [
            'https://www.ithome.com/search/adt_all_uos_0.html',
            'https://www.ithome.com/search/adt_all_%E9%93%B6%E6%B2%B3%E9%BA%92%E9%BA%9F_0.html',
            'https://www.ithome.com/search/adt_all_%E4%B8%AD%E6%A0%87%E9%BA%92%E9%BA%9F_0.html',
            'https://www.ithome.com/search/adt_all_%E5%9B%BD%E4%BA%A7%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F_0.html',
            'https://www.ithome.com/search/adt_all_%E4%BF%A1%E5%88%9B_0.html'
        ]
        
        
 #       self.url_pre = 'https://www.ubuntukylin.com/'


        self.count = 0

        self.datalists = []

        self.nowdate = nowdate

    # request 库调用
    def get_page(self, url):

        response = session.get(url,headers=headers)
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
                soup = self.get_page(urladd)

                try:
                    divs = soup.find_all("div",class_="c")
                except:
                    print(sys.exc_info())

                do = False

                for div in divs:

                    do = True
                    # 日期判断
                    try:

                        title = (div.find("a").string).replace('&','&amp;')
                        wurl = (div.find("a").get("href")).replace('&','&amp;')
                        wdate = "2020-"+div.find("div",class_="d").string.replace("月","-").replace("日","")
                      

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
