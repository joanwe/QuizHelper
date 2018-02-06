#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2018 XXX. All Rights Reserved.
# Author:  joanwelol@gmail.com
# QH_http.py 2018/1/25 21:57
# desc:

import requests
import json
from websocket import create_connection

api_id = ''
content = {}
switch = 0


# 选择答题app及获取api_id
def get_key():
    global api_id, switch
    index = input('数字键选择:\n' + channel_infos() + '6.优酷疯狂夺金\n')
    if int(index) == 1:
        api_id = 'xiguashipin'
        switch = 1
    elif int(index) == 2:
        api_id = 'huajiao'
        switch = 1
    elif int(index) == 3:
        api_id = 'chongdingdahui'
        switch = 1
    elif int(index) == 4:
        api_id = 'hjsm'
    elif int(index) == 5:
        api_id = 'zhishichaoren'
        switch = 1
    elif int(index) == 6:
        api_id = 'youku'
        switch = 1
    else:
        print("输入错误,请重新选择")
        get_key()


# 获取搜狗api内容
def get_content():
    api = 'http://140.143.49.31/api/ans2?wdcallback=xx&key=' + api_id
    req = requests.get(api, headers=headers)
    html = req.text.lstrip('xx(').rstrip(')')
    scode = req.status_code
    # 若响应代码为404则重新请求
    while scode == 404:
        req = requests.get(api, headers=headers)
        scode = req.status_code
        html = req.text.lstrip('xx(').rstrip(')')
        fetch_content(content, html)
    fetch_content(content, html)
    return content


# 获取简单搜索websocket数据包
def get_DANcontent():
    global content
    ws = create_connection('wss://selab.baidu.com/nv/answer.sock/?EIO=3&transport=websocket')
    ws.send('40/nv/' + api_id + '/answer,')
    for i in range(5):
        message = ws.recv()
        # print(message)
        if 'question' in message:
            message = message[message.find('{'):].rstrip(']')
            dic = json.loads(message)
            content['title'] = dic['question']['text']
            content['answers'] = [ans['text'] for ans in dic['answers']]
            content['result'] = content['answers'][dic['result']]
            content['summary'] = '暂无参考'
        else:
            content['title'] = 'Dan哥热身中,题目还在路上...'
            content['answers'] = ['暂无答案', '暂无答案', '暂无答案']
            content['result'] = '暂无答案'
            content['summary'] = '暂无参考'
    return content


# 提取搜狗api有效内容
def fetch_content(content, html):
    if len(html) > 0:
        html = json.loads(html)['result'][-1]
        content['answers'] = [i.strip() for i in json.loads(html)['answers']]
        content['title'] = json.loads(html)['title']
        content['result'] = json.loads(html)['result']
        content['summary'] = json.loads(html)['search_infos'][0]['summary']
    else:
        get_content()


# 获取答题app列表及相关信息
def channel_infos():
    txt = ''
    html = requests.get('https://sa.sogou.com/weball/api/assistant/index').json()
    seq = 1
    for key in html['channelTypeList']:
        del key['channel'], key['icon'], key['status'], key['ts']
        key['name'] = str(seq) + '.' + key['name']
        seq += 1
        tup = list(key.values())
        for i in range(len(tup)):
            if i == 0:
                txt += tup[i]
            elif i == 1:
                txt += '    ' + tup[i]
            else:
                txt += '    ' + tup[i] + '\n'
    return txt

headers = {
    'Host': '140.143.49.31',
    'Connection': 'keep-alive',
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_5 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13G36 Sogousearch/Ios/5.9.7',
    'Accept-Language': 'zh-cn',
    'Referer': 'http://nb.sa.sogou.com/',
    'Accept-Encoding': 'gzip, deflate'
}