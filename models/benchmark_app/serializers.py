#!/usr/bin/env python
# -*- coding: utf-8 -*-
#======================================================================
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
#======================================================================

"""
@Desc: serializers module
@File: serializers.py
@Author: liangjinhua
@Date: 2019/1/30 11:31
"""
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from rest_framework import serializers
from benchmark_server.benchmark_models import Job
from benchmark_server.benchmark_models import ViewJobResult
from benchmark_server.benchmark_models import BenchmarkModel
from benchmark_server.benchmark_models import Frame
from benchmark_server.benchmark_models import Image

class JobSerializer(serializers.ModelSerializer):
    """
    this Serializer for table job
    """
    files = serializers.ListField(
        child=serializers.FileField(max_length=100000,
                                    allow_empty_file=False
                                    ), write_only=True
    )

    # files = serializers.FileField(max_length=100000,
    #                                 allow_empty_file=False)

    class Meta(object):
        """db_table"""
        model = Job
        fields = '__all__'

    def create(self, validated_data):
        with open('test', 'w+') as f:
            for key in validated_data:
                if key == 'files':
                    for file in validated_data.get(key):
                        default_storage.save(file.name,
                                                ContentFile(file.read()))
                else:
                    f.writelines(key + "\n")
                    f.writelines(str(validated_data.get(key)) + "\n")

        validated_data.pop('files')
        return Job.objects.create(**validated_data)



class ViewJobResultSerializer(serializers.ModelSerializer):
    """
    this Serializer for view JobResult
    """
    class Meta(object):
        """db_table"""
        model = ViewJobResult
        fields = '__all__'


class BenchmarkModelSerializer(serializers.ModelSerializer):
    """
    this Serializer for table BenchmarkModel
    """
    class Meta(object):
        """db_table"""
        model = BenchmarkModel
        fields = '__all__'

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return BenchmarkModel.objects.create(**validated_data)


class FrameSerializer(serializers.ModelSerializer):
    """
    this Serializer for table frame
    """
    class Meta(object):
        """db_table"""
        model = Frame
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    """
    this Serializer for table Image
    """
    class Meta(object):
        """db_table"""
        model = Image
        fields = '__all__'