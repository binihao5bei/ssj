# coding:utf-8
import allure
import pytest


@allure.story("存储生成的token")
@pytest.mark.dependency(name="store_token", depends=["login"], scope="session")
def test_store_token(rq, value):
    rq(value)


@allure.story("插件获取token")
@pytest.mark.dependency(depends=["store_token"])
def test_get_login_token(rq, value):
    rq(value)


@allure.story("插件获取团队")
@pytest.mark.dependency(depends=["store_token"])
def test_plugin_user_teams(rq, value):
    rq(value)


@allure.story("检测插件可上传状态")
@pytest.mark.dependency(depends=["store_token"])
def test_plugin_err_status(rq, value):
    rq(value)
