#! /usr/bin/env python3
# _*_ coding: utf-8 _*_

import os
import logging
import datetime
import sys
sys.path.append('../')
from config.common_config import LOG_BASE_PATH


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
        self.log_file_path = log_file_path
        # 获得当前时间
        now = datetime.datetime.now()
        # 转换为指定的格式
        path_time = now.strftime("%Y-%m-%d_%H")
        if log_file_path is None:
            self.log_file_path = os.path.join(LOG_BASE_PATH, f"{path_time}.log")

        if not self.logger.handlers:
            self.file_handle = logging.FileHandler(self.log_file_path, encoding='utf-8')
            self.file_handle.setLevel(logging.INFO)

            # 定义日志打印内容
            formatter = logging.Formatter(
                '%(asctime)s --> %(filename)s --> %(name)s --> %(funcName)s --> %(levelno)s : %(levelname)s --> %(message)s')
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


if __name__ == "__main__":
    pass
