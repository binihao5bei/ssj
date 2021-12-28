# coding=utf-8
'''
*****************************************
Author: SunShijiang
Date: 2021/11/3 15:06
FileName: func.py
IDE_Name: PyCharm
Email: huoyingcanai@outlook.com
Desc:
*****************************************
'''
import random
#import MySQLdb
#import pymysql
import requests
#from requests.auth import HTTPBasicAuth
import json
import datetime

# 邮件类
import smtplib
from email.mime.text import MIMEText
from email.header import Header


# HTML页面生成
def htmlmake(maxnum, datalists):

        # HTML头
        message = """

        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml">

        <head>
        <meta http-equiv="Content-Language" content="zh-cn" />
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <title>结果</title>
        <style type="text/css">
        .style1 {
    	border-style: solid;
    	border-width: 1px;
        }
        .style3 {
        	text-align: center;
        	border: 1px solid #000000;
        }

        </style>
        </head>

        <body>

        <table style="width: 750px" class="style1" cellspacing="0" cellpadding="0">
        	<tr style="background-color:#fce5cd">
        		<td class="style3" style="width: 30px; height: 25px;"><font face="arial" size="3"><b>点击查看</b></font></td>
        		<td class="style3" style="width: 250px"><font face="arial" size="4"><b>标题</b></font></td>
        	</tr>

        """

        # 随机取
        if len(datalists) < maxnum:
            maxnum = len(datalists)

        data_show = random.sample(datalists, maxnum)

        for data in data_show:
            message += """

                <tr style="background-color:#FFF8DC">
            		<td class="style3" style="width: 30px; height: 25px;">
            		<a href='""" + data['wurl'] + """' target="_blank">查看</a></td>
            		<td class="style3" style="width: 250px">""" + data['title'] + """</td>
            	</tr>

                """
        # HTML尾
        message += """
        	<tr>
        			<th colspan="2" style="background-color:#fce5cd;clear:both;text-align:center;">
        			<font face="arial">Builder: sunshijiang@jwzg.com</font><br/>
        			<font face="arial" size="2">主站产品技术部-测试部-主站</font><br>
        			<font face="arial" size="2">© 2021 JWZG.COM 有任何问题请随时联系我~</font>
        			
                    </th>
        	    
        	    </tr>

        </table>
        </body>
        </html>

        """

        # 调试用，本地浏览HTML
        '''
        f = open('tmp.html', 'w', encoding='utf-8')
        f.write(message)
        f.close()
        webbrowser.open('tmp.html',new=1)


        '''

        return message




#用于飞书机器人发送
def feishi_send(datalists):
    # 个人小群
    url = "https://open.feishu.cn/open-apis/bot/v2/hook/1e381ec2-9707-4831-9c9d-05ca6d2309ea"

    token_body = {
        "app_id": "cli_9fde208be0bf500c",
        "app_secret": "f7M6acNPllMq529vqDwKFfhpQNTwX6CN"
    }
    headers = {"Content-type": "application/json"}

    #飞书消息卡片头部信息模板代码
    data = {
        "msg_type": "interactive",
        "card": {
            "config": {
                "wide_screen_mode": True
            },
            "header": {
                "template": "yellow",
                "title": {
                    "i18n": {
                        "en_us": "How would you use Sheets if specific permission settings are supported?",
                        "ja_jp": "How would you use Sheets if specific permission settings are supported?",
                        "zh_cn": f"📊 【测试技术日报】{datalists[0]['wdate']}"
                    },
                    "tag": "plain_text"
                }
            },
            "i18n_elements": {
                "zh_cn": [
                    {
                        "alt": {
                            "content": "",
                            "tag": "plain_text"
                        },
                        "img_key": "img_v2_04787a5c-c05f-4032-8a22-eda9cc244acg",
                        "tag": "img"
                    }

                ]
            }
        }
    }

    #消息卡片尾部Note模板代码
    Note_insert = {
        "elements": [
            {
                "content": "💡本栏目每天为你带来测试技术分享，你想在这里看到什么样的帖子？给我留言吧 😘（---By.SunShijiang）",
                "tag": "plain_text"
            }
        ],
        "tag": "note"
    }

    #限制最大显示数量为20条
    if len(datalists) < 50:
        maxnum = len(datalists)

    data_show = random.sample(datalists, maxnum)

    for dd in data_show:
        #爬虫数据模板插入代码
        data_insert = {
            "tag": "div",
            "text": {
                "content": f"[点击查看 >>]({dd['wurl']})  {dd['title']}",
                "tag": "lark_md"
            }
        }

        #分割线模板插入代码
        fenge_insert = {
            "tag": "hr"
        }

        # 飞书消息卡片完整模板代码 = 头部信息模板 + 爬虫数据内容模板 + 分割线模板 + 尾部Note模板
        data['card']['i18n_elements']['zh_cn'].append(data_insert)
        data['card']['i18n_elements']['zh_cn'].append(fenge_insert)
    data['card']['i18n_elements']['zh_cn'].append(Note_insert)
    try:
        auth = requests.post(url=url, data=json.dumps(data), headers=headers)
        print("发送飞书成功！")
        return auth
    except:
        print("发送飞书失败，请查看具体请求是否报错")


