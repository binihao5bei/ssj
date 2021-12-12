# coding=utf-8
from pc_wx import Pc_wx

class Wx_infoq():

    def __init__(self, nowdate):

        self.urladds = 'infoQ'
        self.url_pre = 'https://weixin.sogou.com/weixin?type=1&s_from=input&query='+self.urladds+'&ie=utf8&_sug_=n&_sug_type_='

        self.pc = Pc_wx(nowdate, self.urladds, self.url_pre)

    def get_data(self):

        return self.pc.get_data()
