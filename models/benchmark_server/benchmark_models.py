#!/usr/bin/env python
# -*- coding: utf-8 -*-
#======================================================================
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
#======================================================================

"""
@Desc: benchmark_models module
@File: benchmark_models.py
@Author: liangjinhua
@Date: 2018/12/17 11:09
"""

from django.db import models
from django.utils import timezone


class JobStatus(object):
    """
    JobStatus类
    INIT:初始化
    PEDDING:提交未运行
    RUNNING:运行中
    SUCCESS:完成
    FAIL:失败
    """
    SUBMIT = "submit"
    SCHEDULE = "schedule"
    QUEQUE= "queue"
    RUNNING = "running"
    KILLING = "killing"
    KILLED = "killed"
    SUCCESS = "success"
    FAIL = "fail"
    DELETED = "deleted"
    VALUES_TO_NAMES = {
        0: SUBMIT,
        1: SCHEDULE,
        2: QUEQUE,
        3: RUNNING,
        4: KILLING,
        5: KILLED,
        6: SUCCESS,
        7: FAIL,
        8: DELETED
    }


class RunMachineType(object):
    """
    模型训练时试用机器类型和规模
    ONE_CPU:单机单CPU
    MULTI_CPU:单机多CPU(16)
    MULTI_MACHINE_ONE_CPU:多机单CPU(2ps4trainer)
    MULTI_MACHINE_MULTI_CPU:多机多CPU(2ps4trainer 16)
    ONE_GPU:单机单GPU
    FOUR_GPU:单机多GPU(4)
    MULTI_GPU:单机多GPU(8)
    MULTI_MACHINE_ONE_GPU:多机单GPU(2ps4trainer)
    MULTI_MACHINE_MULTI_GPU:多机多GPU(2ps4trainer)
    SPECIAL: 用户自己指定节点数目，如：ctr 20ps,20trainer
    """
    ONE_CPU = "ONE_CPU"
    MULTI_CPU = "MULTI_CPU"
    MULTI_MACHINE_ONE_CPU = "MULTI_MACHINE_ONE_CPU"
    MULTI_MACHINE_MULTI_CPU = "MULTI_MACHINE_MULTI_CPU"
    ONE_GPU = "ONE_GPU"
    FOUR_GPU = "FOUR_GPU"
    MULTI_GPU = "MULTI_GPU"
    MULTI_MACHINE_ONE_GPU = "MULTI_MACHINE_ONE_GPU"
    MULTI_MACHINE_MULTI_GPU = "MULTI_MACHINE_MULTI_GPU"
    SPECIAL = "SPECIAL"
    MULTI_GPU_MULTI_PROCESS = "MULTI_GPU_MULTI_PROCESS"
    VALUES_TO_NAMES = {
        0: ONE_CPU,
        1: MULTI_CPU,
        2: MULTI_MACHINE_ONE_CPU,
        3: MULTI_MACHINE_MULTI_CPU,
        4: ONE_GPU,
        5: FOUR_GPU,
        6: MULTI_GPU,
        7: MULTI_MACHINE_ONE_GPU,
        8: MULTI_MACHINE_MULTI_GPU,
        9: SPECIAL,
        10: MULTI_GPU_MULTI_PROCESS
    }


class RunRpcType(object):
    """
    多机训练时多机通讯类型
    GRPC_SYNC:grpc 同步
    GRPC_ASYNC:grpc 异步
    BRPC_SYNC:brpc 同步
    BRPC_ASYNC:brcp 异步
    NCCL:nccl rdma
    """
    GRPC_SYNC = "GRPC_SYNC"
    GRPC_ASYNC = "GRPC_ASYNC"
    BRPC_SYNC = "BRPC_SYNC"
    BRPC_ASYNC = "BRPC_ASYNC"
    NCCL = "NCCL"
    VALUES_TO_NAMES = {
        0: GRPC_SYNC,
        1: GRPC_ASYNC,
        2: BRPC_SYNC,
        3: BRPC_ASYNC,
        4: NCCL}


class ReportIndex(object):
    """
    模型验证类型
    SPEED:速度
    CONVERGENCE:收敛
    Memory:显存占用
    """
    SPEED = "speedup_ratio"
    PERFORMANCE = "performance"
    Memory = "memory"
    VALUES_TO_NAMES = {
        0: SPEED,
        1: PERFORMANCE,
        2: Memory}


class ClusterType(object):
    """
    集群类型
    local:本地
    paddlecloud:paddlecloud集群
    qianmo:阡陌集群
    """
    Local = "local"
    PaddleCloud = "paddlecloud"
    QianMo = "qianmo"
    VALUES_TO_NAMES = {
        0: Local,
        1: PaddleCloud,
        2: QianMo}


