#! /usr/bin/env python3
# _*_ coding: utf-8 _*_

import unittest
import time

from base.running_log import RunningLog
from base.running_driver import RunDriver
from handle.login import Login
from util.util import pil_screenshot
from util.util import tesseract_content
from config.common_config import LOGIN_URL_ONLINE


class TestLogin(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.log = RunningLog(logger='Login')
        cls.logger = cls.log.get_log()

    def setUp(self):
        rd = RunDriver()
        self.url = LOGIN_URL_ONLINE
        self.driver = rd.get_driver()
        self.driver.maximize_window()
        self.driver.get(self.url)

    def test01_login_success(self):
        lg = Login(self.driver)
        lg.login()
        try:
            time.sleep(6)
            pil_screenshot('login_success')
            time.sleep(2)
            self.assertTrue(tesseract_content('设 计 规 范', 'login_success'))
            self.logger.info('登录成功')
        except Exception:
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
