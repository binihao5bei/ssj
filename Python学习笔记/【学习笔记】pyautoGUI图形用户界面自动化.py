import pyautogui

#1.常用操作
#（1）调用在执行动作后暂停的秒数
pyautogui.PAUSE=0.1

# (2）启用自动防故障功能，左上角的坐标为（0，0），将鼠标移到屏幕的左上角，来抛出failSafeException异常
pyautogui.FAILSAFE=True

# (3) 获取屏幕长宽大小
x,y=pyautogui.size()
print(f'屏幕大小为：{x}x{y}')

#（4）获取当前鼠标位置
current_x,current_y=pyautogui.position()
print(f'当前鼠标所在位置为：{current_x}x{current_y}')

#（5）判断（x,y）是否在屏幕上
if_x,if_y=1020,1079
print(pyautogui.onScreen(if_x,if_y))  #在屏幕上则返回True





#2.鼠标操作
#（1）控制鼠标移动到指定坐标位置
pyautogui.moveTo(100,100,duration=0.25) #用0.25s时间移动鼠标到指定的（100,100）位置

#（2）控制鼠标从当前位置移动指定x,y距离（x为正则向右移动，y为正则向下移动，x或y为0表示当前方式不移动）
pyautogui.moveRel(100,0,duration=0.25) #用0.25s时间将鼠标从当前位置向右移动100
pyautogui.moveRel(0,100,duration=0.25) #用0.25s时间将鼠标从当前位置向下移动100
pyautogui.moveRel(100,100,duration=0.25) #用0.25s时间将鼠标从当前位置先向右移动100，再向下移动100
pyautogui.moveRel(-100,0,duration=0.25) #用0.25s时间将鼠标从当前位置向左移动100
pyautogui.moveRel(0,-100,duration=0.25) #用0.25s时间将鼠标从当前位置向上移动100
pyautogui.moveRel(-100,-100,duration=0.25) #用0.25s时间将鼠标从当前位置先向左移动100，再向上移动100

#（3）按住鼠标把鼠标拖动到指定坐标位置
pyautogui.dragTo(100,100,button='left',duration=0.25) #按住鼠标左键，用0.25s时间将鼠标从当前位置先向右移动100，再向下移动100
pyautogui.dragTo(100,100,button='right',duration=0.25) #按住鼠标右键，用0.25s时间将鼠标从当前位置先向右移动100，再向下移动100

#（4）按住鼠标把鼠标拖动指定x,y距离（x为正则向右拖动，y为正则向拖移动，x或y为0表示当前方式不拖动）
pyautogui.dragRel(100,100,button='left',duration=0.25) #按住鼠标左键,将鼠标从当前位置先向右拖动100，再向下拖动100
pyautogui.dragRel(100,100,button='right',duration=0.25) #按住鼠标右键,将鼠标从当前位置先向右拖动100，再向下拖动100

#（5）控制鼠标滑轮进行滚动，x为正表示向上滚动x格，x为负表示向下滚动x格
pyautogui.scroll(10)  #向上滚动10格
pyautogui.scroll(-10) #向下滚动10格
pyautogui.scroll(10,100,100)     #先将鼠标移动到(100, 100)位置后再向上滚动10格（写法一）
pyautogui.scroll(10,x=100,y=100) #先将鼠标移动到(100, 100)位置后再向上滚动10格（写法二）

#（6）鼠标点击
pyautogui.mouseDown() #按下默认的鼠标左键
pyautogui.mouseUp()   #抬起（释放）按下的左键
pyautogui.click() #等价于上述2个操作的集合，在当前默认位置使用左键单击一下（按下再抬起）
pyautogui.click(100,100,button='left/right/middle') #先将鼠标移动到（100,100）位置后使用鼠标左键/右键/中键单击一下（按下再抬起）
pyautogui.rightClick() #在当前默认位置使用右键单击一下（按下再抬起）
pyautogui.middleClick() #在当前默认位置使用中键单击一下（按下再抬起）
pyautogui.doubleClick() #在当前默认位置使用左键双击一下
pyautogui.doubleClick(100,100,button='left/right/middle') #先将鼠标移动到（100,100）位置后使用鼠标左键/右键/中键双击一下
pyautogui.tripleClick() #在当前默认位置使用左键三击一下





#3.键盘操作
#（1）输入字符串
str='Hello World'
pyautogui.typewrite(str) #输入Hello World字符串
pyautogui.typewrite(str,interval=0.25) #每次输入间隔0.25,输入Hello World字符串
pyautogui.typewrite(str,duration=0.25) #每次输入间隔0.25,输入Hello World字符串

#（2）按下按键（不抬起）
pyautogui.keyDown('shiftleft') #按下左shift按键不抬起
pyautogui.keyDown('shiftright') #按下右shift按键不抬起
pyautogui.keyDown('shift') #按下默认的左shift按键不抬起

