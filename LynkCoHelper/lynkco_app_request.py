#!/usr/bin/python3

import requests
from com.uestcit.api.gateway.sdk import lynco_api_auth as authsdk

class lynkco_app_request():
    """接口请求封装类"""
    def __init__(self, app_key, app_secret):
        self.__host = 'https://app-services.lynkco.com.cn'
        self.__app_key = app_key
        self.__app_secret = app_secret
        self.__lynco_api_auth = authsdk.LyncoApiAuth(app_key = self.__app_key, app_secret = self.__app_secret)
        pass

    def login(self, username, password):
        """APP端登录"""
        params = { 'deviceType': 'ANDROID', 'username': username, 'password': password }
        response = requests.post(self.__host + '/auth/login/login', params = params, data = {}, auth = self.__lynco_api_auth, proxies = {});
        return response.json()
       
    def member_info(self, token, userid):
        """APP端获取用户信息（CO币余额等信息）"""
        params = { 'id': userid }
        headers = { 'token': token }
        response = requests.get(self.__host + '/app/member/service/memberInFo', params = params, data = {}, auth = self.__lynco_api_auth, proxies = {}, headers = headers);
        return response.json()

    def get_co_by_share(self, token, userid):
        """APP端每日分享获取5Co币，每天可以操作3次"""
        params = { 'accountId': userid, 'type': 3 }
        headers = { 'token': token }
        response = requests.post(self.__host + '/app/v1/task/reporting', params = params, data = {}, auth = self.__lynco_api_auth, proxies = {}, headers = headers);
        return response.json()

    def get_vcode_by_regist(self, mobile):
        """获取短信（注册时）"""
        params = { 'mobile': mobile }
        response = requests.get(self.__host + '/auth/register/sendSms', params = params, data = {}, auth = self.__lynco_api_auth, proxies = {});
        return response.json()

    def regist(self, mobile, password, vcode):
        """注册接口"""
        params = { 'mobile': mobile, 'password': password, 'passwordConfirm': password, 'verificationCode': vcode }
        response = requests.post(self.__host + '/auth/register/registerByMobile', params = params, data = {}, auth = self.__lynco_api_auth, proxies = {});
        return response.json()

    
    def article_like(self, token, tid, is_like):
        """圈子帖子点赞接口"""
        params = { 'isForward': is_like }
        response = requests.put('https://community-opt-app.lynkco.com/api/v1/biz/article/like/' + tid, params = params, data = { 'isForward': false }, proxies = {});
        return response.json()

    def get_user_dynamic_list(self, uid, page, size):
        """获取用户动态列表"""
        params = { 'dynamicsPageNo': page, 'dynamicsPageSize': size, 'userId': uid }
        response = requests.get(self.__host + '/app/explore/home-page/query/user/dynamics', params = params, data = {}, auth = self.__lynco_api_auth, proxies = {});
        return response.json()