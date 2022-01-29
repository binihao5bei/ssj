#! /usr/bin/env python3
# _*_ coding: utf-8 _*_

from base.find_element import FindElement


class Register(object):

    def __init__(self, driver):
        self.driver = driver
        self.fe = FindElement(self.driver, section='RegisterElement')

    # 注册
    def register(self, email='00@03.com', pwd='123456'):
        # 注册
        self.fe.get_element('register_email').send_keys(email)
        self.fe.get_element('register_pwd').send_keys(pwd)
        self.fe.get_element('register_button').click()


if __name__ == "__main__":
    pass
