#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create by shiyang on 2021/8/27

import time

import pyautogui as pg

from base.find_element import FindElement2
from base.running_log import RunningLog
from config.common_config import HOME_URL, SHORT_TIME, LONG_TIME


class TopBar:
    """上方功能栏"""

    def __init__(self, driver):
        self.driver = driver
        self.find_util = FindElement2(driver, node="ItemListTop")
        self.logger = RunningLog(logger='TopBar}').get_log()

    def go_home(self):
        # 验证后，返回主页
        self.driver.get(HOME_URL)

    def create(self, create_type, name):
        """新建项目、新建文件夹"""
        create_btn_ele = self.find_util.get_element("create_btn")
        create_btn_ele.click()
        time.sleep(SHORT_TIME)
        if create_type == 'item':
            type_name = "新建项目"
        elif create_type == 'dir':
            type_name = "新建文件夹"
        else:
            self.logger.error('create type error')
            raise Exception

        create_item_ele = self.find_util.get_elements("create_list", type_name)
        create_item_ele.click()
        time.sleep(SHORT_TIME)

        input_ele = self.find_util.get_element("item_input")
        input_ele.clear()
        input_ele.send_keys(name)
        time.sleep(SHORT_TIME)

        ok_ele = self.find_util.get_element("ok")
        ok_ele.click()

    def search(self, search_info):
        """搜索"""
        search_ele = self.find_util.get_element("search_btn")
        search_ele.click()

        pg.write(search_info)
        pg.press("enter")

    def bind(self):
        """绑定"""
        bind_ele = self.find_util.get_element("bind_btn")
        bind_ele.click()

    def notify(self):
        """通知"""
        notify_ele = self.find_util.get_element("notify_btn")
        notify_ele.click()

    def download(self, plugin_name):
        """下载"""
        download_ele = self.find_util.get_element("download_btn")
        download_ele.click()
        time.sleep(SHORT_TIME)
        plugin_ele = self.find_util.get_elements('plugin_list', plugin_name.strip())
        plugin_ele.click()

    def more(self):
        """更多"""


class LeftBar:
    """左侧"""

    def __init__(self, driver):
        self.driver = driver
        self.find_util = FindElement2(driver, node="ItemListLeft")
        self.logger = RunningLog(logger='LeftBar').get_log()

    def go_home(self):
        # 验证后，返回主页
        self.driver.get(HOME_URL)

    def invite(self):
        """邀请成员"""
        invite_btn = self.find_util.get_element('invite_btn')
        invite_btn.click()
        time.sleep(SHORT_TIME)

        copy_btn = self.find_util.get_element('copy_link_btn')
        copy_btn.click()
        time.sleep(SHORT_TIME)

    @staticmethod
    def close_invite_window():
        # 点击空白处（1255, 382），「x」难定位 针对于上面「邀请」
        pg.click(1255, 382)

    def team_setting(self):
        """团队设置"""
        team_setting_btn = self.find_util.get_element('team_setting_btn')
        team_setting_btn.click()

    def update(self):
        """立即升级"""
        time.sleep(LONG_TIME)
        update_btn = self.find_util.get_element('update_btn')
        update_btn.click()

    def design_rule(self):
        """设计规范"""
        design_rule_btn = self.find_util.get_element('design_rule_btn')
        design_rule_btn.click()

    def team_room(self):
        """团队空间"""
        team_room_btn = self.find_util.get_element('team_room_btn')
        team_room_btn.click()

    def open_team_item(self):
        """打开团队项目"""
        team_item_btn = self.find_util.get_element('team_item_btn')
        team_item_btn.click()

    def create_item_dir(self, create_type, name):
        """创建项目/文件夹"""
        add_btn = self.find_util.get_element('team_item_create_btn')
        add_btn.click()
        time.sleep(SHORT_TIME)
        if create_type == 'item':
            type_name = "新建项目"
        elif create_type == 'dir':
            type_name = "新建文件夹"
        else:
            self.logger.error('create type error')
            raise Exception
        create_item_btn = self.find_util.get_elements('create_list', type_name)
        create_item_btn.click()
        time.sleep(SHORT_TIME)
        input_btn = self.find_util.get_element('input')
        input_btn.send_keys(name)
        time.sleep(SHORT_TIME)
        ok_ele = self.find_util.get_element('ok_btn')
        ok_ele.click()
        time.sleep(SHORT_TIME)

    def into_item_dir(self, name):
        """进入项目/文件夹"""
        item_btn = self.find_util.get_elements('item_dir_name', name)
        item_btn.click()

    def rename_item_dir(self, old_name, new_name):
        """项目/文件夹 重命名"""
        # 根据名字定位 //*[@class="folder-self"]//*[contains(text(),"demo")]/../..//*[@class="setting"]
        try:
            setting_btn = self.driver.find_element_by_xpath(
                f'//*[@class="folder-self"]//*[contains(text(),"{old_name}")]/../..//*[@class="setting"]')
        except Exception as e:
            self.logger.error('rename error')
            raise e
        setting_btn.click()
        time.sleep(SHORT_TIME)
        rename_btn = self.find_util.get_elements('setting_menu', "重命名")
        rename_btn.click()
        time.sleep(SHORT_TIME)
        input_btn = self.find_util.get_element('input')
        input_btn.clear()
        input_btn.send_keys(new_name)
        time.sleep(SHORT_TIME)
        ok_ele = self.find_util.get_element('ok_btn')
        ok_ele.click()

    def delete_item_dir(self, delete_type, name):
        """删除项目/文件夹"""
        try:
            setting_btn = self.driver.find_element_by_xpath(
                f'//*[@class="folder-self"]//*[contains(text(),"{name}")]/../..//*[@class="setting"]')
        except Exception as e:
            self.logger.error('delete item/dir error')
            raise e
        setting_btn.click()
        time.sleep(SHORT_TIME)
        delete_btn = self.find_util.get_elements('setting_menu', "删除")
        delete_btn.click()
        time.sleep(SHORT_TIME)
        if delete_type == "item":
            input_btn = self.find_util.get_element('delete_item_input')
            delete_btn = self.find_util.get_elements('delete_item_btn', "删除")
        elif delete_type == "dir":
            input_btn = self.find_util.get_element('delete_dir_input')
            delete_btn = self.find_util.get_element('delete_dir_btn')
        else:
            self.logger.error('delete type error')
            raise Exception
        input_btn.clear()
        input_btn.send_keys(name)
        time.sleep(SHORT_TIME)
        delete_btn.click()


if __name__ == '__main__':
    pass