#（3）抬起按键
pyautogui.keyUp('shift') #将按下的shift按键抬起来

#（4）按下并抬起按键
pyautogui.press('shift') #按下shift按键后抬起来
pyautogui.press(['shift','ctrl','enter','space']) #依次按下并抬起shift键,ctrl键,enter键,space键
pyautogui.hotkey('ctrl','v') #依次按下ctrl,v  再依次按相反顺序抬起来（先抬起v再抬起shift)，即模拟ctrl+v粘贴组合键
'''--------------------------------------------'''
    #pyautogui.hotkey('ctrl','v')等价于以下：
pyautogui.keyDown('ctrl') #按下shift按键不抬起
pyautogui.press('v')      #按下v后抬起
pyautogui.keyUp('ctrl')   #将按下的shift按键抬起来
'''--------------------------------------------'''
#（5）快捷键组合
pyautogui.hotkey('shift','ctrl','f') #依次按下shift,ctrl,f  再依次按相反顺序抬起来（先抬起f再抬起ctrl再抬起shift)，即模拟shift+ctrl+f简繁切换组合键
    #pyautogui.KEYBOARD_KEYS数组中就是press()，keyDown()，keyUp()和hotkey()函数可以输入的按键名称
pyautogui.KEYBOARD_KEYS=['\t', '\n', '\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.',
              '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@',
              '[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
              'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~',
              'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace', 'browserback',
              'browserfavorites', 'browserforward', 'browserhome', 'browserrefresh', 'browsersearch',
              'browserstop', 'capslock', 'clear', 'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal',
              'del', 'delete', 'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
              'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20', 'f21', 'f22',
              'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'final', 'fn', 'hanguel', 'hangul',
              'hanja', 'help', 'home', 'insert', 'junja', 'kana', 'kanji', 'launchapp1', 'launchapp2',
              'launchmail', 'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
              'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6', 'num7', 'num8', 'num9',
              'numlock', 'pagedown', 'pageup', 'pause', 'pgdn', 'pgup', 'playpause', 'prevtrack', 'print',
              'printscreen', 'prntscrn', 'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select',
              'separator', 'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',
              'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen', 'command',
              'option', 'optionleft', 'optionright']





#4.弹窗操作
#（1）显示一个简单的带文字、‘仅显示确定’按钮的消息弹窗。用户点击后返回button的文字
b=pyautogui.alert(text='要开始程序么？',title='请求框',button='OK')
print(b) #弹出一个简单的消息弹窗，标题显示“请求框‘，弹窗内容显示’要开始程序么？‘，点击确定按钮后弹窗消失，返回button内容为ok

#（2）显示一个简单的带文字、‘确定’按钮和‘取消’按钮的消息弹窗。用户点击后返回button的文字
b=pyautogui.confirm(text='要开始程序么？',title='请求框',buttons=['OK','Cancel'])
print(b) #弹出一个简单的消息弹窗，标题显示“请求框‘，弹窗内容显示’要开始程序么？‘，点击确定按钮后弹窗消失，返回button内容为ok；点击取消按钮后弹窗消失，返回button内容为cancel

#（3）显示一个简单的带文字、10个按键0-9按钮的消息弹窗。用户点击后返回所点击的button按钮对应的文字
b=pyautogui.confirm(text='要开始程序么？',title='请求框',buttons=range(10))
print(b) #弹出一个简单的消息弹窗，标题显示“请求框‘，弹窗内容显示’要开始程序么？‘，点击任意数字按钮（如：1）后弹窗消失，返回button内容为1

#（4）显示一个可以明文输入的消息弹窗，带OK和Cancel按钮。用户点击OK按钮返回输入的文字，点击Cancel按钮返回None
pyautogui.prompt(text='要开始程序么？',title='请求框',default='OK')

#（5）样式同prompt()，用于输入密码等密文输入，消息用*表示。带OK和Cancel按钮。用户点击OK按钮返回输入的文字，点击Cancel按钮返回None
pyautogui.password(text='要开始程序么？',title='请求框',default='OK',mask="*")





#5.图像操作
#（1）全屏截图但不保存，用来获取指定坐标位置的颜色
img=pyautogui.screenshot()
color=img.getpixel((100,100))
print ("该坐标的像素点的颜色是：{}".format(color))

#（2）全屏截图并以指定名称保存在指定位置
pyautogui.screenshot(r'C:\Users\Sogou-SunShijiang\Desktop\my_screenshot.png')

#（3）以起点坐标值、截图宽度、长度为参数的区域截图并以指定名称保存在指定位置
pyautogui.screenshot(r'C:\Users\Sogou-SunShijiang\Desktop\my_screenshot.png',region=(x,y,width,height))
pyautogui.screenshot(r'C:\Users\Sogou-SunShijiang\Desktop\my_screenshot.png',region=(0,0,300,400))
