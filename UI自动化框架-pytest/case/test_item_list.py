#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create by shiyang on 2021/8/30

import time
import unittest

from parameterized import parameterized

from base.running_driver import RunDriver
from base.running_log import RunningLog
from handle.login_page import login
from handle.item_list import TopBar, LeftBar
from assert_func.assert_item_list import AssertTopBar, AssertLeftBar
from config.common_config import LONG_TIME


class TestTopBar(unittest.TestCase):
    """测试 项目列表-->上方工具栏"""

    @classmethod
    def setUpClass(cls):
        cls.logger = RunningLog('TestTopBar').get_log()

    def setUp(self):
        self.driver = RunDriver().get_driver()
        login(self.driver)
        self.top_bar = TopBar(self.driver)
        self.assert_t = AssertTopBar(self.driver)
        self.assert_l = AssertLeftBar(self.driver)

    # @parameterized.expand([('item', 'pop-test-item'), ('dir', 'pop-test-dir')])
    def test_create_item(self, create_type='item', name='pop-test'):
        """测试新建项目/文件夹"""
        self.top_bar.create(create_type, name)
        time.sleep(LONG_TIME)
        self.top_bar.go_home()
        time.sleep(LONG_TIME)
        result = self.assert_l.a_create_item_dir(name)
        self.assertTrue(result)
        self.logger.debug(f'新建类型[{create_type}] 名称[{name}] 测试结果 [{result}]')

    # @parameterized.expand(["test"])
    def test_search_has_result(self, info="test"):
        """测试有结果的搜索
        TODO: 断言方法有待修复
        """
        self.top_bar.search(info)
        time.sleep(LONG_TIME)
        result = self.assert_t.a_search_has_result(info)
        self.assertTrue(result)
        self.logger.debug(f'搜索内容[{info}] 测试结果 [{result}]')

    # @parameterized.expand(["invite", "member"])
    def test_search_no_result(self, info="invite"):
        """测试没有结果的搜索"""
        self.top_bar.search(info)
        time.sleep(LONG_TIME)
        result = self.assert_t.a_search_no_result()
        self.assertTrue(result)
        self.logger.debug(f'搜索内容[{info}] 测试结果[{result}]')

    def test_notify(self):
        """测试通知"""
        self.top_bar.notify()
        time.sleep(LONG_TIME)
        result = self.assert_t.a_notify()
        self.assertTrue(result)
        self.logger.debug(f'测试「通知」 测试结果[{result}]')

    # @parameterized.expand(['设计规范云', '蓝湖 Axure', 'Figma 插件', 'Sketch 插件', 'Photoshop 插件', 'Adobe XD 插件', '手机 App'])
    def test_download(self, plugin_name="设计规范云"):
        """测试下载插件"""
        self.top_bar.download(plugin_name)
        time.sleep(LONG_TIME)
        result = self.assert_t.a_download(plugin_name)
        self.assertTrue(result)
        self.logger.debug(f'测试插件下载[{plugin_name}] 测试结果[{result}]')

    def tearDown(self):
        self.driver.quit()


class TestLeftBar(unittest.TestCase):
    """测试 项目列表-->左侧栏功能"""

    @classmethod
    def setUpClass(cls):
        cls.logger = RunningLog('TestLeftBar').get_log()

    def setUp(self):
        self.driver = RunDriver().get_driver()
        login(self.driver)
        self.left_bar = LeftBar(self.driver)
        self.assert_l = AssertLeftBar(self.driver)

    def tearDown(self):
        self.driver.quit()

    def test_invite(self):
        """测试邀请成员"""
        self.left_bar.invite()
        result = self.assert_l.a_invite()
        self.assertTrue(result)
        self.logger.debug(f'测试邀请成员 测试结果[{result}]')

    def test_team_setting(self):
        """测试团队设置"""
        self.left_bar.team_setting()
        result = self.assert_l.a_team_setting()
        self.assertTrue(result)
        self.logger.debug(f'测试团队设置 测试结果[{result}]')

    def test_update(self):
        """测试立即升级"""
        self.left_bar.update()
        time.sleep(LONG_TIME)
        result = self.assert_l.a_update()
        self.assertTrue(result)
        self.logger.debug(f'测试立即升级 测试结果[{result}]')

    def test_design_rule(self):
        """测试设计规范"""
        self.left_bar.design_rule()
        result = self.assert_l.a_design_rule()
        self.assertTrue(result)
        self.logger.debug(f'测试设计规范 测试结果[{result}]')

    def test_team_room(self):
        """测试团队空间"""
        self.left_bar.team_room()
        time.sleep(LONG_TIME)
        result = self.assert_l.a_team_room()
        self.assertTrue(result)
        self.logger.debug(f'测试团队空间 测试结果[{result}]')

    def test_open_team_item(self):
        """测试打开团队项目"""
        self.left_bar.open_team_item()
        result = self.assert_l.a_open_team_item()
        self.assertTrue(result)
        self.logger.debug(f'测试打开团队项目 测试结果[{result}]')

    # @parameterized.expand([('item', 'item-test'), ('dir', 'dir-test')])
    def test_create_item_dir(self, create_type="item", name="item-test"):
        """测试创建项目/文件夹"""
        self.left_bar.create_item_dir(create_type, name)
        time.sleep(LONG_TIME)
        self.left_bar.go_home()
        time.sleep(LONG_TIME)
        result = self.assert_l.a_create_item_dir(name)
        self.assertTrue(result)
        self.logger.debug(f'测试新建类型[{create_type}] 新建名称[{name}] 测试结果[{result}]')

    # @parameterized.expand([('dir-test', 'dir-test1'), ('item-test', 'item-test1')])
    def test_rename_item_dir(self, old_name="item-test", new_name="item-test1"):
        """测试重命名项目/文件夹
           改名之前 old_name = n ; new_name = m
           改名之后 old_name = n-1 ; new_name = m+1
        """
        n, m = self.assert_l.get_names_num(old_name, new_name)
        self.left_bar.rename_item_dir(old_name, new_name)
        time.sleep(LONG_TIME)
        n1, m1 = self.assert_l.get_names_num(old_name, new_name)
        result = (n-1 == n1) and (m+1 == m1)
        self.assertTrue(result)
        self.logger.debug(f'测试重命名，旧名称[{old_name}]，新名称[{new_name}] 测试结果[{result}]')

    # @parameterized.expand([('item', 'item-test1'), ('dir', 'dir-test1')])
    def test_delete_item_dir(self, delete_type='item', name='pop-test'):
        """测试删除项目/文件夹
           n ：删除前的数量
           n1: 删除后的数量
        """
        n = self.assert_l.get_name_num(name)
        self.left_bar.delete_item_dir(delete_type, name)
        time.sleep(LONG_TIME)
        n1 = self.assert_l.get_name_num(name)
        result = (n-n1 == 1)
        self.assertTrue(result)
        self.logger.debug(f'测试删除类型[{delete_type}] 删除名称[{name}] 测试结果[{result}]')


if __name__ == '__main__':
    unittest.main()
