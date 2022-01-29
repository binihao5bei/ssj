# -*- coding:UTF-8 -*-
'''
*****************************************
Author: SunShijiang
Date: 2021-10-21 17:15:08
LastEditTime: 2021-11-19 08:09:52
FilePath: /蓝湖自动化项目/uiframework/runner/suite.py
Description: 
*****************************************
'''
#! /usr/bin/env python3
# _*_ coding: utf-8 _*_

import unittest
import sys
sys.path.append('../')

from base.running_report import RunningReport
from case.test_item_list import TestTopBar


if __name__ == "__main__":
    run = RunningReport()
    run.run_all_case(py_name='test_register.py')
    run.send_email()
    # suite = unittest.TestSuite()
    # r = RunningReport()
    # suite.addTest(TestTopBar('test_create_item'))
    # r.run_report(suite)


