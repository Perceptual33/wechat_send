import requests, json, time
from sys import exit
from random import choice

class Send(object):
    
    def __init__(self, wechat_corpid, wechat_corpsecret):
        self.__wechat_corpid = wechat_corpid
        self.__wechat_corpsecret = wechat_corpsecret

    def get_token_id(self):
        URL = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        data = {
            'corpid' : self.__wechat_corpid,
            'corpsecret' : self.__wechat_corpsecret,
        }
        jsonall = json.loads(requests.get(URL, params=data).text)
        return jsonall['access_token']
        
    def get_party_id(self):
        URL = 'https://qyapi.weixin.qq.com/cgi-bin/department/list'
        getdata = {
            'access_token' : Send.get_token_id(self),
        }
        jsondata = json.loads(requests.get(URL, params=getdata).text)
        return jsondata['department'][0]['id']

    def sendchat(self, message):
        URL = 'https://qyapi.weixin.qq.com/cgi-bin/message/send'
        getdata = {
            'access_token' : Send.get_token_id(self),
        }
        postdata = {
            'toparty' : '1',
            # 部门信息
            'msgtype' : 'text',
            'agentid' : '1000002',
            # 企业内部应用id
            'text' : {
                'content' : message,
            },
            'safe' : 0,
        }
        requests.post(URL, params=getdata, data=json.dumps(postdata))

class Send_datas(Send):
    def __init__(self, hf_location, hf_key, wechat_corpid, wechat_corpsecret):
        super().__init__(wechat_corpid, wechat_corpsecret)
        self.__hf_location = hf_location
        self.__hf_key = hf_key

    def get_weather(self):
        URL = 'https://devapi.qweather.com/v7/weather/now'
        api_index = {
            'location' : self.__hf_location,
            'key' : self.__hf_key,
            'lang' : 'zh',
        }
        jsondata = json.loads(requests.get(URL, params=api_index).text)
        return "现在是：%s年%s月%s日%s\n" %(jsondata['updateTime'][0:4], \
        jsondata['updateTime'][5:7], jsondata['updateTime'][8:10], \
        jsondata['updateTime'][11:16]) + \
        "当前温度：%s摄氏度\n" %jsondata['now']['temp'] + \
        "当前天气状况：%s\n" %jsondata['now']['text'] + \
        "当前风向：%s\n" %jsondata['now']['windDir'] + \
        "当前风力等级：%s级\n" %jsondata['now']['windScale'] + \
        "当前相对湿度：%s%%\n" %jsondata['now']['humidity'] + \
        "当前大气压强：%s帕\n" %jsondata['now']['pressure'] + \
        "当前能见度：%s千米" %jsondata['now']['vis']

    def get_saying(self):
        saying = ['The answer to world, the universe and everything is 42.','少就是多，快就是慢。','This is a test message!']
        return choice(saying)

    def sendmyfile(self):
        token_id = Send.get_token_id(self)
        Send.sendchat(self, self.get_weather() + '\n' + self.get_saying())
        exit(0)
        
def main():
    hf_location = ''
    # 城市编号
    hf_key = ''
    # 和风天气api密钥
    wechat_corpid = ''
    # 企业微信企业id
    wechat_corpsecret = ''
    # 企业微信 应用密钥
    data = Send_datas(hf_location, hf_key, wechat_corpid, wechat_corpsecret)
    data.sendmyfile()

if __name__ == '__main__':
    main()
