#!/usr/bin/env python
# -*- coding: utf-8 -*-
#======================================================================
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
#======================================================================

"""
@Desc: utils module
@File: utils.py
@Author: liangjinhua
@Date: 2017/12/29 11:29
"""
import codecs
import imp
import importlib
import json
import logging
import os.path
import re
import types
from collections import OrderedDict

import yaml
from numpy import long
from numpy import unicode
from requests.compat import basestring
from requests.structures import CaseInsensitiveDict
from libs.common import exception
from conf import base_conf

try:
    string_type = basestring
    long_type = long
    PYTHON_VERSION = 2
except NameError:
    string_type = str
    long_type = int
    PYTHON_VERSION = 3


def remove_prefix(text, prefix):
    """ remove prefix from text
    """
    if text.startswith(prefix):
        return text[len(prefix):]
    return text


def load_yaml_file(yaml_file):
    """ load yaml file and check file content format
    """
    with codecs.open(yaml_file, 'r+', encoding='utf-8') as stream:
        yaml_content = yaml.load(stream)
        check_format(yaml_file, yaml_content)
        return yaml_content


def load_json_file(json_file):
    """ load json file and check file content format
    """
    with codecs.open(json_file, encoding='utf-8') as data_file:
        try:
            json_content = json.load(data_file)
        except exception.JSONDecodeError:
            err_msg = u"JSONDecodeError: JSON file format error: {}".format(json_file)
            logging.error(err_msg)
            raise exception.FileFormatError(err_msg)

        check_format(json_file, json_content)
        return json_content


def load_file(testcase_file_path):
    """
    load test case file
    :param testcase_file_path:
    :return:
    """
    file_suffix = os.path.splitext(testcase_file_path)[1]
    if file_suffix == '.json':
        return load_json_file(testcase_file_path)
    elif file_suffix in ['.yaml', '.yml']:
        return load_yaml_file(testcase_file_path)
    else:
        # '' or other suffix
        err_msg = u"file is not in YAML/JSON format: {}".format(testcase_file_path)
        logging.warning(err_msg)
        return []


def check_format(file_path, content):
    """ check testcase format if valid
    """
    if not content:
        # testcase file content is empty
        err_msg = u"Testcase file content is empty: {}".format(file_path)
        logging.error(err_msg)
        raise exception.FileFormatError(err_msg)

    elif not isinstance(content, (list, dict)):
        # testcase file content does not match testcase format
        err_msg = u"Testcase file content format invalid: {}".format(file_path)
        logging.error(err_msg)
        raise exception.FileFormatError(err_msg)


def load_folder_files(folder_path, recursive=True, suffix=('.yml', '.yaml', '.json')):
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
            if not filename.endswith(suffix):
                continue

            filenames_list.append(filename)

        for filename in filenames_list:
            file_path = os.path.join(dirpath, filename)
            file_list.append(file_path)

        if not recursive:
            break

    return file_list


def query_json(json_content, query, delimiter='.'):
    """
    :param json_content:
        json_content = {
                "ids": [1, 2, 3, 4],
                "person": {
                    "name": {
                        "first_name": "Leo",
                        "last_name": "Lee",
                    },
                    "age": 29,
                    "cities": ["Guangzhou", "Shenzhen"]
                }
            }
    :param query:
        "person.name.first_name"  =>  "Leo"
        "person.cities.0"         =>  "Guangzhou"
    :param delimiter:
    :return: queried result
    """
    if json_content == "":
        raise exception.ResponseError("response content is empty!")

    try:
        for key in query.split(delimiter):
            if isinstance(json_content, list):
                if key in ['len', 'length', 'count']:
                    json_content = len(json_content)
                else:
                    json_content = json_content[int(key)]
            elif isinstance(json_content, (dict, CaseInsensitiveDict)):
                json_content = json_content[key]
            else:
                raise exception.ParseResponseError(
                    "response content is in text format! failed to query key {}!".format(key))
    except (KeyError, ValueError, IndexError):
        raise exception.ParseResponseError("failed to query json when extracting response!")

    return json_content


