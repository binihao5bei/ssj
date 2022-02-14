import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

SMTP_HOST = '邮箱SMTP地址'
SMTP_USER = '发件人邮箱'
SMTP_PWD = os.getenv('发件人密码')

def send_email(self, body, subject, receivers, file_path):
    msg = MIMEMultipart()
    msg.attach(MIMEText(body, 'html', 'utf-8'))

    att1 = MIMEText(open(file_path, 'rb').read(), 'base64', 'utf-8')
    att1['Content-Type'] = 'application/octet-stream'
    att1["Content-Disposition"] = f'attachment; filename={file_name}'
    msg.attach(att1)
    
    msg['From'] = SMTP_USER
    msg['To'] = ','.join(receivers)
    msg['Subject'] = subject
    
    smtp = smtplib.SMTP_SSL(SMTP_HOST)
    smtp.login(SMTP_USER, SMTP_PWD)
    for person in receivers:
        print(f'发送邮件给: {person}')
        smtp.sendmail(SMTP_USER, person, msg.as_string())
    print('邮件发送成功')