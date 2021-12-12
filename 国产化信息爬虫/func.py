# coding=utf-8

import random
#import MySQLdb
import pymysql
import requests
from requests.auth import HTTPBasicAuth
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
        	border: 1px solid #000000;
        }

        </style>
        </head>

        <body>

                <table style="width: 750px;border-radius: 4px;" class="style1" cellspacing="1" cellpadding="1"  >
        	      <caption style="margin-bottom:0;text-align: center;background-color:#FFA500;"><h1>╠︽︾ ToB NEWS ︾︽╣</h1></caption>
        	        <tr style="background-color:#FFD700">

        		      <th class="style3" style="width: 30px; height: 25px;" align='center'>点击查看</th>
        		      <th class="style3" style="width: 250px" align='center'>标题</th>
        	        </tr>

        """

        # 随机取
        if len(datalists) < maxnum:
            maxnum = len(datalists)

        data_show = random.sample(datalists, maxnum)

        for data in data_show:
            message += """

                <tr style="background-color:#FFF8DC">
            		<td class="style3" style="width: 30px; height: 25px;" align='center'>
            		<a href='""" + data['wurl'] + """' target="_blank">查看</a></td>
            		<td class="style3" style="width: 250px" align='left'>""" + data['title'] + """</td>
            	</tr>


                """
        # HTML尾
        message += """
        		<tr>
        			<th colspan="2" style="background-color:#F0E68C;clear:both;text-align:center;">Builder:</font></i></b> <font face="arial">sunshijiang@sogou-inc.com</font><br/>
        			<font face="arial" size="3">搜狗输入法-ToB国产化-测试组</font><br>
        			<font face="arial" size="2">© 2020 SOGOU.COM 有任何问题请随时联系我~</font>
        			
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

def tablemake(datalists):

        # HTML头
        message = """
            <table class="style1 confluenceTable" cellspacing="0" cellpadding="0">
                <tr>
                    <th class="style3 confluenceTh numberingColumn" contenteditable="true">序号</th>
                    <th class="style3 confluenceTh">标题</th>
                </tr>
        """
        i=1
        for data in datalists:
            message += """
                <tr>
                    <td class="style3 confluenceTd numberingColumn" contenteditable="false">""" + str(i) +"""</td>
                    <td class="style3 confluenceTd" ><a href='""" + data['wurl'] + """' target="_blank">""" + data['title'] + """</a></td>
                </tr>
                """
            i = i+1
        # HTML尾
        message += """
            </table>
        """
        print(message)
        return message



# 邮件
# 第三方 SMTP 服务
mail_host = "mail.sogou-inc.com"  # 设置服务器
mail_user = "venus@sogou-inc.com"  # 用户名
mail_pass = "vns-2014"  # 口令


def sendmailnow(To, Title, mail_msg, From="venus@sogou-inc.com"):
    # @
    #    From：发件人
    #    To：收件人
    #    Title：邮件标题
    #    mail_msg：邮件内容（可以是html，或文本）
    #    主题信息
    message = MIMEText(mail_msg, 'html', 'utf-8')
    message['From'] = Header(From, 'utf-8')
    message['To'] = Header("; ".join(To), 'utf-8')

    #   subject = 'Python SMTP 邮件测试'
    message['Subject'] = Header(Title, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(From, To, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")


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
    space_key = "IMEQA"
    page_connect = connect


    data = json.dumps({"type":"page","title":page_title,"ancestors":[{"id":12976968}], "space":{"key":space_key},"body":{"storage":{"value":page_connect,"representation":"storage"}}})
    #data = json.dumps({"type":"page","title":page_title,"ancestors":[{"id":6488246}], "space":{"key":space_key},"body":{"storage":{"value":page_connect,"representation":"storage"}}})
    headers = {"Content-Type":"application/json;charset=UTF-8"}
    auth = HTTPBasicAuth(uname, upassword)

    r = requests.post(url, data=data, headers=headers, auth=auth)
    print(r.content)

