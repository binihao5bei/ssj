#!/bin/sh


echo "授权UI已验证完成！！！"
echo "是否要重启系统开始使用输入法以验证授权功能？please输入：y/n"
read input

if [ "$input"x = "y"x ] || [ "$input"x = "Y"x ];then
    echo 123 |sudo -S killall Xorg
    #sudo killall Xorg
elif [ "$input"x = "n"x ] || [ "$input"x = "N"x ];then
    echo "那你自己注销系统吧，或者手动重启fcitx，要不然不让用！！！"
    break
else
    echo "输入错误，你抬杠那？自己注销！"
fi

