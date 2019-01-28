# coding=utf-8

import logging
import datetime
from soc import models
from soc_ssa.models import SSAScoreSystem
from django.core.management.base import BaseCommand
from soc_ssa.views.ssa_views.es_common import get_es_data, cycle

logger = logging.getLogger('soc_ssa')


class Command(BaseCommand):
    def handle(self, *args, **options):
        """处理SSA作业
        """
        # 漏洞资产 ssa_score_system
        agents = models.Agent.objects.all()
        score_data = (datetime.datetime.now() - datetime.timedelta(days=1)).date()
        score_data = datetime.datetime.strftime(score_data, '%Y-%m-%d')
        for agent in agents:
            hole_assets_number = hole_assets(agent, None)
            hole_serious_number = hole_serious(agent, None)
            trojan_number = trojan(agent, None)
            attack_number = attack(agent, None)
            business_health_number = business_health(agent, None)
            business_visit_number = business_visit(agent, None)
            security_mark = 0.15 * hole_assets_number + 0.25 * hole_serious_number + 0.20 * attack_number + 0.20 * trojan_number + 0.10 * business_health_number + 0.10 * business_visit_number
            obj, status = SSAScoreSystem.objects.get_or_create(agent=agent, score_date=score_data)
            obj.hole_assets = hole_assets_number
            obj.hole_serious = hole_serious_number
            obj.trojan = trojan_number
            obj.attack = attack_number
            obj.business_health = business_health_number
            obj.business_visit = business_visit_number
            obj.security_mark = int(security_mark)
            obj.save()


def business_visit(agent, company):
    """
    业务访问指数
    攻击接口返回值 200 400 500之类  ==>TODO   
    """

    start_time = (datetime.datetime.now() - datetime.timedelta(days=1)).date()
    str_start_time = datetime.datetime.strftime(start_time, '%Y-%m-%d') + ' 00:00:00'
    end_time = (datetime.datetime.now() - datetime.timedelta(days=0)).date()
    str_end_time = datetime.datetime.strftime(end_time, '%Y-%m-%d') + ' 00:00:00'
    body = {
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {"key": "web-log-http_status_count"}
                    }, {
                        "range": {"time": {"gte": str_start_time}}
                    },
                    {
                        "range": {"time": {"lt": str_end_time}}
                    }
                ]
            }
        },
        "aggs": {
            "mydata": {
                "terms": {
                    "field": "data.web_log_host",
                    "size": 0,
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
    # 先取出访问量最大的网站 再分辨算出网站具体访问状态的数据
    for domain in domains:
        body = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {"key": "web-log-http_status_count"}
                        }, {
                            "range": {"time": {"gte": str_start_time}}
                        }, {
                            "match": {"data.web_log_host": domain}
                        },
                        {
                            "range": {"time": {"lt": str_end_time}}
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
    total = 0
    success = 0
    for domain in domains:
        total += domain_dict[domain]['2xx'] + domain_dict[domain]['3xx'] + domain_dict[domain]['4xx'] + \
                 domain_dict[domain]['5xx']
        success += domain_dict[domain]['2xx']
    if total:
        return int(float(success) / total * 100)
    return 0


def business_health(agent, company):
    """业务流康指数"""
    # 攻击流量小于基础流量为100分 大于最大流量为0分 中间线性变化
    max_fow = 10 * 1024   # 评分为0的流量上线 10G
    base_flow = 1      # 基础流量 1M
    start_time = (datetime.datetime.now() - datetime.timedelta(days=1)).date()
    str_start_time = datetime.datetime.strftime(start_time, '%Y-%m-%d') + ' 00:00:00'
    end_time = (datetime.datetime.now() - datetime.timedelta(days=0)).date()
    str_end_time = datetime.datetime.strftime(end_time, '%Y-%m-%d') + ' 00:00:00'
    body = {
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {"key": "anti-ddos-max_throughput"}
                    },
                    {
                        "range": {"time": {"gte": str_start_time}}
                    },
                    {
                        "range": {"time": {"lt": str_end_time}}
                    }
                ]
            }
        },
        "sort": {"time": {"order": "desc"}},
        "aggs": {
            "mydata": {
                "date_histogram": {
                    "field": "time",
                    "interval": "hour",
                    "format": "yyyy-MM-dd HH:mm:ss",
                    "min_doc_count": 0,
                    "extended_bounds": {
                        "min": str_start_time,
                        "max": str_end_time
                    }
                },
                "aggs": {
                    "mycount": {
                        "sum": {"field": "data.anti_ddos_max_throughput"}
                    }
                }
            }
        }
    }
    result = get_es_data(body, size=0)
    x = []
    y = []
    if result.get('aggregations') and result.get('aggregations').get('mydata') and result.get('aggregations').get(
            'mydata').get("buckets"):
        data = result.get('aggregations').get('mydata').get("buckets")
        for da in data:
            x.append(da.get('key_as_string'))
            y.append(da.get('mycount').get('value'))
    max_y = max(y)
    max_y = float(max_y) / (1024 * 1024)
    if max_y < base_flow:
        business_health_number = 100
    elif max_y > max_fow:
        business_health_number = 0
    else:
        business_health_number = 80.0078 - 0.0078*max_y
    return int(business_health_number)


