#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Time    : 2021/10/22 1:21 下午
@File    : test_team.py
@Author  : zhangxue
@Desc    : 团队相关操作
'''
import allure
from config import RunConfig
import time
from playwright.async_api import Browser
import pytest
from common.Log import logger
from playwright.sync_api import Page
from common.util import *
from page import tsPage
import os
import json

@allure.feature('团队相关测试')
class TestTeam():

    # scope = class, autouse = true，等同于 setup_class()
    @pytest.fixture(scope="class", autouse=True)
    def page(self, browser: Browser):
        # page 也可以放到 conftest作为全局fixture来使用
        # 注意，自己new_page会导致 browser_context_args 钩子失效，
        # 需要在 new_page() 时传入 record_video_dir 参数 才能录制视频
        page = browser.new_page(locale="zh-CN")


        # Go to http://localhost/shopxo/admin.php
        page.goto("http://lanhuapp.com")

        # 常规设计模式，在 setup_class() 中访问 base_url 并且登录。
        # 这样可以单独执行任意一个 测试方法，都能顺利打开浏览器并且登录。
        # 而同时执行整个测试集也不会重复启动浏览器与登录而浪费时间。
        yield page


    @staticmethod
    @allure.story("登录后台")
    def test_admin_login(page: Page):
        """
        登录后台
        """
        tsPage.emailLogin(page)


    # @staticmethod
    # @allure.story("新建团队")
    # def test_createTeam(page: Page):
    #     """
    #     步骤：
    #     1、进入页面，登录
    #     2、选择对应的团队
    #     3、选择对应的超级文档tab
    #     检查点：
    #     * 校验文档信息
    #     """
    #     page.wait_for_timeout(2000)
    #     page.goto(RunConfig.team_url)
    #     page.goto(RunConfig.team_url)
    #     # Click span:has-text("线上001")
    #     page.click("span:has-text(\"线上001\")")
    #     # Click text=创建新团队
    #     page.click("text=创建新团队")
    #     assert page.url == "https://lanhuapp.com/web/#/item"
    #     # Click [placeholder="团队名称"]
    #     page.click("[placeholder=\"团队名称\"]")
    #     # Fill [placeholder="团队名称"]
    #     page.fill("[placeholder=\"团队名称\"]", "自动化" + get_nowtime())
    #
    #     # Click button:has-text("确定")
    #     # with page.expect_navigation(url="https://lanhuapp.com/web/#/item?createTeam=createTeam"):
    #     with page.expect_navigation():
    #         page.click("button:has-text(\"确定\")")
    #
    #     name = page.text_content(".team_name")
    #     logger.info("teamName+" + name)

    @staticmethod
    def test_team(page: Page):
        page.goto(RunConfig.team_url)
        page.goto(RunConfig.team_url)
        with page.expect_navigation():
            page.click("text=超级文档")
        # frame = page.frame(name="micro-app-ts-iframe")
        # frame.click("button.create-btn")
        # frame.click(".ts-template-wrapper .btn-use-default")
        # frame.click("#title")
        # frame.fill("#title", "测试文档" + get_nowtime())
        # frame.fill(".ce-paragraph >> nth=0", "默认文本，现在是：" + get_nowtime())

        # # self.tsUtils.creatDocument()
        # creatDocument(page)

        # Click button:has-text("新建文档")
        with page.expect_navigation():
            page.frame(name="micro-app-ts-iframe").click("button:has-text(\"新建文档\")")
        # Click text=创建空白页面
        page.frame(name="micro-app-ts-iframe").click("text=创建空白页面")
        # Click #title
        page.frame(name="micro-app-ts-iframe").click("#title")
        # Press Enter
        page.frame(name="micro-app-ts-iframe").fill("#title", "测试文档" + get_nowtime())
        page.frame(name="micro-app-ts-iframe").fill(".ce-paragraph >> nth=0", "默认文本，现在是：" + get_nowtime())



