#!/usr/bin/env python
# -*- coding: utf-8 -*-
#======================================================================
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
#======================================================================

"""
@Desc: db module
@File: db.py
@Author: liangjinhua
@Date: 2019/5/5 19:30
"""
import argparse
import MySQLdb
import os
import uuid

import time

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    "--log_path",
    type=str,
    default='/home/crim/benchmark/logs',
    help="The cases files. (default: %(default)d)")

parser.add_argument(
    "--code_commit_id",
    type=str,
    default='',
    help="The benchmark repo commit id")

parser.add_argument(
    "--image_commit_id",
    type=str,
    default='',
    help="The benchmark repo commit id")

parser.add_argument(
    "--cuda_version",
    type=str,
    default='9.0',
    help="The benchmark run on cuda version")

parser.add_argument(
    "--cudnn_version",
    type=str,
    default='7',
    help="The benchmark run on cudnn version")

parser.add_argument(
    "--paddle_version",
    type=str,
    default='test',
    help="The benchmark run on paddle whl version")

class BaseError(Exception):
    """
    base error class
    """
    def __init__(self, error_text):
        self.error_text = error_text

    def __str__(self):
        return self.error_text


class DBError(BaseError):
    """
    database operation error class
    """
    def __init__(self, error_text):
        super(DBError, self).__init__(error_text)


class ParseFileError(BaseError):
    """
    Parse log_file error class
    """
    def __init__(self, error_text):
        super(ParseFileError, self).__init__(error_text)


class CommonDao(object):
    """
    定义数据库的常用操作
    """
    @staticmethod
    def get_conn(ksargs):
        """ 连接数据库 """
        host = ksargs['host'] if 'host' in ksargs else ''
        user = ksargs['user'] if 'user' in ksargs else ''
        port = ksargs['port'] if 'port' in ksargs else ''
        passwd = ksargs['passwd'] if 'passwd' in ksargs else ''
        db = ksargs['db'] if 'db' in ksargs else ''
        charset = ksargs['charset'] if 'charset' in ksargs else ''
        try:
            conn = MySQLdb.connect(host=host, user=user, passwd=passwd,
                               db=db, port=port, charset=charset)
            cur = conn.cursor()

        except MySQLdb.Error as e:
            raise DBError('%s%s' % (e.message, 'ConnectError!'))
        return conn, cur

    @staticmethod
    def exe_update(conn, cur, sql):
        """ 更新语句，可执行Update，Insert语句 """
        try:
            sta = cur.execute(sql)
            conn.commit()
        except MySQLdb.Error as e:
            conn.rollback()
            raise DBError('%s%s' % (e.message, 'Update error!'))
        return sta

    @staticmethod
    def exe_delete(conn, cur, sql):
        """ 删除语句 """
        try:
            sta = cur.execute(sql)
            conn.commit()
        except MySQLdb.Error as e:
            conn.rollback()
            raise DBError('%s%s' % (e.message, "Delete error!"))
        return sta

    @staticmethod
    def exe_query(cur, sql):
        """ 查询语句 """
        try:
            cur.execute(sql)
            result = cur.fetchall()
        except MySQLdb.Error as e:
            raise DBError('%s%s' % (e.message, "Select error!"))
        return result

    @staticmethod
    def conn_close(conn, cur):
        """ 关闭所有连接 """
        try:
            cur.close()
            conn.close()
        except MySQLdb.Error as e:
            raise DBError('%s%s' % (e.message, "Close error!"))


def load_folder_files(folder_path, recursive=True):
    """
    :param folder_path: specified folder path to load
    :param recursive: if True, will load files recursively
    :return:
    """
    if isinstance(folder_path, (list, set)):
        files = []
        for path in set(folder_path):
            files.extend(load_folder_files(path, recursive))

        return files

    if not os.path.exists(folder_path):
        return []

    file_list = []

    for dirpath, dirnames, filenames in os.walk(folder_path):
        filenames_list = []

        for filename in filenames:
            filenames_list.append(filename)

        for filename in filenames_list:
            file_path = os.path.join(dirpath, filename)
            file_list.append(file_path)

        if not recursive:
            break

    return file_list


