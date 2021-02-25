# coding:utf-8
import os
import xlrd
import glob
import  xml.dom.minidom
import datetime
from xlrd import xldate_as_tuple

#获取当前文件所在一级父路径
Tpath=os.getcwd()


#拼接一级父路径与安装脚本文件夹名称生成该安装脚本的具体路径
path_install=os.path.join(Tpath,"Install")

print("输入法安装脚本路径：{}".format(path_install))
os.chdir(path_install)          #切换到该路径
print("开始安装输入法~~~~")
os.system('./install-king.sh')  #执行输入法安装脚本
print("开始下载批量的授权文件")
os.system('./install_licend.sh')#执行授权文件下载脚本
os.chdir(Tpath)                 #切换回原来的路径



#获取xlsx格式的文件名称
for excel_name in glob.glob("*.xlsx"):
    print("需求列表名称为：{}".format(excel_name))
#拼接一级父路径与xlsx文件名称生成该需求列表xlsx文件的具体路径
path_excel=os.path.join(Tpath,excel_name)
print("需求列表excel路径：{}".format(path_excel))
print("*"*50)

#拼接一级父路径与文件名称生成该授权文件的具体路径
path_licend=os.path.join(path_install,"sogouime_license_pkg")
print("授权文件路径：{}".format(path_licend))
print("*"*50)

#1.获取excel列表中的内容
excel = xlrd.open_workbook(path_excel)
sheet=excel.sheets()[0]
nrows=sheet.nrows
ncols=sheet.ncols
a=[]                   #读取excel列表中第一列（授权对象列）生成列表，用于和授权文件安装包中的授权对象进行比较
for i in range(nrows):
#    print(sheet.row_values(i)[0])
    a.append(sheet.row_values(i)[0])
a.remove('授权对象')    #移出第一行表头非相关内容
print("*"*50)  
print("获取需求列表中所有授权对象：{}".format(a))
print("需求列表中共有授权对象个数：{}".format(len(a)))
print("*"*50)  
 
d1=[]                  #读取excel列表中所有列生成字典，用于和授权文件安装完成后的xml文件中的所有授权信息进行比较
for i in range(nrows):
    for j in range(ncols):
        if j==0:                                 #获取excel表中第一列内容：授权对象
            cell_value0=sheet.row_values(i)[0]
        if j==1:                                 #获取excel表中第二列内容：授权开始时间
            ctype=sheet.cell(i,1).ctype          #获取当前表格属性（用于解决日期格式结果为显示数值型问题）
            cell_value1=sheet.row_values(i)[1]
            if ctype==3:
                date=datetime.datetime(*xldate_as_tuple(cell_value1, 0))   #转化当前表格属性从数值型-->日期型
                cell_value1=date.strftime('%Y-%m-%d')   
        if j==2:                                 #获取excel表中第三列内容：授权到期时间
            ctype=sheet.cell(i,2).ctype          
            cell_value2=sheet.row_values(i)[2]
            if ctype==3:
                date=datetime.datetime(*xldate_as_tuple(cell_value2, 0))
                cell_value2=date.strftime('%Y-%m-%d')
        if j==3:                                 #获取excel表中第四列内容：彻底过期时间
            ctype=sheet.cell(i,3).ctype
            cell_value3=sheet.row_values(i)[3]
            if ctype==3:
                date=datetime.datetime(*xldate_as_tuple(cell_value3, 0))
                cell_value3=date.strftime('%Y-%m-%d')
    d={
        'author':cell_value0,
        'active':cell_value1,
        'deactive':cell_value2,
        'outactive':cell_value3
        }
    d1.append(d)
d1.pop(0)             #移出表头不相关内容
#print(d1)
print(len(d1))

#2.获取授权文件压缩包中所有授权文件的名称
b=[]               #读取打包出的批量授权文件的授权对象名称生成列表，用于和excel需求表中的授权对象进行比较
for dirname in os.listdir(path_licend ):
    #print(dirname)
    b.append(dirname)
print("*"*50)  
print("获取打包的所有授权对象：{}".format(b))
print("授权文件安装包中共有个数：{}".format(len(b)))
print("*"*50)

aa=set(a)    #将列表转化成集合
bb=set(b)

if aa==bb:   #判断转化后的2个集合元素内容是否相等
    print("打包打出的授权对象 = 需求列表中的授权对象")
    print("开始安装授权文件！")
    count=0
    error_result=[]
    error_filename=[]
    for r in os.listdir(path_licend):
        TTpath=os.path.join(path_licend,r)
        print(TTpath)

        os.chdir(TTpath)
        os.system('./sogouime_license.bin')

        #打开xml文档
        dom = xml.dom.minidom.parse('/opt/apps/com.sogou.sogoupinyin-uos/files/.license/license.signed.xml')

        #得到文档元素对象
        root = dom.documentElement
        auth_name = root.getElementsByTagName('auth_name')[0].childNodes[0].data
        active_date=root.getElementsByTagName('active_date')[0].childNodes[0].data
        deactive_date=root.getElementsByTagName('deactive_date')[0].childNodes[0].data
        out_of_date=root.getElementsByTagName('out_of_date')[0].childNodes[0].data
        d2={                     #读取授权文件安装完成后xml中的授权信息生成字典，用于和excel表中的所有授权信息进行比较
            'author':auth_name,
            'active':active_date,
            'deactive':deactive_date,
            'outactive':out_of_date}
        print(d2)

        if d2 in d1:
            count+=1
            print("验证通过！！")
            print("-"*50)
            continue
        else:
            count+=0
            error_result.append(d2)
            error_filename.append(r)
            print("【{}】验证不通过，生成的xml文件中授权信息不符合需求".format(r))
            print("发生错误的授权文件信息为：{}".format(d2))
    print("一共验证通过了{}项".format(count))
    if count==len(d1):
        print("本次共验证{}个授权文件，验证全部通过~~~~".format(count))
    else:
        print("本次共验证{}个授权文件，其中验证通过{}个,【{}】验证未通过，验证失败的文件信息为：{}".format(len(d1),count,error_filename,error_result))

    print("*"*50)
else:
    print("打包打出的授权对象 ！= 安装完成后的授权对象")
    print("请检查打包是否完全符合需求？提测是否通过？")
#拼接一级父路径与安装脚本文件夹名称生成该安装脚本的具体路径
path_install=os.path.join(Tpath,"Install")
print("输入法安装脚本路径：{}".format(path_install))
os.chdir(path_install)
os.system('./loginout.sh')
print("*"*50)