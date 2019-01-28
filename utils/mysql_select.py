# -*- coding:utf-8 -*-

from django.db import connection

""" SQL 执行
"""


def exec_sql(sql):
    """
    执行SQL查询es数据
    :param sql:
    :return:
    """
    result = []
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        rawData = cursor.fetchall()
        col_names = [desc[0] for desc in cursor.description]
        for row in rawData:
            objDict = dict()
            # 把每一行的数据遍历出来放到Dict中
            for index, value in enumerate(row):
                objDict[col_names[index]] = value
            result.append(objDict)
        return result
    except Exception as e:
        print '执行sql出错!', e
        return result
