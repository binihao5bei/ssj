# -*- coding:UTF-8 -*-
'''
*****************************************
Author: SunShijiang
Date: 2021-10-06 16:44:31
LastEditTime: 2021-10-18 17:40:24
FilePath: /未命名文件夹/test1.py
Description: 
*****************************************
'''
# -*- coding:UTF-8 -*-
#安装库：pip3 install PyYaml
import yaml

def load_yaml_data(file_path):
    with open(file_path, encoding='utf-8') as f:
        data = yaml.safe_load(f)
    print(f"加载yaml文件: {file_path} 数据为: {data}")
    return data

print(load_yaml_data('./test1.yaml'))