 # coding=utf-8
import datetime
import time

# ===web网站站点定义
from web_xinchuang import Xinch

# 自定义函数
from func import htmlmake, sendmailnow

# ===站点类清单
weblist = []
# 网页爬虫
#weblist += [Ukylin]
weblist += [Xinch]
# 微信爬虫
#weblist += [Wx_ukylin]

# 初始化参数
F_datalists = []
#nowdate = datetime.datetime.now().strftime('%Y-%m-%d')
# 每日最大发布记录条数
maxnum = 30

# ===测试用自定义日期
nowdate = '2020-12-28'

# 遍历网站类列表
for webclass in weblist:
    # 类定义Kylin
    web = webclass(nowdate)
    # 数据获取
    F_datalists += web.get_data()

#列表根据里面的字典key（title）去重

datalists=[]
values=[]
for d in F_datalists:
    if d['title'] not in values:
        datalists.append(d)
    values.append(d['title'])

# 打印最终结果
#print(datalists)
print("==总共抓取到：" + str(len(datalists)) + "条记录。")
'''
# 写数据库
if len(datalists)>0:
    add_db(datalists)
'''
# 发邮件
if __name__ == '__main__':
    if len(datalists) > 0:
        mail_msg = htmlmake(maxnum, datalists)
        nowdate = datetime.datetime.now().strftime('%Y-%m-%d')
        sendmailnow(["sunshijiang@sogou-inc.com"], "【今日最新消息】" + str(nowdate), mail_msg)
'''
        # 发布到wiki
        pageConnect = tablemake(datalists)
        add_wiki(str(nowdate), pageConnect)
'''
        
        # sendmailnow(["sunxiao@sogou-inc.com"], "【今日最新消息】" + str(nowdate), mail_msg)
