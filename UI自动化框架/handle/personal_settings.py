#! /usr/bin/env python3
# _*_ coding: utf-8 _*_

import time

import pyautogui

from base.find_element import FindElement
from util.read_ini import ReadIni


class PersonalSettings(object):

    def __init__(self, driver, confidence=0.9, duration=1):
        self.driver = driver
        self.confidence = confidence
        self.duration = duration
        self.fe_ps = FindElement(self.driver, section='PersonalSettingsElement')
        self.read_ini_isp = ReadIni(section='ImgSlicePath', file_name='img_path.ini')

    # 点击进入个人设置页面
    def personal_settings(self):
        self.fe_ps.get_element('button_setting').click()
        self.fe_ps.get_element('button_personal_setting').click()

    # 头像编辑
    def headshot_edit(self, img_headshot=None):
        self.fe_ps.get_element('headshot').click()
        self.fe_ps.get_element('headshot_load').click()
        time.sleep(1)
        # 点击进入桌面
        img_desktop = self.read_ini_isp.get_value('img_desktop')
        tar_x, tar_y = pyautogui.locateCenterOnScreen(img_desktop, confidence=self.confidence)
        # print(tar_x, tar_y)
        # 高清屏截图坐标需要除以 2
        x = tar_x // 2
        y = tar_y // 2
        pyautogui.click(x, y, duration=self.duration)
        time.sleep(1)
        if img_headshot is None:
            # 选择将更换的头像图片
            img_hummingbird = self.read_ini_isp.get_value('img_hummingbird')
            tar_x, tar_y = pyautogui.locateCenterOnScreen(img_hummingbird, confidence=self.confidence)
            # print(tar_x, tar_y)
            x = tar_x // 2
            y = tar_y // 2
            pyautogui.click(x, y, duration=self.duration)
            time.sleep(1)
        else:
            img_mockingbird = self.read_ini_isp.get_value('img_mockingbird')
            tar_x, tar_y = pyautogui.locateCenterOnScreen(img_mockingbird, confidence=self.confidence)
            # print(tar_x, tar_y)
            x = tar_x // 2
            y = tar_y // 2
            pyautogui.click(x, y, duration=self.duration)
            time.sleep(1)
        # 点击"打开"
        img_open = self.read_ini_isp.get_value('img_open')
        tar_x, tar_y = pyautogui.locateCenterOnScreen(img_open, confidence=self.confidence)
        # print(tar_x, tar_y)
        x = tar_x // 2
        y = tar_y // 2
        pyautogui.click(x, y, duration=self.duration)
        time.sleep(1)
        # 点击"确定"
        img_confirm = self.read_ini_isp.get_value('img_confirm')
        tar_x, tar_y = pyautogui.locateCenterOnScreen(img_confirm, confidence=self.confidence)
        # print(tar_x, tar_y)
        x = tar_x // 2
        y = tar_y // 2
        pyautogui.click(x, y, duration=self.duration)
        time.sleep(1)

    # 邮箱编辑
    def email_edit(self, email='n@1.com'):
        self.fe_ps.get_element('email_icon').click()
        self.fe_ps.get_element('email_pwd').send_keys('123456')
        self.fe_ps.get_element('email_new').send_keys(email)
        self.fe_ps.get_element('email_new_again').send_keys(email)
        time.sleep(1)
        img_confirm = self.read_ini_isp.get_value('img_confirm')
        tar_x, tar_y = pyautogui.locateCenterOnScreen(img_confirm, confidence=self.confidence)
        # print(tar_x, tar_y)
        x = tar_x // 2
        y = tar_y // 2
        pyautogui.click(x, y, duration=self.duration)
        time.sleep(1)

    # 用户名编辑
    def username_edit(self, username='username_nn'):
        self.fe_ps.get_element('username_icon').click()
        self.fe_ps.get_element('username_input').send_keys(username)
        img_confirm = self.read_ini_isp.get_value('img_confirm')
        tar_x, tar_y = pyautogui.locateCenterOnScreen(img_confirm, confidence=self.confidence)
        # print(tar_x, tar_y)
        x = tar_x // 2
        y = tar_y // 2
        pyautogui.click(x, y, duration=self.duration)

    # 团队备注名编辑
    def remark_name_edit(self, remark_name='remark_name_nn'):
        self.fe_ps.get_element('remark_icon').click()
        self.fe_ps.get_element('remark_input').send_keys(remark_name)
        img_confirm = self.read_ini_isp.get_value('img_confirm')
        tar_x, tar_y = pyautogui.locateCenterOnScreen(img_confirm, confidence=self.confidence)
        # print(tar_x, tar_y)
        x = tar_x // 2
        y = tar_y // 2
        pyautogui.click(x, y, duration=self.duration)

    # 密码修改
    def pwd_edit(self, pwd='123456'):
        self.fe_ps.get_element('pwd_icon').click()
        self.fe_ps.get_element('pwd_login').send_keys('123456')
        self.fe_ps.get_element('pwd_new').send_keys(pwd)
        self.fe_ps.get_element('pwd_new_again').send_keys(pwd)
        img_confirm = self.read_ini_isp.get_value('img_confirm')
        tar_x, tar_y = pyautogui.locateCenterOnScreen(img_confirm, confidence=self.confidence)
        # print(tar_x, tar_y)
        x = tar_x // 2
        y = tar_y // 2
        pyautogui.click(x, y, duration=self.duration)


if __name__ == "__main__":
    pass
