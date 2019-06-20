#!/usr/bin/env python
# -*- coding: utf-8 -*-
#======================================================================
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
#======================================================================

"""
@Desc: error module
@File: error.py
@Author: liangjinuha
@Date: 17/11/30 上午10:40
"""
import os
import sys
import json

try:
    JSONDecodeError = json.decoder.JSONDecodeError
except AttributeError:
    JSONDecodeError = ValueError


class BaseError(Exception):
    """
    base error class
    """
    def __init__(self, error_text):
        self.error_text = error_text

    def __str__(self):
        return self.error_text

class NullPointerError(BaseError):
    """
    null pointer error class
    """
    def __init__(self, error_text):
        super(NullPointerError, self).__init__(error_text)

class DBError(BaseError):
    """
    database operation error class
    """
    def __init__(self, error_text):
        super(DBError, self).__init__(error_text)

class DelDataError(BaseError):
    """
    del data error error class
    """
    def __init__(self, error_text):
        super(DelDataError, self).__init__(error_text)

class FileFormatError(BaseError):
    """
    File Format Error class
    """
    def __init__(self, error_text):
        super(FileFormatError, self).__init__(error_text)

class ParamsError(BaseError):
    """
    Parameters  Error class
    """
    def __init__(self, error_text):
        super(ParamsError, self).__init__(error_text)

class ResponseError(BaseError):
    """
    Response Error class
    """
    def __init__(self, error_text):
        super(ResponseError, self).__init__(error_text)

class ParseResponseError(BaseError):
    """
    Parse Response error class
    """
    def __init__(self, error_text):
        super(ParseResponseError, self).__init__(error_text)

class ValidationError(BaseError):
    """
    Validation error class
    """
    def __init__(self, error_text):
        super(ValidationError, self).__init__(error_text)

class NotFoundError(BaseError):
    """
    Base not found error class
    """
    def __init__(self, error_text):
        super(NotFoundError, self).__init__(error_text)

class FunctionNotFound(NotFoundError):
    """
    Function not found error class
    """
    def __init__(self, error_text):
        super(FunctionNotFound, self).__init__(error_text)

class VariableNotFound(NotFoundError):
    """
    Variable not found error class
    """
    def __init__(self, error_text):
        super(VariableNotFound, self).__init__(error_text)

class ApiNotFound(NotFoundError):
    """
    Api not found error class
    """
    def __init__(self, error_text):
        super(ApiNotFound, self).__init__(error_text)

class SuiteNotFound(NotFoundError):
    """
    Suite not found error class
    """
    def __init__(self, error_text):
        super(SuiteNotFound, self).__init__(error_text)

class TestcaseNotFound(NotFoundError):
    """
    Test case not found  error class
    """
    def __init__(self, error_text):
        super(TestcaseNotFound, self).__init__(error_text)