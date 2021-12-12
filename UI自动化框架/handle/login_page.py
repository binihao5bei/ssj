#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create by shiyang on 2021/8/27

"""登录页面：登录、注册、忘记密码"""


import time

from base.find_element import FindElement2
from config.common_config import LOGIN_URL


def login(driver, name="shiyang@jwzg.com", passwd="123456"):
    """给一个默认的登录账号"""
    driver.get(LOGIN_URL)
    find_util = FindElement2(driver, node="Login")
    name_ele = find_util.get_element("name")
    passwd_ele = find_util.get_element("password")
    login_btn_ele = find_util.get_element("login_btn")

    name_ele.clear()
    name_ele.send_keys(name)
    time.sleep(1)

    passwd_ele.clear()
    passwd_ele.send_keys(passwd)
    time.sleep(1)

    login_btn_ele.click()


if __name__ == '__main__':
    # login(driver_demo, 'shiyang@jwzg.com', '123456')
    pass
