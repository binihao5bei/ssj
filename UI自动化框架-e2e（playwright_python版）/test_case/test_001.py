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
from page.tsPage import *
import os
import json

@allure.feature('block相关测试')
class Test001():


    @pytest.fixture(scope="class", autouse=True)
    def before(self, page:Page):
        self.page = page
        emailLogin(self.page)

        page.goto(RunConfig.team_url)
        page.goto(RunConfig.team_url)
        with page.expect_navigation():
            page.click("text=超级文档")
        page.wait_for_timeout(2000)
        frame = creatDocument(page)
        yield frame

    def setup(self):
        print("在每个用例执行前的初始化工作 :打开浏览器，加载网页。。。。")

    @pytest.mark.run(order=1)
    @pytest.mark.parametrize(
        "title",
        ['一级标题', '二级标题', '三级标题'],
    )
    def test_addHBlock(self, frame, title):
        addHeaderBlock(frame, title)

    @pytest.mark.run(order=2)
    @pytest.mark.parametrize(
        "type",
        ['有序列表', '无序列表'],
    )
    def test_addListBlock(self, frame, type):
        addListBlock(frame, type)

    @pytest.mark.run(order=3)
    def test_addExplainBlock(self, frame, name='特殊说明'):
        addExplainBlock(frame, name)

    @pytest.mark.run(order=4)
    def test_addTodoListBlock(self, frame, name='待办事项'):
        addTodoListBlock(frame, name)





    def teardown(self):
        print("每个用例之后的扫尾工作: 关闭浏览器..")

    def teardown_class(self):
        print("每个类之后的扫尾工作: 销毁日志对象  数据库对象..")

if __name__ == '__main__':
       pytest.main(["-s","test_001.py"]) # 调用pytest的main函数执行测试
