# coding:utf-8
import allure
import pytest


@allure.story("下载插件")
def test_down_file(rq, value):
    rq(value)


@allure.story("app版本")
def test_app_version(rq, value):
    rq(value)
