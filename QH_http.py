#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2018 XXX. All Rights Reserved.
# Author:  joanwelol@gmail.com
# QH_http.py 2018/1/25 21:57
# desc:

import requests
import json

api_key = ''


# 获取api_key
def get_key():
    global api_key
    index = input('数字键选择:\n1:冲顶大会\n2:芝士超人\n3:西瓜百万英雄\n4:花椒百万赢家\n5:一直播黄金十秒\n')
    if int(index) == 1:
        api_key = 'cddh'
    elif int(index) == 2:
        api_key = 'zscr'
    elif int(index) == 3:
        api_key = 'xigua'
    elif int(index) == 4:
        api_key = 'huajiao'
    elif int(index) == 5:
        api_key = 'hjsm'
    else:
        print("输入错误,请重新选择")
        get_key()


# 获取搜狗api内容
def get_content():
    api = 'http://140.143.49.31/api/ans2?wdcallback=xx&key=' + api_key
    html = requests.get(api, headers=headers).text
    try:
        if len(html) != 0:
            html = html[html.find("(") + 1: len(html) - 1]
            return json.loads(html)['result']
        else:
            print('赋值错误')
    except:
        html = requests.get(api, headers=headers).text
        html = html[html.find("(") + 1: len(html) - 1]
        return json.loads(html)['result']


headers = {
    'Host': '140.143.49.31',
    'Connection': 'keep-alive',
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_5 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13G36 Sogousearch/Ios/5.9.7',
    'Accept-Language': 'zh-cn',
    'Referer': 'http://nb.sa.sogou.com/',
    'Accept-Encoding': 'gzip, deflate'
}
