#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
两个机器人对话程序(chatterbot VS Baidu)
"""

import time
import random
import requests
from chatterbot import ChatBot


class RobotConversation(object):
    def __init__(self):
        self.headers = {'content-type': 'application/x-www-form-urlencoded'}
        self.app_key = '【百度AI应用的app_key】'       # 百度AI应用的app_key
        self.secret_key = '【百度AI应用的secret_key】'    # 百度AI应用的secret_key
        self.service_id = '【百度机器人ID】'  # 百度机器人ID
        self.access_token = self.getBaiDuAK()  # 获取百度应用的access_token
        self.url = 'https://aip.baidubce.com/rpc/2.0/unit/service/chat?access_token=' + self.access_token  # 生成URL

        self.doudou = ChatBot('doudou', storage_adapter='chatterbot.storage.MongoDatabaseAdapter')

    def getBaiDuAK(self):
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + \
            self.app_key + '&client_secret=' + self.secret_key
        r = requests.get(host)
        return r.json()['access_token']

    def baiduUNIT(self, say):
        session_id = ''         # session_id初始为空值
        ran = 'UNITTEST_%d' % random.randint(1000, 10000)       # 随机生成log_id
        post_dict = '{"log_id":"' + ran + '","version":"2.0","service_id":"'\
                    + self.service_id + '","session_id":"' \
                    + session_id + '","request":{"query":"' \
                    + say + '","user_id":"UNIT_WEB_37819"}}'       # 字符串格式的字典
        response = requests.post(self.url, data=post_dict.encode(), headers=self.headers)
        if response.json()['error_code'] != 0:
            return print('出错了:%s' % response.json())       # 打印出错信息
        else:
            session_id = response.json()['result']['session_id']    # 得到session_id值
            ss = response.json()['result']['response_list']
            baidu_say = ss[0]['action_list'][0]['say']
            print('  Baidu: %s' % baidu_say)     # 输出返回的机器对话
            return baidu_say

    def doudouRobot(self, say):
        doudou_say = self.doudou.get_response(say).text.strip("'")
        print('Robot: %s' % doudou_say)
        return doudou_say


def main():
    robot_conversation = RobotConversation()
    say_b = '你好'
    while True:
        say_a = robot_conversation.doudouRobot(say_b)
        time.sleep(2)
        say_b = robot_conversation.baiduUNIT(say_a)     # 开始聊天
        time.sleep(2)


if __name__ == '__main__':
    main()
