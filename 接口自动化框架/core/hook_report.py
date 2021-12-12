from datetime import datetime

from config.config import *
from core.client import HttpClient
from core.oss_log import UploadLogs
from core.util import *


class SendReport:
    def __init__(self):
        self.elements = []
        self.status = []
        self.log_url, self.monitor_url, self.html_url = UploadLogs().up()
        self.count = {}
        self.com()

    def env(self):
        config = ConfigObj("pytest.ini", encoding="UTF8")
        env = config.get("pytest").get("base_env", "")
        return env

    def com(self):
        com_status = [status for status in results.values()]
        self.count["passed"] = com_status.count("passed")
        self.count["failed"] = com_status.count("failed")
        self.count["total"] = len(com_status)

    def get_elements(self):
        for (case, status) in results.items():
            self.status.append(status)
            if "passed" not in status:
                text = f"\n{case}:  {status}".replace("failed", "**failed**")
                self.elements.append({"tag": "markdown", "content": text})

    def com_text(self):
        passed = self.count["passed"]
        failed = self.count["failed"]
        total = self.count["total"] if self.count["total"] else 1
        com_text = f"用例总数：{total}  成功条数：{passed}  失败条数：{failed}  成功率：{passed / total * 100:.2f}%"
        print(com_text)
        return com_text

    def boom_text(self):
        boom_text = ""
        if boom:
            num = len(boom)
            text = [f"{name}: {status}" for name, status in boom.items()]
            boom_str = "\n".join(text)
            boom_text = f"\n有 **{num}** 个接口5XX：\n{boom_str}\n<at id=all></at>"
        return boom_text

    def com_elements(self):
        summary = self.com_text() + self.boom_text()
        self.elements.extend(
            [
                {
                    "tag": "markdown",
                    "content": "\n --------------\n" + summary,
                },
                {
                    "tag": "markdown",
                    "content": f"[点击查看：测试日志]({self.log_url}) [完整测试报告]({report_msg.get('address')})",
                },
            ]
        )
        return self.elements

    def send_qa_report(self):
        base_url = "http://39.105.181.226:5000/"
        api_path = "/addRunHistory.json"
        url = base_url + api_path
        env = self.env()
        if env in ["k8sv1", "k8sv2", ""]:
            env = "online"
        elif env in ["next", "pre"]:
            env = "pre"
        else:
            env = "test"
        error_num = self.count.get("failed")
        data = {
            "type": "2",
            "module": "主站 API",
            "result_status": 1 if error_num else 0,
            "total_case": self.count.get("total"),
            "error_num": error_num,
            "result_txt": self.log_url,
            "result_html": self.html_url,
            "env": env,
        }

        client = HttpClient(url=url, method="post", body_type="json", session=None)
        client.set_body(data)
        client.send()

    def send_feishu_report(self):
        url = (
            f"https://open.feishu.cn/open-apis/bot/v2/hook/{report_msg.get('hook_id')}"
        )

        data = {
            "msg_type": "interactive",
            "card": {
                "config": {"wide_screen_mode": True, "enable_forward": True},
                "elements": self.com_elements(),
                "header": {
                    "title": {
                        "content": f"{datetime.today().date()} 接口测试报告",
                        "tag": "plain_text",
                    }
                },
            },
        }

        client = HttpClient(url=url, method="post", body_type="json", session=None)
        client.set_body(data)
        client.send()

    def send_report(self):
        self.send_feishu_report()
        self.send_qa_report()
