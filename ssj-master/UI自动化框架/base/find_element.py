#! /usr/bin/env python3
# _*_ coding: utf-8 _*_

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from base.running_log import RunningLog
from util.read_ini import ReadIni, ReadIni2
from config.common_config import TIMEOUT


class FindElement(object):

    def __init__(self, driver, file_name=None, section=None):
        self.driver = driver
        self.readini = ReadIni(file_name=file_name, section=section)

    # 定位元素
    def get_element(self, key):
        data = self.readini.get_value(key)
        method, value = data.split('->')
        locator = (method, value)
        if not isinstance(locator, tuple):
            print("locator参数类型错误，传元组： loc = ('id','value1')")
        else:
            try:
                print("正在定位元素信息：定位方式-->%s, value值-->%s" % (locator[0], locator[1]))
                element = WebDriverWait(timeout=12, poll_frequency=0.5, driver=self.driver).until(
                    lambda x: x.find_element(*locator))
                return element
            except Exception:
                raise Exception("定位元素超时，未定位到该元素")


class FindElement2(object):
    """
    初始化内引用 read_ini.py 读取配置文件内的 element 信息传递给 get_element & get_elements 两个函数使用。
    key : 继承自 read_ini.py 内的 get_value 读取配置文件信息;
    get_elements(target) : 对 elements 定位方式拿回的数据，循环查找匹配对象的赋值变量;
    """

    def __init__(self, driver, ini_file_path=None, node=None):
        self.driver = driver
        self.read_ini = ReadIni2(ini_file_path=ini_file_path, node=node)
        self.read_inis = ReadIni2(ini_file_path=ini_file_path, node=node)
        self.logger = RunningLog(logger='find_element').get_log()
        self.find_fun_map = {
            "id": By.ID,
            "xpath": By.XPATH,
            "css": By.CSS_SELECTOR,
        }

    def get_element(self, key):
        """element 基础定位方式"""
        data = self.read_ini.get_value(key)
        by, element = data.split('->')
        ele = None

        try:
            by_type = self.find_fun_map.get(by)
            ele = WebDriverWait(self.driver, TIMEOUT).until(
                EC.presence_of_element_located((by_type, element))) if by_type else None

        except Exception as e:
            self.logger.error(f"doesn't find element [{key}]")
            self.logger.error(e)
        finally:
            return ele

    def get_elements(self, key, target):
        """elements 定位方式"""
        datas = self.read_inis.get_value(key)
        bys, elements = datas.split('->')
        ele = None

        try:
            bys_type = self.find_fun_map.get(bys)
            eles = WebDriverWait(self.driver, TIMEOUT).until(
                EC.presence_of_all_elements_located((bys_type, elements))) if bys_type else None
            ele = (i for i in eles if i.text.strip() == target).__next__()
        except Exception as e:
            self.logger.error(f"doesn't find element [{key} {target}]")
            self.logger.error(e)
        finally:
            return ele

    def get_original_elements(self, key):
        """返回多个元素"""
        data = self.read_ini.get_value(key)
        by, element = data.split('->')
        eles = None

        try:
            by_type = self.find_fun_map.get(by)
            eles = WebDriverWait(self.driver, TIMEOUT).until(
                EC.presence_of_all_elements_located((by_type, element))) if by_type else None
        except Exception as e:
            self.logger.error(f"doesn't find elements [{key}]")
            self.logger.error(e)
            eles = None
        finally:
            return eles

    # 鼠标悬浮
    def hover_element(self, key):
        el = key
        ActionChains(self.driver).move_to_element(el).perform()


if __name__ == '__main__':
    pass



