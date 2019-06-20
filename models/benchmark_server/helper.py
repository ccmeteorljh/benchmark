#!/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python
"""
test file
"""
import os
import sys
import logging
import time
import datetime
import django
import conf.base_conf as conf
sys.path.append(os.path.abspath(os.path.join(conf.ROOT_PATH, "models")))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "benchmark_server.settings")
django.setup()

from benchmark_server import benchmark_models as bm

def get_frame_latest_version(frame_id):
    """
    get the current frame latest version in database
    :return:
    """
    pv = bm.Image.objects.filter(frame_id=frame_id).order_by('-create_time')[0]
    return pv


def get_cluster_job_info(job_name, list):
    """
    get the job info
    :return:
    """
    if job_name:
        pcjs = bm.Job.objects.filter(job_name='%s' % job_name)
    else:
        pcjs = bm.Job.objects.all()
    pcjs = pcjs.filter(status__in=list)
    pcjs = pcjs.order_by('-create_time')
    return pcjs


def get_final_job_with_no_extractlog():
    """
    condition = {"log_extracted": ["=", "no"], "status": ["in", ("success", "fail")]}
    filters = ["cloud_job_id", "model", "paddle_version", "job_type",
               "run_rpc_type", "run_machine_tpye", "run_batch_size"]
    extract_jobs = build_in.get_jobs_with_conditions(conn, cur, False, filters, condition)
    :return:
    """
    update_final_job_logstatus()
    list = ["success", "fail"]
    pcjs = bm.Job.objects.filter(log_extracted='no')
    pcjs = pcjs.filter(status__in=list)
    pcjs = pcjs.order_by('create_time')
    return pcjs


def update_final_job_logstatus():
    """
    set log_extracted is fail where job's status is in [killled, deleted]
    :return:
    """
    list = ["deleted", "killed"]
    pcjs = bm.Job.objects.filter(log_extracted='no')
    pcjs = pcjs.filter(status__in=list)
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for job in pcjs:
        bm.Job.objects.filter(job_id=job.job_id).update(
            log_extracted='fail')
        bm.Job.objects.filter(job_id=job.job_id).update(
            update_time=dt)


def insert_job(job_instance):
    """ insert the job info to the table named job by django
    """
    if job_instance.conf["image_id"] == "latest":
        image_id = get_frame_latest_version(job_instance.conf["frame_id"]).image_id
    else:
        image_id = job_instance.conf["image_id"]
    pcj = bm.Job()
    pcj.job_name = job_instance.conf["body"]["jobName"]
    pcj.cluster_job_id = job_instance.conf["cluster_job_id"]
    pcj.cluster_type_id = job_instance.conf["cluster_type_id"]
    pcj.cluster_conf = job_instance.conf["body"]["clusterConf"]

    pcj.model_name = job_instance.conf["model"]
    pcj.report_index = job_instance.conf["report_index"]

    pcj.repo_address = job_instance.conf["repo_address"]
    pcj.code_branch = job_instance.conf["code_branch"]
    pcj.job_type = job_instance.conf["job_type"]

    pcj.run_rpc_type = job_instance.conf["run_rpc_type"]
    pcj.run_machine_type = job_instance.conf["run_machine_tpye"]
    pcj.batch_size = job_instance.conf["batch_size"]
    pcj.frame_id = job_instance.conf["frame_id"]
    pcj.image_id = image_id
    pcj.cuda_version = job_instance.conf["cuda_version"]
    pcj.cudnn_version = job_instance.conf["cudnn_version"]
    pcj.run_cmd = job_instance.conf["run_cmd"]
    pcj.eval_cmd = job_instance.conf["eval_cmd"]
    pcj.infer_cmd = job_instance.conf["infer_cmd"]

    pcj.submit_period = job_instance.conf["ploy"].submit_period
    pcj.check_period = job_instance.conf["ploy"].check_period
    pcj.statistics_unit = job_instance.conf["ploy"].statistics_unit

    pcj.status = "submit"
    pcj.save()


def insert_result(job_info, job_result, log_dict):
    """
    insert job result to db
    :param job_info:
    :param job_result:
            {"performance": {"acc1": (step_last, result_avg)
              "acc5": (step_last, result_avg)}}
             or
             {"speed":result_avg}
    :param log_dict:
    :return:
    """
    job_id = job_info.job_id
    model_name = job_info.model_name
    indexs = sorted([int(x) for x in (str(job_info.report_index).split(','))], reverse=True)
    for index in indexs:
        mr = bm.JobResults()
        mr.job_id = job_id
        mr.model_name = model_name
        mr.report_index_id = index
        if index == 0:
            values = {}
            for key in job_result["performance"].keys():
                values[key] = job_result["performance"][key][1]
            mr.report_result = values
            mr.result_log = log_dict
        elif index == 1:
            mr.report_result = job_result["speed"]
        elif index == 2:
            mr.report_result = job_result["gpu_train_mem_max"]
        elif index == 3:
            mr.report_result = job_result["train_time"]
        elif index == 4:
            mr.report_result = job_result["infer_speed"]
        elif index == 5:
            mr.report_result = job_result["gpu_infer_mem_max"]
        else:
            logging.error("error!")
        mr.save()


if __name__ == "__main__":
    print get_cluster_job_info("dddd", ['success', 'fail', 'killed', 'deleted'])
    get_final_job_with_no_extractlog()
