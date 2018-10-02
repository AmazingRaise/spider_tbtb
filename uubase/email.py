#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/14 上午11:50
# @Author  : Aries
# @Site    : 
# @File    : email.py.py
# @Software: PyCharm Community Edition
import os
from retry import retry
import datetime
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
logger = logging.getLogger(__name__)


class SendEmail(object):

    def __init__(self):
        self.email_user = 'zhangmianze@uusense.com'
        self.email_pass = 'nihaoma123'
        self.email_host = 'smtp.exmail.qq.com'
        self.sslPort = 465
        self.email_receiver_list = ['zhangmianze@uusense.com']
        self.message = None
        self.sender = 'zhangmianze@uusense.com'

    def multipart(self, filename_li):
        if isinstance(filename_li, str):
            filename_li = [filename_li]
        self.message = MIMEMultipart()
        self.message['From'] = Header('zhangmianze', 'utf-8')
        self.message['To'] = Header('jobhunter2012@126.com', 'utf-8')
        subject = '测试结果' + str(datetime.datetime.now())
        self.message['Subject'] = Header(subject, 'utf-8')

        self.message.attach(MIMEText('您好，附件为本周报告，请您查收，万分感谢', 'plain', 'utf-8'))
        for filename in filename_li:
            dispaly_name = os.path.split(filename)
            att1 = MIMEText(open(filename, 'rb').read(), 'base64', 'utf-8')
            att1["Content-Type"] = 'application/octet-stream'
            att1["Content-Disposition"] = 'attachment; filename="%s"' % (dispaly_name[1])
            self.message.attach(att1)

    @retry(exceptions=Exception, tries=3, delay=3)
    def send(self):
        try:
            # smtpObj = smtplib.SMTP()
            smtp = smtplib.SMTP_SSL(self.email_host, self.sslPort)
            smtp.ehlo()
            smtp.login(self.email_user, self.email_pass)

            # smtpObj.connect(self.email_host, 25)  # 25 为 SMTP 端口号
            # smtpObj.login(self.email_user, self.email_pass)
            smtp.sendmail(self.sender, self.email_receiver_list, self.message.as_string())
            logger.info("邮件发送成功")
        except smtplib.SMTPException:
            logger.info("Error: 无法发送邮件")


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(filename)s: %(message)s',  # 定义输出log的格式
        datefmt='%Y-%m-%d %A %H:%M:%S')
    se = SendEmail()
    se.multipart(['./data/2018_37.xlsx', './requiment.txt'])
    se.send()
