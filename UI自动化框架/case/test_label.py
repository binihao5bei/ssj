#! /usr/bin/env python3
# _*_ coding: utf-8 _*_

import unittest

from base.running_log import RunningLog
from base.running_driver import RunDriver
from base import running_driver
from handle.login import Login
from util.util import *


class TestLabel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.log = RunningLog(logger='Label')
        cls.logger = cls.log.get_log()

    def setUp(self):
        rd = RunDriver()
        self.url = running_driver.web_url()
        self.driver = rd.run_driver()
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.driver.get(self.url)
        self.driver.implicitly_wait(10)

    def test01_login_success(self):
        lg = Login(self.driver)
        lg.login()
        try:
            time.sleep(6)
            pil_screenshot('login_success')
            time.sleep(2)
            self.assertTrue(tesseract_content('设 计 规 范', 'login_success'))
            self.logger.info('登录成功')
        except:
            self.logger.error('未找到【设 计 规 范】字样')
            raise AssertionError

    def tearDown(self):
        time.sleep(2)
        self.driver.quit()

    @classmethod
    def tearDownClass(cls):
        cls.log.close_handle()


if __name__ == "__main__":
    unittest.main()

