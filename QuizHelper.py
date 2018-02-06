#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2018 XXX. All Rights Reserved.
# Author:  joanwe
# Time:    2018/01/20 22:23
# desc:    直播答题辅助,支持冲顶大会/芝士超人/西瓜视频百万英雄/花椒百万赢家


from QH_http import get_key, get_content, get_DANcontent
from QH_data import data_processing
from QH_print import print_table
import time


def main():
    get_key()
    from QH_http import switch
    while True:
        global counter
        if switch == 0:
            content = get_content()
            if results['title'] != content['title']:
                results['title'] = content['title']
                data_processing(content)
                print_table(content)
            else:
                counter += 1
                string = '页面刷新中...共计%d次' % counter
                print('\r', string, end='')  # 覆盖打印不换行
                time.sleep(0.5)
        if switch == 1:
            content = get_DANcontent()
            if results['title'] != content['title']:
                results['title'] = content['title']
                data_processing(content)
                print_table(content)
            else:
                counter += 1
                string = '页面刷新中...共计%d次' % counter
                print('\r', string, end='')  # 覆盖打印不换行
                time.sleep(0.5)


# 计数器
counter = 0

# 判断是否出现新题目
results = {'title': ''}

if __name__ == '__main__':
    main()
