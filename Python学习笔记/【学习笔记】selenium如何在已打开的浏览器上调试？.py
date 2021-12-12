【步骤】：
1.进入Chrome安装目录
2.打开终端并cd 到Chrome安装目录
3.执行命令：     chrome.exe --remote-debugging-port=9222 --user-data-dir="D:\selenium_ui_auto\chrome_temp"
    备注："D:\selenium_ui_auto\chrome_temp"为任意存在或新建的目录，最好是和项目脚本在同级目录下



*-------Python脚本代码如下 ↓ -------*

from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
import time
url="www.baidu.com"
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
chrome_driver = r"D:\code\python\selenium_ui_auto\driver\chromedriver.exe"
driver = webdriver.Chrome(chrome_driver, chrome_options=chrome_options) 
driver.get(url)
time.sleep(4)
driver.find_element_by_id('kw').send_keys(u'测试工程师小站')

*-------Python脚本代码如上 ↑ -------*