def get_image_id(image_commit_id, cur):
    cur_time = time.time()
    ct = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(cur_time))
    # paddle_version = time.strftime('%Y%m%d%H%M%S',
    #                 time.localtime(cur_time)) + '.post{}7'.format(args.cuda_version.split('`,.')[0])
    insert_sql = "insert into image(`frame_id`, `version`, `cuda_version `cudnn_version`, " \
                 "`image_commit_id`, `image_type`, `create_time`) " \
                 "values('0', '{}', '{}', '{}', '{}', 2, '{}')".format(
                  args.paddle_version, args.cuda_version, args.cudnn_version, image_commit_id, ct)
    CommonDao.exe_update(conn, cur, insert_sql)

    select_sql = "select image_id from image where image_commit_id='{}'" \
                 " ORDER BY create_time DESC LIMIT 1".format(image_commit_id)
    result = CommonDao.exe_query(cur,select_sql)
    if result:
        return result[0][0]


def get_job_id(cluster_job_id, cur):
    sql = "select job_id from job where cluster_job_id='{}'".format(cluster_job_id)
    result = CommonDao.exe_query(cur, sql)
    if result:
        return result[0][0]


def parse_logs(args, conn, cur):
    image_id = get_image_id(args.image_commit_id, cur)
    file_list = load_folder_files(os.path.join(args.log_path, "index"))
    dict_run_machine_type = {
        '1gpus' : 'ONE_GPU',
        '4gpus' : 'FOUR_GPU',
        '8gpus' : 'MULTI_GPU'
    }
    cv_models = ['DeepLab_V3+', 'CycleGAN', 'mask_rcnn', 'SE-ResNeXt50', 'yolov3']
    nlp_models = ['bert', 'paddingrnn_large', 'paddingrnn_small', 'transformer']
    rl_models = ['ddpg_deep_explore']

    for file in file_list:
        # file_name like CycleGAN_mem_1gpus or ddpg_deep_explore_speed_1gpus
        cluster_job_id = uuid.uuid1()
        file_name = file.split('/')[-1]
        model_name = '_'.join(file_name.split('_')[:-2])
        key_word = "FPS:" if model_name in cv_models else 'Avg:'
        job_name = 'pb_' + model_name
        task_index = file_name.split('_')[-2]
        if task_index == 'speed':
            report_index = 1
        elif task_index == 'mem':
            report_index = 2
        else:
            report_index = 6

        run_machine_type = dict_run_machine_type[file_name.split('_')[-1]]
        job_sql = "insert into job(`job_name`, `cluster_job_id`, `cluster_type_id`, " \
                  "`model_name`, `report_index`, `code_branch`, `code_commit_id`, " \
                  "`job_type`, `run_machine_type`, `frame_id`, `image_id`, " \
                  "`cuda_version`, `cudnn_version`, `log_extracted`)" \
                  "values('{}', '{}', '{}', '{}', '{}', '{}', '{}', " \
                  "'{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(job_name,
                   cluster_job_id, 0, model_name, report_index, "master",
                   args.code_commit_id, 2, run_machine_type, 0, image_id,
                   args.cuda_version, args.cudnn_version, 'yes')

        train_log_name = "{}_{}_{}_{}".format(model_name, "train",
                                              task_index, file_name.split('_')[-1][0])
        train_log_path = os.path.join(os.path.basename(args.log_path),
                                      "train_log", train_log_name)
        CommonDao.exe_update(conn, cur, job_sql)
        job_id = get_job_id(cluster_job_id, cur)
        result = ""
        with open(file, 'r+') as file_obj:
            file_lines = file_obj.readlines()
            try:
                if report_index == 2:
                    result = file_lines[-1].split()[-1]
                elif report_index == 1:
                    lines = file_lines[-10:-1]
                    for line in lines:
                        if key_word in line:
                            result = line.split(':')[1].split(' ')[1]
                else:
                    value = file_lines[-1].split()[-1]
                    result = int(value) if str.isdigit(value) else 0

                result_sql = "insert into job_results(`job_id`, `model_name`, " \
                             "`report_index_id`, `report_result`, `train_log_path`)" \
                             "values('{}', '{}', '{}', '{}', '{}')".format(job_id,
                                model_name, report_index, result, train_log_path)

                print result_sql
                CommonDao.exe_update(conn, cur, result_sql)
            except ParseFileError as pfe:
                print pfe


if __name__ == '__main__':
    args = parser.parse_args()

    DATABASE = {
        'host': '10.62.51.15',
        'port': 8806,
        'user': 'root',
        'passwd': '',
        'db': 'paddle_benchmark',
        'charset': 'utf8'
    }
    conn, cur = CommonDao.get_conn(DATABASE)
    parse_logs(args, conn, cur)
    CommonDao.conn_close(conn, cur)