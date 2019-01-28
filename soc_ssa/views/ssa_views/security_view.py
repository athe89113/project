# coding: utf-8

import time
import json
import logging
import datetime
from dwebsocket import accept_websocket, require_websocket
from rest_framework.views import APIView
from rest_framework.response import Response
from kafka import KafkaConsumer, TopicPartition
from .es_common import get_cycle, get_es_data, business_es_body, global_es_data, get_str_now
from .business_view import kafka_data
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

logger = logging.getLogger('soc_ssa')


class SecurityTrend(APIView):
    """安全态势感知"""

    def get(self, request):
        """攻击事件数发展趋势/蠕虫感染数量趋势"""
        now = datetime.datetime.now()
        my_type = request.GET.get('type')  # attack_event/worm_num 攻击事件数发展趋势/蠕虫感染数量趋势
        days = int(request.GET.get("days", 0))  # 0 1 7 30 表示今天昨天最近7天最近30天
        if my_type not in ["attack_event", "worm_num"] or days not in [0, 1, 7, 30]:
            return Response({
                "status": 500,
                "msg": "获取数据错误",
                "data": []
            })
        interval = "hour"
        if days == 0:
            start_time = str(now)[:10] + ' 00:00:00'
            end_time = str(now)[:19]
        elif days == 1:
            start_time = str(now - datetime.timedelta(days=1))[:10] + ' 00:00:00'
            end_time = str(now)[:10] + ' 00:00:00'
        else:
            interval = "day"
            start_time = str(now - datetime.timedelta(hours=days * 24))[:13] + ':00:00'
            end_time = str(now)[:19]
        if my_type in ['attack_event']:
            key = "security-total_count"
            field = "data.security_total_count"
        else:
            key = "virus-total_count"
            field = "data.count"
        x, y, count = global_es_data(key, field, start_time=start_time, end_time=end_time, interval=interval, days=31)
        data = {
            "x": x,
            "y": y
        }
        return Response({
            "status": 200,
            "msg": "获取数据成功",
            "data": data
        })


class SecurityAttackTop5(APIView):
    """安全态势感知"""

    def get(self, request):
        """攻击目标IP地址top5/攻击单位top5"""
        body = business_es_body("security-dst_ip_count", "data.security_dst_ip")
        x = []
        y = []
        result = get_es_data(body, size=0)
        if result.get('aggregations') and result.get('aggregations').get('mydata') and result.get('aggregations').get(
                'mydata').get("buckets"):
            data = result.get('aggregations').get('mydata').get("buckets")
            for da in data:
                x.append(da.get('key'))
                y.append(da.get('mycount').get('value'))
        x = x + ['' for i in range(5)]
        y = y + [0 for i in range(5)]
        x = x[:5]
        y = y[:5]
        data = {
            "x": x,
            "y": y
        }
        return Response({
            "status": 200,
            "msg": "获取数据成功",
            "data": data
        })


class SecurityUnusualFlow(APIView):
    """安全态势感知"""

    def get(self, request):
        """异常流量7日峰值"""
        now = datetime.datetime.now()
        start_time = str(now - datetime.timedelta(hours=24*7))[:19]
        end_time = str(datetime.datetime.now())[:19]
        body = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {"key": "network-abnormal_throughput_peak"}
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
                        "interval": "day",
                        "format": "yyyy-MM-dd HH:mm:ss",
                        "min_doc_count": 0,
                        "extended_bounds": {
                            "min": start_time,
                            "max": end_time
                        }
                    },
                    "aggs": {
                        "mycount": {
                            "max": {"field": "data.network_max_in_bytes"}
                        }
                    }
                }
            }
        }
        x = []
        y = []
        result = get_es_data(body, size=0, days=8)
        if result.get('aggregations') and result.get('aggregations').get('mydata') and result.get('aggregations').get(
                'mydata').get("buckets"):
            data = result.get('aggregations').get('mydata').get("buckets")
            for da in data:
                x.append(da.get("key_as_string"))
                value = da.get('mycount').get('value') if da.get('mycount').get('value') else 0
                y.append(value)
        data = {
            "x": x,
            "y": y
        }
        return Response({
            "status": 200,
            "msg": "获取数据成功",
            "data": data
        })


