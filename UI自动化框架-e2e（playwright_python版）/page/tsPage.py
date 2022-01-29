
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Time    : 2021/10/26 6:38 下午 
@File    : tsPage.py
@Author  : zhangxue
@Desc    : ts的一些封装方法
'''
from playwright.async_api import Page
from common.userData import *
from config import RunConfig
from common.util import *
import asyncio

from playwright.async_api import Playwright, async_playwright



"""邮箱登录"""
def emailLogin(page, email=base_email, password=base_password):

    login_text = "text=登录"  # 主页面登录文案
    emailPhone_input = "input[name=\"email\"]"  # 邮箱手机号输入框
    password_input = "input[name=\"password\"]"  # 密码输入框
    login_button = "button:has-text(\"登录\")"  # 登录按钮
    baseUrl = RunConfig.baseUrl

    page.goto(baseUrl)
    page.click(login_text)
    page.click(emailPhone_input)
    page.fill(emailPhone_input, email)
    page.click(password_input)
    page.fill(password_input, password)
    with page.expect_navigation():
        page.click(login_button)
    return page


"""退出登录"""
def logout(page):
    # Click button:has-text("帐号设置")
    # page.click("button:has-text(\"帐号设置\")")
    # # Click text=退出登录
    # # with page.expect_navigation(url="https://lanhuapp.com/web/#/user/login"):
    # with page.expect_navigation():
    #     page.click("text=退出登录")
    setting_text = "button:has-text(\"帐号设置\")"  # 账号设置文案
    logout_text = "text=退出登录"  # 退出登录文案
    page.click(setting_text)
    with page.expect_navigation():
        page.click(logout_text)

"""创建文档"""
def creatDocument(page):
    frame = page.frame(name="micro-app-ts-iframe")
    frame.wait_for_selector("button:has-text(\"新建文档\")")
    with frame.expect_navigation():
        frame.click("button:has-text(\"新建文档\")")
        frame.click("text=创建空白页面")
    frame.wait_for_selector('#title')
    frame.fill("#title", '测试文档' + get_nowtime())
    frame.press("#title", "Enter")
    frame.fill(".ce-paragraph >> nth=0", "默认文本，现在是：" + get_nowtime())
    return frame

"""删除文档"""
def removeDocument(frame):
    frame.wait_for_timeout(2000)
    frame.wait_for_selector('.bar_menu')
    frame.click(".bar_menu")
    frame.wait_for_selector('.bar_delete')
    frame.click('.bar_delete')
    frame.wait_for_timeout(1000)
    with frame.expect_navigation():
        frame.click("button:has-text(\"是\")")

"""添加指定类型的block"""
def addBlock(frame,title):
    frame.hover('.ce-paragraph >> nth=-1')
    frame.wait_for_selector('.ce-toolbar__plus')
    frame.click('.ce-toolbar__plus')
    frame.wait_for_selector('.ce-toolbox')
    frame.click('text='+title)

"""创建标题block"""
def addHeaderBlock(frame,title):
    addBlock(frame, title)
    frame.wait_for_timeout(2000)
    text = '这是新建的' + title
    selector = '.ce-header >> nth=0'
    locator = frame.locator(selector)
    frame.fill(selector, text)
    assert title in locator.text_content()

"""创建有序无序列表block"""
def addListBlock(frame,type):
    addBlock(frame, type)
    frame.wait_for_timeout(2000)
    textList = ['列表1','列表2','列表3']
    for i in range(0,len(textList)):
        selector = '.cdx-nested-list__item-content >> nth='+ str(i)
        frame.fill(selector, textList[i])
        frame.press(selector, 'Enter')
        assert textList[i] in frame.locator(selector).text_content()
    style ='--order-list-style:decimal;' if type == '有序列表' else '--unordered-list-style:"•";'
    for j in range(0, len(textList)):
        yuansu = '.cdx-nested-list__item >> nth=' + str(i)
        assert style == frame.locator(yuansu).get_attribute('style')


"""创建特殊说明block"""
def addExplainBlock(frame,name):
    addBlock(frame,name)
    frame.wait_for_timeout(1000)
    selector = 'div[data-placeholder="输入内容..."]'
    contentFirstLine = '特殊说明 block 第一行内容'
    contentSecondLine = '特殊说明 block 第二行内容'
    frame.wait_for_selector(selector)
    frame.type(selector, contentFirstLine, delay=100)
    frame.press(selector, 'Shift+Enter')
    frame.type(selector, contentSecondLine,  delay=100)
    assert contentFirstLine in frame.locator(selector).text_content()
    assert contentSecondLine in frame.locator(selector).text_content()

"""创建待办事项block"""
def addTodoListBlock(frame,name):
    addBlock(frame, name)
    frame.wait_for_timeout(1000)
    # 第一个待办事项编辑框选择器
    firstListItemSelector = '.lanhu-list-content[contenteditable="true"] >> nth=0'
    # 第一个待办事项内容
    firstListItemContent = '第一个待办事项'
    # 等待第一个编辑框 DOM 渲染完毕
    frame.wait_for_selector(firstListItemSelector)
    # 模拟用户在第一个待办事项 block 中输入内容
    frame.fill(firstListItemSelector, firstListItemContent)
    assert firstListItemContent in frame.locator(firstListItemSelector).text_content()

    # 模拟用户勾选第一个待办事项
    frame.click('.cdx-checklist__item-checkbox >> nth=0')
    # 模拟用户按下回车键创建第二个待办事项
    frame.press(firstListItemSelector, 'Enter')
    # 第二个待办事项编辑框选择器
    secondListItemSelector = '.lanhu-list-content[contenteditable="true"] >> nth=1'
    # 第二个待办事项内容
    secondListItemContent = '第二个待办事项'
    # 等待第二个编辑框DOM渲染完毕
    frame.wait_for_selector(secondListItemSelector)
    # 模拟用户在第二个待办事项 block中输入内容
    frame.fill(secondListItemSelector, secondListItemContent)
    assert secondListItemContent in frame.locator(secondListItemSelector).text_content()
    # 模拟用户勾选第二个待办事项
    frame.click('.cdx-checklist__item-checkbox >> nth=1')



