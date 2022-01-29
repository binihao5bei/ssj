#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create by shiyang on 2021/8/30

import os
import time

import pyautogui as pg
import pyperclip

from base.find_element import FindElement2
from base.running_log import RunningLog
from config.common_config import INVITE_LINK, IMG_PATH, LONG_TIME, HOME_URL


class AssertTopBar:
    """项目列表 上方工具栏 断言方法"""

    def __init__(self, driver):
        self.driver = driver
        self.find_util = FindElement2(driver, node="ItemListTop")
        self.logger = RunningLog(logger='AssertTopBar').get_log()

    def a_create_item(self, item_name):
        # 在 LeftBar中验证比较方便
        pass

    def a_create_dir(self, dir_name):
        # 同上
        pass

    def a_search_has_result(self, search_info):
        """有结果的搜索断言，item dir design
        TODO: 需要改
        """
        items = self.find_util.get_original_elements('assert_search_item')
        dirs = self.find_util.get_original_elements('assert_search_dir')
        designs = self.find_util.get_original_elements('assert_search_design')
        search_list = [i for i in [items, dirs, designs] if i is not None]
        search_list = sum(search_list, [])
        result = True
        for one in search_list:
            if search_info not in one.text:
                result = False
                break
        return result

    def a_search_no_result(self):
        """没有结果的搜索断言, 判断没有上面三种的搜索结果"""
        items = self.find_util.get_original_elements('assert_search_item')
        dirs = self.find_util.get_original_elements('assert_search_dir')
        designs = self.find_util.get_original_elements('assert_search_design')
        result = not any([items, dirs, designs])
        return result

    def a_notify(self):
        """断言通知"""
        read_btn = self.find_util.get_element('assert_notify')
        result = True if read_btn else False
        return result

    def a_download(self, plugin_name):
        """断言下载插件"""
        plugin_map = {
            "设计规范云": "assert_plugin_rule.png",
            "蓝湖 Axure": "assert_plugin_Axure.png",
            "Figma 插件": "assert_plugin_Figma.png",
            "Sketch 插件": "assert_plugin_Sketch.png",
            "Photoshop 插件": "assert_plugin_PS.png",
            "Adobe XD 插件": "assert_plugin_XD.png",
            "手机 App": "assert_plugin_App.png"
        }
        img_name = plugin_map.get(plugin_name)
        if not img_name:
            self.logger.error("plugin name not in map")
            raise Exception
        img_path = os.path.join(IMG_PATH, f"item_list/top/{img_name}")
        time.sleep(LONG_TIME)
        result = True if pg.locateOnScreen(img_path) else False
        return result


class AssertLeftBar:
    """项目列表 左侧工具栏 断言方法"""

    def __init__(self, driver):
        self.driver = driver
        self.find_util = FindElement2(driver, node="ItemListLeft")

    def go_home(self):
        # 验证后，返回主页
        self.driver.get(HOME_URL)

    @staticmethod
    def a_invite():
        """断言邀请成员"""
        # 如果邀请链接包含 INVITE_LINK 则复制链接成功
        invite_link = pyperclip.paste()
        return True if INVITE_LINK in str(invite_link) else False

    def a_team_setting(self):
        """断言团队设置"""
        result = self.find_util.get_element('assert_team_setting')
        return True if result else False

    @staticmethod
    def a_update():
        """断言立即升级"""
        result = pg.locateOnScreen(os.path.join(IMG_PATH, 'item_list/left/assert_update.png'))
        return True if result else False

    def a_design_rule(self):
        """断言设计规范"""
        result = self.find_util.get_element('assert_design_rule')
        return True if result else False

    @staticmethod
    def a_team_room():
        """断言团队空间"""
        result = pg.locateOnScreen(os.path.join(IMG_PATH, 'item_list/left/assert_team_room.png'))
        return True if result else False

    def a_open_team_item(self):
        """断言打开团队项目"""
        result = self.find_util.get_element('assert_open_team_item')
        return True if result else False

    def a_create_item_dir(self, name):
        """现在未考虑重名情况，可以参考下面「重命名」「删除」的断言方法"""
        item_dir_list = self.find_util.get_original_elements('assert_create_item_dir')
        # result = True if (i.text for i in item_dir_list if i.text == name).__next__() else False
        result = False
        for item_dir in item_dir_list:
            if item_dir.text == name:
                result = True
                break
        return result

    def get_names_num(self, old_name, new_name):
        """重命名
           拿到根据名字得到的项目/文件夹的数量
           根据名字的数量判断：
           改名之前 old_name = n ; new_name = m
           改名之后 old_name = n-1 ; new_name = m+1
           满足两个条件 才判断成功
           中间需要执行重命名的操作，在case里面组织
        """
        item_dir_list = self.find_util.get_original_elements('assert_create_item_dir')
        old_name_list = [i.text for i in item_dir_list if i.text == old_name]
        new_name_list = [i.text for i in item_dir_list if i.text == new_name]
        old_name_num = len(old_name_list)
        new_name_num = len(new_name_list)
        return old_name_num, new_name_num

    def get_name_num(self, delete_name):
        """删除项目/文件夹
           判断名字个数是否少一个
           删除之前 n；删除之后 n-1
        """
        item_dir_list = self.find_util.get_original_elements('assert_create_item_dir')
        delete_name_list = [i.text for i in item_dir_list if i.text == delete_name]
        delete_name_num = len(delete_name_list)
        return delete_name_num


if __name__ == '__main__':
    pass
