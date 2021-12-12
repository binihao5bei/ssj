import json
import os.path
import random

# import datetime
import allure
import jsonpath
import pytest
import requests
import urllib3
from config.config import PARAMS


class BodyType(object):
    URL_ENCODE = "url-encode"
    JSON = "json"
    XML = "xml"
    FILES = "form-data"


class Method(object):
    GET = "get"
    POST = "post"
    PUT = "put"
    DELETE = "delete"


class HttpClient(object):
    def __init__(
        self, url, data=None, session=None, method="GET", body_type=None, timeout=120
    ):
        self.url = url
        self.method = method
        self.timeout = timeout
        self.body_type = body_type
        self.headers = {}
        self.body = data
        self.res = None
        self.flag = 0
        self.act = None
        self.session = session if session else requests.session()

    def save_session(self):
        PARAMS["session"] = self.session

    def set_header(self, key, value):
        self.headers[key] = value

    def set_headers(self, dic):
        if dic is not None:
            if isinstance(dic, dict):
                self.headers = dic
            else:
                raise Exception("请求头请以字典格式传递")

    def set_cookie(self, dic):
        if dic:
            if isinstance(dic, dict):
                lis = []
                for k, v in dic.items():
                    lis.append("{k}={v}".format(k=k, v=v))
                cookie_str = ";".join(lis)
                if "cookie" in self.headers.keys():
                    self.headers["cookie"] += cookie_str
                else:
                    self.headers["cookie"] = cookie_str
            else:
                print(Exception("Cookie请以字典格式传递"))

    def set_body(self, data):
        self.body = data
        # if isinstance(data, dict):
        #     self.body = data
        # else:

    #     #     raise Exception('请求正文请以字典格式传递')
    #
    # def set_param(self, name, value):
    #     if value is not None:
    #         PARAMS[name] = value
    #     else:
    #         with pytest.assume:
    #             assert False, f"{name}：不存在"

    def send(self):
        urllib3.disable_warnings()
        try:
            if self.method == Method.GET:
                self.res = self.session.get(
                    url=self.url,
                    headers=self.headers,
                    params=self.body,
                    timeout=self.timeout,
                    verify=False,
                )
            elif self.method == Method.PUT:
                self.res = self.session.put(
                    url=self.url,
                    headers=self.headers,
                    json=self.body,
                    timeout=self.timeout,
                    verify=False,
                )
            elif self.method == Method.DELETE:
                self.res = self.session.delete(
                    url=self.url,
                    headers=self.headers,
                    json=self.body,
                    timeout=self.timeout,
                    verify=False,
                )

            elif self.method == Method.POST:
                if self.body_type == BodyType.URL_ENCODE:
                    self.headers["Content-Type"] = "application/x-www-form-urlencoded"
                    self.res = self.session.post(
                        url=self.url,
                        headers=self.headers,
                        data=self.body,
                        timeout=self.timeout,
                        verify=False,
                    )
                elif self.body_type == BodyType.JSON:
                    self.headers["Content-Type"] = "application/json"
                    self.headers["User-From"] = "test"
                    self.res = self.session.post(
                        url=self.url,
                        headers=self.headers,
                        json=self.body,
                        timeout=self.timeout,
                        verify=False,
                    )

                elif self.body_type == BodyType.XML:
                    self.headers["Content-Type"] = "text/xml"
                    self.res = self.session.post(
                        url=self.url,
                        headers=self.headers,
                        data=self.body.get("xml"),
                        timeout=self.timeout,
                        verify=False,
                    )
                elif self.body_type == BodyType.FILES:
                    file = self.body.get("files")
                    del self.body["files"]
                    self.res = self.session.post(
                        url=self.url,
                        headers=self.headers,
                        files={
                            "value": file,
                            "name": "imageA.png",
                            "Content-Type": "image/png",
                        },
                        data=self.body,
                        timeout=self.timeout,
                        verify=False,
                    )

            else:
                raise Exception("不支持的请求方法类型", self.method)
        except Exception as e:
            raise Exception(f"请求发送失败--self.url ", e)
        with allure.step("%s请求接口" % self.method):
            allure.attach(self.url, name="请求地址")
            allure.attach(str(self.headers), "请求头")
            if self.body:
                allure.attach(
                    json.dumps(self.body, indent=4),
                    name="请求参数",
                    attachment_type=allure.attachment_type.JSON,
                )
            allure.attach(f"{self.res.status_code}", name="响应状态码")
            allure.attach(f"{self.res_times}毫秒", name="响应时间")
            if self.res.text:
                allure.attach(
                    json.dumps(self.res_to_json_object(), indent=4),
                    name="响应内容",
                    attachment_type=allure.attachment_type.JSON,
                )

    @property
    def res_text(self):
        if self.res is not None:
            return self.res.text
        else:
            print("响应为空")
            return None

    def res_to_json_object(self):
        try:
            return self.res.json()
        except Exception:
            print("响应的json格式错误")
            return self.res_text

    @property
    def res_status_code(self):
        if self.res is not None:
            return self.res.status_code
        else:
            print("响应为空")
            return None

    @property
    def session_cookie(self):
        return requests.utils.dict_from_cookiejar(self.session.cookies)

    @property
    def res_cookies(self):
        if self.res is not None:
            return self.res.cookies
        else:
            print("响应为空")
            return None

    @property
    def res_cookiejar_cookies(self):
        return requests.utils.dict_from_cookiejar(self.res_cookies)

    @property
    def res_times(self):
        if self.res is not None:
            return round(self.res.elapsed.total_seconds() * 1000)
        else:
            print("响应为空")
            return 100000

    def res_to_json_path(self, path, index=0):
        if isinstance(path, list):
            path, index = path
        a = self.res_to_json_object()
        if a is not None:
            return jsonpath.jsonpath(a, path)[index]

    def res_to_json_paths(self, path):
        a = self.res_to_json_object()
        if a is not None:
            return jsonpath.jsonpath(a, path)

    # 断言
    def check_status_code_is_200(self):
        act = self.res_status_code
        with pytest.assume:
            assert self.res_status_code == 200, f"响应状态码错误：实际结果{act}, 预期结果{200}"

    def check_status_code(self, exp):
        if exp:
            act = self.res_status_code
            assert act // 500 != 1, f"接口状态码{act}"
            with pytest.assume:
                assert self.res_status_code == exp, f"响应状态码错误：实际结果{act}, 预期结果{exp}"

    def check_times_less_than(self, exp):
        act = self.res_times
        with pytest.assume:
            assert self.res_times < exp, f"响应超时：实际结果{act}ms, 预期结果小于{exp}ms"

    def check_text_equal(self, exp):
        act = self.res_text
        with pytest.assume:
            assert self.res_text == exp, f"响应内容错误：实际结果{act}, 预期结果{exp}"

    def check_text_contains(self, exp):
        act = self.res_text
        with pytest.assume:
            assert exp in self.res_text, f"响应内容错误：实际结果{act}, 预期结果{exp}"

    def get_json_value(self, path, index=0):
        a = self.res_to_json_object()
        if a is not None:
            act_list = jsonpath.jsonpath(a, path)
            if act_list:
                if index == 0:
                    r_index = random.randint(0, len(act_list) - 1)
                    act = act_list[r_index]
                else:
                    act = act_list[index - 1]
                return act
            else:
                with pytest.assume:
                    assert False, f" {path}json值不存在"
        else:
            with pytest.assume:
                assert False, "响应非正确的json格式: \n" + self.res_text

    def check_json_paths(self, assertion: dict):
        with allure.step("返回值断言"):
            if assertion:
                for path, value in assertion.items():
                    act = self.get_json_value(f"$.{path}")
                    if value:
                        if value == "exist":
                            act = "exist" if act else "not exist"
                        with pytest.assume:
                            assert act in [
                                value,
                                str(value),
                            ], f"响应内容错误：实际结果{act}, 预期结果{value}"
                        allure.attach(f"实际结果:{act},预期结果:{value}", name=path)

    def check_code_assertion(self, value):
        self.check_status_code(value.get("status", 200))
        self.check_json_paths(value.get("assertion"))
