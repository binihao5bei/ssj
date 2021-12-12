import base64
import re
import sys
from datetime import datetime, timedelta, timezone
from string import Template

import pyotp
from configobj import ConfigObj
from ruamel.yaml import YAML


def local_date():
    bj_time = (
        datetime.utcnow()
        .replace(tzinfo=timezone.utc)
        .astimezone(timezone(timedelta(hours=8)))
    )
    path_time = bj_time.strftime("%Y-%m-%d-%H-%m")
    return path_time


def replace_var(source, data):
    variable_regexp = r"\$<([\w_]+)>"
    result = re.findall(variable_regexp, source)
    if result:
        for key in result:
            if data:
                if data.get(key) is not None:
                    source = source.replace(f"$<{key}>", f"{data.get(key)}")
    return source


class ApiInfo:
    """接口信息"""

    def __init__(self):
        self.base_path = sys.path[0]
        self.api_path = self.base_path + "/config/interface.yaml"
        self.data_path = self.base_path + "/config/data.yaml"
        self.case_path = self.base_path + "/config/cases.yaml"

    @classmethod
    def load(cls, path):
        with open(path, encoding="utf-8") as f:
            yaml = YAML(typ="safe")
            return yaml.load(f)

    def get_api_data(self, name):
        f_data = self.load(self.api_path)
        api = f_data.get(name)
        data = api.get("data")
        return data

    @property
    def data_info(self):
        return self.load(self.data_path)

    def get_data(self, key):
        return self.data_info[key]

    @property
    def case_info(self):
        return self.load(self.case_path)

    @property
    def api_data(self):
        return self.load(self.api_path)

    @staticmethod
    def base_url(api_path=""):
        config = ConfigObj("pytest.ini", encoding="UTF8")
        env = config.get("pytest").get("base_env", "")
        if env in ["k8sv1", "k8sv2", "", "pre"]:
            if "notify" in api_path or "recently_used_project" in api_path:
                env = "lhnotify"
            elif "ws_admin" in api_path:
                env = "ws-admin"
            elif "short" in api_path:
                env = ""
            elif "image_contrast" in api_path:
                env = ""
        elif env in ["zz-test"]:
            if "notify" in api_path or "recently_used_project" in api_path:
                env = "lhnotify-zz-test"
            elif "ws_admin" in api_path:
                env = "ws-admin"
        if env:
            env += "."
        return f"https://{env}lanhuapp.com"

    def api_info(self, name, params):
        api_data = self.api_data
        api = api_data.get(name)
        api_path = api.get("address")
        base_url = self.base_url(api_path)
        url = base_url + Template(api_path).safe_substitute(params)
        method = api.get("method")
        body_type = api.get("body_type")
        return url, method, body_type


def create_code():
    key = base64.b32encode(b"Vk1uyG9QxBa7X5Cj")
    totp = pyotp.TOTP(key, interval=15 * 60)
    return totp.now()
