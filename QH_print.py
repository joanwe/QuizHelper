#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2018 XXX. All Rights Reserved.
# Author:  joanwelol@gmail.com
# QH_print.py 2018/1/25 22:20
# desc:
from prettytable import PrettyTable

table = PrettyTable(['答案选项', '结果总数', '词频计数'])
table.align = 'l'


# 打印表格
def print_table(value):
    title = value['title'].strip()
    answers = value['answers']
    print('\b' * 40, end='', flush=True)  # 删除前面打印字符
    print(title)
    print(table)
    from QH_http import api_id
    # 判断采用汪仔推荐答案还是Dan哥答案
    if api_id[0]== 'youku':
        from QH_http import get_DANcontent
        content = get_DANcontent('result')
        result = content['result']
        sum = 0
        while result not in answers:
            if sum < 3:
                content = get_DANcontent('result')
                result = content['result']
                sum += 1
            else:
                result = '啊呀,这题Dan哥还在想'
                break
        print('Dan哥推荐答案:' + '-->' + result + '<--')
        print('\n')
    else:
        from QH_http import get_WANcontent
        content = get_WANcontent()
        result = content['result']
        sum = 0
        while result not in answers:
            if sum < 3:
                content = get_WANcontent()
                result = content['result']
                sum += 1
            else:
                result = '啊呀,这题汪仔还在想'
                break
        summary = content['summary']
        for i in value['answers']:
            if i in summary:
                # 打印绿色高亮字体    '\033[0;32m' +  + '\033[0m'
                summary = summary.replace(i, '\033[0;32m' + i + '\033[0m')
        print('汪仔推荐答案:' + '-->' + result + '<--')
        print('参考:', summary)
        print('\n')
