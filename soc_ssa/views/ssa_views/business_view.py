# coding: utf-8

import time
import json
import logging
import datetime
from soc.settings import TARGET_LOCATION
from django.http import HttpResponse
from dwebsocket import require_websocket, accept_websocket
from rest_framework.views import APIView
from soc_ssa.models import SelfServiceConf
from rest_framework.response import Response
from kafka import KafkaConsumer, TopicPartition
from .es_common import get_cycle, get_es_data, business_es_body, cycle, get_str_now, global_es_data
from django.contrib.auth.decorators import login_required

logger = logging.getLogger('soc_ssa')


class BusinessVisitCount(APIView):
    """业务态势感知"""

    def get(self, request):
        """当前访问人数"""
        start_time = get_cycle()
        end_time = get_str_now()
        today_start_time = str(datetime.datetime.now())[:10] + " 00:00:00"
        body = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {"key": "web-log-ip_count"}
                        }, {
                            "range": {"time": {"gte": today_start_time}}
                        },
                        {
                            "range": {"time": {"lt": end_time}}
                        }
                    ]
                }
            },
            "aggs": {
                "mydata": {

                    "date_histogram": {
                        "field": "time",
                        "interval": "hour",
                        "format": "yyyy-MM-dd HH:mm:ss",
                        "min_doc_count": 0,
                        "extended_bounds": {
                            "min": today_start_time,
                            "max": end_time,
                        }
                    }
                }
            }
        }
        doc_count = []
        result = get_es_data(body, size=0)
        if result.get('aggregations') and result.get('aggregations').get('mydata') and result.get('aggregations').get(
                'mydata').get("buckets"):
            data = result.get('aggregations').get('mydata').get("buckets")
            for da in data:
                doc_count.append(da.get("doc_count"))

        data = {
            "count_now": doc_count[-1] if doc_count else 0,
            "count_today": sum(doc_count)
        }
        return Response({
            "status": 200,
            "msg": "获取数据成功",
            "data": data
        })


class BusinessVisitTop10(APIView):
    """业务态势感知"""

    def get(self, request):
        """最近访问TOP10 
        最近的意思是一个周期"""
        body = business_es_body("web-log-ip_count", "data.web_log_ip")
        result = get_es_data(body, size=0)
        X = []
        Y = []
        if result.get('aggregations') and result.get('aggregations').get('mydata') and result.get('aggregations').get(
                'mydata').get("buckets"):
            data = result.get('aggregations').get('mydata').get("buckets")
            for da in data:
                X.append(da.get("key"))
                Y.append(da.get("mycount").get("value"))
        X = X + ['' for i in range(10)]
        Y = Y + [0 for i in range(10)]
        X = X[:10]
        Y = Y[:10]

        data = {
            "x": X,
            "y": Y
        }
        return Response({
            "status": 200,
            "msg": "获取数据成功",
            "data": data
        })


class BusinessServerStatus(APIView):
    """业务态势感知"""

    def get(self, request):
        """服务器响应状态占比"""
        start_time = get_cycle()
        end_time = get_str_now()
        body = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {"key": "web-log-http_status_count"}
                        }, {
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
                        "field": "data.web_log_host",
                        "size": 3,
                        "order": {
                            "mycount.value": "desc"
                        }
                    },
                    "aggs": {
                        "mycount": {
                            "sum": {"field": "data.web_log_http_status_total_count"}
                        }
                    }
                }
            },
        }
        result = get_es_data(body, size=0)
        domains = []
        domain_dict = {}
        if result.get('aggregations') and result.get('aggregations').get('mydata') and result.get('aggregations').get(
                'mydata').get("buckets"):
            data = result.get('aggregations').get('mydata').get("buckets")
            for da in data:
                domains.append(da.get('key'))
                domain_dict[da.get('key')] = {"2xx": 0, "3xx": 0, "4xx": 0, "5xx": 0}
        # 先取出访问量最大的是哪个网站 再分辨算出三个网站具体访问状态的数据
        for domain in domains:
            body = {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "match": {"key": "web-log-http_status_count"}
                            }, {
                                "range": {"time": {"gte": start_time}}
                            }, {
                                "match": {"data.web_log_host": domain}
                            },
                            {
                                "range": {"time": {"lt": end_time}}
                            }
                        ]
                    }
                }
            }
            result = get_es_data(body, size=cycle)
            data = result.get('hits').get('hits')
            for da in data:
                for d in da.get('_source').get('data').get('web_log_http_status_count'):
                    if str(d.get('web_log_http_status')).startswith('2'):
                        domain_dict[domain]['2xx'] += d.get('count')
                    if str(d.get('web_log_http_status')).startswith('3'):
                        domain_dict[domain]['3xx'] += d.get('count')
                    if str(d.get('web_log_http_status')).startswith('4'):
                        domain_dict[domain]['4xx'] += d.get('count')
                    if str(d.get('web_log_http_status')).startswith('5'):
                        domain_dict[domain]['5xx'] += d.get('count')
        return_data = {
            "domain": [],
            "2xx": [],
            "3xx": [],
            "4xx": [],
            "5xx": [],
        }
        for domain in domains:
            return_data['domain'].append(domain)
            return_data['2xx'].append(domain_dict[domain]['2xx'])
            return_data['3xx'].append(domain_dict[domain]['3xx'])
            return_data['4xx'].append(domain_dict[domain]['4xx'])
            return_data['5xx'].append(domain_dict[domain]['5xx'])

        return Response({
            "status": 200,
            "msg": "获取数据成功",
            "data": return_data
        })


