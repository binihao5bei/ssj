#! /usr/bin/env python3
# _*_ coding: utf-8 _*_

from base.find_element import FindElement


class Design(object):

    def __init__(self, driver):
        self.driver = driver

    # 设计页
    def design(self, email='n@n.com', pwd='123456'):
        # 设计页
        FindElement('input_email').find_element(self.driver).send_keys(email)
        self.driver.implicitly_wait(10)
        FindElement('input_password').find_element(self.driver).send_keys(pwd)
        self.driver.implicitly_wait(10)
        FindElement('button_login').find_element(self.driver).click()
        self.driver.implicitly_wait(10)


if __name__ == "__main__":
    pass
