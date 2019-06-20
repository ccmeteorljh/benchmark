#!/usr/bin/env python
# -*- coding: utf-8 -*-
#======================================================================
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
#======================================================================

"""
@Desc: views module
@File: views.py
@Author: liangjinhua
@Date: 2019/1/30 14:21
"""
from django.http import HttpResponse, JsonResponse
from django_filters.rest_framework import DjangoFilterBackend, OrderingFilter
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from benchmark_server.benchmark_models import Job
from benchmark_server.benchmark_models import ViewJobResult
from benchmark_server.benchmark_models import BenchmarkModel
from benchmark_server.benchmark_models import Frame
from benchmark_server.benchmark_models import Image
from benchmark_app.serializers import JobSerializer
from benchmark_app.serializers import BenchmarkModelSerializer
from benchmark_app.serializers import ViewJobResultSerializer
from benchmark_app.serializers import FrameSerializer
from benchmark_app.serializers import ImageSerializer
from .filter import JobFilter
from .filter import ImageFilter
from .filter import ViewJobResultFilter

class JSONResponse(HttpResponse):
    """define response
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content-type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class JobViewSet(viewsets.ModelViewSet):
    """view set for table job
    """
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = JobFilter


class BenchmarkModelViewSet(viewsets.ModelViewSet):
    """view set for table BenchmarkModel
    """
    queryset = BenchmarkModel.objects.all()
    serializer_class = BenchmarkModelSerializer


class FrameViewSet(viewsets.ModelViewSet):
    """view set for table frame
    """
    queryset = Frame.objects.all()
    serializer_class = FrameSerializer


class ImageViewSet(viewsets.ModelViewSet):
    """view set for table image
    """
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = ImageFilter


class ViewJobResultModelViewSet(viewsets.ModelViewSet):
    """view set for View JobResultModel
    """
    queryset = ViewJobResult.objects.all()
    serializer_class = ViewJobResultSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = ViewJobResultFilter


# @csrf_exempt
# def job_list(request):
#     """
#     List all code jobs, or create a new job.
#     """
#     if request.method == 'GET':
#         jobs = Job.objects.all()
#         serializer = JobSerializer(jobs, many=True)
#         return JsonResponse(serializer.data, safe=False)
#
#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = JobSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)
#
# @csrf_exempt
# def job_detail(request, job_id):
#     """
#     Retrieve, update or delete a code job.
#     """
#     try:
#         job = Job.objects.get(job_id=1)
#         print job
#     except Job.DoesNotExist:
#         return HttpResponse(status=404)
#
#     if request.method == 'GET':
#         serializer = JobSerializer(job)
#         return JsonResponse(serializer.data)
#
#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = JobSerializer(job, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status=400)
#
#     elif request.method == 'DELETE':
#         job.delete()
#         return HttpResponse(status=204)