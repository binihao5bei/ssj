#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Time    : 2021/10/19 6:51 下午 
@File    : config.py
@Author  : zhangxue
@Desc    : 配置信息
'''



import os
"""邮件配置"""
sender = '17600149541@163.com'  #发送方
receiver = '781929291@qq.com' #接收方
emailusername = '17600149541@163.com'  #登陆邮箱的用户名
emailpassword = 'WDTMGFMREVPRBKEE'  #登陆邮箱的授权码，客户端专用密码
server = 'smtp.163.com'  #smtp服务器
smtp_server_port = '25'


#项目配置
basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# page目录
pagePath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'page')

# case目录
casePath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'page')

#数据目录
dataPath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')

# 报告目录
reportPath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'report')

# os.path.abspath(path) #返回绝对路径
# os.path.basename(path) #返回文件名
# os.path.dirname(path) #返回文件路径
# os.path.join(path1[, path2[, ...]])  #把目录和文件名合成一个路径

