#! /usr/bin/env python3
# _*_ coding: utf-8 _*_

import os
import datetime
import unittest
import yagmail

from config import HTMLTestReportCN
from config.common_config import REPORT_PATH, TEST_CASE_PATH


class RunningReport(object):
    """
        初始化参数，报告路径，报告 title 和描述。
    report_file_path: 报告生成存放路径，
    参数为 None 时 目标 py 文件在根目录下的文件夹内时使用；
    参数为 1 时 目标 py 文件直接在根目录下时使用；
     外部需要生成报告时，import running_report, 在执行时对 RunningReport() 赋值，
    按需传入 report_file_path 路径，其他参数值可不填，
    执行 RunningReport()下的函数 run_report() 运行指令。
    """

    def __init__(self, report_file_path=None, title=None, description=None):

        # 获得当前时间
        now = datetime.datetime.now()
        # 转换为指定的格式
        path_time = now.strftime("%Y-%m-%d_%H:%M:%S")
        self.report_file_path = os.path.join(REPORT_PATH, f'{path_time}.html') if report_file_path is None else report_file_path
        self.title = 'LanHu test report' if title is None else title
        self.description = 'LanHu web testing' if description is None else description
        self.fw = open(self.report_file_path, 'wb')
        self.runner = HTMLTestReportCN.HTMLTestRunner(
            stream=self.fw, title=self.title, description=self.description, verbosity=2)

    def run_report(self, suite):
        self.runner.run(suite)

    def run_all_case(self, py_name=None):
        py_name = '*py' if py_name is None else py_name
        discover = unittest.defaultTestLoader.discover(start_dir=TEST_CASE_PATH, pattern=py_name)
        self.runner.run(discover)

    def send_email(self):
        yag = yagmail.SMTP(user='1029131303@qq.com', password='qeoqngdiczikbdbc', host='smtp.qq.com')
        content = '测试报告'
        yag.send(to='1029131303@qq.com', subject='测试报告', contents=content, attachments=self.report_file_path)
        yag.close()


if __name__ == "__main__":
    pass
