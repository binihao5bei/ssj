 # coding=utf-8

'''
*****************************************
Author: SunShijiang
Date: 2021/11/3 15:06
FileName: run.py
IDE_Name: PyCharm
Email: huoyingcanai@outlook.com
Desc: 
*****************************************
'''


import datetime

# ===站点定义
# 本次默认爬取测试比较热门的测试技术论坛等网站，如：51testing、cnblog、领测技术、测试之家
# 后续再继续完善和补充热门的微信公众号爬虫，如：专知、测试沙龙、大数据文摘等

from web_testerhome import Testerhome
from web_ltest import Ltest
from web_51testing import Testing51
from web_cnblog import Cnblog
from web_softtest import SoftTest



# 自定义函数
from func import htmlmake, sendmailnow, feishi_send

# ===站点类清单
weblist = []
# 网页爬虫
weblist += [Testing51, Ltest, Cnblog,SoftTest]
#weblist += [Testing51, Cnblog, Ltest]
#weblist += [Testwo]

# 微信爬虫
# -----因时间有限，有空再补充微信公众号的爬虫------

# 初始化参数
F_datalists = []
nowdate = datetime.datetime.now().strftime('%Y-%m-%d')
# 每日最大发布记录条数
maxnum = 10

# ===测试用自定义日期
#nowdate = '2021-10-20'

# 遍历网站类列表
for webclass in weblist:
    # 类定义
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
print(datalists)
print("==总共抓取到：" + str(len(datalists)) + "条记录。")


# 发邮件
if __name__ == '__main__':
    if len(datalists) > 0:
        mail_msg = htmlmake(maxnum, datalists)
        #nowdate = datetime.datetime.now().strftime('%Y-%m-%d')

        ''''
        # 发布到wiki
        pageConnect = tablemake(datalists)
        add_wiki(str("2020-12-30"), pageConnect)
        '''
        # 发送到邮箱
        #sendmailnow(["bussqa@sogou-inc.com", "setest@sogou-inc.com", "pdatest@sogou-inc.com"], "【今日最新消息】" + str(nowdate), mail_msg)
        sendmailnow(["sunshijiang@jwzg.com"], "【测试技术日报】" + str(nowdate), mail_msg)

        # 发送到飞书
        feishi_send(datalists)
