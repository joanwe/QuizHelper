#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2018 XXX. All Rights Reserved.
# Author:  joanwe
# Time:    2018/01/20 22:23
# desc:    直播答题辅助,支持冲顶大会/芝士超人/西瓜视频百万英雄/花椒百万赢家


from QH_http import get_id, get_allContent
from QH_data import data_processing
from QH_print import print_table
import time


def main():
    get_id()
    while True:
        global counter
        content = get_allContent(results)
        if content['title'] not in results:
            results.add(content['title'])
            data_processing(content)
            print_table(content)
        else:
            counter += 1
            string = '答题开始后会自动显示答案...共刷新%d次' % counter
            print('\r', string, end='')  # 覆盖打印不换行
            time.sleep(.5)


# 计数器
counter = 0

# 题目去重
results = set()
results.add('答题开始后会自动显示答案')
results.add('Dan哥热身中,题目还在路上...')
results.add('欢迎大家跟着汪仔答题！')

if __name__ == '__main__':
    main()