# 邮件
# 第三方 SMTP 服务
mail_host = "smtp.163.com"  # 设置服务器
mail_user = "huoyingcanai"  # 用户名
mail_pass = "ssj05111217"  # 口令
sender="huoyingcanai@163.com"
receives=['sunshjiang@jwzg.com']


def sendmailnow(To, Title, mail_msg, From=sender):
    # @
    #    From：发件人
    #    To：收件人
    #    Title：邮件标题
    #    mail_msg：邮件内容（可以是html，或文本）
    #    主题信息
    message = MIMEText(mail_msg, 'html', 'utf-8')
    message['From'] =sender
    message['To'] = ';'.join(receives)

    subject = 'Python SMTP 邮件测试'
    message['Subject'] = Header(Title, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(From, To, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")

'''
# 数据库
def add_db(datalists):

    # 写数据库
    # ===参数初始化
    username = 'root'
    dbpd = 'root'
    ipadd = '10.160.67.188'
    dbname = 'sp_test'

    # sqlite3数据库
    # conn = sqlite3.connect('cs.db')

    # MYSQL数据库
    #conn = MySQLdb.connect(ipadd, username, dbpd, dbname, charset='utf8')
    conn = pymysql.connect(ipadd, username, dbpd, dbname, charset='utf8')

    cursor = conn.cursor()

    # 写数据库
    # print("INSERT into xdldwd (qs,num) VALUES ('" + qs + "', '" + str(rec) + "')")

    blist = ['招聘', '培训']

    for data in datalists:
        bl = False

        for bl_data in blist:

            if bl_data in data['title']:

                bl = True
                print('Block:'+data['title'])

        if not bl:

            try:
                cursor.execute(
                    "INSERT into news (datestr, title, url) VALUES ('" + data['wdate'] + "', '" + data['title'] + "', '" +
                    data['wurl'] + "')")
                conn.commit()
            except:
                pass
            else:
                pass

    print("写数据库成功！")
    # 关闭数据库
    conn.close()

# 函数结束===========


# 将获取到的信息发布到wiki中
# curl -u venus:vns-2014 -X POST -H 'Content-Type: application/json' -d '{"type":"page","title":"new p22222age","ancestors":[{"id":6488246}], "space":{"key":"knowledge"},"body":{"storage":{"value":"<p>This is a new page</p>","representation":"storage"}}}' http://wiki.qa.sogou/rest/api/content/
def add_wiki(title, connect):
    uname = "venus"
    upassword = "vns-2014"
    url = "http://wiki.qa.sogou/rest/api/content/"

    page_title = title
    space_key = "knowledge"
    page_connect = connect


    data = json.dumps({"type":"page","title":page_title,"ancestors":[{"id":6488246}], "space":{"key":space_key},"body":{"storage":{"value":page_connect,"representation":"storage"}}})
    headers = {"Content-Type":"application/json"}
    auth = HTTPBasicAuth(uname, upassword)

    r = requests.post(url, data=data, headers=headers, auth=auth)

'''
