 # coding=utf-8
import datetime
import time

# ===web网站站点定义
from web_ukylin import Ukylin
from web_kylin import Kylin
from web_deepin import Deepin
from web_xinchuang import Xinch
from web_shurufa import Shurufa
from web_gcczxt import Gcczxt
#from web_IThome import IThome
from web_uos import UOS
# ===微信爬虫站点定义
from wx_search import WX_search

# ===微博爬虫站点定义
from wb_ukylin import Wb_ukylin
from wb_neokylin import Wb_neokylin
from wb_uos import Wb_uos

# 自定义函数
from func import htmlmake, sendmailnow, add_db, add_wiki, tablemake

# ===站点类清单
weblist = []
# 网页爬虫
#weblist += [Ukylin]
weblist += [Ukylin,Kylin,Deepin,WX_search,Wb_ukylin,Wb_uos,Xinch,Shurufa,Gcczxt]
#weblist += [Ukylin,Kylin,Deepin,UOS,Wb_ukylin,Wb_neokylin,Xinch,Shurufa,Gcczxt]
# 微信爬虫
#weblist += [Wx_ukylin]

# 初始化参数
F_datalists = []
nowdate = datetime.datetime.now().strftime('%Y-%m-%d')
# 每日最大发布记录条数
maxnum = 30

# ===测试用自定义日期
#nowdate = '2021-01-01'

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
    if d['title'].split('】')[1] not in values:
        datalists.append(d)
    values.append(d['title'].split('】')[1])

# 打印最终结果
#print(datalists)
print("==总共抓取到：" + str(len(datalists)) + "条记录。")


# 发邮件
if __name__ == '__main__':
    if len(datalists) > 0:
        mail_msg = htmlmake(maxnum, datalists)
        nowdate = datetime.datetime.now().strftime('%Y-%m-%d')
        sendmailnow(["ImeToB@sogou-inc.com"], "【信创今日最新消息】" + str(nowdate), mail_msg)
        #sendmailnow(["sunshijiang@sogou-inc.com"], "【信创今日最新消息】" + str(nowdate), mail_msg)
        


        #发布到wiki
        pageConnect = tablemake(datalists)
        add_wiki(str(nowdate), pageConnect)

        #sendmailnow(["sunshijiang@sogou-inc.com"], "【信创今日最新消息】" + str(nowdate), mail_msg)

