#!/bin/sh
#从os-release文件里取出NAME
os_name=`cat /etc/os-release | grep -w 'NAME' | awk -F "[\"\"]" '{printf $2}'`
#判断系统是否为rpm的依据
r_name="NeoKylin Linux Desktop"

echo "是否要卸载之前的输入法,y/n"
read input
#卸载输入法
if [ "$os_name"x != "$r_name"x ] && ([ "$input"x = "y"x ] || [ "$input"x = "Y"x ]);then
    #输入系统密码
    echo 123 | sudo -S dpkg -P sogouimebs wps-sogoupinyin sogouimebs-tongfang com.sogou.sogoupinyin-uos
    #卸载安装包
    #sudo dpkg -P sogouimebs  
elif [ "$os_name"x = "$r_name"x ] && ([ "$input"x = "y"x ] || [ "$input"x = "Y"x ]);then
    #输入系统密码
    echo 123 | sudo -S yum autoremove sogouimebs wps-sogoupinyin sogouimebs-tongfang
    #卸载安装包
    #sudo yum autoremove sogouimebs  
    #输入y继续卸载
    echo y | sudo -S yum autoremove sogouimebs
elif [ "$os_name"x != "$r_name"x ] && ([ "$input"x = "n"x ] || [ "$input"x = "N"x ]);then
    echo "那就覆盖安装了！！！"
    break
elif [ "$os_name"x = "$r_name"x ] && ([ "$input"x = "n"x ] || [ "$input"x = "N"x ]);then
    echo "那就覆盖安装了！！！"
    break
else
    echo "不和你玩了，自己卸载去！"
fi 
