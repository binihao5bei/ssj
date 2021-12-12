# coding = utf-8
from datetime import datetime
from time import time

import allure
import pytest
from config.config import *
from core.client import HttpClient
from core.util import *
from core.util import replace_var
from core.wrok_log import RunningLog
from faker import Faker


@pytest.fixture()
def api():
    def _api(api_name, data, params, cookie):
        url, method, body_type = ApiInfo().api_info(api_name, params)
        client = HttpClient(url=url, method=method, body_type=body_type)
        client.set_body(data)
        client.set_cookie(cookie)
        client.send()
        return client

    return _api


@pytest.fixture()
def rq(api):
    def _rq(value=None):
        if value is None:
            value = dict()
        data = value.get("data", {})
        params = value.get("params", {})
        # session = PARAMS.get("session", None)
        # session = None if not value.get("cookies", True) else PARAMS.get("session")
        need_get = value.get("get", {})
        need_set = value.get("set", {})
        api_name = value.get("api_name")
        generate = value.get("generate", {})
        up_dict = {}
        if generate:
            for key, val in generate.items():
                up_dict.update({key: data_f(val)})
            PARAMS.update(up_dict)
        for key, val in need_get.items():
            up_dict.update({key: get_value(val)})
        if up_dict:
            data = eval(replace_var(str(data), up_dict))
            params.update(up_dict)
        # files = data.get("files")
        # if files:
        #     data["files"] = open(files, "rb")
        if not api_name:
            raise ValueError("未填写api_name")
        cookie = {} if not value.get("cookies", True) else get_cookie()
        client = api(api_name=api_name, data=data, params=params, cookie=cookie)
        save_log(api_name + value.get("info"), client)
        status = client.res_status_code
        store_5_xx(api_name, status)
        client.check_code_assertion(value)
        save_values(need_set, client)

        # return client

    return _rq


def store_5_xx(api_name, status):
    if status // 500 == 1:
        boom[api_name] = status


def save_values(need_set: dict, client: object):
    if need_set:
        for key, path in need_set.items():
            if key == "cookie":
                set_value("cookie", client.session_cookie)
            else:
                set_value(key, client.res_to_json_path(path))


def set_value(key, value):
    if value not in [None, ""]:
        PARAMS.update({key: value})
    else:
        raise ValueError(f"{key} 不存在")


def data_f(value):
    f = Faker(locale="zh_CN")
    if value == "email":
        return f.ascii_safe_email()
    elif value == "uuid":
        return f.uuid4()
    elif value == "date":
        return datetime.now().strftime("%Y-%m-%d")
    elif value == "user_name":
        return f.user_name()
    elif value == "mobile":
        return "x" + str(int(round(time() * 10)))[1:]
    elif value == "code":
        return create_code()


def save_log(name, client):
    info = {
        "address": client.url,
        "status": client.res_status_code,
        "time": client.res_times,
    }
    LOG.update({name: info})


def get_value(key):
    value = PARAMS.get(key)
    return value if value else None


def get_cookie():
    cookie = get_value("cookie")
    if cookie:
        return cookie


# *********************************

#
@pytest.fixture
def login():
    data = {"email": "3@1.lanhuapp", "password": "111111"}
    url, method, body_type = ApiInfo().api_info(name="login", params={})
    client = HttpClient(url=url, method=method, body_type=body_type, session=None)
    client.set_body(data)
    client.send()
    client.save_session()
    return login


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item):
    # 获取钩子方法的调用结果
    out = yield
    # 从钩子方法的调用结果中获取测试报告
    report = out.get_result()
    if report.when == "call":
        value = item.funcargs.get("value")
        name = value.get("api_name") + value.get("info")
        results[item.name] = report.outcome
        log = RunningLog(logger=item.name)
        logger = log.get_log()
        log_info = LOG.get(name)
        if log_info:
            msg = f'执行状态：{report.outcome} 请求地址：{log_info.get("address")} 响应状态：{log_info.get("status")} 响应时间:{log_info.get("time")}'
            if report.outcome == "failed":
                logger.error(msg=msg)
            elif report.outcome == "error":
                logger.debug(msg=msg)
            else:
                logger.info(msg=msg)
        log.close_handle()
        print()

        # 钩子函数参数化


def pytest_generate_tests(metafunc):
    """ generate (multiple) parametrized calls to a test function."""
    case_name = str(metafunc.function.__name__).replace("test_", "")
    data = ApiInfo().get_data(case_name)
    if data:
        metafunc.parametrize("value", data, ids=[value.get("info") for value in data])


def pytest_collection_modifyitems(items) -> None:
    # item表示每个测试用例，解决用例名称中文显示问题
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode-escape")
        item._nodeid = item._nodeid.encode("utf-8").decode("unicode-escape")
