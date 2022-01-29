#! /usr/bin/env python3
# _*_ coding: utf-8 _*_

import warnings

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from config.common_config import DRIVER_PATH


class RunDriver(object):

    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            RunDriver.__instance = super().__new__(cls, *args, **kwargs)
        return RunDriver.__instance

    def __init__(self, dr_path=None, driver_name="Chrome"):
        """
        需要用到 FireFox 把 config 内的 geckodriver 复制到 /usr/local/bin 内;
        使用 Safari 需要把浏览器偏好设置内的开发标签打开，并勾选“允许自动化运行”
        使用时，引入该模块，RunDriver(dr_path='路径位置').run_driver(driver='浏览器名称')
        """
        warnings.simplefilter('ignore', ResourceWarning)
        self.dr_path = DRIVER_PATH if not dr_path else dr_path
        self.driver_name = driver_name
        self.driver = eval(f"webdriver.{self.driver_name}('{self.dr_path}')")
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)

    def run_driver(self, driver=None):
        if driver is None:
            return webdriver.Chrome(self.dr_path)
        elif driver == 'FireFox':
            return webdriver.Firefox()
        elif driver == 'Safari':
            return webdriver.Safari()
        elif driver == 'sys_ff':
            driver = webdriver.Remote(
                command_executor='http://172.16.100.249:5555/wd/hub',
                desired_capabilities=DesiredCapabilities.FIREFOX)
            return driver
        elif driver == 'sys_cr':
            driver = webdriver.Remote(
                command_executor='http://101.200.62.54:80/wd/hub',
                desired_capabilities=DesiredCapabilities.CHROME)
            return driver

    def get_driver(self):
        return self.driver


if __name__ == '__main__':
    rd = RunDriver()
    rd.get_driver().get('http://www.baidu.com')
