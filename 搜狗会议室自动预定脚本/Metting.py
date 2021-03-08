import requests
import selenium
from selenium import webdriver
import time
import datetime
import json
from interval import Interval
from urllib.parse import urlencode

headers = {
    'Host' : 'oa.sogou-inc.com',
    'Referer' : 'https://oa.sogou-inc.com/meeting/room-select/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.81'
}

#selenium自动登录
post={}
url1="https://oa.sogou-inc.com/meeting/room-select"
driver = webdriver.Edge(executable_path=r'E:\Python\Scripts\msedgedriver.exe')
driver.get(url1)
time.sleep(3)
driver.find_element_by_id("xiaopFace").click()
time.sleep(3)
driver.execute_script("window.open('https://oa.sogou-inc.com/meeting/room-select');")
time.sleep(3)

#登陆后获取cookie
cookie_items=driver.get_cookies()
for cookie_item in cookie_items:
    post[cookie_item['name']] = cookie_item['value']
cookie_str = json.dumps(post)
with open('cookie.txt', 'w+') as f:
    f.write(cookie_str)
print("cookies信息已保存到本地")

with open('cookie.txt', 'r') as f:
    cookie = f.read()
cookies = json.loads(cookie)

for i in range(60):
    now_date=datetime.datetime.now().strftime('%H:%M:%S')
    if now_date=='11:16:50':
        print("终于到9点啦，现在时间是{}".format(now_date))
        driver.refresh()
        break
    else:
        time.sleep(1)
        continue
    
base_url='https://oa.sogou-inc.com/pub/meeting/api/book/list?'
#预定会议室列表
RoomId_list=['1098','1120','1063']   

'''
#搜狐网络大厦所有会议室的roomId信息参考如下，如需预定某一个或多个会议室，只需要将对应会议室的roomId填写到上述RoomId_list列表中
[
{'roomId': 1082, 'roomName': '高斯'},
{'roomId': 1092, 'roomName': '安卓'}, 
{'roomId': 1105, 'roomName': '科技'}, 
{'roomId': 1120, 'roomName': 'IOS'}, 
{'roomId': 1073, 'roomName': '信息'}, 
{'roomId': 1087, 'roomName': '彩虹'}, 
{'roomId': 1093, 'roomName': '服务器'}, 
{'roomId': 1101, 'roomName': '畅通'}, 
{'roomId': 1104, 'roomName': '指南针'}, 
{'roomId': 1106, 'roomName': '路况导航'}, 
{'roomId': 1069, 'roomName': '交换机'}, 
{'roomId': 1085, 'roomName': '瀚海'}, 
{'roomId': 1096, 'roomName': '网络'}, 
{'roomId': 1099, 'roomName': '达伽马'}, 
{'roomId': 1110, 'roomName': '麦哲伦'}, 
{'roomId': 1063, 'roomName': '磐石'}, 
{'roomId': 1094, 'roomName': '抱石'}, 
{'roomId': 1112, 'roomName': '公交'}, 
{'roomId': 1125, 'roomName': 'APP'}, 
{'roomId': 1064, 'roomName': '灵犀'}, 
{'roomId': 1068, 'roomName': '青春'}, 
{'roomId': 1078, 'roomName': '梦想'}, 
{'roomId': 1079, 'roomName': '阅读'}, 
{'roomId': 1084, 'roomName': '新闻'}, 
{'roomId': 1089, 'roomName': '贝叶斯'}, 
{'roomId': 1091, 'roomName': '网址导航'}, 
{'roomId': 1097, 'roomName': '华罗庚'}, 
{'roomId': 1100, 'roomName': '搜狗地图'}, 
{'roomId': 1102, 'roomName': '晨星'}, 
{'roomId': 1103, 'roomName': '冯诺依曼'}, 
{'roomId': 1107, 'roomName': '网页'}, 
{'roomId': 1116, 'roomName': '旭日'}, 
{'roomId': 1121, 'roomName': '应用'}, 
{'roomId': 1129, 'roomName': '大数据'}, 
{'roomId': 1076, 'roomName': '识图'}, 
{'roomId': 1098, 'roomName': '银河'}, 
{'roomId': 1066, 'roomName': '视频'}, 
{'roomId': 1067, 'roomName': '图灵'}, 
{'roomId': 1075, 'roomName': '特斯拉'}, 
{'roomId': 1080, 'roomName': '发现'}, 
{'roomId': 1083, 'roomName': '问问'}, 
{'roomId': 1086, 'roomName': '购物'}, 
{'roomId': 1088, 'roomName': '语音助手'}, 
{'roomId': 1108, 'roomName': '工具条'}, 
{'roomId': 1115, 'roomName': '知立方'}, 
{'roomId': 1118, 'roomName': '百科'}, 
{'roomId': 1127, 'roomName': '信息流'}]
'''