def attack(agent, company):
    """攻击指数"""
    start_time = (datetime.datetime.now() - datetime.timedelta(days=1)).date()
    str_start_time = datetime.datetime.strftime(start_time, '%Y-%m-%d') + ' 00:00:00'
    end_time = (datetime.datetime.now() - datetime.timedelta(days=0)).date()
    str_end_time = datetime.datetime.strftime(end_time, '%Y-%m-%d') + ' 00:00:00'
    body = {
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {"key": "security-source_count"}
                    },
                    {
                        "range": {"time": {"gte": str_start_time}}
                    },
                    {
                        "range": {"time": {"lt": str_end_time}}
                    }
                ]
            }
        },
        "aggs": {
            "mydata": {
                "terms": {"field": "data.security_src_ip"}
            }
        }
    }
    result = get_es_data(body, size=0)
    attack_total = 0
    if result.get('aggregations') and result.get('aggregations').get('mydata') and result.get("aggregations").get(
            "mydata").get("buckets"):
        data = result.get("aggregations").get("mydata").get("buckets")
        attack_total = len(data)
    attack_num = 0
    net_device_count = models.NetDevice.objects.filter(idc__agent=agent, company=company).count()
    server_count = models.Server.objects.filter(idc__agent=agent, company=company).count()
    terminal_count = models.Terminal.objects.filter(asset__agent=agent, company=company).count()
    total_assets = net_device_count + server_count + terminal_count
    if total_assets:
        attack_num = float(attack_total) / total_assets
        if attack_num>1:
            attack_num = 1
            logger.warning("this user who 'agent_id={0}'  attack_num is more than total_assets !!!".format(agent.id))
    return 100 - int(attack_num * 100)


def trojan(agent, company):
    """僵木蠕指数"""
    start_time = (datetime.datetime.now() - datetime.timedelta(days=1)).date()
    str_start_time = datetime.datetime.strftime(start_time, '%Y-%m-%d') + ' 00:00:00'
    end_time = (datetime.datetime.now() - datetime.timedelta(days=0)).date()
    str_end_time = datetime.datetime.strftime(end_time, '%Y-%m-%d') + ' 00:00:00'
    body = {
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {"key": "virus-asset_top"}
                    },
                    {
                        "range": {"time": {"gte": str_start_time}}
                    },
                    {
                        "range": {"time": {"lt": str_end_time}}
                    }
                ]
            }
        },
        "aggs": {
            "mydata": {
                "terms": {"field": "data.virus_host_ip"}
            }
        }
    }
    result = get_es_data(body, size=0)
    trojan_total = 0
    if result.get('aggregations') and result.get('aggregations').get('mydata') and result.get("aggregations").get(
            "mydata").get("buckets"):
        data = result.get("aggregations").get("mydata").get("buckets")
        trojan_total = len(data)

    net_device_count = models.NetDevice.objects.filter(idc__agent=agent, company=company).count()
    server_count = models.Server.objects.filter(idc__agent=agent, company=company).count()
    terminal_count = models.Terminal.objects.filter(asset__agent=agent, company=company).count()
    total_assets = net_device_count + server_count + terminal_count
    trojan_total_num = 0
    if total_assets:
        trojan_total_num = float(trojan_total) / total_assets
        if trojan_total_num>1:
            trojan_total_num = 1
            logger.warning("this user who 'agent_id={0}'  trojan_total_num is more than total_assets !!!".format(agent.id))
    return 100 - int(trojan_total_num * 100)


