#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2018 XXX. All Rights Reserved.
# Author:  joanwelol@gmail.com
# QH_http.py 2018/1/25 21:57
# desc:

import requests
import json
from websocket import create_connection
import base64
import random

api_id = []


# 获取答题app列表及相关信息
# def channel_infos():
#     txt = ''
#     html = requests.get('https://sa.sogou.com/weball/api/assistant/index').json()
#     seq = 1
#     for items in html['channelTypeList']:
#         del items['channel'], items['icon'], items['status'], items['ts'], items['appName'], items['index']
#         items['name'] = str(seq) + '.' + items['name']
#         seq += 1
#         li = list(items.values())
#         for i in range(len(li)):
#             if i == 0:
#                 txt += li[i]
#             elif i == 1:
#                 txt += '    ' + li[i]
#             else:
#                 txt += '    ' + li[i] + '\n'
#     return txt


# 选择答题app及获取api_id
def get_id():
    global api_id
    index = input('数字键选择:\n1.西瓜视频百万英雄\n2.花椒视频百万赢家\n3.一直播黄金十秒\n4.优酷视频疯狂夺金\n5.芝士超人\n6.冲顶大会\n')
    if int(index) == 1:
        api_id = ['xigua', 'xiguashipin']
    elif int(index) == 2:
        api_id = ['huajiao', 'huajiao']
    elif int(index) == 3:
        api_id = ['hjsm', 'hjsm']
    elif int(index) == 4:
        api_id = ['youku', 'youku']
    elif int(index) == 5:
        api_id = ['zscr', 'zhishichaoren']
    elif int(index) == 6:
        api_id = ['cddh', 'chongdingdahui']
    else:
        print("输入错误,请重新选择")
        get_id()


# 获取汪仔接口内容
def get_WANcontent():
    content = {}
    api = 'https://wdpush.sogoucdn.com/api/anspush?key=' + api_id[0] + '&wdcallback=x'
    resp = requests.get(api, headers=headers)
    html = resp.text.lstrip('x({\"code\": 0, \"allow\": true, \"result\": \"').rstrip('\"})')
    html = base64.b64decode(html).decode('utf-8')
    html = json.loads(html)
    scode = resp.status_code
    # 若响应代码为404则重新请求
    while scode == 404:
        get_WANcontent()
    if len(html) > 0:
        html = html[-1]
        content['answers'] = [i.strip() for i in json.loads(html)['answers']]
        index = json.loads(html)['title'].find('.')
        content['title'] = json.loads(html)['title'][index + 1:].lstrip()
        content['result'] = json.loads(html)['result']
        content['summary'] = json.loads(html)['search_infos'][0]['summary']
    else:
        get_WANcontent()
    return content


# 获取Dan哥接口内容
def get_DANcontent(q):
    content = {}
    ws = create_connection('wss://selab.baidu.com/nv/answer.sock/?EIO=3&transport=websocket')
    ws.send('40/nv/' + api_id[1] + '/answer,')
    for i in range(5):
        message = ws.recv()
        # print(message)
        if q in message:
            message = message[message.find('{'):].rstrip(']')
            dic = json.loads(message)
            content['title'] = dic['question']['text']
            content['answers'] = [ans['text'] for ans in dic['answers']]
            content['result'] = '暂无答案'
            content['summary'] = '暂无参考'
        else:
            content['title'] = 'Dan哥热身中,题目还在路上...'
            content['answers'] = ['暂无答案', '暂无答案', '暂无答案']
            content['result'] = '暂无'
            content['summary'] = '暂无'
    return content


# 随机生成Cookie后六位数字
def gen_cookie():
    li = []
    for i in range(6):
        li.append(random.randint(0, 9))
    return ''.join('%s' % i for i in li)


# 搜狗headers
headers = {
    'Host': 'wdpush.sogoucdn.com',
    'Connection': 'keep-alive',
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; SM705 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36 SogouSearch Android1.0 version3.0 AppVersion/5916',
    'Accept-Language': 'zh-cn',
    'Accept-Encoding': 'gzip, deflate',
    'X-Requested-With': 'com.sogou.activity.src',
    'Referer': 'https://assistant.sogoucdn.com/v5/cheat-sheet?channel=cddh',
    'Cookie': 'APP-SGS-ID=feb1864394010' + gen_cookie()
}


# 判断获得最新题目及答案先后关系
def get_allContent(results):
    if api_id[0] == 'youku':
        content = get_DANcontent('question')
        if content['title'] not in results:
            return content
        else:
            content = {'title': '答题开始后会自动显示答案', 'answers': ['暂无答案', '暂无答案', '暂无答案'], 'result': '暂无', 'summary': '暂无'}
            return content
    elif api_id[0] == 'hjsm':
        content = get_WANcontent()
        if content['result'] not in results:
            return content
    else:
        content1 = get_DANcontent('question')
        content2 = get_WANcontent()
        if content1['title'] not in results:
            return content1
        elif content2['title'] not in results:
            return content2
        else:
            content = {'title': '答题开始后会自动显示答案', 'answers': ['暂无答案', '暂无答案', '暂无答案'], 'result': '暂无', 'summary': '暂无'}
            return content