class Direction(models.Model):
    """
        项目方向表,用于表示benchmark所覆盖的项目方向,比如CV是一个方向,
        一个方向包括多种任务,比如图像分类包含resnet50,se-resnext50
    """
    direction_id = models.AutoField(primary_key=True)
    direction_name = models.CharField(max_length=128)
    desc = models.CharField(max_length=256, null=True, blank=True)

    class Meta(object):
        """
        mysql table
        """
        db_table = 'direction'


class Mission(models.Model):
    """
        方向任务表,用于表示benchmark所覆盖的方向任务,比如图像分类是CV方向的其中一个任务,
        一个任务包括多种模型,比如图像分类包含resnet50,se-resnext50
    """
    mission_id = models.AutoField(primary_key=True)
    #任务所属方向
    direction_id = models.SmallIntegerField()
    mission_name = models.CharField(max_length=32, null=True, blank=True)
    desc = models.CharField(max_length=64, null=True, blank=True)

    class Meta(object):
        """
        mysql table
        """
        db_table = 'mission'


class Frame(models.Model):
    """
        框架表，job运行在某种深度学习框架，如paddle，
    """
    PADDLEPADDLE = "paddlepaddle"
    TENSORFLOW = "tensorflow"
    PYTORCH = "pytorch"
    THEANO = "theano"
    CAFFE = "caffe"
    VALUES_TO_NAMES = {
        0: PADDLEPADDLE,
        1: TENSORFLOW,
        2: PYTORCH,
        3: THEANO,
        4: CAFFE
    }
    frame_id = models.AutoField(primary_key=True)
    frame_name = models.CharField(max_length=32, null=True, blank=True)
    desc = models.CharField(max_length=64, null=True, blank=True)
    add_time = models.DateTimeField(auto_now_add=True)
    class Meta(object):
        """
        mysql table
        """
        db_table = 'frame'


class DockerImage(models.Model):
    """
        docker镜像，为本地启动作业所用
    """
    #todo 后续可以设置一个表将镜像名字与cuda版本对应起来
    VALUES_TO_NAMES = {
        "paddlepaddle": "paddlepaddle/paddle:latest-gpu",
        "tensorflow": "tensorflow/tensorflow:latest-gpu",
        "pytorch": "pytorch/pytorch:0.4_cuda9_cudnn7",
        "theano": "theano/theano:latest",
        "caffe": "caffe/caffe:latest"
    }


class JobType(models.Model):
    """
       作业类型表，说明作业是models例行评估，还是rd临时实验，或者benchmark的
    """
    id = models.SmallIntegerField()
    name = models.CharField(max_length=32)
    describe = models.CharField(max_length=64, null=True, blank=True)
    class Meta(object):
        """ mysql table"""
        db_table = 'job_type'


class Image(models.Model):
    """
        镜像表，一个框架对应多种发布镜像，包括版本，编译环境不同
    """
    image_id = models.AutoField(primary_key=True)
    image_name = models.CharField(max_length=64, null=True, blank=True)
    frame_id = models.SmallIntegerField()
    version = models.CharField(max_length=32)
    cuda_version = models.CharField(max_length=16, default="9.0")
    cudnn_version = models.CharField(max_length=16, default="7")
    #和job_type关联
    image_type = models.SmallIntegerField()
    image_commit_id = models.CharField(max_length=64)
    create_time = models.DateTimeField()

    class Meta(object):
        """
        mysql table
        """
        db_table = 'image'


class BenchmarkModel(models.Model):
    """
    模型表，benchmark需要覆盖的模型
    """
    model_id = models.AutoField(primary_key=True)
    #模型所属任务
    mission_id = models.SmallIntegerField()
    model_name = models.CharField(max_length=64)
    model_dataset = models.CharField(max_length=128)
    model_message = models.CharField(max_length=256, null=True, blank=True)
    model_principal = models.CharField(max_length=64, null=True, blank=True)
    #模型开发状态
    model_status = models.SmallIntegerField()

    class Meta(object):
        """
        db_table
        """
        db_table = 'benchmark_model'


