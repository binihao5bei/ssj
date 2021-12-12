
import tkinter
from pdf2docx import Converter
from tkinter import *

from tkinter.filedialog import *

import os,sys,time




root=Tk(className='PDF转word')

root.geometry('500x350')
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (500, 350, (screenwidth - 500) / 2, (screenheight - 350) / 2)
root.geometry(alignstr)


lable1=Label(text='PDF转Word小工具',font=('华文新魏',32))
lable2=Label(text='by.SunShijiang',font=('华文新魏',12))
lable1.grid(row=0,column=0,columnspan=5)
lable2.grid(row=1,column=0,columnspan=5)
text1=Text(root,width=70,height=2,state=DISABLED)
text1.grid(row=2 ,column=0,columnspan=5,pady=7)
text2=Text(root,width=70,height=2)
text2.grid(row=5 ,column=0,columnspan=5,pady=7)

def bt1():
    text1.config(state=NORMAL)
    text1.delete('0.0','end')


    filepath=askopenfile(title='请选择一个pdf文件',filetypes=[('pdf','*.pdf')])

    text1.insert('end',filepath.name)
    text1.config(state=DISABLED)



def bt3():

    a=text1.get('0.0','end')
    print(len(a))
    if len(a)<=1:
        tkinter.messagebox.showerror(title = '出错了！',message='请先导入要转换的pdf文件。')
    else:



        pdf_file=a.replace('/',r'\\').strip()
        #print(b)
        
        #pdf_file='D:\\文档资料\\新人学习资料\\SAAS学习资料\\01 交付文档\\鼎尖系统资料\\办公平台\\数据字典\\办公平台.pdf'

        docx_file='C:\\Users\\huoyi\\Desktop\\test.docx'


        cv=Converter(pdf_file)
        
        cv.convert(docx_file,start=0,end=None)
        cv.close()
        result=tkinter.messagebox.askokcancel(title = '打开文件',message='转换成功，是否要打开转换后的文件？')
        if result==True:
            os.system(docx_file)




    


button1=Button(root,text='导入文件',relief=RAISED,command=bt1,pady=5)
button1.grid(row=3 ,column=1)


button2=Button(root,text='开始转换',relief=RAISED,command=bt3,pady=5)
button2.grid(row=3 ,column=3)
























root.mainloop()