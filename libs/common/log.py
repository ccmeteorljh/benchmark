#!/usr/bin/env python
# -*- coding: utf-8 -*-
#======================================================================
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
#======================================================================

"""
@Desc: log module
@File: log.py
@Author: liangjinhua
@Date: 2017/12/19 10:27
"""
import os
import logging
import logging.handlers
import threading
import time
from conf import base_conf

class Log(object):
    """define personal log style
    """
    def __init__(self, log_path, level=logging.INFO, when="D", backup=7,
                 format="%(levelname)s: %(asctime)s: %(filename)s:"
                        "%(lineno)d * %(thread)d %(message)s",
                 datefmt="%m-%d %H:%M:%S"):
        """
        init_log - initialize log module

        Args:
          log_path      - Log file path prefix.
                          Log data will go to two files: log_path.log and log_path.log.wf
                          Any non-exist parent directories will be created automatically
          level         - msg above the level will be displayed
                          DEBUG < INFO < WARNING < ERROR < CRITICAL
                          the default value is logging.INFO
          when          - how to split the log file by time interval
                          'S' : Seconds
                          'M' : Minutes
                          'H' : Hours
                          'D' : Days
                          'W' : Week day
                          default value: 'D'
          format        - format of the log
                          default format:
                          %(levelname)s: %(asctime)s: %(filename)s:%(lineno)d * %(thread)d %(message)s
                          INFO: 12-09 18:02:42: log.py:40 * 139814749787872 HELLO WORLD
          backup        - how many backup file to keep
                          default value: 7

        Raises:
            OSError: fail to create log directories
            IOError: fail to open log file
        """
        formatter = logging.Formatter(format)
        # formatter = logging.Formatter(format, datefmt)
        self.logger = logging.getLogger()
        self.logger.setLevel(level)

        dir = os.path.dirname(log_path)
        if not os.path.isdir(dir):
            os.makedirs(dir)

        handler = logging.handlers.TimedRotatingFileHandler(log_path + ".log",
                                                            when=when,
                                                            backupCount=backup)
        handler.setLevel(level)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        pwd = os.getcwd()
        print pwd
        # handler = logging.handlers.TimedRotatingFileHandler(log_path + ".log.wf",
        #                                                     when=when,
        #                                                     backupCount=backup)
        # handler.setLevel(logging.WARNING)
        # handler.setFormatter(formatter)
        # logger.addHandler(handler)

    def get_logger(self):
        """
        get logger
        :return:
        """
        return self.logger


class MyLog(object):
    """
    this is my log style
    """
    log = None
    mutex = threading.Lock()

    def __init__(self):
        pass

    @staticmethod
    def get_log():
        """
        get my style log
        :return:
        """
        if MyLog.log is None:
            MyLog.mutex.acquire()
            title_format = "[%(levelname)s][%(asctime)s][%(thread)d]"
            body_format = "[%(filename)s:%(lineno)s][%(funcName)s] %(message)s"
            formatstr = "%s%s" % (title_format, body_format)
            file_name = '../output/paddle/paddle_%s' \
                        % (time.strftime("%Y%m%d%H", time.localtime()))
            print file_name
            MyLog.log = Log(file_name, format=formatstr)
            MyLog.mutex.release()
        return MyLog.log.get_logger()