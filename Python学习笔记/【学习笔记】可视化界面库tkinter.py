from tkinter import *
import time

ssj=Tk()
ssj.title('这是我第一个Python程序')  #窗口标题
ssj.geometry('500x400+470+250')   # 窗口宽x窗口高+窗口距离上边距离+窗口距离左边距离）

"""------------------------------------------------------------"""
#1.Label标签：用于单行文本显示
label=Label(ssj,
text='欢迎来到Tkinter可视化界面学习',  #属性text如果需要执行后发生变化，则可以使用label.configure(text=newstring)来是显示内容发生变化
bg='#d3fbfb',
fg='red',
font=('华文新魏',18),
relief=SUNKEN
)
#法一：
label.configure(text='新的显示内容')
label.grid(row=1,column=1,columnspan=5)
#法二：
v=StringVar()   #定义一个变量
label2=Label(ssj,textvariable=v)
label2.grid(row=2,column=1,columnspan=5)
v.set('新的显示内容')
label2.update()
print(v.get()) #获取label标签的内容


"""------------------------------------------------------------"""
#2.Entry单行输入框：用户单行文本输入
#show=None表示明文显示
username=Entry(ssj,show=None)
username.grid(row=1,column=1)

#show=“*”表示以*形式密文显示
password=Entry(ssj,show="*")
password.grid(row=2,column=1)


"""------------------------------------------------------------"""
#3.Text多行文本框：用于多行文本的输入和输出显示
text=Text(ssj,height=10)
text.grid(row=3,column=1,columnspan=5)
text.delete('1.0',END)  #清空文本框所有内容
text.insert('insert','要插入的内容') #insert表示光标位置
text.insert(END,'要插入的内容') #表示在末尾插入，原来内容保存不变
text.get('1.0',END) #1.0表示第一行起，END表示最后一行，表示获取文本框所有内容


"""------------------------------------------------------------"""
#4.Buttorn按钮：用于单击触发时间
#普通的不带参数的时间绑定：command=函数名称(不带任何参数)
def hit_me():
    print('你点击了我')

#带传入参数的事件绑定：command= lambda: 函数名称(参数)
def add(a,b):
    result=a+b
    print(f'和是：{result}')
bt1=Button(ssj,text='点击',command=hit_me)
bt2=Button(ssj,text='加法',activeforeground='green',cursor='hand2',command=lambda:add(3,4)) #cursor表示鼠标样式，有pencil、hand1、hand2等
bt1.grid(row=4,column=2)
bt2.grid(row=4,column=3)


"""------------------------------------------------------------"""
#5.Listbox列表框：用于显示文本列表
listbox=Listbox(ssj)
listbox.grid(row=5,column=1)


"""------------------------------------------------------------"""
#6.Menu菜单：用于创建菜单
#基于主窗口创建菜单栏
menubar=Menu(ssj)

#基于菜单栏创建“文件”的子菜单项
filemenu=Menu(menubar)
#在菜单栏中创建一个子选项“文件”：add_cascade(),最重要的属性是menu，表示将菜单项关联到该子菜单
menubar.add_cascade(label='文件',menu=filemenu)
#创建“文件”的子菜单：add_command()
filemenu.add_command(label='新建')
filemenu.add_command(label='打开')
filemenu.add_command(label='保存')
filemenu.add_command(label='退出')

editmenu=Menu(menubar)
menubar.add_cascade(label='编辑',menu=editmenu)
editmenu.add_command(label='剪切')
editmenu.add_command(label='复制')
editmenu.add_command(label='粘贴')

helpmenu=Menu(menubar)
menubar.add_cascade(label='帮助',menu=helpmenu)
helpmenu.add_command(label='关于')
helpmenu.add_command(label='发行说明')
helpmenu.add_command(label='隐私声明')

#最后可以用窗口的 menu 属性指定我们使用哪一个作为它的顶层菜单
ssj.config(menu=menubar)



"""------------------------------------------------------------"""
#7.复选框
def select():
    if (var1.get()==1 and var2.get()==0):
        label.configure(text='I love python')
    elif (var1.get()==0 and var2.get()==1):
        label.configure(text='I love java')
    elif (var1.get()==1 and var2.get()==1):
        label.configure(text='I love python, also love java')
    elif (var1.get()==0 and var2.get()==0):
        label.configure(text='neither be loved')

var1=IntVar()
var2=IntVar()

c1=Checkbutton(ssj,text='python',variable=var1,onvalue=1,offvalue=0,command=select,state=NORMAL)
c2=Checkbutton(ssj,text='java',variable=var2,onvalue=1,offvalue=0,command=select,state=NORMAL)
c1.grid(row=6,column=1)
c2.grid(row=6,column=2)



"""------------------------------------------------------------"""
#8.单选框
v_radio=IntVar()
v_radio.set(2) #设置默认值

def get_value():
    print(v_radio.get())  #获取当前选中值

r1=Radiobutton(ssj,text='python',value=1,variable=v_radio,command=get_value)
r2=Radiobutton(ssj,text='java',value=2,variable=v_radio,command=get_value)
r3=Radiobutton(ssj,text='c++',value=3,variable=v_radio,command=get_value)
r1.grid(row=7,column=1)
r2.grid(row=7,column=2)
r3.grid(row=7,column=3)



"""------------------------------------------------------------"""
#9.窗口部件
#基于主窗口创建主框架
frame=Frame(ssj)
frame.pack()

#基于主框架创建第二层框架
frame1=Frame(frame)
frame2=Frame(frame)
frame1.pack(side='left')
frame2.pack(side='right')


label5=Label(frame1,text='Python')
label5.grid(row=1,column=1)

label6=Label(frame2,text='JAVA')
label6.grid(row=1,column=1)



"""------------------------------------------------------------"""
#10.消息窗口部件
import tkinter.messagebox
def show():
    tkinter.messagebox.showinfo(title='HI',message='你好')
    time.sleep(0.5)
    tkinter.messagebox.showwarning(title='HI',message='警告')
    time.sleep(0.5)
    tkinter.messagebox.showerror(title='HI',message='错误')
    time.sleep(0.5)
    tkinter.messagebox.askquestion(title='HI',message='询问') #返回yes 或 no
    time.sleep(0.5)
    tkinter.messagebox.askyesno(title='HI',message='询问') #返回True 或 False
    time.sleep(0.5)
    tkinter.messagebox.askretrycancel(title='HI',message='重试') #返回True 或 False


bt1=Button(root,text='hit me',command=show) 
bt1.grid(row=1,column=1)



"""------------------------------------------------------------"""
#11.滑块
#创建一个长度200字符，从0开始10结束，以2为刻度，精度为0.01的横向滑动条
hk=Scale(ssj,label='请滑动我',from_=0,to=10,length=200,orient=HORIZONTAL,tickinterval=2,resolution=0.01,showvalue=0)
hk.grid(row=1,column=1)





"""------------------------------------------------------------"""
ssj.mainloop()
