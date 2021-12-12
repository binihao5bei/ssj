#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

import logging
import os
import sys
from datetime import datetime, timedelta, timezone

from core.util import local_date


def is_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)


class RunningLog(object):
    """
    log_file_path: 日志生成存放路径；
    参数为 None 时 目标 py 文件在根目录下的文件夹内时使用；
    参数为 1 时 目标 py 文件直接在根目录下时使用；
    日志命名为当前本地时间；
    formatter: 单行日志打印参数与样式，具体参数说明请看 Formatter 模块注释。
    """

    def __init__(self, logger, log_file_path=None):
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)
        # 获取 文件夹 路径
        folder_path = sys.path[0] + "/logs/"
        is_folder(folder_path)
        if not log_file_path:
            log_file_path = folder_path + local_date() + ".log"
        if not self.logger.handlers:
            formatter = logging.Formatter(
                "%(asctime)s::%(levelname)s::%(name)s-->%(message)s"
            )
            self.file_handle = logging.FileHandler(log_file_path, encoding="utf-8")
            self.file_handle.setLevel(logging.DEBUG)
            self.file_handle.setFormatter(formatter)
            self.logger.addHandler(self.file_handle)

    def get_log(self):
        return self.logger

    def close_handle(self):
        """
        关闭日志系统，释放内存占用；
        一般用在 tearDown 内。
        """
        self.logger.removeHandler(self.file_handle)
        self.file_handle.close()
