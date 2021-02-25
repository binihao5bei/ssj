# coding=utf-8
import requests
import lxml
import json
import sys
from bs4 import BeautifulSoup
import time,datetime
import webbrowser

class Pc_wx():

    def __init__(self, nowdate, urladds, url_pre):

        self.urladds = urladds
        self.url_pre = url_pre
        self.count = 0
        self.datalists = []
        self.nowdate = nowdate
        self.sleeptime = [2,12]

    # request 库调用
    def get_page(self, url):
        #headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2859.0 Safari/537.36'}
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36 QQBrowser/3.9.3943.400",'X-Requested-With': 'XMLHttpRequest'}
        response = requests.get(url)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'lxml')
        return soup

    def get_data(self):
        try:
            print("本次爬取今日： [" + self.nowdate + "] 的数据记录。")
            time.sleep(self.sleeptime[0])
            # 地址池遍历变量初始化
            do = True
            page = 1
            print("\n")
            print(self.urladds, '正在进入...')
            # 搜索关键字
            soup = self.get_page(self.url_pre)
            # print(soup)

            # 验证信息
            while (str(soup).find('请输入验证码') > 0):
                print('\n验证请求！请输入验证码，15秒后自动重试:')
                content = soup.find('p', class_='p4')
                webbrowser.open('https://weixin.sogou.com/antispider/?from=' + content.find(
                    'input').next_sibling.next_sibling.next_sibling.next_sibling.get('value'), new=1)
                time.sleep(self.sleeptime[1])
                soup = self.get_page(self.url_pre)

            time.sleep(self.sleeptime[0])
            sys.stdout.write('正在爬取，请稍候.')
            sys.stdout.flush()

            divs = soup.find_all('div', class_='gzh-box2')
            for div in divs:
                url_act = div.find('a').get('href')
                break

            # print(url_act)

            # 搜索结果重链
            soup2 = self.get_page(url_act)
            # print(soup2)

            # 验证信息
            while (str(soup2).find('请输入验证码') > 0):
                print('\n验证请求！请输入验证码，15秒后自动重试:')
                webbrowser.open(url_act, new=1)
                time.sleep(self.sleeptime[1])
                soup2 = self.get_page(url_act)

            # 字符串解析
            result = str(soup2)[str(soup2).find('msgList') + 10:str(soup2).find('seajs.use') - 10]
            # print(result)

            # 主爬虫
            result_js = json.loads(result)['list']
            for result_j in result_js:

                # 日期判断
                wdate = str(datetime.datetime.fromtimestamp(result_j['comm_msg_info']['datetime'])).split(' ')[0]
                if wdate != self.nowdate: break

                title = result_j['app_msg_ext_info']['title']
                wurl = 'https://mp.weixin.qq.com' + result_j['app_msg_ext_info']['content_url'].replace('amp;', '')
                self.count += 1
                self.datalists.append({'wdate': wdate, 'title': title, 'wurl': wurl})

                # 同一日期下更多条目
                for result_m in result_j['app_msg_ext_info']['multi_app_msg_item_list']:
                    title = result_m['title']
                    wurl = 'https://mp.weixin.qq.com' + result_m['content_url'].replace('amp;', '')
                    self.count += 1
                    self.datalists.append({'wdate': wdate, 'title': title, 'wurl': wurl})

            # 统计返回
            if self.count == 0:
                print("\n今日无更新")
            else:
                print("\n该站点共抓取到：" + str(self.count) + "条记录！")
                print(self.datalists)
        except:
            pass
        return self.datalists
