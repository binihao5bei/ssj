 # coding=utf-8
import datetime

# ===站点定义
# from web_testerhome import Testerhome
# from web_ltest import Ltest
from web_51testing import Testing51
from web_cnblog import Cnblog
# ===微信爬虫站点定义
from wx_infoq import Wx_infoq
from wx_qunar import Wx_qunar
from wx_importnew import WX_importnew
from wx_zz import Wx_zz
from wx_dsj import Wx_dsj
from wx_sgcs import Wx_sgcs

# 自定义函数
from func import htmlmake, sendmailnow, add_wiki, tablemake

# ===站点类清单
weblist = []
# 网页爬虫
# weblist += [Testerhome, Testing51, Ltest, Cnblog]
weblist += [Testing51, Cnblog]
# 微信爬虫
# weblist += [Wx_infoq, Wx_qunar, WX_importnew, Wx_zz, Wx_dsj, Wx_sgcs]f
weblist += [WX_importnew, Wx_zz, Wx_dsj, Wx_sgcs]

# 初始化参数
datalists = []
nowdate = datetime.datetime.now().strftime('%Y-%m-%d')
# 每日最大发布记录条数
maxnum = 10

# ===测试用自定义日期
#nowdate = '2018-10-30'

# 遍历网站类列表
for webclass in weblist:
    # 类定义
    web = webclass(nowdate)
    # 数据获取
    datalists += web.get_data()

# 打印最终结果
print(datalists)
print("==总共抓取到：" + str(len(datalists)) + "条记录。")


# 发邮件
if __name__ == '__main__':
    if len(datalists) > 0:
        mail_msg = htmlmake(maxnum, datalists)
        nowdate = datetime.datetime.now().strftime('%Y-%m-%d')

        # 发布到wiki
        pageConnect = tablemake(datalists)
        add_wiki(str("2020-12-30"), pageConnect)

        #sendmailnow(["bussqa@sogou-inc.com", "setest@sogou-inc.com", "pdatest@sogou-inc.com"], "【今日最新消息】" + str(nowdate), mail_msg)
        #sendmailnow(["sunshijiang@sogou-inc.com"], "【今日最新消息】" + str(nowdate), mail_msg)
