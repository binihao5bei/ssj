#! /usr/bin/env python3
# _*_ coding: utf-8 _*_

import time
import configparser

import os
import pytesseract
import pyautogui as pg
from PIL import Image
from PIL import ImageGrab
from config.common_config import IMG_PATH
from config.common_config import IMG_INI_FILE_PATH


# 断言-截图
def pil_screenshot(img_assert_name):
    img_path = os.path.join(IMG_PATH, 'img_assert/' + img_assert_name + '.png')
    img = ImageGrab.grab()
    img.save(img_path)
    time.sleep(1)
    config = configparser.ConfigParser()
    config.read(IMG_INI_FILE_PATH)
    config.set('ImgAssertPath', img_assert_name, img_path)
    with open(IMG_INI_FILE_PATH, 'w') as f:
        config.write(f)


# 断言-图片内容转文字
def tesseract_content(content_part=None, img_name=None):
    config = configparser.ConfigParser()
    config.read(IMG_INI_FILE_PATH)
    img_path = config.get('ImgAssertPath', img_name)
    img = Image.open(img_path)
    content = pytesseract.image_to_string(img, lang='chi_sim+eng')
    # print(content)
    if content_part in content:
        return True


def fix_pos_macos(x, y, w=0, h=0):
    return x//2+w//4, y//2+h//4


def close_page():
    pg.keyDown('command')
    pg.keyDown('w')
    pg.keyUp('w')
    pg.keyUp('command')


if __name__ == "__main__":
    # pil_screenshot('pycharm')
    print(tesseract_content('images', 'pycharm'))


