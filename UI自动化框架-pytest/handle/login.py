#! /usr/bin/env python3
# _*_ coding: utf-8 _*_

from base.find_element import FindElement


class Login(object):

    def __init__(self, driver):
        self.driver = driver
        self.fe = FindElement(self.driver)

    # 登录
    def login(self, email='n@n.com', pwd='123456'):
        # 登录
        self.fe.get_element('input_email').send_keys(email)
        self.fe.get_element('input_password').send_keys(pwd)
        self.fe.get_element('button_login').click()


if __name__ == "__main__":
    pass
