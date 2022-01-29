import os
import pytest
from py.xml import html
from config import RunConfig
import allure
from slugify import slugify
from playwright.sync_api import sync_playwright
from common.config import *
from playwright.sync_api import BrowserType
from playwright.async_api import Browser
from typing import Dict
# 项目目录配置
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPORT_DIR = BASE_DIR + "/test_report/"


# 定义基本测试环境
@pytest.fixture(scope='session')
def base_url():
    return RunConfig.baseUrl


# 设置用例描述表头
def pytest_html_results_table_header(cells):
    cells.insert(2, html.th('Description'))
    cells.pop()


# 设置用例描述表格
def pytest_html_results_table_row(report, cells):
    cells.insert(2, html.td(report.description))
    cells.pop()


# @pytest.mark.hookwrapper
# def pytest_runtest_makereport(item):
#     """
#     pytest-html原生模版
#     用于向测试用例中添加用例的开始时间、内部注释，和失败截图等.
#     :param item:
#     """
#     pytest_html = item.config.pluginmanager.getplugin('html')
#     outcome = yield
#     report = outcome.get_result()
#     report.description = description_html(item.function.__doc__)
#     extra = getattr(report, 'extra', [])
#     page = item.funcargs["page"]
#     if report.when == 'call':
#         xfail = hasattr(report, 'wasxfail')
#         if (report.skipped and xfail) or (report.failed and not xfail):
#             case_path = report.nodeid.replace("::", "_") + ".png"
#             if "[" in case_path:
#                 case_name = case_path.split("-")[0] + "].png"
#             else:
#                 case_name = case_path
#
#             capture_screenshots(case_name, page)
#             img_path = "image/" + case_name.split("/")[-1]
#             print("img_path")
#             print(img_path)
#             if img_path:
#                 html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
#                        'onclick="window.open(this.src)" align="right"/></div>' % img_path
#                 extra.append(pytest_html.extras.html(html))
#
#         report.extra = extra

# TODO: 使用 allure 以更好的呈现截图与视频
# ref: https://zenn.dev/yusukeiwaki/articles/cfda648dc170e5
@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    """
    allure报告模版
    用于向测试用例中添加用例的开始时间、内部注释，和失败截图等.
    :param item:
    """
    if call.when == "call":
        # 失败的情况下
        if call.excinfo is not None and "page" in item.funcargs:
            from playwright.async_api import Page
            page: Page = item.funcargs["page"]

            allure.attach(
                page.screenshot(type='png'),
                name=f"{slugify(item.nodeid)}.png",
                attachment_type=allure.attachment_type.PNG
            )

            # # 向报告中添加视频
            # video_path = page.video.path()
            # page.context.close()  # ensure video saved
            # allure.attach(
            #     open(video_path, 'rb').read(),
            #     name=f"{slugify(item.nodeid)}.webm",
            #     attachment_type=allure.attachment_type.WEBM
            # )

    callers = yield

def description_html(desc):
    """
    将用例中的描述转成HTML对象
    :param desc: 描述
    :return:
    """
    if desc is None:
        return "No case description"
    desc_ = ""
    for i in range(len(desc)):
        if i == 0:
            pass
        elif desc[i] == '\n':
            desc_ = desc_ + ";"
        else:
            desc_ = desc_ + desc[i]
    
    desc_lines = desc_.split(";")
    desc_html = html.html(
        html.head(
            html.meta(name="Content-Type", value="text/html; charset=latin1")),
        html.body(
            [html.p(line) for line in desc_lines]))
    return desc_html


def capture_screenshots(case_name, page):
    """
    配置用例失败截图路径
    :param case_name: 用例名
    :return:
    """
    global driver
    file_name = case_name.split("/")[-1]
    if RunConfig.NEW_REPORT is None:
        raise NameError('没有初始化测试报告目录')
    else:
        image_dir = os.path.join(RunConfig.NEW_REPORT, "image", file_name)
        page.screenshot(path=image_dir)

#
# @pytest.fixture(scope="session")
# def context(
#     browser_type: BrowserType,
#     browser_type_launch_args: Dict,
#     browser_context_args: Dict
# ):
#     context = browser_type.launch_persistent_context("./foobar", **{
#         **browser_type_launch_args,
#         **browser_context_args,
#         "locale": "de-DE",
#     })
#     yield context
#     context.close()

@pytest.fixture()
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "ignore_https_errors": True,
        "viewport": {
            "width": 1920,
            "height": 1080,
        }
    }


@pytest.fixture(scope="class")
def page(browser: Browser):
    # page 也可以放到 conftest作为全局fixture来使用
    # 注意，自己new_page会导致 browser_context_args 钩子失效，
    # 需要在 new_page() 时传入 record_video_dir 参数 才能录制视频
    page = browser.new_page(locale="zh-CN")
    # 常规设计模式，在 setup_class() 中访问 base_url 并且登录。
    # 这样可以单独执行任意一个 测试方法，都能顺利打开浏览器并且登录。
    # 而同时执行整个测试集也不会重复启动浏览器与登录而浪费时间。
    yield page



if __name__ == "__main__":
    capture_screenshots("test_case/test_baidu_search.test_search_python.png")
