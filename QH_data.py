#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2018 XXX. All Rights Reserved.
# Author:  joanwelol@gmail.com
# QH_data.py 2018/1/25 21:57
# desc:

import asyncio
import aiohttp
from bs4 import BeautifulSoup as bs4
import json
from QH_print import table


# 获取搜索结果总数
async def get_search_counts(title, anwsers, search_counts):
    async with aiohttp.ClientSession() as session:
        async with session.get('http://www.baidu.com/s?wd=' + title + ' ' + anwsers) as resp1:
            html1 = await resp1.text()
            index = html1.find('百度为您找到相关结果约') + 11
            html1 = html1[index:]
            index = html1.find('个')
            search_counts[anwsers] = html1[:index].replace(',', '')


# 获取首页出现次数
async def get_appear_counts(title, anwers, appear_counts):
    async with aiohttp.ClientSession() as session:
        async with session.get('http://www.baidu.com/s?wd=' + title) as resp2:
            html2 = await resp2.text()
            html2 = bs4(html2, 'lxml')
            html2 = html2.find_all('div', attrs={'class': 'result c-container '})
            html2 = str(html2)
            appear_counts[anwers] = html2.count(anwers)


# 处理数据表格
def data_processing(value):
    value = json.loads(value)
    if len(value['answers']) > 0:
        search_counts = {}
        appear_counts = {}
        for name in value['answers']:
            search_counts = {name: 0}
            appear_counts = {name: 0}
        title = value['title']
        table.clear_rows()

        # 异步io 获取数据结果
        async def main():
            coroutines1 = [get_search_counts(title, answers, search_counts) for answers in value['answers']]
            coroutines2 = [get_appear_counts(title, answers, appear_counts) for answers in value['answers']]
            coroutines = coroutines1 + coroutines2
            tasks = [asyncio.ensure_future(coroutine) for coroutine in coroutines]
            await asyncio.wait(tasks)

        # 启动和关闭事件循环
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
        loop.close()

        # 向表格添加数据结果
        index = value['answers']
        table.add_row(['1.' + index[0], search_counts[index[0]], appear_counts[index[0]]])
        table.add_row(['2.' + index[1], search_counts[index[1]], appear_counts[index[1]]])
        table.add_row(['3.' + index[2], search_counts[index[2]], appear_counts[index[2]]])
