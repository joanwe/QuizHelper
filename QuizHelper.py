#!/usr/bin/python
# -*- coding: utf-8 -*-

# Author:  joanwe
# Time:    2018/01/20 22:23
# desc:    直播答题辅助,支持冲顶大会/芝士超人/西瓜视频百万英雄/花椒百万赢家

import requests as req
import json
import time
from prettytable import PrettyTable
from threading import Thread


def main():
    select_app()
    thd = Thread(target=reselect_app)
    thd.start()
    while True:
        for value in get_content():
            if not isInresults(value):
                results.add(value)
                display_content(value)
                time.sleep(0.5)


# 重新选择答题App
def reselect_app():
    index = input()
    if int(index) == 0:
        main()


# 选择答题APP
def select_app():
    global api_key
    index = input(('请选择答题APP:\n1:冲顶大会\n2:芝士超人\n3:西瓜百万英雄\n4:花椒百万赢家'
                   '\n----------------\n提示:过程中输入数字键0可重新选择答题app\n'))
    if int(index) == 1:
        api_key = 'cddh'
    elif int(index) == 2:
        api_key = 'zscr'
    elif int(index) == 3:
        api_key = 'xigua'
    elif int(index) == 4:
        api_key = 'huajiao'
    else:
        print("输入错误,请重新选择")
        select_app()


# 获取搜狗api内容
def get_content():
    api = 'http://140.143.49.31/api/ans2?key=' + api_key
    headers = {
        'Host': '140.143.49.31',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_5 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13G36 Sogousearch/Ios/5.9.7',
        'Accept-Language': 'zh-cn',
        'Referer': 'http://nb.sa.sogou.com/',
        'Accept-Encoding': 'gzip, deflate'
    }

    html = req.get(api, headers=headers)
    html = html.text
    html = html[html.find("(") + 1: len(html) - 1]
    return json.loads(html)['result']


# 展示问题及答案
def display_content(value):
    value = json.loads(value)
    # 处理搜索结果
    if len(value['answers']) > 0:
        search_counts = []
        appear_counts = []
        table = PrettyTable(['答案选项', '搜索结果总数', '首页出现次数'])
        table.align['答案选项'] = 'l'
        title = value['title']
        for anwsers in value['answers']:
            # 多线程
            t1 = Thread(target=get_appear_counts(title, anwsers, appear_counts))
            t2 = Thread(target=get_search_counts(title, anwsers, search_counts))
            t2.start()
            t1.start()

            # 单线程
            # get_search_counts(title, anwsers, search_counts)
            # get_appear_counts(title, anwsers, appear_counts)

        # 将数据添加到表格
        table.add_row(['A.' + value['answers'][0], search_counts[0], appear_counts[0]])
        table.add_row(['B.' + value['answers'][1], search_counts[1], appear_counts[1]])
        table.add_row(['C.' + value['answers'][2], search_counts[2], appear_counts[2]])

        # 打印绿色高亮字体    '\033[0;32m' +  + '\033[0m'
        # 推荐答案添加字母排序
        letter = ''
        letters = ['A.', 'B.', 'C.']
        recommend = value['recommend']
        summary = value['search_infos'][0]['summary']
        for i in value['answers']:
            if recommend in i:
                letter = letters[value['answers'].index(i)]
        for i in value['answers']:
            if i in summary:
                summary = summary.replace(i, '\033[0;32m' + i + '\033[0m')

        # 打印表格
        print(title)
        print(table)
        print('推荐答案:', letter + value['recommend'])
        print('参考:', summary)
        print('\n')


# 判断是否出现新题目
results = set([])


def isInresults(value):
    return value in results


# 获取搜索结果总数
def get_search_counts(title, anwsers, search_counts):
    r = req.get('http://www.baidu.com/s', params={'wd': title + '' + anwsers})
    html = r.text
    index = html.find('百度为您找到相关结果约') + 11
    html = html[index:]
    index = html.find('个')
    search_counts.append(html[:index].replace(',', ''))


# 获取首页出现次数
def get_appear_counts(title, anwers, appear_counts):
    page = req.get('http://www.baidu.com/s', params={'wd': title}).text
    appear_counts.append(page.count(anwers))


if __name__ == '__main__':
    main()
