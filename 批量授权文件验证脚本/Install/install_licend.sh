#!/bin/sh

#获取用户目录名称
dir=`whoami`

#从os-release文件里取出NAME
os_name=`cat /etc/os-release | grep -w 'NAME' | awk -F "[\"\"]" '{printf $2}'`
#判断系统是否为rpm的依据


wd=$(dirname $(dirname $(dirname '$PWD')))
echo $wd
#获取最新下载支线
echo "请手动填写要下载的版本号：(1.0.0/3xxx)，注意第三个符号为/而非."
read input


#获取授权文件安装包的最新下载链接
d_link_x86="http://installer.sogou-inc.com/mirror_installer/ime_bs_linux/ime_bs_linux_license/0000/$input/sogouime_license_pkg.zip"




#下载zip安装包
wget -v -P $wd $d_link_x86
sleep 3

#解压文件
unzip -o -d $wd/sogouime_license_pkg sogouime_license_pkg.zip
sleep 3
rm -rf sogouime_license_pkg.zip