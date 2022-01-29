
import sys
from time import sleep
from common.config import dataPath
from seldom.testdata.conversion import json_to_list
import pytest
from page.baidu import BaiduElem
import allure


@allure.feature("参数化测试")
class TestParamertrize():
    def setup_class(cls):
        cls.dataPath = dataPath

    @pytest.mark.parametrize(
        "name, search_key",
        [("1", "Selenium"),
         ("2", "pytest文档"),
         ("3", "pytest-html"),
         ],
        ids=["case1", "case2", "case3"]
    )
    @allure.story("test001-参数化1")
    def test_baidu_search_param(self, name, search_key, page, base_url):
        page.goto(base_url)
        page.type(BaiduElem.search_input, search_key)
        page.click(BaiduElem.search_button)
        sleep(2)
        assert page.title() == search_key + "_百度搜索"


    @pytest.mark.parametrize(
        "name, search_key",
        json_to_list(dataPath + "/data_file.json")
    )
    @allure.story("test002-参数化2")
    def test_baidu_search_data_file(self, name, search_key, page, base_url):
        page.goto(base_url)
        page.type(BaiduElem.search_input, search_key)
        page.click(BaiduElem.search_button)
        sleep(2)
        assert page.title() == search_key + "_百度搜索"
