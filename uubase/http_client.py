#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/15 下午9:42
# @Author  : Aries
# @Site    : 
# @File    : http_client.py
# @Software: PyCharm Community Edition
import random
import selenium
from selenium import webdriver
import time
from retry import retry
from requests import request
from selenium.webdriver.chrome.options import Options
from requests.exceptions import HTTPError, ConnectionError, ConnectTimeout, ReadTimeout


@retry((HTTPError, ConnectionError, ConnectionError, ReadTimeout), tries=10, delay=3)
def request_http(url, headers, postdata=None, timeout=60):
    if postdata:
        method = 'POST'
    else:
        method = 'GET'
    if not url.startswith('http'):
        url = 'https://' + url
    result = request(
        method=method,
        url=url,
        headers=headers,
        data=postdata,
        timeout=timeout,
        verify=False
    )
    if not check_error(result):
        raise HTTPError()
    time.sleep(random.uniform(0, 2))
    return result.content, result.encoding


def check_error(r):
    if r.status_code == 200 and r.content and r.encoding:
        return True
    else:
        return False

#
# @retry(exceptions=Exception, tries=3, delay=2)
# def request_http(url, rh_wp):
#     rh_wp.action_navigate(url)
#     return rh_wp.source()


class WebdriverProcess(object):

    def __init__(self, browser='chrome'):
        if browser.lower() == 'ie':
            self.driver = webdriver.Ie()
        elif browser.lower() == 'chrome':
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            prefs = {"profile.managed_default_content_settings.images": 2}  # not load image
            chrome_options.add_experimental_option("prefs", prefs)
            self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.window_handle = []
        self.html = None

    def action_navigate(self, url):
        self.driver.get(url)
        if 'login' in self.driver.title:
            self.do_login_action()

    def do_login_action(self):
        self.driver.find_element_by_id()

    def source(self):
        return self.driver.page_source

    def quit(self):
        self.driver.quit()

    def close(self):
        self.driver.close()


if __name__ == '__main__':
    wp = WebdriverProcess()
    wp.action_navigate('https://www.baidu.com')
    wp.action_navigate('https://www.sina.cn')
    print(wp.source())