class SecurityWormTop5(APIView):
    """安全态势感知"""

    def get(self, request):
        """蠕虫感染top5"""
        start_time = get_cycle()
        end_time = get_str_now()
        body = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {"key": 'virus-asset_top'}
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

                    "terms": {
                        "field": 'data.virus_host_ip',
                        "size": 0,
                        "order": {
                            "mycount.value": "desc"
                        }
                    },
                    "aggs": {
                        "mycount": {
                            "sum": {"field": "data.virus_btw_count"}
                        }
                    }
                }
            }
        }
        x = []
        y = []
        result = get_es_data(body, size=0)
        if result.get('aggregations') and result.get('aggregations').get('mydata') and result.get('aggregations').get(
                'mydata').get("buckets"):
            data = result.get('aggregations').get('mydata').get("buckets")
            for da in data:
                x.append(da.get("key"))
                value = da.get('mycount').get('value')
                y.append(value)
        x = x + ['' for i in range(5)]
        y = y + [0 for i in range(5)]
        x = x[:5]
        y = y[:5]
        data = {
            "x": x,
            "y": y
        }
        return Response({
            "status": 200,
            "msg": "获取数据成功",
            "data": data
        })


class SecuritySeriousWormTop5(APIView):
    """安全态势感知"""

    def get(self, request):
        """严重蠕虫top5"""
        start_time = get_cycle()
        str_end_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        body = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {"key": 'virus-btw_asset_top'}
                        },
                        {
                            "range": {"time": {"gte": start_time}}
                        },
                        {
                            "range": {"time": {"lt": str_end_time}}
                        }
                    ]
                }
            },
            "sort": {"time": {"order": "desc"}},
        }
        result = get_es_data(body, size=5)
        data = result.get('hits').get('hits')
        return_data = []
        for da in data:
            temp = da.get('_source').get('data')
            return_data.append({"name": temp.get('virus_virusname'), "ip": temp.get('virus_host_ip')})
        # data = [
        #     {"name": "webaccess SQL注入", "ip": "192.168.0.1"},
        #     {"name": "webaccess HTFS", "ip": "192.168.1.2"},
        #     {"name": "web worm ssh", "ip": "192.168.0.3"},
        #     {"name": "webaccess", "ip": "192.168.0.4"},
        #     {"name": "web FTP", "ip": "192.168.0.5"},
        # ]
        return Response({
            "status": 200,
            "msg": "获取数据成功",
            "data": return_data
        })


class SecurityAttackEventTop24(APIView):
    """安全态势感知"""

    def get(self, request):
        """最近24小时攻击事件数"""
        start_time = get_cycle()
        str_end_time = get_str_now()
        body = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {"key": "security-events"}
                        },
                        {
                            "match": {"data.security_level": "严重"}
                        },
                        {
                            "range": {"time": {"gte": start_time}}
                        },
                        {
                            "range": {"time": {"lt": str_end_time}}
                        }
                    ]
                }
            },
            "sort": {"data.security_time": {"order": "desc"}},
        }
        result = get_es_data(body, size=50)
        data = result.get('hits').get('hits')
        return_data = []
        for da in data:
            source = da.get('_source')
            d = source.get('data')
            temp = {"date_time": source.get('time'), "security_dst_ip": d.get('security_dst_ip'),
                    "security_dst_ip_location": d.get("security_dst_ip_location"),
                    "security_src_ip": d.get("security_src_ip")}
            return_data.append(temp)
        # data = [
        #     {"data_time": "2018-04-03 12:11:10", "target": "web服务器01", "ip": "192.168.1.2", "location": "成都",
        #      "status": "严重", "source_ip": "10.10.10.11"},
        #     {"data_time": "2018-04-03 12:11:10", "target": "web服务器01", "ip": "192.168.1.2", "location": "成都",
        #      "status": "严重", "source_ip": "10.10.10.11"},
        #     {"data_time": "2018-04-03 12:11:10", "target": "web服务器01", "ip": "192.168.1.2", "location": "成都",
        #      "status": "严重", "source_ip": "10.10.10.11"},
        #     {"data_time": "2018-04-03 12:11:10", "target": "web服务器01", "ip": "192.168.1.2", "location": "成都",
        #      "status": "严重", "source_ip": "10.10.10.11"},
        #     {"data_time": "2018-04-03 12:11:10", "target": "web服务器01", "ip": "192.168.1.2", "location": "成都",
        #      "status": "严重", "source_ip": "10.10.10.11"}
        # ]
        return Response({
            "status": 200,
            "msg": "获取数据成功",
            "data": return_data
        })


@require_websocket
def attack_map(request):
    if not request.is_websocket():
        logger.error("not websocket !!!")
        return HttpResponse('not websocket !!!')
    else:
        kafka_data("attack_map", request)