class BusinessVisitTrend(APIView):
    """业务态势感知"""

    def get(self, request):
        """访问趋势"""
        time_x, uv, count = global_es_data("web-log-uv", 'data.count')
        time_x, pv, count = global_es_data("web-log-pv", 'data.count')
        data = {
            "x": time_x,
            "pv": pv,
            "uv": uv
        }
        return Response({
            "status": 200,
            "msg": "获取数据成功",
            "data": data
        })


class BusinessFlowTrend(APIView):
    """业务态势感知"""

    def get(self, request):
        """流量趋势"""
        time_x, flow_in, count = global_es_data("network-throughput", 'data.network_in_bytes')
        time_x, flow_out, count = global_es_data("network-throughput", 'data.network_out_bytes')
        data = {
            "x": time_x,
            "in": flow_in,
            "out": flow_out
        }

        return Response({
            "status": 200,
            "msg": "获取数据成功",
            "data": data
        })


class BusinessVisitLocation(APIView):
    """业务态势感知"""

    def get(self, request):
        """访问地理位置"""
        body = business_es_body("web-log-location_count", "data.web_log_location")
        result = get_es_data(body, size=0)
        X = []
        Y = []
        if result.get('aggregations') and result.get('aggregations').get('mydata') and result.get('aggregations').get(
                'mydata').get("buckets"):
            data = result.get('aggregations').get('mydata').get("buckets")
            for da in data:
                X.append(da.get("key"))
                Y.append(da.get("mycount").get("value"))
        # 取前五个 不够的补0
        X = X + ['', '', '', '', '']
        Y = Y + [0, 0, 0, 0, 0]
        X = X[:5]
        Y = Y[:5]
        data = {
            "x": X,
            "y": Y
        }
        return Response({
            "status": 200,
            "msg": "获取数据成功",
            "data": data
        })


class BusinessVisitOS(APIView):
    """业务态势感知"""

    def get(self, request):
        """访问操作系统"""
        body = business_es_body("web-log-os_count", "data.web_log_os")
        result = get_es_data(body, size=0)
        return_data = []
        if result.get('aggregations') and result.get('aggregations').get('mydata') and result.get('aggregations').get(
                'mydata').get("buckets"):
            data = result.get('aggregations').get('mydata').get("buckets")
            for da in data:
                return_data.append({"name": da.get("key"), "value": da.get("mycount").get("value")})
        return_data = return_data[:5]
        if return_data[5:]:
            return_data.append({"其他": sum([x.get("value") for x in return_data[5:]])})
        # data = [
        #     {"name": "ubuntu", "value": 19},
        #     {"name": "windows", "value": 9},
        #     {"name": "max os", "value": 10},
        # ]
        return Response({
            "status": 200,
            "msg": "获取数据成功",
            "data": return_data
        })


class BusinessVisitBrowser(APIView):
    """业务态势感知"""

    def get(self, request):
        """访问浏览器"""
        body = business_es_body("web-log-browser_count", "data.web_log_browser")
        result = get_es_data(body, size=0)
        return_data = []
        if result.get('aggregations') and result.get('aggregations').get('mydata') and result.get('aggregations').get(
                'mydata').get("buckets"):
            data = result.get('aggregations').get('mydata').get("buckets")
            for da in data:
                return_data.append({"name": da.get("key"), "value": da.get("mycount").get("value")})
        return_data = return_data[:5]
        if return_data[5:]:
            return_data.append({"其他": sum([x.get("value") for x in return_data[5:]])})
        # data = [
        #     {"name": "ie", "value": 19},
        #     {"name": "safari", "value": 9},
        #     {"name": "chrome", "value": 10},
        # ]
        return Response({
            "status": 200,
            "msg": "获取数据成功",
            "data": return_data
        })


def kafka_data(key, request, target=None):
    if not request.user.is_authenticated():
        logger.error("not login !!!")
        return HttpResponse('Unauthorized', status=401)
    agent = request.user.userinfo.agent
    company = request.user.userinfo.company
    # from soc.models import Agent
    # agent = Agent.objects.get(id=2)
    # company = None
    try:
        servers = SelfServiceConf.objects.get(agent=agent, company=company, service='kafka')
        bootstrap_servers = servers.host
    except SelfServiceConf.DoesNotExist:
        msg = "no kafka"
        logger.error(msg)
        request.websocket.send(msg)
    c = KafkaConsumer(group_id="soc", bootstrap_servers=bootstrap_servers)  # hd-datanode2:9092
    # 指定偏移位读取数据 web_log_ip_map
    c.assign([TopicPartition(key, 0)])
    try:
        for message in c:
            try:
                return_data = json.loads(message.value)
            except (TypeError, ValueError):
                logger.error(message.value, 'message typeerror or valueerror')
            else:
                for data in return_data:
                    if target:
                        data['target_location'] = target
                    request.websocket.send(json.dumps(data))
    except Exception as e:
        logger.error(str(e))
        request.websocket.send('get kafka error!!')


@require_websocket
def business_visit_people(request):
    if not request.is_websocket():
        logger.error("not websocket !!!")
        return HttpResponse('not websocket !!!')
    else:
        kafka_data('realtime_uv', request, target=TARGET_LOCATION)


@require_websocket
def business_visit_map(request):
    if not request.is_websocket():
        logger.error("not websocket !!!")
        return HttpResponse('not websocket !!!')
    else:
        kafka_data('web_log_ip_map', request)
