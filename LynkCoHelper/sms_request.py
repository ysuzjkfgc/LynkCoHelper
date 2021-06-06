#!/usr/bin/python3

import requests

class sms_request():
    """接口请求封装类"""
    def __init__(self):
        self.__host = 'http://apd.guanfangdiping.com:8080'
        pass

    def login(self, username, password):
        """SMS账户登录"""
        params = { 'username': username, 'password': password }
        response = requests.get(self.__host + '/login.php', params = params, data = {});
        return response.text
       
    def get_phone(self, token, id):
        """获取一个手机号"""
        params = { 'id': id, 'operator': '0', 'Region': '0', 'card': '0', 'phone': '', 'loop': '1', 'token': token }
        response = requests.get(self.__host + '/yhquhao.php', params = params, data = {});
        return response.text

    def get_phone_msg(self, token, id, phone):
        """获取验证码"""
        params = { 'id': id, 'phone': phone, 't': 'a437936609', 'token': token }
        response = requests.get(self.__host + '/yhquma.php', params = params, data = {});
        return response.text

    def set_blank_list(self, token, id, phone):
        """拉黑"""
        params = { 'id': id, 'phone': phone, 'token': token }
        response = requests.get(self.__host + '/yhlh.php', params = params, data = {});
        return response.text
