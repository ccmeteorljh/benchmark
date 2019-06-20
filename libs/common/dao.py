#!/usr/bin/env python
# -*- coding: utf-8 -*-
#======================================================================
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
#======================================================================

"""
@Desc: dap module
@File: dap.py
@Author: liangjinhua
@Date: 2018/1/3 17:28
"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#======================================================================
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
#======================================================================

"""
@Desc: dao module
@File: dao.py
@Author: liangjinuha
@Date: 17/11/30 上午11:40
"""
import MySQLdb

import libs.common.exception as myexception


class CommonDao(object):
    """
    定义数据库的常用操作
    """
    @staticmethod
    def get_conn(**ksargs):
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
            raise myexception.DBError('%s%s' % (e.message, 'ConnectError!'))
        return conn, cur

    @staticmethod
    def exe_update(conn, cur, sql):
        """ 更新语句，可执行Update，Insert语句 """
        try:
            sta = cur.execute(sql)
            conn.commit()
        except MySQLdb.Error as e:
            conn.rollback()
            raise myexception.DBError('%s%s' % (e.message, 'Update error!'))
        return sta

    @staticmethod
    def exe_delete(conn, cur, sql):
        """ 删除语句 """
        try:
            sta = cur.execute(sql)
            conn.commit()
        except MySQLdb.Error as e:
            conn.rollback()
            raise myexception.DBError('%s%s' % (e.message, "Delete error!"))
        return sta

    @staticmethod
    def exe_query(cur, sql):
        """ 查询语句 """
        try:
            cur.execute(sql)
            result = cur.fetchall()
        except MySQLdb.Error as e:
            raise myexception.DBError('%s%s' % (e.message, "Select error!"))
        return result

    @staticmethod
    def conn_close(conn, cur):
        """ 关闭所有连接 """
        try:
            cur.close()
            conn.close()
        except MySQLdb.Error as e:
            raise myexception.DBError('%s%s' % (e.message, "Close error!"))


