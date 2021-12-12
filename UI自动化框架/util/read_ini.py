#! /usr/bin/env python3
# _*_ coding: utf-8 _*_

import os
import configparser

from config.common_config import INI_FILE_PATH
from config.common_config import BASE_PATH


class ReadIni(object):

    def __init__(self, file_name=None, section=None):
        if file_name is None:
            self.file_name = 'page_element.ini'
        else:
            self.file_name = file_name
        self.path_ini = os.path.abspath(os.path.join(BASE_PATH, 'config', self.file_name))
        if section is None:
            self.section = "LoginElement"
        else:
            self.section = section

    def get_value(self, _key):
        cp = configparser.ConfigParser()
        cp.read(self.path_ini)
        _value = cp.get(self.section, _key)
        return _value


class ReadIni2(object):

    def __init__(self, ini_file_path=None, node=None):
        """初始化路径、节点"""
        self.ini_file_path = INI_FILE_PATH if not ini_file_path else ini_file_path
        self.node = 'LoginPageElement' if not node else node
        self.cf = self.load_ini(self.ini_file_path)

    @staticmethod
    def load_ini(ini_file_path):
        """读取 ini 文件"""
        cf = configparser.ConfigParser()
        cf.read(ini_file_path)
        return cf

    def get_value(self, key):
        """获取对应节点的 key"""
        data = self.cf.get(self.node, key)
        return data


if __name__ == '__main__':
    # print(os.getcwd())
    # print(BASE_PATH)
    # print(ReadIni().path_ini)
    ri = ReadIni(file_name='img_path.ini', section='ImgSlicePath')
    print(ri.get_value('img_china'))
