#!/usr/bin/env python
# -*- coding: utf-8 -*-
#======================================================================
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
#======================================================================

"""
@Desc: runner module
@File: runner.py
@Author: liangjinhua
@Date: 2018/12/12 21:24
"""
import logging
import os
import sys
from libs.job_scheduler import scheduler

sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))


class JobRunner(object):
    """
    class run job ,check data and paint
    """
    def __init__(self, path, args):
        self.path = path
        self.args = args

    def run(self):
        """start all process"""
        logging.info("start ClockSubmitJobProcess! ")
        csjp = scheduler.ClockSubmitJobProcess(60, self.path, logging.getLoggerClass(), self.args)
        csjp.daemon = True
        csjp.start()

        logging.info("start ClockExtractResultProcess! ")
        cerp = scheduler.ClockExtractResultProcess(60)
        cerp.daemon = True
        cerp.start()
        #
        # cvpp = scheduler.ClockVisualDLProcess(24 * 60)
        # cvpp.daemon = True
        # cvpp.start()

        # logging.info("start ClockLocalJobRunProcess! ")
        # cljr = scheduler.LocalJobRunProcess(2)
        # cljr.daemon = True
        # cljr.start()

        cerp.join()
        csjp.join()
        # cvpp.join()
        #cljr.join()





