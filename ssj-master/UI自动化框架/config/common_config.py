#! /usr/bin/env python3
# _*_ coding: utf-8 _*_

import os


BASE_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# .ini 文件路径 存储 元素的相关信息
INI_FILE_PATH = os.path.join(BASE_PATH, 'config/page_element.ini')
IMG_INI_FILE_PATH = os.path.join(BASE_PATH, 'config/img_path.ini')
CONSTANT_INI_FILE_PATH = os.path.join(BASE_PATH, 'config/constant.ini')
# 查找元素的超时时间
TIMEOUT = 5
# 查找元素的轮询时间
FIND_INTERVAL = 0.5     # 默认 POLL_FREQUENCY 参数就是 0.5
# 日志目录
LOG_BASE_PATH = os.path.join(BASE_PATH, 'logs')
# 测试报告目录
REPORT_PATH = os.path.join(BASE_PATH, 'report')
# 测试用例目录
TEST_CASE_PATH = os.path.join(BASE_PATH, 'case')
# 登录地址
LOGIN_URL = "https://dev.lanhuapp.com/web/#/user/login"
# 主页地址
HOME_URL = "https://dev.lanhuapp.com/web/#/item"
# 线上登录地址
LOGIN_URL_ONLINE = "https://lanhuapp.com/web/#/user/login"
# 线上注册地址
REGISTER_URL_ONLINE = "https://lanhuapp.com/web/#/user/register?isPhone=0"
# 浏览器驱动路径
DRIVER_PATH = os.path.join(BASE_PATH, "config/chromedriver_92_0_4515")
# 图片目录 路径
IMG_PATH = os.path.join(BASE_PATH, 'images')
# 元素操作后等待时间
LONG_TIME = 3
SHORT_TIME = 1
# 验证邀请链接
INVITE_LINK = "https://dev.lanhuapp.com/url"


if __name__ == "__main__":
    pass
