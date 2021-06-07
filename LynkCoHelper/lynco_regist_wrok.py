#!/usr/bin/python3

import threading
import time
import base64
from lynkco_app_request import lynkco_app_request
from com.uestcit.api.gateway.sdk.auth.aes import aes as AES
from sms_request import sms_request
import json
import sys
import os
import re

class lynco_regist_wrok(threading.Thread):
    """新开线程处理任务"""
    def __init__(self, config):
        # 初始化线程
        threading.Thread.__init__(self)
        # 缓存配置信息
        self.config = config
        self.project_id = self.config['sms_platform']['project_id']
        self.max_count = int(self.config['sms_platform']['count'])
        self.sms_request = sms_request()
         # 缓存APPKEY(因为存储的是base64后的值，所以需要base64解码一次)
        self.app_key = base64.b64decode(self.config['api_geteway']['app_key']).decode('utf-8')
        # 缓存APPSECRET(因为存储的是base64后的值，所以需要base64解码一次)
        self.app_secret = base64.b64decode(self.config['api_geteway']['app_secret']).decode('utf-8')
        # 缓存AESKEY(因为存储的是两次base64后的值，所以需要base64解码两次)
        self.aes_key = base64.b64decode(base64.b64decode(self.config['aes_key']).decode('utf-8')).decode('utf-8')
        self.lynkco_app_request = lynkco_app_request(self.app_key, self.app_secret)
        
    def run(self):
        """线程开始的方法"""
        print ("开始注册任务 " + time.strftime('%Y-%m-%d %H:%M:%S'))
        self.token = self.get_token()
        if('' == self.token):
            return 0
        
        phone_list = []
        try:
            while len(phone_list) < self.max_count:
                phone = self.regist()
                if('' == phone):
                    continue
                phone_list.append({ 'username': phone, 'password': 'a123456789' })
        finally:
            with open(sys.path[0] + '/phone_list_' + time.strftime('%Y%m%d%H%M%S') + '.json', 'w') as json_file:
                json_file.write(json.dumps(phone_list,ensure_ascii = False))

        print ("注册执行完成任务 " + time.strftime('%Y-%m-%d %H:%M:%S'))

    def get_token(self):
        """登录获取token"""
        sms_username = self.config['sms_platform']['username']
        sms_password = self.config['sms_platform']['password']
        context = self.sms_request.login(sms_username, sms_password)
        array = context.split('|')
        if(int(array[0]) != 1):
            print("短信账户登录失败：" + context + " " + time.strftime('%Y-%m-%d %H:%M:%S'))
            return ''
        token = array[1]
        print("短信账户登录成功，token：" + token + " " + time.strftime('%Y-%m-%d %H:%M:%S'))
        return token

    def regist(self):
        """App端操作流程"""
        time.sleep(1)
        # 获取一个手机号
        context = self.sms_request.get_phone(self.token, self.project_id)
        array = context.split('|')
        if(int(array[0]) != 1):
            print("短信账户获取手机号失败：" + context + " " + time.strftime('%Y-%m-%d %H:%M:%S'))
            return ''
        phone = array[1]
        print("短信账户获取手机号成功：" + context + "，phone=" + phone + " " + time.strftime('%Y-%m-%d %H:%M:%S'))
        try:
            # 发送注册短信
            response = self.lynkco_app_request.get_vcode_by_regist(phone)
            if response['code'] != 'success':
                print("发送注册短信失败" + response['message'] + " " + time.strftime('%Y-%m-%d %H:%M:%S'))
                return ''

            # 循环10次获取短信内容，每次获取失败等待3秒钟
            vcode = ''
            fail_count = 0;
            while fail_count < 10:
                context = self.sms_request.get_phone_msg(self.token, self.project_id, phone)
                array = context.split('|')
                if(int(array[0]) != 1):
                    print("短信账户获取验证码内容失败：" + context + " " + time.strftime('%Y-%m-%d %H:%M:%S'))
                    fail_count += 1
                    time.sleep(3)
                else:
                    context = array[1]
                    # 此处需要正则取验证码
                    pattern = re.compile(r'\d{6}')
                    result = pattern.findall(context)
                    if(len(result) != 1):
                        print("短信账户解析验证码内容失败：" + context + " " + time.strftime('%Y-%m-%d %H:%M:%S'))
                    else:
                        vcode = result[0]
                        print("短信账户获取验证码内容成功：" + vcode + " " + time.strftime('%Y-%m-%d %H:%M:%S'))
                    break
            if('' == vcode):
                return ''

            # 发送注册
            self.AES = AES(self.aes_key)
            password = self.AES.encrypt('a123456789')
            response = self.lynkco_app_request.regist(phone, password, vcode)
            if response['code'] != 'success':
                print("发送注册接口失败" + response['message'] + " " + time.strftime('%Y-%m-%d %H:%M:%S'))
                return ''
            # 尝试登陆一次
            response = self.lynkco_app_request.login(phone, password)
            if response['code'] != 'success':
                print("尝试接口失败" + response['message'] + " " + time.strftime('%Y-%m-%d %H:%M:%S'))
                return phone
            return phone
        finally:
            time.sleep(1)
            context = self.sms_request.set_blank_list(self.token, self.project_id, phone)
            print("拉黑手机号结果" + context + " " + time.strftime('%Y-%m-%d %H:%M:%S'))
