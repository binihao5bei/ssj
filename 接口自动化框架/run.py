# coding:utf-8
import sys

import pytest
from configobj import ConfigObj
from core.hook_report import SendReport
from core.util import *

if __name__ == "__main__":
    # env = ""
    if len(sys.argv) == 2:
        if sys.argv[1] in ["dev", "next", "k8sv1", "k8sv2", "zz-test", ""]:
            env = sys.argv[1]
    env = "zz-test"  # 写死环境
    config = ConfigObj("pytest.ini", encoding="UTF8")
    config["pytest"]["base_env"] = env
    config.write()
    path = sys.path[0]
    try:
        cases = []
        f_data = ApiInfo().case_info
        for suite in f_data.values():
            for x in suite:
                file_name, method_name = x.split("-")
                case = "::".join([f"{path}/case/{file_name}.py", method_name])
                cases.append(case)
            pytest.main(
                [
                    "--reruns=1",  # 失败重跑次数
                    # "--clean-alluredir",
                    "--alluredir=./allure-results",
                    "-s",
                    *cases,
                    f"--html=./reports/{local_date()}.html",  # 可选 输出html
                ]
            )
            with open("./allure-results/environment.properties", "w+") as f:
                f.write(f"base_url= {ApiInfo().base_url()}")
                f.close()

    except Exception as e:
        raise Exception(e)
    # finally:
    #     SendReport().send_report()
