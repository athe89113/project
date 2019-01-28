# -*- coding:utf-8 -*-
import copy
import requests
import time
from django.conf import settings

""" IP 事件ES查询
"""


def exec_es_sql(sql):
    """
    执行SQL查询es数据
    :param sql:
    :return:
    """
    start_time = time.time()
    print('[exec sql]:', sql)
    result = send_es_request(data=str(sql).encode('utf-8'))
    hits = result.get("hits", {}).get("hits")
    aggregations = result.get('aggregations')
    if aggregations:
        data_list = format_aggres_data(aggregations)
    elif hits:
        data_list = format_hits_data(hits)
    else:
        return []
    end_time = time.time()
    print('[cost_time]:', end_time - start_time)
    return data_list

def exec_es_sql_total(sql):
    """
    执行SQL查询es数据
    :param sql:
    :return:
    """
    result = send_es_request(data=str(sql).encode('utf-8'))
    total = result['hits']['total']
    if result.get('aggregations'):
        data_list = format_aggres_data(result['aggregations'])
    else:
        if not result:
            return []
        data_list = format_hits_data(result['hits']['hits'])
    data = dict()
    data['total'] = total
    data['data_list'] = data_list
    return data


def format_aggres_data(aggregations):
    """
    如果有bucket参数，会执行递归操作, 如果没有正常执行
    :param es_data:
    :param bucket:
    :return:
    """
    name_list = []
    value_list = []

    def make_bucket_list(data):
        bucket_list = []
        for field in data:
            if isinstance(data[field], dict):
                buckets = data[field].get('buckets', [])
                if buckets:
                    for bucket in buckets:
                        bucket_list.append({"bucket_name": field, "bucket": bucket})

                    for b in bucket_list:
                        name_list.append(b['bucket_name'])
                        if b['bucket'].get('key_as_string'):
                            value_list.append(format_value(b['bucket']['key_as_string']))
                        else:
                            value_list.append(format_value(b['bucket']['key']))

                        bucket_obj = b.get('bucket', [])
                        for field2, value in bucket_obj.items():
                            if isinstance(value, dict) and value.get('buckets'):
                                make_bucket_list(bucket_obj)
                            else:
                                if isinstance(value, dict) and value.get('value') is not None:
                                    name_list.append(field2)
                                    value_list.append(format_value(value['value']))
                else:
                    value = data[field]
                    if isinstance(value, dict) and value.get('value') is not None:
                        name_list.append(field)
                        value_list.append(format_value(value['value']))

    make_bucket_list(aggregations)

    distinct_field = []
    for field_name in name_list:
        if field_name in distinct_field:
            continue
        distinct_field.append(field_name)
    make_value_list = []
    value_dict = {}
    if value_list and distinct_field:
        for index in range(len(name_list)):
            value_dict[name_list[index]] = value_list[index]
            if name_list[index] == distinct_field[-1]:
                make_value_list.append(copy.deepcopy(value_dict))
    return make_value_list


def format_hits_data(hits):
    data = []
    for hit in hits:
        hit = hit['_source']
        _data = {}
        for k, v in hit.items():
            if isinstance(v, dict):
                for _k, _v in v.items():
                    if _k == "value":
                        _k = ""
                    else:
                        _k = ".{}".format(_k)
                    _data["{}{}".format(k, _k)] = _v
            else:
                _data[k] = v
        data.append(_data)
    return data


def send_es_request(url='', data={}, method='post'):
    """
    发送请求
    :param url:
    :param data:
    :param method:
    :return:
    """
    es_host = getattr(settings, 'ELASTICSEARCH_HOSTS', ["http://127.0.0.1:9200/"])
    url = es_host[0] + '/_sql'
    if method == 'get':
        for k, v in data.items():
            url += '?' + k + '=' + v + '&'
        url = url[0: len(url) - 1]
        try:
            response = requests.get(url, headers={'Connection': 'close', 'Content-Type': 'application/json'})
            if response.status_code != 200:
                return {}
        except requests.exceptions.ConnectionError as e:
            return {}
        return response.json()
    else:
        try:
            response = requests.post(url, data, headers={'Connection': 'close', 'Content-Type': 'application/json'})
            if response.status_code != 200:
                return {}
        except requests.exceptions.ConnectionError as e:
            return {}
        return response.json()


def format_value(data):
    if isinstance(data, float):
        return int(data)
    return data
