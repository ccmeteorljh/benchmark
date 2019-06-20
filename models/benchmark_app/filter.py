#!/usr/bin/env python
# -*- coding: utf-8 -*-
#======================================================================
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
#======================================================================

"""
@Desc: model_filter module
@File: model_filter.py
@Author: liangjinhua
@Date: 2019/1/30 19:45
"""
from django.db.models import Q, Min, Max
from django_filters import rest_framework as filters
from rest_framework.parsers import JSONParser
from benchmark_server import benchmark_models as bm
from benchmark_server.benchmark_models import Job
from benchmark_server.benchmark_models import ViewJobResult
from benchmark_server.benchmark_models import BenchmarkModel
from benchmark_server.benchmark_models import Image

class JobFilter(filters.FilterSet):
    """filter of job """

    # sn = filters.CharFilter(name='sn', method='sn_filter', lookup_expr='icontains')
    # address = filters.CharFilter(name='address', lookup_expr='icontains')
    # memo = filters.CharFilter(name='memo', lookup_expr='icontains')
    create_time = filters.DateFilter(name='registered_time', lookup_expr='gte')
    update_time = filters.DateFilter(name='registered_time', lookup_expr='lte')
    frame_id = filters.NumberFilter(name='frame_id', lookup_expr='exact')
    model_name = filters.CharFilter(name='model_name', lookup_expr='icontains')

    class Meta(object):
        """
        db_table
        """
        model = Job
        #fields = '__all__'
        fields = ['job_id', 'frame_id', 'model_name', 'image_id', 'job_type']

    @staticmethod
    def sn_filter(queryset, name, value):
        """
        自定义过滤方法，sn可以包含逗号，如'2016,2017'，进行or查询
        查询sn中包含'2016'或'2017'的所有集控

        允许'2016,2017' , '2016,' , '2016, 2017' , '2016 ,2017'等形式
        """
        value = value.replace(' ', '')
        Q_sn = Q()
        for sn in value.split(','):
            if sn:
                Q_sn.add(Q(**{'sn__icontains': sn}), Q.OR)
        queryset = queryset.filter(Q_sn)
        return queryset


