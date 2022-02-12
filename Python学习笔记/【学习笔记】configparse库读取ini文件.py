import configparser,sys

a=configparser.ConfigParser()
print(a.read('./【学习笔记】configparse库读取ini文件.ini',encoding="utf-8-sig"))
#b=a.get(section='DEFAULT',option='Compression')
#print(b)
print('*'*30)
#获取所有section
print(f'所有section：{a.sections()}')
print('*'*30)
#获取指定section下所有的option内容（key，value）
print(a.items('Default'))
print(a.items('bitbucket.org'))
print(a.items('topsecret.server.com'))
print('*'*30)
#获取所有section下所有的option
print(f"指定section=Default下所有option：{a.options('Default')}")
print(f"指定section=bitbucket.org下所有option：{a.options('bitbucket.org')}")
print(f"指定section=topsecret.server.com下所有option：{a.options('topsecret.server.com')}")
print('*'*30)
#获取指定section下指定option的value值
print(f"指定section=Default下指定option=serveraliveinterval的value值：{a.get(section='Default',option='serveraliveinterval')}")
print(f"指定section=bitbucket.org下指定option=user的value值：{a['bitbucket.org']['user']}")
