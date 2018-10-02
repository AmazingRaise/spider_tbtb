#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/23 下午1:54
# @Author  : Aries
# @Site    : 
# @File    : get_tb_product_info.py
# @Software: PyCharm Community Edition
import json
import time
import datetime
import calendar
import traceback
import re
import logging
from threading import Thread
from uubase.http_client import request_http, WebdriverProcess
from uubase.excel_helper import ExcelHelper
from db import SqlHandler


logger = logging.getLogger(__name__)
HEADERS = {}


class TBProductInfo(object):

    SEARCH_CONSTANT = 'https://s.taobao.com/search?q=%s&search_type=item&ie=utf8&sort=sale-desc'

    def __init__(self, search_words, steps, sql):
        self.search_list = search_words
        self.search_words = None
        self.url = self.SEARCH_CONSTANT % search_words
        self.page = 0
        self.product_info = []
        self.step = steps
        self.result = None
        self.sql = sql
        self.selenium_driver = WebdriverProcess()

    def bootstrap(self):
        if isinstance(self.search_list, list):
            pass
        elif isinstance(self.search_list, str):
            self.search_list = [self.search_list]
        else:
            return

    def into_taobao(self):
        self.selenium_driver.action_navigate('https://www.taobao.com')

    def start(self):
        self.bootstrap()
        self.into_taobao()
        for search_key in self.search_list:
            self.selenium_driver.find_element_by_xpath('//*[@id="q"]').sendkeys(search_key)
            self.selenium_driver.find_element_by_xpath('//*[@id="J_TSearchForm"]/div[1]/button').click()
            self.search_words = search_key
            logger.info('request_url:' + self.url)
            for i in range(0, self.step):
                self.url = self.SEARCH_CONSTANT % search_key
                self.prepare_url()
                self.page = self.page + 1
                if self.request_url():
                    break
            self.page = 0

    def prepare_url(self):
        if self.page == 0:
            pass
        elif self.page < self.step:
            self.url = self.url + '&s=%d' % (44 * (self.page + 1))
        else:
            logging.info('finish spider for has been ...')

    def request_url(self):
        print('url: %s, page:%s' % (self.url, self.page))
        try:
            content = request_http(self.url, self.selenium_driver)
            if not content:
                raise ValueError('request_http error, please check')
            self.get_tb_page_config(content)
            return self.get_basic_info()
        except Exception as e:
            traceback.print_exc()
            self.write_error('main_url:' + self.url + '\n')

    def write_error(self, message):
        fp = open('./error.txt', 'a')
        fp.write(message)
        fp.close()

    def insert_task_into_table(self):
        is_need_finish = False
        insert_result = []
        for basic_info in self.result:
            if 'view_sales' not in basic_info.keys():
                continue
            if basic_info['view_sales'] == '0人收货':
                is_need_finish = True
                continue
            result = [basic_info['nid'], basic_info['raw_title'], basic_info['detail_url'], basic_info['view_price'],
                      basic_info['view_sales'], basic_info['comment_count'], basic_info['nick'], self.search_words]
            insert_result.append(result)

        try:
            if insert_result:
                sql_line = 'insert into tbTaskInfo(`nid`, `raw_title`, `detail_url`, `view_price`, `view_sales`, ' \
                           '`comment_count`, `nick`, `search_key`) values(?, ?, ?, ?, ?, ?, ?, ?)'
                self.sql.update(sql_line, insert_result)
        except Exception as e:
            traceback.print_exc()
            logger.info(insert_result)
            logger.error('sql insert error...')
            logger.error(e)
        return is_need_finish

    def get_basic_info(self):
        is_need_finish = False
        if self.result:
            is_need_finish = self.insert_task_into_table()
        else:
            logger.error('info not found...url:%s' % self.url)
        self.result = []
        return is_need_finish

    def write_txt(self, content):
        filename = './data.txt'
        fp = open(filename, 'a')
        fp.write('\t'.join(content) + '\n')
        fp.close()

    def write_excel(self):
        pass

    def get_tb_page_config(self, content):
        b = re.findall('auctions":(.+),"recommendAuctions"', content)
        if len(b) > 0:
            self.result = json.loads(b[0])
        else:
            self.result = None

    def update_search_word(self, search_word):
        self.search_words = search_word
        self.page = 0


