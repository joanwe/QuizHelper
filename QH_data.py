#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2018 XXX. All Rights Reserved.
# Author:  joanwelol@gmail.com
# QH_data.py 2018/1/25 21:57
# desc:

import asyncio, aiohttp, json, re
from bs4 import BeautifulSoup as bs4
from QH_print import table
from urllib.parse import quote


# 获取结果总数
async def get_search_counts(title, anwsers, search_counts):
    async with aiohttp.ClientSession() as session:
        async with session.get('http://www.baidu.com/s', params={'wd': quote(title) + quote(anwsers)},
                               headers=headers) as resp:
            html = await resp.text()
            index = re.findall('百度为您找到相关结果约([\d|,]+)个', html)
            search_counts[anwsers] = index[0]


# 获取词频计数
async def get_appear_counts(title, answers_list, appear_counts):
    async with aiohttp.ClientSession() as session:
        async with session.get('http://www.baidu.com/s', params={'wd': quote(title)}, headers=headers) as resp:
            html = await resp.text()
            soup = bs4(html, 'lxml')
            data = soup.find_all('div', class_='result c-container ')
            data = str(data)
            for answer in answers_list:
                appear_counts[answer] = len(re.findall(answer, data, re.I))


# 处理数据表格
def data_processing(value):
    value = json.loads(value)
    if len(value['answers']) > 0:
        search_counts = {}
        appear_counts = {}
        answers_list = []
        for tag in value['answers']:
            search_counts = {tag: 0}
            appear_counts = {tag: 0}
            answers_list.append(tag)
        title = value['title']
        table.clear_rows()

        # 异步io 获取数据结果
        async def main():
            cor1 = [get_search_counts(title, answers, search_counts) for answers in value['answers']]
            cor2 = [get_appear_counts(title, answers_list, appear_counts)]
            cor = cor1 + cor2
            tasks = [asyncio.ensure_future(cor) for cor in cor]
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


headers = {
    'User-Agent': 'Mozilla/4.0+(compatible;+MSIE+8.0;+Windows+NT+5.1;+Trident/4.0;+GTB7.1;+.NET+CLR+2.0.50727)'
}
