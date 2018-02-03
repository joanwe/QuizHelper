#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2018 XXX. All Rights Reserved.
# Author:  joanwe
# Time:    2018/01/20 22:23
# desc:    直播答题辅助,支持冲顶大会/芝士超人/西瓜视频百万英雄/花椒百万赢家


from QH_http import get_key, get_content
from QH_data import data_processing
from QH_print import print_table
import time


def main():
    get_key()
    while True:
        if not isInresults(get_content()):
            results['title']=get_content()['title']
            data_processing(get_content())
            print_table(get_content())
        else:
            global counter
            counter += 1
            string = '页面刷新中...共计%d次' % counter
            print('\r', string, end='')  # 覆盖打印不换行
            time.sleep(0.5)


# 计数器
counter = 0

# 判断是否出现新题目
results = {'title':''}


def isInresults(value):
    return value['title'] == results['title']


if __name__ == '__main__':
    main()