class Job(models.Model):
    """
    任务表，一些例行回归的任务或者实验性任务
    """
    job_id = models.AutoField(primary_key=True)
    job_name = models.CharField(max_length=64)
    cluster_job_id = models.CharField(max_length=128, blank=True)
    cluster_type_id = models.SmallIntegerField()
    cluster_conf = models.CharField(max_length=1024, blank=True)

    model_name = models.CharField(max_length=64)
    report_index = models.CharField(max_length=32)
    repo_address = models.CharField(max_length=64, blank=True)
    code_branch = models.CharField(max_length=32, default="develop")
    code_commit_id = models.CharField(max_length=64, default="latest")
    #JobRype 0:models 1:experiment 2:benchmark
    job_type = models.SmallIntegerField()
    #RunRpcType
    run_rpc_type = models.CharField(max_length=32, default="GRPC_SYNC")

    #RunMachineType
    run_machine_type = models.CharField(max_length=32, default="ONE_GPU")
    batch_size = models.IntegerField(blank=True)
    frame_id = models.SmallIntegerField(blank=True)
    image_id = models.SmallIntegerField()
    cuda_version = models.CharField(max_length=16, default="9.0")
    cudnn_version = models.CharField(max_length=16, default="7")

    #v100 or p40
    gpu_type = models.CharField(max_length=32, default="v100")

    #staticgraph or dygraph
    model_implement_type = models.CharField(max_length=32, default="staticgraph")

    #cmd
    run_cmd = models.CharField(max_length=1024, blank=True)
    eval_cmd = models.CharField(max_length=1024, blank=True)
    infer_cmd = models.CharField(max_length=1024, blank=True)

    submit_period = models.SmallIntegerField(blank=True)
    check_period = models.SmallIntegerField(blank=True)
    statistics_unit = models.CharField(max_length=10, blank=True, default="mins")

    create_time = models.DateTimeField(auto_now_add=True)
    # update_time = models.DateTimeField(auto_now=True)
    update_time = models.DateTimeField(default=timezone.now)
    #JobStatus
    status = models.CharField(max_length=20, default="submit")
    #log_extracted
    log_extracted = models.CharField(max_length=20, default="no")
    class Meta(object):
        """
        db_table
        """
        db_table = 'job'


class JobResults(models.Model):
    """
    模型benchmark结果表
    """
    result_id = models.AutoField(primary_key=True)
    job_id = models.IntegerField()
    model_name = models.CharField(max_length=32, blank=True)
    report_index_id = models.SmallIntegerField()
    report_result = models.CharField(max_length=64)
    result_log = models.TextField(max_length=8192)
    train_log_path = models.CharField(max_length=128)
    #result_log = models.CharField(max_length=8192, blank=True)
    class Meta(object):
        """
        db_table
        """
        db_table = 'job_results'


class PaddleVersion(models.Model):
    """
    Paddle 的版本管理表
    """
    id = models.IntegerField
    version = models.CharField(max_length=16, blank=True)
    whl_name = models.CharField(max_length=64, blank=True)
    description = models.CharField(max_length=64, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    class Meta(object):
        """
        db_table
        """
        db_table = 'paddle_version'


class ViewVisualDLLog(models.Model):
    """
    visualdl log view table
    """
    job_id = models.IntegerField()
    job_name = models.CharField(max_length=32)
    cluster_type_id = models.SmallIntegerField()

    model_name = models.CharField(max_length=64)
    report_index_id = models.SmallIntegerField()
    # JobRype 0:benchmark 1:experiment
    job_type = models.SmallIntegerField()
    # RunRpcType
    run_rpc_type = models.CharField(max_length=32, default="GRPC_SYNC")
    # RunMachineType
    run_machine_type = models.CharField(max_length=32, default="ONE_GPU")
    frame_name = models.CharField(max_length=32)
    frame_version = models.CharField(max_length=32)
    result_log = models.TextField(max_length=8192)
    class Meta(object):
        """
        db_table
        """
        db_table = 'visualDL_log'


class ViewJobResult(models.Model):
    """
    job_result view table
    """
    mission_name = models.CharField(max_length=32, null=True, blank=True)
    result_id = models.AutoField(primary_key=True)
    job_id =  models.IntegerField()
    job_name = models.CharField(max_length=64)
    cuda_version = models.CharField(max_length=16, default="9.0")
    cudnn_version = models.CharField(max_length=16, default="7")
    # v100 or p40
    gpu_type = models.CharField(max_length=32, default="v100")

    # staticgraph or dygraph
    model_implement_type = models.CharField(max_length=32, default="staticgraph")

    job_type = models.SmallIntegerField()
    code_commit_id = models.CharField(max_length=64)
    image_commit_id = models.CharField(max_length=64)
    model_name = models.CharField(max_length=64)
    version = models.CharField(max_length=32)
    frame_name = models.CharField(max_length=32)
    run_rpc_type = models.CharField(max_length=32, default="GRPC_SYNC")
    # RunMachineType
    run_machine_type = models.CharField(max_length=32, default="ONE_GPU")
    batch_size = models.CharField(max_length=32, blank=True)
    report_index_id = models.SmallIntegerField()
    report_result = models.CharField(max_length=64)
    statistics_unit = models.CharField(max_length=32)
    train_log_path = models.CharField(max_length=128)

    class Meta(object):
        """
        db_table
        """
        db_table = 'job_result'
