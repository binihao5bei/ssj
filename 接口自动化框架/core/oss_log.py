# -*- coding: utf-8 -*-
import os
import sys
from datetime import datetime, timedelta, timezone

import natsort
import oss2


def oss_upload_file(name, file):
    auth = oss2.Auth("LTAI4GGFVf9JMCGZ31NJvDFJ", "eZZ6YGMXDFJJofHEqe1hVZqw70vf7R")
    bucket = oss2.Bucket(
        auth,
        "https://oss-cn-beijing.aliyuncs.com",
        "395ed701-5bb5-4efc-8e5a-a38026b37793",
    )

    with open(file, "rb") as file_obj:
        file_push = bucket.put_object(
            name, file_obj, headers={"Content-Type": "application/json"}
        )
        if file_push.status == 200:
            upload_url = (
                "https://395ed701-5bb5-4efc-8e5a-a38026b37793.oss-cn-beijing.aliyuncs.com/"
                + name
            )
    file_obj.close()
    print(upload_url)
    return upload_url


def last_file(file_path):
    file_list = os.listdir(file_path)
    file_list = [i for i in file_list if "." in i]
    name = natsort.natsorted(file_list)[-1]
    path = file_path + name
    return name, path


def local_date():
    bj_time = (
        datetime.utcnow()
        .replace(tzinfo=timezone.utc)
        .astimezone(timezone(timedelta(hours=8)))
    )
    path_time = bj_time.strftime("%Y-%m-%d")
    return path_time


def is_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)


def upload_file(file_path):
    name, path = last_file(file_path)
    return oss_upload_file(name, path)


class UploadLogs:
    def __init__(self):
        self.home_path = sys.path[0]
        self.log_path = self.home_path + "/logs/"
        self.monitor_path = self.home_path + "/monitor/"
        self.html_path = self.home_path + "/reports/"

    def save_monitor(self, log_url):
        file_path = self.monitor_path + local_date() + ".txt"
        is_folder(self.monitor_path)
        with open(file_path, "a+") as file_obj:
            file_obj.write(f"LogUrl: {log_url}\n")
        file_obj.close()

    def up(self):
        log_url = upload_file(self.log_path)
        self.save_monitor(log_url)
        monitor_url = upload_file(self.monitor_path)
        html_url = upload_file(self.html_path)
        return log_url, monitor_url, html_url
