import os
PRO_PATH = os.path.dirname(os.path.abspath(__file__))


class RunConfig:
    """
    运行测试配置
    """
    # 运行测试用例的目录或文件
    # cases_path = os.path.join(PRO_PATH, "test_case")
    cases_path = os.path.join(PRO_PATH, "test_case", "test_001.py")
    #

    # 配置浏览器驱动类型(chromium, firefox, webkit)。
    browser = "chromium"

    # 运行模式（headless, headful）
    # mode = "headless"
    mode = "headful"

    # 配置运行的 URL
    # baseUrl = "https://www.baidu.com"
    baseUrl = "https://lanhuapp.com/"

    # 失败重跑次数
    rerun = "0"

    # 当达到最大失败数，停止执行
    max_fail = "5"

    # 报告路径（不需要修改）
    NEW_REPORT = None

    #测试的团队的链接
    team_url = baseUrl + "web/#/item?tid=fc8b78dd-56ca-442d-b564-0030635e9834&fid=all"

    team_name = "线上001"
