#!/usr/bin/env python
# -*- coding: utf-8 -*-
#======================================================================
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
#======================================================================

"""
@Desc: post_log module
@File: post_log.py
@Author: liangjinhua
@Date: 2018/7/19 15:22
"""
import requests
import os

from requests.adapters import HTTPAdapter

model = os.getenv("model")
image_version = os.getenv("image_version")
frame = os.getenv("frame")
log_name = os.getenv("log_name")
url = "http://10.62.51.15:8301/{0}/{1}/{2}".format(frame, image_version, model)
print(url)
data = None
s = requests.Session()
s.mount('http://', HTTPAdapter(max_retries=3))
s.mount('https://', HTTPAdapter(max_retries=3))
file_name = '/home/crim/%s' % log_name
if os.path.exists(file_name):
    files = {'file': open(file_name, 'rb')}
else:
    files = {'file': open('./%s' % log_name, 'rb')}
r = s.post(url, data, files=files)
s.close()