def deep_update_dict(origin_dict, override_dict):
    """
    update origin dict with override dict recursively
    :param origin_dict:
        origin_dict = {'a': 1, 'b': {'c': 2, 'd': 4}}
    :param override_dict:
        override_dict = {'b': {'c': 3}}
    :return:
        {'a': 1, 'b': {'c': 3, 'd': 4}}
    """
    for key, val in override_dict.items():
        if isinstance(val, dict):
            tmp = deep_update_dict(origin_dict.get(key, {}), val)
            origin_dict[key] = tmp
        else:
            origin_dict[key] = override_dict[key]

    return origin_dict


def is_function(tup):
    """ Takes (name, object) tuple, returns True if it is a function.
    """
    name, item = tup
    return isinstance(item, types.FunctionType)


def is_variable(tup):
    """ Takes (name, object) tuple, returns True if it is a variable.
    """
    name, item = tup
    if callable(item):
        # function or class
        return False

    if isinstance(item, types.ModuleType):
        # imported module
        return False

    if name.startswith("_"):
        # private property
        return False

    return True


def get_imported_module(module_name):
    """ import module and return imported module
    """
    return importlib.import_module(module_name)


def get_imported_module_from_file(file_path):
    """ import module from python file path and return imported module
    """
    # Python 2.7
    imported_module = imp.load_source('module_name', file_path)
    return imported_module


def filter_module(module, filter_type):
    """
    filter functions or variables from import module
    :param module: imported module
    :param filter_type: "function" or "variable"
    :return:
    """
    filter_type = is_function if filter_type == "function" else is_variable
    module_functions_dict = dict(filter(filter_type, vars(module).items()))
    return module_functions_dict


def search_conf_item(start_path, item_type, item_name):
    """
    search expected function or variable recursive upward
    :param start_path:  search start path
    :param item_type: "function" or "variable"
    :param item_name:  function name or variable name
    :return:
    """
    dir_path = base_conf.ROOT_PATH
    target_file = os.path.join(dir_path, "conf/base_conf.py")

    if os.path.isfile(target_file):
        imported_module = get_imported_module_from_file(target_file)
        items_dict = filter_module(imported_module, item_type)
        if item_name in items_dict:
            return items_dict[item_name]
        else:
            return search_conf_item(dir_path, item_type, item_name)

    if dir_path == start_path:
        # system root path
        err_msg = "{} not found in recursive upward path!".format(item_name)
        if item_type == "function":
            raise exception.FunctionNotFound(err_msg)
        else:
            raise exception.VariableNotFound(err_msg)

    return search_conf_item(dir_path, item_type, item_name)


def lower_dict_keys(origin_dict):
    """
    convert keys in dict to lower case
    e.g.
        Name => name, Request => request
        URL => url, METHOD => method, Headers => headers, Data => data
    :param origin_dict:
    :return:
    """
    if not origin_dict or not isinstance(origin_dict, dict):
        return origin_dict

    return {
        key.lower(): value
        for key, value in origin_dict.items()
    }


def lower_config_dict_key(config_dict):
    """ convert key in config dict to lower case, convertion will occur in two places:
        1, all keys in config dict;
        2, all keys in config["request"]
    """
    config_dict = lower_dict_keys(config_dict)
    if "request" in config_dict:
        config_dict["request"] = lower_dict_keys(config_dict["request"])

    return config_dict


def convert_to_order_dict(map_list):
    """
    convert mapping in list to ordered dict
    :param map_list:
         [
            {"a": 1},
            {"b": 2}
        ]
    :return:
        OrderDict({
            "a": 1,
            "b": 2
        })
    """
    ordered_dict = OrderedDict()
    for map_dict in map_list:
        ordered_dict.update(map_dict)

    return ordered_dict


def construct_update_sql(conditions):
    """

    :param conditions:
        {
            "table_name": "paddle_cloud_job",
            "set":{
                "log_extracted": '0'
            },
            "where":{
               "cloud_job_id": "1"
            }
        }
    :return: update paddle_cloud_job set log_extracted=0 where cloud_job_id='1'
    """
    table_name = conditions["table_name"]
    set = ''
    for key, value in conditions["set"].items():
        set += " %s='%s'," % (key, value)
    set = set[0:len(set)-1]

    where = ' 1=1 '

    for key, value in conditions["where"].items():
        where += "and %s='%s' " % (key, value)

    sql = "update {} set{} where {}".format(table_name, set, where)
    return sql
