#! /usr/bin/env python3
# -*- coding: UTF-8 -*-
# excle读取
from pathlib import Path
import xlrd
import sys

sys.path.append(str(Path.home()) + "/ApiTestFramework")


class ReadFile(object):
    def __init__(self, sheet_name=None, file_path=None):
        # 获取 Excel 位置
        home = str(Path.home())
        if file_path is None:
            self.file_path = home + "/ApiTestFramework/config/APITestFile.xlsx"
        elif file_path == 1:
            self.file_path = sys.argv[1]
        self.xl = xlrd.open_workbook(filename=self.file_path)

        # 通过传入指定 sheet 名称获取
        if sheet_name is None:
            sheet_name = "account"
        self.xl_sheet = self.xl.sheet_by_name(sheet_name=sheet_name)

    # 返回的指定 sheet
    def get_sheet(self):
        return self.xl_sheet

    # 获取 Excel 指定单元格内容，row=所在行，col=所在列, 数值依据 Python 排序起始第一个为 0 以此类推；

    # 获取测试目标名称
    def get_test_name(self, row):
        name = self.xl_sheet.cell_value(rowx=row, colx=0)
        return name

    # 获取请求方法
    def get_method(self, row):
        method = self.xl_sheet.cell_value(rowx=row, colx=1)
        return method

    # 读取请求头
    def get_headers(self, row):
        headers = self.xl_sheet.cell_value(rowx=row, colx=2)
        return headers

    # 读取请求地址
    def get_api(self, row):
        api = self.xl_sheet.cell_value(rowx=row, colx=3)
        return api

    # 读取 请求参数
    def get_data(self, row):
        data = self.xl_sheet.cell_value(rowx=row, colx=4)
        return data

    # 读取响应状态码
    def get_status_code(self, row):
        code = self.xl_sheet.cell_value(rowx=row, colx=5)
        return code

    # 读取预期判断值
    def get_judge_key(self, row):
        key = self.xl_sheet.cell_value(rowx=row, colx=6)
        return key

    # 读取预期断言结果
    def get_judge_value(self, row):
        value = self.xl_sheet.cell_value(rowx=row, colx=7)
        return value

    # 读取预期结果
    def get_info(self, row):
        info = self.xl_sheet.cell_value(rowx=row, colx=8)
        return info


if __name__ == "__main__":
    r = ReadFile(sheet_name="project")
    print(r.get_data(row=6))
