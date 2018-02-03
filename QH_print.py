#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2018 XXX. All Rights Reserved.
# Author:  joanwelol@gmail.com
# QH_print.py 2018/1/25 22:20
# desc:
import json
from prettytable import PrettyTable

table = PrettyTable(['答案选项', '结果总数', '词频计数'])
table.align= 'l'


# 打印表格
def print_table(value):
    title = value['title']
    result = value['result']
    summary = value['summary']
    for i in value['answers']:
        if i in summary:
            # 打印绿色高亮字体    '\033[0;32m' +  + '\033[0m'
            summary = summary.replace(i, '\033[0;32m' + i + '\033[0m')
    print('\b' * 24, end='', flush=True)  # 删除前面打印字符
    print(title)
    print(table)
    print('推荐答案:' + '-->' + result + '<--')
    print('参考:', summary)
    print('\n')
