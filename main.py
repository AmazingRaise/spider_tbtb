#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/14 上午11:32
# @Author  : Aries
# @Site    : 
# @File    : main.py.py
# @Software: PyCharm Community Edition
import os
import datetime
import traceback
import time
import logging
from db import SqlHandler
from data_to_excel import DataToExcel
from uubase.common import mouth_first_day, mouth_last_day, now_weekday
from uubase.email import SendEmail
from get_tb_product_info import RequestDetail, get_detail
from taobao_selenium.taobao_search import SeleniumItemGetter
logger = logging.getLogger(__name__)


def start():
    logging.basicConfig(
                    level=logging.DEBUG,
                    format='%(asctime)s %(filename)s: %(message)s',    # 定义输出log的格式
                    datefmt='%Y-%m-%d %A %H:%M:%S')
    db = SqlHandler(filename='./rr.sqlite')
    # 江苏、广东、浙江、山东、北京、内蒙
    search_list = ['江苏移动卡 -充值', '江苏联通卡 -充值', '江苏电信卡 -充值',
                   '广东移动卡 -充值', '广东联通卡 -充值', '广东电信卡 -充值',
                   '浙江移动卡 -充值', '浙江联通卡 -充值', '浙江电信卡 -充值',
                   '山东移动卡 -充值', '山东联通卡 -充值', '山东电信卡 -充值',
                   '北京移动卡 -充值', '北京联通卡 -充值', '北京电信卡 -充值',
                   '内蒙移动卡 -充值', '内蒙联通卡 -充值', '内蒙电信卡 -充值']
    # search_list = ['内蒙移动卡+-充值', '内蒙联通卡+-充值', '内蒙电信卡+-充值']

    time.sleep(3)

    while True:
        try:
            logger.info('has month start task')
            sig = SeleniumItemGetter(db)
            sig.start(search_list)
            rd = RequestDetail(db)
            rd.get_details()
            dte = DataToExcel(db)
            dte.start()
            send_report()
        except Exception:
            traceback.print_exc(file=open('./data/error.txt', 'a'))
        # if mouth_first_day() == datetime.datetime.now().day:
        #     try:
        #         logger.info('has month start task')
        #         get_detail(search_list, db)
        #         rd = RequestDetail(db)
        #         rd.get_details()
        #         dte = DataToExcel(db)
        #         dte.start()
        #         send_report()
        #     except Exception:
        #         traceback.print_exc(file=open('./data/error.txt', 'a'))
        #
        # elif mouth_last_day() == datetime.datetime.now().day:
        #     try:
        #         logger.info('has month end task')
        #         get_detail(search_list, db)
        #         rd = RequestDetail(db)
        #         rd.get_details()
        #         dte = DataToExcel(db)
        #         dte.create_monthly_data()
        #         send_report()
        #     except Exception:
        #         traceback.print_exc(file=open('./data/error.txt', 'a'))
        #
        # if now_weekday() == 3:
        #     try:
        #         logger.info('today have weekly task')
        #         sig = SeleniumItemGetter(db)
        #         sig.start(search_list)
        #         rd = RequestDetail(db)
        #         rd.get_details()
        #         dte = DataToExcel(db)
        #         dte.create_weekly_data(search_list)
        #         send_report()
        #     except Exception:
        #         traceback.print_exc(file=open('./data/error.txt', 'a'))
        # else:
        #     logger.info('today have no task')
        # time.sleep(3600 * 24)


def send_report():
    files = os.listdir('./data')
    send_files = []
    for file_name in files:
        if file_name.startswith('.'):
            continue
        send_files.append(os.path.join('./data', file_name))
    se = SendEmail()
    se.multipart(send_files)
    se.send()
    remove_dir_files(send_files)


def remove_dir_files(send_files):
    for file_root in send_files:
        file_name = os.path.split(file_root)[1]
        if file_name.startswith('.'):
            continue
        os.remove(file_root)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(filename)s: %(message)s',  # 定义输出log的格式
        datefmt='%Y-%m-%d %A %H:%M:%S',
        filename='./tbrequest.log',
        filemode='a'
    )
    start()
    # search_list = ['江苏移动卡 -充值', '江苏联通卡 -充值', '江苏电信卡 -充值',
    #                '广东移动卡 -充值', '广东联通卡 -充值', '广东电信卡 -充值',
    #                '浙江移动卡 -充值', '浙江联通卡 -充值', '浙江电信卡 -充值',
    #                '山东移动卡 -充值', '山东联通卡 -充值', '山东电信卡 -充值',
    #                '北京移动卡 -充值', '北京联通卡 -充值', '北京电信卡 -充值',
    #                '内蒙移动卡 -充值', '内蒙联通卡 -充值', '内蒙电信卡 -充值']
    # db = SqlHandler(filename='./r3.sqlite')
    # dte = DataToExcel(db)
    # dte.create_weekly_data(search_list)
    # send_report()
