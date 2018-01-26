#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2018 XXX. All Rights Reserved.
# Author:  joanwelol@gmail.com
# QH_http.py 2018/1/25 21:57
# desc:

import requests as req
import json
from math import floor
from random import random

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
    api = 'http://140.143.49.31/api/ans2?key=' + api_key
    headers = {
        'Referer': 'http://wd.sa.sogou.com',
        'User-Agent': ('User-Agent: Mozilla/5.0 (X11; Linux x86_64) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36 Sogousearch/Ios/5.9.7'),
        'Cookie': 'dt_ssuid=' + str(floor(100000 * random()))
    }
    html = req.get(api, headers=headers)
    html = html.text
    html = html[html.find("(") + 1: len(html) - 1]
    return json.loads(html)['result']
