#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright By Eric in 2020

"""
基于百度语音识别、语音合成api，以及chatterbot库实现的语音聊天机器人
"""

import os
import time
import speech_recognition as sr
from playsound import playsound
from aip import AipSpeech
from chatterbot import ChatBot


class Baidu(object):
    def __init__(self):
        # 你的百度appID AK SK
        self.APP_ID = '18520466'
        self.API_KEY = 'b4sHKyIrpnNhygMT08rBwT7V'
        self.SECRET_KEY = 'YRyiZm1FmiSsIy68yyyrYUbg0t8M61qI'
        self.client = AipSpeech(self.APP_ID, self.API_KEY, self.SECRET_KEY)

    def SaveMp3(self, content):
        n = time.time()
        result = self.client.synthesis(content, 'zh', 1, {'spd': 5, 'vol': 7, 'per': 4})
        with open(r'%s.mp3' % str(n), 'wb') as f:
            f.write(result)
        playsound(r'%s.mp3' % str(n))
        os.remove(r'%s.mp3' % str(n))

    def RecordVoice(self):
        r = sr.Recognizer()
        mic = sr.Microphone(sample_rate=16000)      # 麦克风
        while True:
            # 开始录音，请说话...
            with mic as source:
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
            # 录音结束，识别中...

            audio_data = audio.get_wav_data()
            # 识别本地文件
            ret = self.client.asr(audio_data, 'wav', 16000, {'dev_pid': 1536, })
            if ret and ret['err_no'] == 0:
                result = ret['result'][0]
                return result
            else:
                print('----没听清，再说一次，错误信息：%s'%ret['err_msg'])
            # logging.info('end')


class Robot(object):
    def __init__(self):
        self.doudou = ChatBot('doudou', storage_adapter='chatterbot.storage.MongoDatabaseAdapter')

    def GetResponse(self, sentence):
        return self.doudou.get_response(sentence).text


def main():
    baidu = Baidu()     # 实例化百度语音识别、语音合成
    robot = Robot()     # 实例化聊天机器人
    while True:
        sentence = baidu.RecordVoice()
        print('小宝：%s'%sentence)
        if sentence != '不玩了':
            content = robot.GetResponse(sentence)
            baidu.SaveMp3(content)
            print('机器人：%s\n'%content)
        else:
            break


if __name__ == '__main__':
    main()
