#!/bin/sh

#获取用户目录名称
dir=`whoami`

#从os-release文件里取出NAME
os_name=`cat /etc/os-release | grep -w 'NAME' | awk -F "[\"\"]" '{printf $2}'`
#判断系统是否为rpm的依据
r_name="NeoKylin Linux Desktop"

#获取系统的架构
os_arch=`arch`

#用户架构
r_arch_x86="x86_64"
r_arch_arm="aarch64"
r_arch_mips="mips64"

#获取最新下载支线
echo "请手动填写要下载的支线：(develop,develop-2.1...)"
read input

#获取x86最新下载链接
d_link_x86=`curl "http://build.sogou-inc.com/system_build/out_interface/common/getlastpackage.php?project=ime_bs_linux&class=ime_bs_linux&branch=$input"`

#获取arm deb最新下载链接
d_link_arm=`curl "http://build.sogou-inc.com/system_build/out_interface/common/getlastpackage.php?project=ime_bs_linux&class=ime_bs_linux_arm64&branch=$input"`

#获取mips deb最新下载链接
d_link_mips=`curl "http://build.sogou-inc.com/system_build/out_interface/common/getlastpackage.php?project=ime_bs_linux&class=ime_bs_linux_mips64&branch=$input"`

#获取mips rpm最新下载链接
d_link_mips_rpm=`curl "http://build.sogou-inc.com/system_build/out_interface/common/getlastpackage.php?project=ime_bs_linux&class=ime_bs_linux_mips64_rpm&branch=$input"`

#获取arm rpm最新下载链接
d_link_arm_rpm=`curl "http://build.sogou-inc.com/system_build/out_interface/common/getlastpackage.php?project=ime_bs_linux&class=ime_bs_linux_arm64_rpm&branch=$input"`

#获取x86安装包下载后的文件解压后的文件夹名
b_name_x86=$(basename $d_link_x86 .zip)

#获取arm deb安装包下载后的文件解压后的文件夹名
b_name_arm=$(basename $d_link_arm .zip)

#获取mips deb安装包下载后的文件解压后的文件夹名
b_name_mips=$(basename $d_link_mips .zip)

#获取mips rpm安装包下载后的文件解压后的文件夹名
b_name_mips_rpm=$(basename $d_link_mips_rpm .zip)

#获取arm rpm安装包下载后的文件解压后的文件夹名
b_name_arm_rpm=$(basename $d_link_arm_rpm .zip)

#卸载输入法
sh Uninstall.sh
sleep 3

#x86架构deb安装包
if [ "$os_name"x != "$r_name"x ] && [ "$os_arch"x = "$r_arch_x86"x ];then  
    #下载zip安装包
    wget -v -P /home/$dir/InstallPackage/x86_64 $d_link_x86
    sleep 3
    #进入解压目录
    cd /home/$dir/InstallPackage/x86_64
    #解压文件
    unzip -o -d /home/$dir/InstallPackage/x86_64/$b_name_x86 $b_name_x86.zip
    sleep 3
    #进入安装目录
    cd /home/$dir/InstallPackage/x86_64/$b_name_x86
    #输入系统密码
    echo 123 | sudo -S dpkg -i *.deb
    #安装输入法
    #sudo dpkg -i *.deb
    sleep 3
    rm -rf /home/$dir/InstallPackage/x86_64/*

#arm架构deb安装包    
elif [ "$os_name"x != "$r_name"x ] && [ "$os_arch"x = "$r_arch_arm"x ];then 
    #下载zip安装包
    wget -v -P /home/$dir/InstallPackage/arm $d_link_arm
    sleep 3
    #进入解压目录
    cd /home/$dir/InstallPackage/arm
    #解压文件
    unzip -o -d /home/$dir/InstallPackage/arm/$b_name_arm $b_name_arm.zip
    sleep 3
    #进入安装目录
    cd /home/$dir/InstallPackage/arm/$b_name_arm
    #输入系统密码
    echo 123 | sudo -S dpkg -i *.deb
    #安装输入法
    #sudo dpkg -i *.deb
    sleep 3
    rm -rf /home/$dir/InstallPackage/arm/*

#mips架构deb安装包  
elif [ "$os_name"x != "$r_name"x ] && [ "$os_arch"x = "$r_arch_mips"x ];then
    #下载zip安装包
    wget -v -P /home/$dir/InstallPackage/mips $d_link_mips
    sleep 3
    #进入解压目录
    cd /home/$dir/InstallPackage/mips
    #解压文件
    unzip -o -d /home/$dir/InstallPackage/mips/$b_name_mips $b_name_mips.zip
    sleep 3
    #进入安装目录
    cd /home/$dir/InstallPackage/mips/$b_name_mips
    #输入系统密码
    echo 123 | sudo -S dpkg -i *.deb
    #安装输入法
    #sudo dpkg -i *.deb
    sleep 3
    rm -rf /home/$dir/InstallPackage/mips/*

#x86架构rpm安装包
elif [ "$os_name"x = "$r_name"x ] && [ "$os_arch"x = "$r_arch_x86"x ];then    
    #下载zip安装包
    wget -v -P /home/$dir/InstallPackage/x86_64 $d_link_x86
    sleep 3
    #进入解压目录
    cd /home/$dir/InstallPackage/x86_64
    #解压文件
    unzip -o -d /home/$dir/InstallPackage/x86_64/$b_name_x86 $b_name_x86.zip
    sleep 3
    #进入安装目录
    cd /home/$dir/InstallPackage/x86_64/$b_name_x86
    #输入系统密码
    echo 123 | sudo -S yum install *.rpm
    #安装输入法
    #sudo yum install *.rpm
    #输入y继续安装
    echo y | sudo -S yum install *.rpm
    sleep 3
    rm -rf /home/$dir/InstallPackage/x86_64/*

#mips架构rpm安装包
elif [ "$os_name"x = "$r_name"x ] && [ "$os_arch"x = "$r_arch_mips"x ];then  
    #下载zip安装包
    wget -v -P /home/$dir/InstallPackage/mips $d_link_mips_rpm
    sleep 3
    #进入解压目录
    cd /home/$dir/InstallPackage/mips
    #解压文件
    unzip -o -d /home/$dir/InstallPackage/mips/$b_name_mips_rpm $b_name_mips_rpm.zip
    sleep 3
    #进入安装目录
    cd /home/$dir/InstallPackage/mips/$b_name_mips_rpm
    #输入系统密码
    echo 123 | sudo -S yum install *.rpm
    #安装输入法
    #sudo yum install *.rpm
    #输入y继续安装
    echo y | sudo -S yum install *.rpm
    sleep 3
    rm -rf /home/$dir/InstallPackage/mips/*

#arm架构rpm安装包
else
    #下载zip安装包
    wget -v -P /home/$dir/InstallPackage/arm $d_link_arm_rpm
    sleep 3
    #进入解压目录
    cd /home/$dir/InstallPackage/arm
    #解压文件
    unzip -o -d /home/$dir/InstallPackage/arm/$b_name_arm_rpm $b_name_arm_rpm.zip
    sleep 3
    #进入安装目录
    cd /home/$dir/InstallPackage/arm/$b_name_arm_rpm
    #输入系统密码
    echo 123 | sudo -S yum install *.rpm
    #安装输入法
    #sudo yum install *.rpm
    #输入y继续安装
    echo y | sudo -S yum install *.rpm
    sleep 3
    rm -rf /home/$dir/InstallPackage/arm/*
fi

