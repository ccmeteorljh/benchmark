#!/usr/bin/env python
# -*- coding: utf-8 -*-
#======================================================================
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
#======================================================================

"""
@Desc: visualdl_paint module
@File: visualdl_paint.py
@Author: liangjinhua
@Date: 2018/8/2 11:38
"""
import random
import json
from visualdl import LogWriter
import os
from benchmark_server import benchmark_models as bm

from conf import base_conf as conf


def get_result(test_for):
    """
    get log from db and produce protobuf logs
    :return:
    """
    result_logs = bm.ViewVisualDLLog.objects.filter(test_for=test_for)
    if not result_logs:
        print("no {} results in latest paddle version".format(test_for))
        return
    paddle_version = result_logs[0].paddle_version if result_logs else ''
    version_path = os.path.join(conf.ROOT_PATH, 'visualdl_logs', paddle_version)
    cmd = "if [ ! -d %s ]; then mkdir %s; fi" % (version_path, version_path)
    os.system(cmd)
    logdir = os.path.join(version_path, test_for)
    #logdir_des = conf.ROOT_PATH + '/visualdl_logs/latest'
    logdir_des = os.path.join(conf.ROOT_PATH, 'visualdl_logs', 'latest', test_for)
    cmd = "if [ -e %s ]; then rm -rf %s; fi; mkdir %s" % (logdir, logdir, logdir)
    os.system(cmd)

    logge = LogWriter(logdir, sync_cycle=1)

    def sample_log(result_log_dict, model, run_machine_type):
        """sample log from db log depends on model and run_machine_type"""
        if model == 'ocr':
            sample_ratio = 1
            if run_machine_type.startswith("MULTI_MACHINE_MULTI"):
                sample_ratio = 62
            elif run_machine_type.startswith("MULTI_MACHINE_ONE"):
                sample_ratio = 15
            elif run_machine_type.startswith("ONE"):
                sample_ratio = 15
            elif run_machine_type.startswith("FOUR"):
                sample_ratio = 15
            elif run_machine_type.startswith("MULTI_GPU"):
                sample_ratio = 15

            for k, v in result_log_dict.items():
                sample_list = [v[index] for index in range(len(v)) if index % sample_ratio == 0]
                result_log_dict[k] = [[index + 1, sample_list[index][1]] for index in range(len(sample_list))]

        return result_log_dict

    for log in result_logs:
        model = log.model
        test_for = log.test_for
        #code_from = log.code_from
        run_rpc_type = log.run_rpc_type.lower()
        run_machine_type= log.run_machine_type.lower()
        tag = "%s_%s_%s" % (test_for.split('_')[0], run_machine_type, run_rpc_type)
        result_log_dict = json.loads(log.result_log)
        #sample_log_dict = sample_log(result_log_dict, model, run_machine_type)
        print ("visualdl_paint cur is: %s_%s_%s" % (model, tag, log.cloud_job_id))
        for indicant, values in result_log_dict.items():
            with logge.mode(indicant) as logge:
                val_tag = logge.scalar("%s/%s" % (model, tag))
                for step, value in values:
                    if value != 'NaN':
                        val_tag.add_record(int(step), float(value))

    cmd = "rm -rf %s && cp -r %s %s" % (logdir_des, logdir, logdir_des)
    os.system(cmd)


def get_all_result():
    """get models and frame performance"""
    get_result("models_per")
    get_result("frame_per")

