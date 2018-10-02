#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/19 上午10:50
# @Author  : Aries
# @Site    : 
# @File    : tb_constant.py.py
# @Software: PyCharm Community Edition

CREATE_TASK_TB_DB = "CREATE TABLE `tbTaskInfo` (" \
                    "`id` INTEGER primary key AUTOINCREMENT," \
                    "`nid` varchar(300) not null," \
                    "`raw_title` varchar(300) not null," \
                    "`detail_url` varchar(300) not null," \
                    "`view_price` varchar(30) not null," \
                    "`view_sales` text(300)," \
                    "`comment_count` text(300)," \
                    "`nick` varchar(64) not null," \
                    "`search_key` varchar(64) not null," \
                    "`status` char(2) default 0" \
                    ");"

CREATE_DETAILS_TB_DB = "CREATE TABLE `tbDetails` (" \
                        "`id` INTEGER primary key AUTOINCREMENT," \
                        "`nid` varchar(300) not null," \
                        "`raw_title` varchar(300) not null," \
                        "`detail_url` varchar(300) not null," \
                        "`view_price` varchar(30) not null," \
                        "`view_sales` text(300)," \
                        "`comment_count` text(300)," \
                        "`nick` varchar(64) not null," \
                        "`search_key` varchar(64) not null," \
                        "`province` varchar(64)," \
                        "`city` varchar(64)," \
                        "`band_name` varchar(64)," \
                        "`tc` varchar(64)," \
                        "`card_type` varchar(64)," \
                        "`sales` varchar(64)," \
                        "`year` varchar(4)," \
                        "`month` varchar(2)," \
                        "`day` varchar(2)," \
                        "`week` varchar(2)" \
                        ");"