def hole_serious(agent, company):
    "漏洞严重指数"
    start_time = (datetime.datetime.now() - datetime.timedelta(days=1)).date()
    str_start_time = datetime.datetime.strftime(start_time, '%Y-%m-%d') + ' 00:00:00'
    end_time = (datetime.datetime.now() - datetime.timedelta(days=0)).date()
    str_end_time = datetime.datetime.strftime(end_time, '%Y-%m-%d') + ' 00:00:00'

    body = {
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {"key": "vul-vul_level_count"}
                    },
                    {
                        "range": {"time": {"gte": str_start_time}}
                    },
                    {
                        "range": {"time": {'lt': str_end_time}}
                    }
                ]
            }
        },
        "aggs": {
            "mydata": {

                "terms": {
                    "field": "data.vul_level",
                    "size": 0,
                    "order": {
                        "mycount.value": "desc"
                    }
                },
                "aggs": {
                    "mycount": {
                        "sum": {"field": "data.count"}
                    }
                }
            }
        }
    }

    result = get_es_data(body, size=0)
    serious = 0
    total = 0
    if result.get('aggregations') and result.get('aggregations').get('mydata') and result.get("aggregations").get(
            "mydata").get("buckets"):
        data = result.get("aggregations").get("mydata").get("buckets")
        for da in data:
            if da.get('key') == '严重':
                serious += da.get('mycount').get('value')
            total += da.get('mycount').get('value')
    if total:
        hole_serious_num = float(serious) / total
        return 100 - int(hole_serious_num * 100)
    return 100


def hole_assets(agent, company):
    "漏洞资产指数"
    net_device_count = models.NetDevice.objects.filter(idc__agent=agent, company=company).count()
    server_count = models.Server.objects.filter(idc__agent=agent, company=company).count()
    terminal_count = models.Terminal.objects.filter(asset__agent=agent, company=company).count()
    total_assets = net_device_count + server_count + terminal_count

    start_time = (datetime.datetime.now() - datetime.timedelta(days=1)).date()
    str_start_time = datetime.datetime.strftime(start_time, '%Y-%m-%d') + ' 00:00:00'

    end_time = (datetime.datetime.now() - datetime.timedelta(days=0)).date()
    str_end_time = datetime.datetime.strftime(end_time, '%Y-%m-%d') + ' 00:00:00'
    body = {
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {"key": "vul-vul_total_count"}
                    }, {
                        "range": {"time": {"gte": str_start_time}}
                    },
                    {
                        "range": {"time": {"lt": str_end_time}}
                    }
                ]
            }
        },

        "sort": {"time": {"order": "desc"}},
    }
    result = get_es_data(body, size=24)
    data = result.get("hits").get('hits')
    hole_total = 0
    for source in data:
        if source.get("_source") and source.get("_source").get('data'):
            es_data = source.get("_source").get('data')
            hole_total = hole_total + es_data.get("vul_total_count")
    hole_assets_num = 0
    if total_assets:
        hole_assets_num = float(hole_total) / total_assets
        if hole_assets_num > 1:
            hole_assets_num = 1
            logger.warning("this user who 'agent_id={0}'  hole_total is more than total_assets !!!".format(agent.id))
    return 100 - int(hole_assets_num * 100)
