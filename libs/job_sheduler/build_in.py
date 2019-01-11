import datetime
import logging

import os
import sys
import json

from libs.common import utils
from libs.common import exception
import libs.local.docker_utils as docker_utils
import libs.paddlecloud.padddlecloud_api as api
import models.benchmark_server.helper as helper
from benchmark_server import benchmark_models as bm


def load_jobs_by_path(path, args):
    """ load jobs from file path
    @param path: path could be in several type
        - absolute/relative file path
        - absolute/relative folder path
        - list/set container with file(s) and/or folder(s)
    @return testcase sets list, each testset is corresponding to a file
        [
            testset_dict_1,
            testset_dict_2
        ]
    """
    if isinstance(path, (list, set)):
        testsets = []

        for file_path in set(path):
            testset = load_jobs_by_path(file_path, args)
            if not testset:
                continue
            testsets.extend(testset)

        return testsets

    if not os.path.isabs(path):
        path = os.path.join(os.getcwd(), path)

    if os.path.isdir(path):
        files_list = utils.load_folder_files(path)
        jobs_list = load_jobs_by_path(files_list, args)

    elif os.path.isfile(path):
        try:
            jobs_list = utils.load_file(path)
        except exception.FileFormatError:
            jobs_list = []
        if jobs_list:
            for job in jobs_list:
                #默认执行框架为paddlepaddle
                if 'frame_id' not in job["test"]:
                    job["test"]["frame_id"] = args.frame_id
                else:
                    job["test"]["frame_id"] = int(args.frame_id)

                #默认运行在paddlecloud上
                if 'cluster_type_id' not in job["test"]:
                    job["test"]["cluster_type_id"] = 1
                else:
                    job["test"]["cluster_type_id"] = int(job["test"]["cluster_type_id"])

    else:
        logging.error(u"file not found: {}".format(path))
        jobs_list = []

    #print jobs_list
    return jobs_list


def construct_job_result_dict(job_info, result, log_dict):
    """
    :param job_info: django models model_result
    :param result:
            {"acc1": (step_last, result_avg)
              "acc5": (step_last, result_avg)}
             or
             {"speed":result_avg}
    :return:
    """
    result_dict = {
        "job_id": job_info.job_id,
        "model_name": job_info.model_name,
        "report_index_results": {}
    }

    if result:
        report_index_results = {}
        indexs = sorted([int(x) for x in (str(job_info.report_index).split(','))],
                              reverse=True)
        for index in indexs:
            if index == 0:
                report_index_results[0] = {}
                for key in result.keys():
                    report_index_results[0][key] = result[key][1]
                report_index_results[0]["visualdl_log"] = log_dict
            elif index == 1:
                report_index_results[1] = result["speed"]
                result.pop("speed")
            elif index == 2:
                report_index_results[2] = result["gpu_mem_max"]
                result.pop("gpu_mem_max")
            else:
                logging.error("")

        result_dict["report_index_results"] = report_index_results
    return result_dict


def update_job_status():
    """
    更新作业信息
    :return:
    """
    status_list = ['running', 'submit', 'schedule', 'killing', 'queue']
    middle_status_list = helper.get_cluster_job_info('', status_list)
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for job_info in middle_status_list:
        #local job 只检查处于running中间状态的作业，
        # submit状态不检查等待启动，成功则转到running，失败就是fail
        job_status = "submit"
        if int(job_info.cluster_type_id) == 0 and job_info.status == "running":
            #update local job's status
            job_status = docker_utils.check_container_status(str(job_info.cluster_job_id))
        elif int(job_info.cluster_type_id) == 1:
            # update paddlecloud job's status
            job_status = api.get_job_status(job_info.cluster_job_id)
        elif int(job_info.cluster_type_id) == 2:
            # todo
            # update qianmo job's status
            pass
        else:
            logging.error("not support {} cluster_tpye".format(job_info.cluster_type_id))

        if job_status != job_info.status:
            bm.Job.objects.filter(job_id=job_info.job_id).update(status=job_status)
            bm.Job.objects.filter(job_id=job_info.job_id).update(update_time=dt)
