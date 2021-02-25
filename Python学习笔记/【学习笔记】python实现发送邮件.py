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