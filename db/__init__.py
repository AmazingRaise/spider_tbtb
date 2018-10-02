#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/19 上午10:41
# @Author  : Aries
# @Site    : 
# @File    : __init__.py
# @Software: PyCharm Community Edition
from db.tb_constant import CREATE_TASK_TB_DB, CREATE_DETAILS_TB_DB
import sqlite3
import os
import logging
logger = logging.getLogger(__name__)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class SqlHandler(object):

    def __init__(self, filename):
        self.db_name = filename
        self.conn = None
        self.cu = None
        self.is_exit()

    def is_exit(self):
        if os.path.exists(self.db_name):
            self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
            # out_put = dict
            self.conn.row_factory = dict_factory
            self.conn.text_factory = str
        else:
            self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
            self.conn.row_factory = dict_factory
            self.conn.text_factory = str
            self.create_table()

    def create_table(self):
        sql_li = [CREATE_DETAILS_TB_DB, CREATE_TASK_TB_DB]
        self.cu = self.conn.cursor()
        for sql in sql_li:
            self.cu.execute(sql)
        self.cu.close()

    def update(self, sql, sqlstring=None):
        cursor = self.conn.cursor()
        if sqlstring:
            print(sqlstring)
            cursor.executemany(sql, sqlstring)
        else:
            cursor.execute(sql)
        self.conn.commit()
        cursor.close()

    def query(self, sql, sqlstring=False):
        cursor = self.conn.cursor()
        if sqlstring:
            cursor.executemany(sql, sqlstring)
        else:
            cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        return data
