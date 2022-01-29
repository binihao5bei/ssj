#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Time    : 2021/10/22 3:16 下午 
@File    : util.py
@Author  : zhangxue
@Desc    : 工具类
'''
from common.userData import *
from config import RunConfig
import datetime
"""获取当前时间"""
def get_nowtime():
    # now_time = datetime.datetime.now()
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return now_time



print(get_nowtime())