class ViewJobResultFilter(filters.FilterSet):
    """filter of jobresult """

    # sn = filters.CharFilter(name='sn', method='sn_filter', lookup_expr='icontains')
    # address = filters.CharFilter(name='address', lookup_expr='icontains')
    # memo = filters.CharFilter(name='memo', lookup_expr='icontains')
    cuda_version = filters.CharFilter(name='cuda_version', lookup_expr='exact', method="cuda_filter")
    cudnn_version = filters.CharFilter(name='cudnn_version', lookup_expr='exact', method="cudnn_filter")
    job_type = filters.NumberFilter(name='job_type', lookup_expr='exact', method="job_type_filter")
    model_name = filters.CharFilter(name='model_name', lookup_expr='icontains')
    frame_name = filters.CharFilter(name='frame_name', lookup_expr='exact', method='frame_filter')
    gpu_type = filters.CharFilter(name='gpu_type', lookup_expr='exact',
                                  method='gpu_type_filter')
    model_implement_type = filters.CharFilter(name='model_implement_type',
                                              lookup_expr='exact',
                                              method='model_implement_type_filter')
    version = filters.CharFilter(name='version', lookup_expr='exact', method="version_filter")
    report_index_id = filters.NumberFilter(name='report_index_id', lookup_expr='exact')
    run_rpc_type = filters.NumberFilter(name='run_rpc_type', lookup_expr='exact')
    run_machine_type = filters.CharFilter(name='run_machine_type', lookup_expr='exact')


    class Meta(object):
        """
        db_table
        """
        model = ViewJobResult
        #fields = '__all__'
        #决定filter顺序
        fields = ['job_id', 'cuda_version', 'cudnn_version', 'job_type',
                  'model_name', 'frame_name', 'gpu_type', 'model_implement_type',
                  'version', 'report_index_id', 'run_rpc_type', 'run_machine_type']

    def job_type_filter(self, queryset, name, value):
        """cuda 过滤"""
        self.cur_job_type = value
        queryset = queryset.filter(**{'job_type': value})
        return queryset

    def gpu_type_filter(self, queryset, name, value):
        """cuda 过滤"""
        self.cur_gpu_type = value
        queryset = queryset.filter(**{'gpu_type': value})
        return queryset

    def model_implement_type_filter(self, queryset, name, value):
        """cuda 过滤"""
        self.cur_model_implement_type = value
        queryset = queryset.filter(**{'model_implement_type': value})
        return queryset

    def frame_filter(self, queryset, name, value):
        """frame 过滤"""
        #frame_name = bm.Frame.objects.filter(frame_name=value)
        if value:
            #self.cur_frame_id = str(frame_name[0].frame_id)
            self.cur_frame_name = value
            print "this frame_name is: " + self.cur_frame_name
            queryset = queryset.filter(**{'frame_name': value})
        return queryset

    def cuda_filter(self, queryset, name, value):
        """cuda 过滤"""
        self.cur_cuda_version = value
        queryset = queryset.filter(**{'cuda_version': value})
        return queryset

    def cudnn_filter(self, queryset, name, value):
        """cudnn 过滤"""
        self.cur_cudnn_version = value
        queryset = queryset.filter(**{'cudnn_version': value})
        return queryset

    def version_filter(self, queryset, name, value):
        """增加获取最新版本号的数据"""
        values = []
        versions = bm.ViewJobResult.objects
        if hasattr(self, 'cur_cuda_version'):
            versions = versions.filter(cuda_version=self.cur_cuda_version)
            print "cuda_version is: {}".format(self.cur_cuda_version)
        if hasattr(self, 'cur_cudnn_version'):
            versions = versions.filter(cudnn_version=self.cur_cudnn_version)
            print "cudnn_version is: {}".format(self.cur_cudnn_version)
        if hasattr(self, 'cur_job_type'):
            versions = versions.filter(job_type=self.cur_job_type)
            print "image_type is: {}".format(self.cur_job_type)
        if hasattr(self, 'cur_gpu_type'):
            versions = versions.filter(gpu_type=self.cur_gpu_type)
            print "gpu_type is: {}".format(self.cur_gpu_type)
        if hasattr(self, 'cur_model_implement_type'):
            versions = versions.filter(job_type=self.cur_job_type)
            print "model_implement_type is: {}".format(self.cur_model_implement_type)

        if value == "latest":
            if hasattr(self, 'cur_frame_name'):
                versions = versions.filter(frame_name=self.cur_frame_name).order_by('-version')
                #print versions.query
                #print versions.count()
                if versions:
                    values.append(versions[0].version)
            else:
                versions_results = versions.values('frame_name').annotate(version=Max("version"))
                print versions_results

                for version in versions_results:
                    values.append(version['version'])

            print "this name is: ", name
            print "this version is: ", values
            # value = [u'20190508081718.post97', u'1.12.0.post97', u'1.0.0.post87', u'1.14.0.post97']
        # versions = bm.Image.objects
        # if hasattr(self, 'cur_cuda_version'):
        #     versions = versions.filter(cuda_version=self.cur_cuda_version)
        #     print "cuda_version is: {}".format(self.cur_cuda_version)
        # if hasattr(self, 'cur_cudnn_version'):
        #     versions = versions.filter(cudnn_version=self.cur_cudnn_version)
        #     print "cudnn_version is: {}".format(self.cur_cudnn_version)
        # if hasattr(self, 'cur_job_type'):
        #     versions = versions.filter(image_type=self.cur_job_type)
        #     print "image_type is: {}".format(self.cur_job_type)
        #
        # if value == "latest":
        #     if hasattr(self, 'cur_frame_id'):
        #         versions = versions.filter(frame_id=self.cur_frame_id).order_by('-create_time')
        #         print versions.count()
        #         if versions:
        #             values.append(versions[0].version)
        #     else:
        #         create_time_results = versions.values('frame_id').annotate(create_time=Max("create_time"))
        #         create_time_filters = []
        #         for create_time in create_time_results:
        #             create_time_filters.append(create_time['create_time'])
        #
        #         versions = versions.filter(create_time__in=create_time_filters)
        #         print versions
        #         for version in versions:
        #             values.append(version.version)
        #
        #     print "this name is: ", name
        #     print "this version is: ", values
        #     #value = [u'20190508081718.post97', u'1.12.0.post97', u'1.0.0.post87', u'1.14.0.post97']
        else:
            values.append(value)
        # Q_sn = Q()
        # for value in values:
        #     Q_sn.add(Q(**{'version': value}), Q.OR)
        #     queryset = queryset.filter(Q_sn)

        queryset = queryset.filter(version__in=values)
        if queryset:
            print queryset.query
        return queryset


class ImageFilter(filters.FilterSet):
    """filter of image """

    frame_id = filters.CharFilter(name='frame_id', lookup_expr='exact')
    version = filters.CharFilter(name='version', lookup_expr='exact')
    cuda_version = filters.CharFilter(name='cuda_version', lookup_expr='exact')
    cudnn_version = filters.CharFilter(name='cudnn_version', lookup_expr='exact')
    image_type = filters.NumberFilter(name='image_type', lookup_expr='exact')

    class Meta(object):
        """
        db_table
        """
        model = Image
        #fields = '__all__'
        fields = ['frame_id', 'version', 'cuda_version', 'cudnn_version', 'image_type']