#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/6 下午3:40
# @Author  : Aries
# @Site    : 
# @File    : data_to_excel.py.py
# @Software: PyCharm Community Edition
import logging
import time
import datetime
from db import SqlHandler
from uubase.excel_helper import ExcelHelper


class DataToExcel(object):

    def __init__(self, db):
        self.db = db
        self.content = None
        self.page = 0
        self.excel = ExcelHelper()

    # def sql_query_summary(self, search_key):
    #     sql = "select * from tbdetails where search_key='%s'" % search_key
    #     values = self.db.query(sql)
    #     band_name = search_key[2:3]
    #
    # def caculate(self, val, band_name):
    #     if '旗舰店' in val

    def query_data_with_number(self, num=1000):
        sql_line = 'select * from tbDetails limit %d, %d' % (self.page * num, (self.page + 1) * num)
        return self.db.query(sql_line)

    def start(self):
        content_li = [['id', 'nid', '商品名', 'url', '价格', '收货人数', '评论数', '店铺名称', '搜索关键词', '省份', '城市',
                      '运营商', '套餐', '卡类型', '年', '月', '日', '周数', '销售量']]
        while True:
            content = self.query_data_with_number()
            if not content:
                break
            for value in content:
                self.content = value
                val = self.prepare_data()
                content_li.append(val)
            self.page = self.page + 1

        self.data_to_excel(content_li)

    def query_data(self, week=True, last_week=False, month_start=False, keyword=None):

        if week:
            # 取week数据
            now = datetime.datetime.now()
            if last_week:
                now = now - datetime.timedelta(days=7)
            ret_week_tuple = now.isocalendar()
            week_number = ret_week_tuple[1]
            if keyword:
                sql = 'select * from tbDetails where week="%d" and search_key="%s"' % (week_number, keyword)
            else:
                sql = 'select * from tbDetails where week="%d"' % week_number
        else:
            # 取month数据
            now = datetime.datetime.now()
            year = now.year
            month = now.month
            if month_start:
                day = 1
            else:
                day = now.month()
            sql = 'select * from tbDetail where year="%d" and month="%d" and day="%d"' % (year, month, day)

        content = self.db.query(sql)
        week_value = {}
        # for k, v in enumerate(content):
        nid_list = []
        for value in content:
            self.content = value
            v = self.prepare_data()
            week_value.update({value['nid']: v})
            nid_list.append(value['nid'])
        return week_value, nid_list

    def weekly_process(self, search_list):
        result = [['id', 'nid', '商品名', 'url', '价格', '收货人数', '评论数', '店铺名称', '搜索关键词', '省份', '城市',
                   '运营商', '套餐', '卡类型', '年', '月', '日', '周数', '上周销售量', '本周销售量']]
        for search_key in search_list:
            last_week_data, last_week_nid = self.query_data(last_week=True, keyword=search_key)
            current_week_data, current_week_nid = self.query_data(keyword=search_key)
            new_nids = set(current_week_nid).difference(set(last_week_nid))
            off_shelves = set(last_week_nid).difference(set(current_week_nid))
            for nid in current_week_nid:
                if nid in new_nids:
                    print(current_week_data[nid][0: -2])
                    print([current_week_data[nid][-1]])
                    result.append(current_week_data[nid][0: -1] + ['N/A'] + [current_week_data[nid][-1]])
                elif nid in off_shelves:
                    result.append(last_week_data[nid] + ['下架'])
                else:
                    result.append(last_week_data[nid] + [current_week_data[nid][-1]])
        return result

    def monthly_process(self):
        month_start_data, month_start_nid = self.query_data(last_week=False, month_start=True)
        month_end_data, month_end_nid = self.query_data(last_week=False)
        new_nids = set(month_end_nid).difference(set(month_start_nid))
        off_shelves = set(month_start_nid).difference(set(month_end_nid))
        result = []
        for nid in month_end_nid:
            if nid in new_nids:
                result.append(month_end_data[nid][0: -2] + [' '] + [month_end_data[nid][-1]])
            elif nid in off_shelves:
                result.append(month_start_data[nid] + [' '])
            else:
                result.append(month_start_data[nid] + [month_end_data[nid][-1]])
        return result

    def create_weekly_data(self, search_list):
        result = self.weekly_process(search_list)
        self.data_to_excel(result)

    def create_monthly_data(self):
        result = self.monthly_process()
        self.data_to_excel(result)

    def prepare_data(self):
        value = [self._db_id, self._nid, self._raw_title, self._detail_url, self._view_price, self._view_sales,
                 self._comment_count, self._nick, self._search_key, self._province, self._city, self._band_name,
                 self._tc, self._card_type, self._year, self._month, self._day, self._week, self._sales]
        return value

    @property
    def _db_id(self):
        return self.content['id']

    @property
    def _nid(self):
        return self.content['nid']

    @property
    def _raw_title(self):
        return self.content['raw_title']

    @property
    def _detail_url(self):
        return self.content['detail_url']

    @property
    def _view_price(self):
        return self.content['view_price']

    @property
    def _view_sales(self):
        return self.content['view_sales']

    @property
    def _comment_count(self):
        return self.content['comment_count']

    @property
    def _nick(self):
        return self.content['nick']

    @property
    def _search_key(self):
        return self.content['search_key']

    @property
    def _province(self):
        return self.content['province']

    @property
    def _city(self):
        return self.content['city']

    @property
    def _band_name(self):
        return self.content['band_name']

    @property
    def _tc(self):
        return self.content['tc']

    @property
    def _card_type(self):
        return self.content['card_type']

    @property
    def _sales(self):
        return self.content['sales']

    @property
    def _week(self):
        return self.content['week']

    @property
    def _year(self):
        return self.content['year']

    @property
    def _month(self):
        return self.content['month']

    @property
    def _day(self):
        return self.content['day']

    def data_to_excel(self, data):
        self.excel.insert_data(data)
        self.excel.save_excel()


if __name__ == '__main__':
    logging.basicConfig(
                    level=logging.DEBUG,
                    format='%(asctime)s %(filename)s: %(message)s',    # 定义输出log的格式
                    datefmt='%Y-%m-%d %A %H:%M:%S')
    db = SqlHandler(filename='./tb_request.sqlite')
    dte = DataToExcel(db)
    dte.start()
    dte.excel.save_excel()