class RequestDetail(object):

    def __init__(self, db):
        self.db = db
        self.single_task_info = None
        # self.selenium_driver = WebdriverProcess()

    def get_details(self):
        while True:
            ret = self.do_single_task()
            if ret:
                break

    def do_single_task(self):
        need_stop = False
        sql = 'select * from tbTaskInfo limit 1'
        self.single_task_info = self.db.query(sql)

        if not self.single_task_info:
            logger.info('no task found, please wait')
            need_stop = True
            return need_stop

        url = self.single_task_info[0]['detail_url']
        if url.startswith('//'):
            url = url[2:]

        content = self.request_detail_url(url)
        sales = self.request_sales(self.single_task_info[0]['nid'])
        single_task_info = [self.single_task_info[0]['id'],
                            self.single_task_info[0]['nid'],
                            self.single_task_info[0]['raw_title'],
                            self.single_task_info[0]['detail_url'],
                            self.single_task_info[0]['view_price'],
                            self.single_task_info[0]['view_sales'],
                            self.single_task_info[0]['comment_count'],
                            self.single_task_info[0]['nick'],
                            self.single_task_info[0]['search_key'],
                            ]
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        day = datetime.datetime.now().day
        week = time.strftime("%W")

        result = single_task_info + content + sales + [year, month, day, week]
        self.insert_result_to_table(result)
        self.delete_task_by_id(self.single_task_info[0]['id'])
        return need_stop

    def delete_task_by_id(self, id):
        sql = 'DELETE FROM `tbTaskInfo` WHERE id=%d' % id
        self.db.update(sql)

    def insert_result_to_table(self, result):
        sql = 'insert into `tbDetails` values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
        self.db.update(sql, [tuple(result)])

    def request_detail_url(self, detail_url):
        content, content_encode = request_http(detail_url)
        content = content.decode(content_encode, 'ignore')
        result = []
        product_param_li = re.findall('<ul id="J_AttrUL">[^$]+</ul>', content)
        if product_param_li:
            province = re.findall('号码归属市[^;]+;([^<]+)</li>', product_param_li[0])
            cities = re.findall('地市:([^<]+)</li>', product_param_li[0])
            band_name = re.findall('J_attrBrandName[^;]+;(.+)">', product_param_li[0])
            tc = re.findall('套餐:([^<]+)</li>', product_param_li[0])
            card_type = re.findall('手机卡类型:&nbsp;([^<]+)</li>', product_param_li[0])
            result.append(self.find_list_value(province))
            result.append(self.find_list_value(cities))
            if band_name:
                result.append(self.find_list_value(band_name))
            else:
                result.append('')
            result.append(self.find_list_value(tc))
            result.append(self.find_list_value(card_type))
        return result

    def request_sales(self, nid):
        detail_url = 'https://world.taobao.com/item/%s.htm' % str(nid)
        try:
            content, encoding = request_http(detail_url)
            content = content.decode(encoding, 'ignore')
            sales = re.findall('月銷量[^\d]+([\d]+)<', content)
            if sales:
                return sales
            else:
                return self.request_sales_ex(nid)
        except Exception as e:
            traceback.print_exc()
            logger.info('err in request sales')
            logger.info(e)
        return [' ']

    def request_sales_ex(self, nid):
        detail_url = 'https://www.taobao.com/list/item-amp/%s.htm' % str(nid)
        try:
            content, encoding = request_http(detail_url)
            content = content.decode(encoding, 'ignore')
            sales = re.findall('月销量[^\d]+([\d]+)<', content)
            if sales:
                return sales
        except Exception as e:
            traceback.print_exc()
            logger.info('err in request sales_ex')
            logger.info(e)
        return [' ']

    @staticmethod
    def find_list_value(val):
        if val:
            content = val[0].replace('&nbsp', '')
            if content.startswith(';'):
                return content[1:]
            else:
                return content
        else:
            return ''


def get_detail(search_list, db):
    tbpi = TBProductInfo(search_list, 50, db)
    tbpi.start()


if __name__ == '__main__':
    logging.basicConfig(
                    level=logging.DEBUG,
                    format='%(asctime)s %(filename)s: %(message)s',    # 定义输出log的格式
                    datefmt='%Y-%m-%d %A %H:%M:%S')
    db = SqlHandler(filename='./tb_request2.sqlite')
    # 江苏、广东、浙江、山东、北京、内蒙
    search_list = ['江苏移动卡+-充值', '江苏联通卡+-充值', '江苏电信卡+-充值',
                   '广东移动卡+-充值', '广东联通卡+-充值', '广东电信卡+-充值',
                   '浙江移动卡+-充值', '浙江联通卡+-充值', '浙江电信卡+-充值',
                   '山东移动卡+-充值', '山东联通卡+-充值', '山东电信卡+-充值',
                   '北京移动卡+-充值', '北京联通卡+-充值', '北京电信卡+-充值',
                   '内蒙移动卡+-充值', '内蒙联通卡+-充值', '内蒙电信卡+-充值']
    # search_list = ['内蒙移动卡+-充值', '内蒙联通卡+-充值', '内蒙电信卡+-充值']
    # get_detail(search_list, db)
    # time.sleep(3)
    # rd = RequestDetail(db)
    # rd.get_details()
