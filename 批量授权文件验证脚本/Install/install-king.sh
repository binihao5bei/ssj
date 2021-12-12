#!/bin/bash

echo "-----------------------"
echo "(a) 安装最新版输入法"
echo "(b) 安装自定义输入法"
echo "(c) 单纯的卸载一下输入法"
echo "(?) 退出"
echo "-----------------------"

read input

case $input in
    a)
    sh install_new.sh
    ;;
    b)
    sh install_zdy.sh
    ;;
    c)
    sh Uninstall.sh
    ;;
    ?)
    echo "你自己玩吧！"
    exit 1;;
esac
