lidc=[
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
{'roomId': 1127, 'roomName': '信息流'}
]

def Id_Name(roomId):

    for i in lidc:
        if i['roomId']==roomId:
            return i['roomName']
            break
        else:
            continue
def get_data():
    roomId=1083    
    print("roomname{}".format(Id_Name(roomId)))
a=get_data()

    
