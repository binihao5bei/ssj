# coding:utf-8
import allure
import pytest


@allure.story("全局搜索")
@pytest.mark.dependency(name="search", depends=["create_team"], scope="session")
def test_search(rq, value):
    rq(value)
