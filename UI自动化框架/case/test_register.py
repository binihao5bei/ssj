#! /usr/bin/env python3
# _*_ coding: utf-8 _*_

import unittest
import time

from base.running_log import RunningLog
from base.running_driver import RunDriver
from handle.register import Register
from util.util import pil_screenshot
from util.util import tesseract_content
from config.common_config import REGISTER_URL_ONLINE


class TestRegister(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.log = RunningLog(logger='Register')
        cls.logger = cls.log.get_log()

    def setUp(self):
        rd = RunDriver()
        self.url = REGISTER_URL_ONLINE
        self.driver = rd.get_driver()
        self.driver.maximize_window()
        self.driver.get(self.url)

    def test01_register_success(self):
        lg = Register(self.driver)
        lg.register()
        try:
            time.sleep(6)
            pil_screenshot('register_success')
            time.sleep(2)
            self.assertTrue(tesseract_content(' 欢 迎 来 到 蓝 湖', 'register_success'))
            self.logger.info('注册成功')
        except Exception:
            self.logger.error('注册失败')
            raise AssertionError

    def tearDown(self):
        time.sleep(2)
        self.driver.quit()

    @classmethod
    def tearDownClass(cls):
        cls.log.close_handle()


if __name__ == "__main__":
    unittest.main()

