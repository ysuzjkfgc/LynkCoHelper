#!/usr/bin/python3

import sys
import os
import json
from lynco_wrok import lynco_wrok
from lynco_regist_wrok import lynco_regist_wrok
import time
import base64
from com.uestcit.api.gateway.sdk.auth.aes import aes as AES

def main():
    # 加载应用配置
    config = json.load(open(sys.path[0] + '/config.json'))
    # 加载账号配置
    account_list = json.load(open(sys.path[0] + '/account.json'))
    # 检查是否是注册任务
    if(config['sms_platform']['enable'] == 1):
        regist_thread(config, account_list)
    else:
        work_thread(config, account_list)
    
    print('执行完成')

# 执行注册任务
def regist_thread(config, account_list):
    # 目前使用单线程单个依次注册的方式调用，后续考虑多线程
    # 定义线程数组
    threads = []
    # 实例化
    thread = lynco_regist_wrok(config)
    # 保存到线程数组
    threads.append(thread)
    # 运行线程
    thread.start()
    # 遍历线程数组，调用join方法等待线程执行完成后再退出程序
    for thread in threads:
        thread.join()
    


# 执行日常任务
def work_thread(config, account_list):
    # 定义线程数组
    threads = []
    # 遍历账号列表，每个账号开启一个线程进行处理
    for account in account_list:
        # 实例化
        thread = lynco_wrok(config, account)
        # 保存到线程数组
        threads.append(thread)
        # 运行线程
        thread.start()

    # 遍历线程数组，调用join方法等待线程执行完成后再退出程序
    for thread in threads:
        thread.join()

if __name__ == '__main__':
    main()