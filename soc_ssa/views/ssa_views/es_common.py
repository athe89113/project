# coding: utf-8

import datetime
import logging
from django.conf import settings
from django.utils import timezone
from elasticsearch import Elasticsearch

ES_HOSTS = settings.ELASTICSEARCH_HOSTS

es_hosts = ES_HOSTS
es = Elasticsearch(hosts=es_hosts)
ES_TIMEOUT = 60
cycle = 24  # 周期的小时

logger = logging.getLogger('soc_ssa')


def get_cycle():
    """获得指定周期cycle的开始时间 cycle单位为小时"""  # from soc_ssa.views import ssa_views
    now = datetime.datetime.now()
    starttime = now - timezone.timedelta(hours=cycle)
    return timezone.datetime.strftime(starttime, '%Y-%m-%d %H:%M:%S')


def get_str_now():
    """获得指定周期cycle的开始时间 cycle单位为小时"""  # from soc_ssa.views import ssa_views
    now = datetime.datetime.now()
    return timezone.datetime.strftime(now, '%Y-%m-%d %H:%M:%S')


def get_es_data(body, size=0, days=2):
    """"""
    indexes = []
    now = datetime.datetime.now()
    for i in range(days):
        # indexes.append("ssa-result-" + timezone.datetime.strftime(now, '%Y%m%d'))
        indexes.append("ssa-result-" + timezone.datetime.strftime(now -
                                                                  timezone.timedelta(days=i), '%Y%m%d'))
    result = es.search(request_timeout=ES_TIMEOUT, size=size, doc_type='result', body=body, index=indexes,
                       ignore_unavailable=True)
    return result


def global_es_data(key, field, start_time=None, end_time=None, interval='hour', days=2):
    "全局态势资产总览"
    if not start_time:
        start_time = get_cycle()
    if not end_time:
        end_time = str(datetime.datetime.now())[:19]
    body = {
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {"key": key}
                    },
                    {
                        "range": {"time": {"gte": start_time}}
                    },
                    {
                        "range": {"time": {"lt": end_time}}
                    }
                ]
            }
        },
        "sort": {"time": {"order": "desc"}},
        "aggs": {
            "mydata": {
                "date_histogram": {
                    "field": "time",
                    "interval": interval,
                    "format": "yyyy-MM-dd HH:mm:ss",
                    "min_doc_count": 0,
                    "extended_bounds": {
                        "min": start_time,
                        "max": end_time
                    }
                },
                "aggs": {
                    "mycount": {
                        "sum": {"field": field}
                    }
                }
            }
        }
    }
    try:
        result = get_es_data(body, size=0, days=days)
    except Exception as e:
        logger.error(body)
        logger.error(e)
        result = {}
    x = []
    y = []
    if result.get('aggregations') and result.get('aggregations').get('mydata') and result.get('aggregations').get(
            'mydata').get("buckets"):
        data = result.get('aggregations').get('mydata').get("buckets")
        for da in data:
            x.append(da.get('key_as_string'))
            y.append(da.get('mycount').get('value')
                     if da.get('mycount').get('value') else 0)
    count = y[-1] if y else 0
    return x, y, count


def business_es_body(key, field, start_time=None, end_time=None, count_field="data.count"):
    if not start_time:
        start_time = get_cycle()
    if not end_time:
        end_time = timezone.datetime.strftime(
            datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    body = {
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {"key": key}
                    },
                    {
                        "range": {"time": {"gte": start_time}}
                    },
                    {
                        "range": {"time": {'lt': end_time}}
                    }
                ]
            }
        },
        "aggs": {
            "mydata": {

                "terms": {
                    "field": field,
                    # "size": 0,
                    "order": {
                        "mycount.value": "desc"
                    }
                },
                "aggs": {
                    "mycount": {
                        "sum": {"field": count_field}
                    }
                }
            }
        }
    }
    return body


def get_business_es(key, field, start_time=None, end_time=None, count_field="data.count"):
    """获取按key分类的数量统计
    """
    body = business_es_body(key, field, start_time, end_time, count_field)
    result = get_es_data(body, size=0)
    result_list = []
    if result:
        data = result.get('aggregations', {}).get(
            'mydata', {}).get("buckets", [])
        for da in data:
            result_list.append({
                "name": da.get("key"),
                "value": da.get("mycount").get("value")
            })
    return result_list


def get_aggs_sum_data(key, field, start_time, end_time):
    """按照field分类再sum后的数据"""
    body = {
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {"key": key}
                    },
                    {
                        "range": {"time": {"gte": start_time}}
                    },
                    {
                        "range": {"time": {"lt": end_time}}
                    }
                ]
            }
        },
        "aggs": {
            "mydata": {
                "sum": {"field": field}
            }
        }
    }
    total = 0
    result = get_es_data(body, size=0)
    if result.get('aggregations') and result.get('aggregations').get('mydata'):
        total = result.get('aggregations').get('mydata').get("value")
    return total
