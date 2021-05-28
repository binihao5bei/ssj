from tkinter import *
import requests
import time 

def get_content():
    #print(text1.get("1.0","end"))
    return text1.get("1.0","end")

def get_result(a,flag):
    url='https://www.shulijp.com/word/process'
    data={
        'text':a,
        'flag':flag
    }

    response=requests.post(url=url,data=data)
    #print(response.json().get('words'))
    return response.json().get('words')




def bt1():
    a=get_content()
    time.sleep(0.02)
    #print(a)
    flag='convertToTraditionalChinese'
    print(get_result(a,flag))
    text2.delete("1.0","end")
    time.sleep(0.02)
    text2.insert(INSERT,get_result(a,flag))
    text2.update()

def bt2():
    a=get_content()
    time.sleep(0.02)
    flag='convertToSimplifiedChinese'
    print(get_result(a,flag))
    text2.delete("1.0","end")
    time.sleep(0.02)
    text2.insert(INSERT,get_result(a,flag))
    text2.update()
def bt3():
    a=get_content()
    time.sleep(0.02)
    flag='pinyinWithToneMark'

    print(get_result(a,flag))
    text2.delete("1.0","end")
    time.sleep(0.02)
    text2.insert(INSERT,get_result(a,flag))
    text2.update()



root=Tk(className='我的第一个python窗口')

root.geometry('500x350')
lable1=Label(text='转换小工具',font=('华文新魏',32))
lable2=Label(text='by.SunShijiang',font=('华文新魏',12))
lable1.grid(row=0,column=0,columnspan=9)
lable2.grid(row=1,column=0,columnspan=9)
text1=Text(root,width=30,height=20)
text1.grid(row=2 ,column=0, rowspan=9)


button1=Button(root,text='简——>繁',relief=RAISED,command=bt1)
button1.grid(row=4 ,column=3)

button2=Button(root,text='繁——>简',relief=RAISED,command=bt2)
button2.grid(row=6 ,column=3)

button3=Button(text='拼音标注',relief=RAISED,command=bt3)
button3.grid(row=8 ,column=3)

text2=Text(root,width=30,height=20,state=NORMAL)
text2.grid(row=2 ,column=5,rowspan=9)























root.mainloop()