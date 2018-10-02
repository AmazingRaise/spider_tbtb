#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/14 上午10:46
# @Author  : Aries
# @Site    : 
# @File    : common.py.py
# @Software: PyCharm Community Edition

import time
import datetime
import calendar


def mouth_first_day():
    return 1


def mouth_last_day():
    now = datetime.datetime.now()
    ret = calendar.monthrange(now.year, now.month)
    return ret[1]


def now_weekday():
    now = datetime.datetime.now()
    ret = calendar.weekday(now.year, now.month, now.day)
    return ret


if __name__ == '__main__':
    print(datetime.datetime.now())
    print(mouth_last_day())
    print(now_weekday())
