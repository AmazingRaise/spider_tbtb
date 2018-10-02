#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/6 上午11:11
# @Author  : Aries
# @Site    : 
# @File    : test_get_single_task.py
# @Software: PyCharm Community Edition
import logging
from db import SqlHandler

from get_tb_product_info import RequestDetail
logging.basicConfig(
                    level=logging.DEBUG,
                    format='%(asctime)s %(filename)s: %(message)s',    # 定义输出log的格式
                    datefmt='%Y-%m-%d %A %H:%M:%S')
db = SqlHandler(filename='./tb_request.sqlite')
rd = RequestDetail(db)
ret = rd.request_detail_url('https://detail.tmall.com/item.htm?id=570987947722&ns=1&abbucket=0')
print(len(ret))
sales = rd.request_sales(rd.single_task_info[0]['nid'])
single_task_info = [rd.single_task_info[0]['id'],
                    rd.single_task_info[0]['nid'],
                    rd.single_task_info[0]['raw_title'],
                    rd.single_task_info[0]['detail_url'],
                    rd.single_task_info[0]['view_price'],
                    rd.single_task_info[0]['view_sales'],
                    rd.single_task_info[0]['comment_count'],
                    rd.single_task_info[0]['nick'],
                    rd.single_task_info[0]['search_key'],
                    ]

result = single_task_info + ret + sales
rd.insert_result_to_table(result)
