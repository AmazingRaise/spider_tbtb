#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/19 下午5:15
# @Author  : Aries
# @Site    : 
# @File    : taobao_search.py
# @Software: PyCharm Community Edition
import traceback
import re
import random
import json
import time
from db import SqlHandler
from get_tb_product_info import RequestDetail
from selenium.webdriver.chrome.options import Options
from data_to_excel import DataToExcel
from selenium import webdriver


class SeleniumItemGetter(object):

    def __init__(self, db):
        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--disable-gpu')
        # self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.driver = webdriver.Safari()
        self.db = db
        self.page = 0
        self.source_html = None
        self.temp_url = None

    def start(self, search_list):
        for search_keyword in search_list:
            print('keyword: ' + search_keyword)
            self.task_runner(search_keyword)
        self.driver.close()
        self.driver.quit()

    def task_runner(self, search_keyword):
        self.page = 0
        ret = self.task_runnerex(search_keyword)
        while not ret:
            try:
                ret = self.next_page(search_keyword)
                time.sleep(5)
            except Exception as e:
                traceback.print_exc(file=open('./error', 'a'))
                print('sql insert error...')
                print(e)

    def task_runnerex(self, keyword):
        # keyword = '江苏移动电话卡-充值'
        print('task start runner ...')
        self.temp_url = None
        # keywords_list = keyword.split('-')
        self.driver.get('https://www.taobao.com')
        self.driver.find_element_by_xpath('//*[@id="q"]').click()
        time.sleep(3)
        self.driver.find_element_by_css_selector("#q").clear()
        self.driver.find_element_by_css_selector("#q").send_keys(keyword)
        time.sleep(3)
        self.driver.find_element_by_class_name('btn-search').submit()
        self.driver.refresh()
        if 'login.taobao' in self.driver.current_url:
            self.do_login_action()
        self.driver.find_element_by_xpath('//*[@id="J_relative"]/div[1]/div/ul/li[2]/a').click()
        st = time.time()
        print(self.driver.current_url)
        while time.time() - st < 180:
            if 'sale-desc' not in self.driver.current_url:
                time.sleep(2)
            else:
                break
        time.sleep(random.uniform(1, 3))
        #
        # self.driver.find_element_by_css_selector('#q-exclude').send_keys(keywords_list[1])
        # self.driver.find_element_by_xpath('//*[@id="mainsrp-header"]/div/div/div/div[4]/a').click()
        # self.driver.find_element_by_xpath('//*[@id="J_relative"]/div[1]/div/ul/li[2]/a').click()
        # while time.time() - st < 180:
        #     if 'sale-desc' not in self.driver.current_url:
        #         time.sleep(2)
        #     else:
        #         break
        self.driver.refresh()
        html = self.driver.page_source
        self.source_html = html
        self.temp_url = self.driver.current_url
        is_need_stop = self.get_info_into_table(html, keyword)
        self.page = self.page + 1
        return is_need_stop

    def do_login_action(self):
        self.driver.find_element_by_xpath('//*[@id="J_Quick2Static"]').click()
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="TPL_username_1"]').send_keys('13575465942')
        self.driver.find_element_by_xpath('//*[@id="TPL_password_1"]').send_keys('nihaoma891003')
        time.sleep(5)
        self.driver.find_element_by_xpath('//*[@id="J_SubmitStatic"]').submit()

    def get_info_into_table(self, html, keyword):
        print('get_info')
        result = self.get_page_info(html)
        is_need_finish = False
        insert_result = []
        for basic_info in result:
            if 'view_sales' not in basic_info.keys():
                continue
            if basic_info['view_sales'] == '0人收货':
                is_need_finish = True
                continue
            result = [basic_info['nid'], basic_info['raw_title'], basic_info['detail_url'], basic_info['view_price'],
                      basic_info['view_sales'], basic_info['comment_count'], basic_info['nick'], keyword]
            insert_result.append(result)

        try:
            if insert_result:
                sql_line = 'insert into tbTaskInfo(`nid`, `raw_title`, `detail_url`, `view_price`, `view_sales`, ' \
                           '`comment_count`, `nick`, `search_key`) values(?, ?, ?, ?, ?, ?, ?, ?)'
                self.db.update(sql_line, insert_result)
        except Exception as e:
            traceback.print_exc(file=open('./error', 'a'))
            print(insert_result)
            print('sql insert error...')
            print(e)
        return is_need_finish

    def get_page_info(self, html):
        b = re.findall('auctions":(.+),"recommendAuctions"', html)
        if len(b) > 0:
            result = json.loads(b[0])
        else:
            result = None
        return result

    def next_page(self, keyword):
        # 下一页
        print('get next page')
        s = self.page * 44
        self.driver.find_element_by_xpath('//*[@id="mainsrp-pager"]/div/div/div/ul/li[8]/a/span[1]').click()
        st = time.time()
        url = self.temp_url + '&s=%d' % s
        # print('navigate url: %s' % url)
        # self.driver.get(url)
        while time.time() - st < 180:
            match_url = 's=%d' % s
            if match_url not in self.driver.current_url:
                time.sleep(2)
            else:
                break
        print(self.driver.current_url)
        self.driver.refresh()
        html = self.driver.page_source
        is_need_stop = self.get_info_into_table(html, keyword)
        self.page += 1
        time.sleep(random.uniform(1, 3))
        return is_need_stop


if __name__ == '__main__':
    db = SqlHandler(filename='./r4.sqlite')
    # 江苏、广东、浙江、山东、北京、内蒙
    search_list = ['江苏移动卡 -充值', '江苏联通卡 -充值', '江苏电信卡 -充值',
                   '广东移动卡 -充值', '广东联通卡 -充值', '广东电信卡 -充值',
                   '浙江移动卡 -充值', '浙江联通卡 -充值', '浙江电信卡 -充值',
                   '山东移动卡 -充值', '山东联通卡 -充值', '山东电信卡 -充值',
                   '北京移动卡 -充值', '北京联通卡 -充值', '北京电信卡 -充值',
                   '内蒙移动卡 -充值', '内蒙联通卡 -充值', '内蒙电信卡 -充值']
    sig = SeleniumItemGetter(db)
    sig.start(search_list)
    rd = RequestDetail(db)
    rd.get_details()
    dte = DataToExcel(db)
    dte.create_weekly_data()

