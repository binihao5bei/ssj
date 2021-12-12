#! /usr/bin/env python3
# _*_ coding: utf-8 _*_

import unittest
import time

from base.running_log import RunningLog
from base.running_driver import RunDriver
from handle.login import Login
from handle.personal_settings import PersonalSettings
from util.util import pil_screenshot
from util.util import tesseract_content
from base.find_element import FindElement
from config.common_config import LOGIN_URL_ONLINE


class TestPersonalSettings(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.log = RunningLog(logger='PersonalSettings')
        cls.logger = cls.log.get_log()

    def setUp(self):
        rd = RunDriver()
        self.url = LOGIN_URL_ONLINE
        self.driver = rd.get_driver()
        self.driver.maximize_window()
        self.driver.get(self.url)
        lg = Login(self.driver)
        lg.login()
        self.ps = PersonalSettings(self.driver)
        self.ps.personal_settings()
        self.fe = FindElement(self.driver, section='PersonalSettingsElement')

    def test01_headshot_edit(self):
        headshot_edit = self.ps.headshot_edit()
        try:
            time.sleep(6)
            pil_screenshot('headshot_edit_success')
            time.sleep(2)
            self.assertTrue(tesseract_content('头 像', 'headshot_edit_success'))
            self.logger.info('编辑头像成功')
        except Exception:
            self.logger.error('编辑头像失败')
            raise AssertionError
        finally:
            time.sleep(2)
            headshot_reduction = self.ps.headshot_edit(img_headshot='img_mockingbird')

    def test02_email_edit(self):
        email_edit = self.ps.email_edit()
        try:
            time.sleep(2)
            pil_screenshot('email_edit_success')
            time.sleep(2)
            self.assertTrue(tesseract_content('邮 箱 修 改 成 功', 'email_edit_success'))
            self.logger.info('邮箱修改成功')
        except Exception:
            self.logger.error('邮箱修改失败')
            raise AssertionError
        finally:
            time.sleep(2)
            self.fe.get_element('email_login_pwd').send_keys('123456')
            self.fe.get_element('email_login_button').click()
            ps_email = PersonalSettings(self.driver)
            ps_email.personal_settings()
            headshot_reduction = self.ps.email_edit(email='n@n.com')
            time.sleep(2)

    def test03_username_edit(self):
        username_edit = self.ps.username_edit()
        try:
            time.sleep(2)
            pil_screenshot('username_edit_success')
            time.sleep(2)
            self.assertTrue(tesseract_content('username_nn', 'username_edit_success'))
            self.logger.info('用户名修改成功')
        except Exception:
            self.logger.error('用户名修改失败')
            raise AssertionError
        finally:
            time.sleep(2)
            username_reduction = self.ps.username_edit(username='yhm_nn')
            time.sleep(2)

    def test04_remark_name_edit(self):
        remark_name_edit = self.ps.remark_name_edit()
        try:
            time.sleep(2)
            pil_screenshot('remark_name_edit_success')
            time.sleep(2)
            self.assertTrue(tesseract_content('remark_name_nn', 'remark_name_edit_success'))
            self.logger.info('备注名修改成功')
        except Exception:
            self.logger.error('备注名修改失败')
            raise AssertionError
        finally:
            time.sleep(2)
            remark_name_edit = self.ps.remark_name_edit(remark_name='bzm_nn')
            time.sleep(2)

    def test05_pwd_edit(self):
        pwd_edit = self.ps.pwd_edit()
        try:
            time.sleep(2)
            pil_screenshot('pwd_edit_success')
            time.sleep(2)
            self.assertTrue(tesseract_content('密 码 修 改 成 功', 'pwd_edit_success'))
            self.logger.info('密码修改成功')
        except Exception:
            self.logger.error('密码修改失败')
            raise AssertionError

    def tearDown(self):
        time.sleep(2)
        self.driver.quit()

    @classmethod
    def tearDownClass(cls):
        cls.log.close_handle()


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(TestPersonalSettings('test05_pwd_edit'))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite) 


