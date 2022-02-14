import yagmail

sender='huoyingcanai@163.com'
passwd='ssj05111217'
receiver='sunshijiang@jwzg.com'

server=yagmail.SMTP(sender,passwd,host='smtp.163.com')

#发送文本：
text='这是一封yagmail发送文本的邮件'
title='这是标题'
# server.send(contents=text,to=receiver,subject=title)

# #发送图片：
img=yagmail.inline('./1.jpg')
server.send(contents=text,to=receiver,subject=title,attachments=img)

# #发送附件：
# fujian='./1.jpg'
# server.send(contents=text,to=receiver,subject=title,attachments=fujian)