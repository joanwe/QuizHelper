#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2018 XXX. All Rights Reserved.
# Author:  joanwelol@gmail.com
# QH_print.py 2018/1/25 22:20
# desc:
from prettytable import PrettyTable
from websocket import create_connection
import requests
import json

table = PrettyTable(['答案选项', '结果总数', '词频计数'])
table.align = 'l'


# 打印表格
def print_table(value):
    title = value['title']
    result = value['result'].strip()
    summary = value['summary']
    for i in value['answers']:
        if i in summary:
            # 打印绿色高亮字体    '\033[0;32m' +  + '\033[0m'
            summary = summary.replace(i, '\033[0;32m' + i + '\033[0m')
    print('\b' * 22, end='', flush=True)  # 删除前面打印字符
    print(title)
    print(table)
    from QH_http import switch
    if switch == 0:
        print('推荐答案:' + '-->' + result + '<--')
        print('参考:', summary)
        print('\n')
    else:
        get_SougouAnswer(value)


# 简单搜索模式下获取搜狗api答案
def get_SougouAnswer(value):
    id = ''
    note = '等待出答案...'
    from QH_http import api_id
    if api_id == 'xiguashipin':
        id = 'xigua'
    elif api_id == 'huajiao':
        id = 'huajiao'
    elif api_id == 'chongdingdahui':
        id = 'cddh'
    elif api_id == 'zhishichaoren':
        id = 'zscr'
    elif api_id == 'youku':
        get_DanAnswer(value)
    url = 'http://140.143.49.31/api/ans2?wdcallback=xx&key='  + id
    html = requests.get(url, headers=headers)
    scode = html.status_code
    html = html.text.lstrip('xx(').rstrip(')')
    # 若响应代码为404则重新请求
    while scode == 404:
        req = requests.get(url, headers=headers)
        scode = req.status_code
        html = req.text.lstrip('xx(').rstrip(')')
    if len(html) > 0 :
        html = json.loads(html)['result'][-1]
    else:get_SougouAnswer(value)
    answers = value['answers']
    result = json.loads(html)['result']
    summary = json.loads(html)['search_infos'][0]['summary']
    if result not in answers:
        print('\r',note,end='')
        get_SougouAnswer(value)
    print('\b'*len(note),end='',flush=True)
    print('推荐答案:' + '-->' + result + '<--')
    print('参考:', summary)
    print('\n')


# 获取Dan哥答案
def get_DanAnswer(value):
    note = '等待出答案...'
    ws = create_connection('wss://selab.baidu.com/nv/answer.sock/?EIO=3&transport=websocket')
    ws.send('40/nv/youku/answer,')
    for i in range(5):
        message = ws.recv()
        if 'result' in message:
            message = message[message.find('{'):].rstrip(']')
            dic = json.loads(message)
            answers = [ans['text'] for ans in dic['answers']]
            result = answers[dic['result']]
            answers2 = value['answers']
            if result not in answers2:
                print('\r', note, end='')
                get_DanAnswer(value)
            print('\b' * len(note), end='', flush=True)
            print('推荐答案:' + '-->' + result + '<--')
            print('\n')
        else:
            print('\r', note, end='')
            get_DanAnswer(value)


headers = {
    'Host': '140.143.49.31',
    'Connection': 'keep-alive',
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_5 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13G36 Sogousearch/Ios/5.9.7',
    'Accept-Language': 'zh-cn',
    'Referer': 'http://nb.sa.sogou.com/',
    'Accept-Encoding': 'gzip, deflate'
}
