#!/usr/bin/env python
# -*- coding: utf-8 -*-
#======================================================================
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
#======================================================================

"""
@Desc: log_extract_re module
@File: log_extract_re.py
@Author: liangjinhua
@Date: 2018/12/19 12:59
"""
import conf.base_conf as conf
import requests
import libs.job_scheduler.log_extract_re as ler
import numpy as np
from requests.adapters import HTTPAdapter
import os
import sys
import ast
import logging
import time
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from benchmark_server import benchmark_models as bm

def get_log_file(frame, image_version, model, file_name):
    """
    download files from http server for logs
    :param frame: 框架名字
    :param model: 模型名字
    :param image_version: 镜像版本号
    :return:
    """
    url = "%s/%s/%s/%s/%s" % (conf.log_host, frame, image_version, model, file_name)
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=3))
    s.mount('https://', HTTPAdapter(max_retries=3))

    file = s.get(url)
    s.close()

    return file


class LogExtractRe(object):
    """
    记录作业日志文件的提取规则
    """

    @classmethod
    def file_parser(cls, job_info, file, job_re):
        """
        parse log file
        :param job_info:
        :param file:
        :return:{"performance":
                    {"acc1": [(step1, values1), (step2, values2),..],
                    "acc5": [(step1, values1), (step2, values2),..]}}
                 or
                 {"speed": [values1, values2,..]}
                 or
                 {
                 "performance": {"acc1": [(step1, values1), (step2, values2),..],
                                "acc5": [(step1, values1), (step2, values2),..]},
                "speed": [values1, values2,..]
                }
        """
        #result_dict performance eg:
        # {"performance": {"acc1": [(step1, values1), (step2, values2),..]
        #                  "acc5": [(step1, values1), (step2, values2),..]}}
        #result_dict speed eg: {"speed": [values1, values2,..]}
        report_index = [int(x) for x in (str(job_info.report_index).split(','))]
        result_dict = {} #存储所有结果的字典
        return_dict = {} #存储最终一个值结果的字典
        step_current = {}
        model = job_info.model_name

        def get_performance():
            """获取收敛数据"""
            perf_file = file.split('myjob_train_end_time')[0]
            result_dict["performance"] = {}
            return_dict["performance"] = {}
            job_type_re = job_re[model]["performance"]
            re_indicants = [re["indicant"] for re in job_type_re]
            for indicant in re_indicants:
                result_dict["performance"][indicant] = []
                step_current[indicant] = 0

            for line in perf_file.split('\n'):
                line = '"%s"' % line
                for re_element in job_type_re:
                    if isinstance(re_element["keyword"], str) and \
                                    re_element["keyword"] not in line:
                        continue

                    elif not isinstance(re_element["keyword"], str) and \
                               not re_element["keyword"].findall(line):
                        continue

                    try:
                        step_current[re_element["indicant"]] += 1
                        re_result = re_element["result"]
                        result = float(eval(line + '.' + re_result))
                        step = int(eval(line + '.' + re_element["step"])) \
                            if re_element["step"] != 'index'  \
                            else step_current[re_element["indicant"]]
                        result_dict["performance"][re_element["indicant"]].append((step, result))
                    except Exception as ee:
                        logging.info("error {} {}".format(ee, line))

        def get_train_speed():
            """获取训练速度数据"""
            ts_file = file.split('myjob_train_end_time')[0]
            job_type_re = job_re[model]["speedup_ratio"]
            result_dict["speed"] = []
            for line in ts_file.split('\n'):
                if job_type_re["keyword"] not in line:
                    continue
                line = '"%s"' % line
                re_result = job_type_re["result"]
                print(line + '.' + re_result)
                try:
                    result = float(eval(line + '.' + re_result))
                    result_dict["speed"].append(result)
                    if len(result_dict["speed"]) == 5:
                        break
                except Exception as ee:
                    logging.error("model is: {},error {} {}".format(model, ee, line))

        def get_train_memory():
            """获取train显存占用数据"""
            gpu_mem_content = file.content.split('used_gpu_memory [MiB]\n')[1]
            gpu_mem_list = []
            if gpu_mem_content:
                for line in gpu_mem_content.split("\n"):
                    if "MiB" in line:
                        gpu_mem_list.append(int(line.split()[0]))
            result_dict["gpu_train_mem_max"] = [max(gpu_mem_list)]

        def get_total_train_time():
            """获取总训练时间"""
            if int(job_info.cluster_type_id) != 0:
                #todo 其他集群类型(如paddlecloud...)后续补充
                pass
            else:
                start_time = file.content.split(
                                    'myjob_start_time=')[1].split('\n')[0]
                train_end_time = file.content.split(
                                    'myjob_train_end_time=')[1].split('\n')[0]
                myjob_st = time.mktime(time.strptime(start_time, '%Y%m%d-%H%M%S'))
                myjob_et = time.mktime(time.strptime(train_end_time, '%Y%m%d-%H%M%S'))
                #单位为分钟
                result_dict["train_time"] = [(myjob_et - myjob_st) / 60.0]

        def get_infer_speed():
            """获取infer速度数据"""
            infer_file = file.split('begin inference cmd with gpu\n')[1]
            infer_file = infer_file.split('myjob_gpu_infer_end_time')[0]
            job_type_re = job_re[model]["infer_speed"]
            result_dict["infer_speed"] = []
            for line in infer_file.split('\n'):
                if job_type_re["keyword"] not in line:
                    continue
                line = '"%s"' % line
                re_result = job_type_re["result"]
                print(line + '.' + re_result)
                try:
                    result = float(eval(line + '.' + re_result))
                    result_dict["infer_speed"].append(result)
                    if len(result_dict["infer_speed"]) == 5:
                        break
                except Exception as ee:
                    logging.error("infer_speed extract error!, "
                                  "model is: {},error {} {}".format(model, ee, line))

        def get_infer_memory():
            """获取infer显存占用数据"""
            gpu_mem_content = file.content.split('used_gpu_memory [MiB]\n')[-1]
            gpu_mem_list = []
            if gpu_mem_content:
                for line in gpu_mem_content.split("\n"):
                    if "MiB" in line:
                        gpu_mem_list.append(int(line.split()[0]))
            result_dict["gpu_infer_mem_max"] = [max(gpu_mem_list)]

        #todo 根据报表id，映射到具体的方法，后续可以设置成自动配置
        report_index_dict = {0: get_performance,
                             1: get_train_speed,
                             2: get_train_memory,
                             3: get_total_train_time,
                             4: get_infer_speed,
                             5: get_infer_memory}

        for index in report_index:
            report_index_dict[index]()

        # check and return data
        for key in result_dict.keys():
            if key == "performance":
                for pk in result_dict[key]:
                    if not result_dict[key][pk]:
                        logging.error("{}.{}.{} is null".format(model, key, pk))
                        return False, False
                    else:
                        return_dict[key][pk] = result_dict[key][pk][-1]
            elif not result_dict[key]:
                logging.error("{}.{} is null".format(model, key))
                return False, False
            else:
                return_dict[key] = result_dict[key][-1]
        return return_dict, result_dict

    @classmethod
    def compute_result(cls, job_info, result_list, job_re):
        """
        计算多个日志文件的平均值
        :param job_info:
        :param result_list:
            eg: [{"performance": {"acc1": (step_n, result_n)
                "acc5": (step_n, result_n)}},
                ...
            ]
            or
            [{"speed":result},..]
        :return:
             {"performance": {"acc1": (step_n, result_n)
              "acc5": (step_n, result_n)}}
             or
             {"speed":result}
             or
             {"gpu_mem_max"：result}
             or
             {"performance":{"acc1": (step_n, result_n),
              "acc5": (step_n, result_n)},
              "speed":result,
              "gpu_mem_max"：result}
        """
        result = {}
        def compute_performance():
            """计算多个trainer平均收敛数据"""
            result["performance"] = {}
            indicants = result_list[0]["performance"].keys()
            for indicant in indicants:
                step = result_list[0]["performance"][indicant][0]
                performance = [file_result["performance"][indicant][1] for file_result in result_list]
                performance_np = np.array(performance)
                result["performance"][indicant] = (step, "%.5f" % performance_np.mean())

        def compute_train_speed():
            """计算多个trainer的平均速度"""
            speed_list = [file_result["speed"] for file_result in result_list]
            if 'else' in job_re[job_info.model_name]['speedup_ratio']:
                if job_re[job_info.model_name]['speedup_ratio']['else'] == 'reciprocal':
                    speed_list = [1.0 / speed for speed in speed_list]

            result_np = np.array(speed_list)
            method = job_re[job_info.model_name]['speedup_ratio']['method'] if 'method' in \
                        job_re[job_info.model_name]['speedup_ratio'] else 'sum'
            if method == 'mean':
                result["speed"] = "%.5f" % result_np.mean()
            elif method == 'sum':
                result["speed"] = "%.5f" % result_np.sum()
            else:
                pass

        def compute_train_memory():
            """计算多个trainer平均内存数据"""
            result_np = np.array([file_result["gpu_train_mem_max"] for file_result in result_list])
            result["gpu_train_mem_max"] = "%.5f" % result_np.mean()

        def compute_total_train_time():
            """计算多个trainer的最大训练时间"""
            result_np = np.array([file_result["train_time"] for file_result in result_list])
            result["train_time"] = "%.5f" % result_np.max()

        def compute_infer_speed():
            """计算多个trainer的平均infer速度"""
            speed_list = [file_result["infer_speed"] for file_result in result_list]
            if 'else' in job_re[job_info.model_name]['infer_speed']:
                if job_re[job_info.model_name]['infer_speed']['else'] == 'reciprocal':
                    speed_list = [1.0 / speed for speed in speed_list]

            result_np = np.array(speed_list)
            method = job_re[job_info.model_name]['infer_speed']['method'] if 'method' in \
                        job_re[job_info.model_name]['infer_speed'] else 'sum'
            if method == 'mean':
                result["infer_speed"] = "%.5f" % result_np.mean()
            elif method == 'sum':
                result["infer_speed"] = "%.5f" % result_np.sum()
            else:
                pass

        def compute_infer_memory():
            """计算多个infer平均内存数据"""
            result_np = np.array([file_result["gpu_infer_mem_max"] for file_result in result_list])
            result["gpu_infer_mem_max"] = "%.5f" % result_np.mean()

        # todo 根据报表id，映射到具体的方法，后续可以设置成自动配置
        report_index_dict = {0: compute_performance,
                             1: compute_train_speed,
                             2: compute_train_memory,
                             3: compute_total_train_time,
                             4: compute_infer_speed,
                             5: compute_infer_memory}

        report_index = [int(x) for x in (str(job_info.report_index).split(','))]
        for index in report_index:
            report_index_dict[index]()
        return result

    @classmethod
    def log_extract(cls, job_info):
        """
        extract job
        :param job:
            [cluster_job_id, model, paddle_version, job_type, run_env, batch_size]
        :return:
            {"acc1": (step_last, result_avg)
              "acc5": (step_last, result_avg)}
             or
             {"speed":result_avg}
        """
        cluster_type_id = int(job_info.cluster_type_id)
        cluster_job_id = str(job_info.job_id) if cluster_type_id == 0 \
            else job_info.cluster_job_id
        model = job_info.model_name
        print("cluster_job_id is:{} ".format(cluster_job_id))
        image_version = bm.Image.objects.filter(image_id=int(job_info.image_id))[0].version
        cluster_conf = ast.literal_eval(job_info.cluster_conf)
        frame = bm.Frame.VALUES_TO_NAMES[int(job_info.frame_id)]
        job_re = ler.frame2re[frame]

        if model not in job_re:
            logging.error("please add models %s log re" % model)
            return
        logging.info('--------extracting job:{}'.format(job_info.cluster_job_id))
        trainers_result = []

        trainers = 1
        if cluster_type_id == 0:
            #目前local集群仅仅支持单机模式
            trainers = 1
        elif cluster_job_id == 1:
            if cluster_conf["clusterType"] == 'MPI':
                trainers = int(cluster_conf["mpiNodes"])
            else:
                trainers = 1 if int(cluster_conf["k8sIsLocal"]) \
                    else int(cluster_conf["k8sTrainersCount"])
        else:
            pass

        model_job_name = model + '_' + cluster_job_id
        for index in range(trainers):
            file_name = model_job_name + '_' + str(index)
            file = get_log_file(frame, image_version, model, file_name)

            if file.status_code == 200:
                return_dict, result_dict = cls.file_parser(job_info, file, job_re)

                if not return_dict:
                    return False, False
                else:
                    trainers_result.append(return_dict)

        if len(trainers_result) != trainers:
            #raise myexception.ResponseError("Files {}/{}/{} not "
            #    "yet produce".format(paddle_version, model, model_job_name))
            logging.info("Job status:{}, Files {}/{}/{}/{} less then "
                "trainers".format(job_info.status, frame, image_version, model, model_job_name))
            return False, False
        else:
            result = cls.compute_result(job_info, trainers_result, job_re)
            report_index = str(job_info.report_index).split(',')
            #为了用visualdl画图，把非收敛性数据删掉
            vd_dict = {}
            if '0' in report_index:
                vd_dict = result_dict["performance"]
            return result, vd_dict


if __name__ == '__main__':
    job_info = bm.Job.objects.filter(job_id=56)
    LogExtractRe.log_extract(job_info[0])
