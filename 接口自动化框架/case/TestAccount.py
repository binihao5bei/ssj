# coding:utf-8
import allure
import pytest


@allure.story("检测邮箱")
def test_check_email(rq, value):
    rq(value)


@allure.story("获取短信验证码")
@pytest.mark.dependency(name="register")
def test_send_sms_code(rq, value):
    rq(value)


@allure.story("短信注册")
@pytest.mark.dependency(name="register")
def test_sms_register(rq, value):
    rq(value)


@allure.story("初始化")
@pytest.mark.dependency(name="register")
def test_register(rq, value):
    rq(value)


@allure.story("登录接口")
@pytest.mark.dependency(name="login")
def test_login(rq, value):
    rq(value)


@allure.story("退出登录")
@pytest.mark.dependency(name="logout", depends=["login"])
def test_logout(rq, value):
    rq(value)


@allure.story("获取用户团队")
def test_user_teams(rq, value):
    rq(value)


@allure.story("忘记密码发送邮件")
def test_reset_password(rq, value):
    rq(value)


@allure.story("邮件修改密码")
def test_put_reset_password(login, rq, value):
    rq(value)


@allure.story("修改密码")
@pytest.mark.dependency(depends=["register"])
def test_change_password(rq, value):
    rq(value)


@allure.story("修改用户信息")
@pytest.mark.dependency(depends=["login"])
def test_put_userinfo(rq, value):
    rq(value)


@allure.story("获取个人设置")
@pytest.mark.dependency(depends=["login"])
def test_get_user_settings(rq, value):
    rq(value)


@allure.story("个人操作设置")
@pytest.mark.dependency(depends=["login"])
def test_user_profile(rq, value):
    rq(value)


@allure.story("用户信息")
@pytest.mark.dependency(depends=["login"])
def test_user_detail(rq, value):
    rq(value)


@allure.story("获取当前用户的配置信息")
@pytest.mark.dependency(depends=["login"])
def test_current_user_in_list(rq, value):
    rq(value)


@allure.story("获取版本更新")
@pytest.mark.dependency(depends=["login"])
def test_version_tips(rq, value):
    rq(value)


@allure.story("微信")
@pytest.mark.dependency(depends=["login"])
def test_wechat(rq, value):
    rq(value)


@allure.story("飞书")
@pytest.mark.dependency(depends=["login"])
def test_lark_lark(rq, value):
    rq(value)


@allure.story("ws_url")
@pytest.mark.dependency(depends=["login"])
def test_ws_url(rq, value):
    rq(value)


@allure.story("用户弹窗信息")
@pytest.mark.dependency(depends=["login"])
def test_user_pop_up(rq, value):
    rq(value)
