#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/20 下午4:10
# @Author  : Aries
# @Site    : 
# @File    : demo.py.py
# @Software: PyCharm Community Edition
import time
from selenium import webdriver


for i in range(0, 50):
    driver = webdriver.Chrome()
    driver.get('https://www.wenjuan.com/s/3qqEVbA')
    driver.find_element_by_xpath('//*[@id="question_5ba3022092beb5119dfd75f2"]/div[2]/div[3]/label').click()
    driver.find_element_by_xpath('//*[@id="question_5ba3027592beb50e6f84ef6e"]/div[2]/div[3]/label').click()
    driver.find_element_by_xpath('//*[@id="question_5ba3029f92beb5113ea694b1"]/div[2]/div[3]/label').click()
    driver.find_element_by_xpath('//*[@id="question_5ba302cd92beb50f2d9e90c7"]/div[2]/div[3]/label').click()
    driver.find_element_by_xpath('//*[@id="question_5ba302f892beb50e3bbb3520"]/div[2]/div[3]/label').click()
    driver.find_element_by_xpath('//*[@id="question_5ba3031892beb50f2d9e90e4"]/div[2]/div[3]/label').click()
    driver.find_element_by_xpath('//*[@id="question_5ba3032592beb51039397628"]/div[2]/div[3]/label').click()
    driver.find_element_by_xpath('//*[@id="question_5ba3032e92beb50f2d9e90ea"]/div[2]/div[3]/label').click()
    driver.find_element_by_xpath('//*[@id="question_5ba303bc92beb50fdd2c350c"]/div[2]/div[3]/label').click()
    driver.find_element_by_xpath('//*[@id="question_5ba303d992beb50e3bbb354f"]/div[2]/div[3]/label').click()
    driver.find_element_by_xpath('//*[@id="next_button"]').click()
    time.sleep(2)
    driver.close()
    driver.quit()
