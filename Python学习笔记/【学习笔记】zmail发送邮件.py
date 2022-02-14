import zmail

sender='huoyingcanai@163.com'
passwd='ssj05111217'
receiver='sunshijiang@jwzg.com'

#发送文本：
body1={
    'subject':'【zamil发送邮件文本】',
    'content_text':'这是邮件测试文本哦'
}


#发送html:
body2={
    'subject':'【zamil发送邮件html】',
    'content_html':'''
    <h1>发送html测试</h1>
    <h3>测试1</h3>
    <table>
        <tr>
            <th>name</th>
            <th>age</th>
        </tr>
        <tr>
            <td>xiaoming</td>
            <td>34</td>
        </tr>
    </table>  
    '''
}


#发送附件：
body3={
    'subject':'【zamil发送邮件附件】',
    'content_text':'这是邮件测试附件哦',
    'attachments':'./1.jpg'
}

server=zmail.server(sender,passwd)
server.send_mail(receiver,body3)