class Meeting():
    def __init__(self,startTime,endTime,nowdate):
        self.nowdate = nowdate
        self.startTime=startTime
        self.endTime=endTime
    

    def get_content(self,url):
        
        response = requests.get(url, headers=headers,cookies=cookies)
        #print(response.json())

        bookLists=response.json().get('data').get('bookList')
        return bookLists
    
        
    
    def get_data(self):
        will_book=Interval(self.startTime, self.endTime)    #预期要预定会议室的时间段区间
        for i in RoomId_list:
            params={
            'roomId':i,
            'day':self.nowdate
            }
            urladd=base_url + urlencode(params)

            counted=0       
            if self.get_content(urladd):
                for i in self.get_content(urladd):
                    startTime=i.get('startTime')
                    endTime=i.get('endTime')
                    time_interval=Interval(startTime,endTime)
                    print(time_interval)                                      #获取已经被预定会议室的时间段
                    
                    if self.startTime not in time_interval:                   #首先判断预期要定会议室的起始时间是否不包含在已经被预定的时间段中
                        if will_book.overlaps(time_interval):                 #如果上述不包含，则判断预期要定的时间段区间与当前已经预定的时间段是否重叠
                            print("与该时间段{}重叠，".format(time_interval))    #有重叠则直接跳过该时间段
                            counted+=1
                            break
                        else:
                            print("与该时间段{}不重叠".format(time_interval))   #没有重叠则继续与下一个已经预定的时间段比较
                            counted+=0
                            continue
                    elif self.startTime in time_interval:
                        print("与该时间段{}重叠".format(time_interval))
                        counted+=1
                        break
                        
         
                if counted==0:
                    print('该会议室还未被预定，抓紧预定把')

                    roomId=params['roomId']
                    day=params['day']
                    print('roomId:{}'.format(roomId))
                    print('day:{}'.format(day))
                    print('*'*80)
                    return roomId,day
                    

                    break

                elif counted==1:
                    print('预期想预定的会议室与其他已经预定的时间段发生重叠，该会议室已经被预定，开始下一个会议室')

                    roomId=params['roomId']
                    day=params['day']
                    print('roomId:{}'.format(roomId))
                    print('day:{}'.format(day))
                    print('*'*80)
                    continue
                
            else:
                print("当前会议室没有任何人预定")

                roomId=params['roomId']
                day=params['day']
                print('roomId:{}'.format(roomId))
                print('day:{}'.format(day))
                print('*'*80)
                return roomId,day
                break
             

    def meeting_book(self):
        url2='https://oa.sogou-inc.com/pub/meeting/api/book'
        RoomId=self.get_data()[0]
        data={
        'roomId':RoomId,
        'date': self.nowdate,
        'startTime':datetime.datetime.strptime(self.startTime,"%H:%M:%S").strftime("%H:%M"),                 
        'endTime':datetime.datetime.strptime(self.endTime,"%H:%M:%S").strftime("%H:%M"),                   
        'source':'App',
        'inviteUidList':'', #邀请参会人员信息，可自定义添加或删除人员
        'xiaopGroup':'0',
        'title':'pc测试周例会'                #预定会议室的主题，可自定义修改
        }
        h=requests.post(url=url2,headers=headers,data=data,cookies=cookies)
        print(h.json())

if __name__=="__main__":
    startTime='19:00:00'                   #预定会议室的起始时间，可自定义修改，目前仅支持一刻时间（即间隔15min）
    endTime='21:00:00'                     #预定会议室的截止时间，可自定义修改，目前仅支持一刻时间（即间隔15min）
    nowdate = (datetime.datetime.now()+ datetime.timedelta(days = 6)).strftime('%Y-%m-%d')  #预定当前时间之后6天的会议室
    a=Meeting(startTime,endTime,nowdate)
    a.meeting_book()
    
