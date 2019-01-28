# coding: utf-8

import logging
import datetime
from soc import models
from django.utils import timezone
from soc.settings import SSA_COMPANY
from rest_framework.views import APIView
from soc_ssa.models import SSAScoreSystem
from rest_framework.response import Response
from .es_common import get_cycle, get_es_data, business_es_body, cycle, get_str_now, get_aggs_sum_data, global_es_data


logger = logging.getLogger('soc_ssa')


class GlobalSecurityOverview(APIView):
    """全局态势感知"""

    def get(self, request):
        """安全总览
        评分不是100分就认为存在风险
        """
        agent = request.user.userinfo.agent
        score_date = (datetime.datetime.now() - datetime.timedelta(days=1)).date()
        scores = SSAScoreSystem.objects.filter(agent=agent, score_date=score_date)
        security_mark = 0
        business_situation = 0
        business_visit = 0
        if scores:
            score = scores[0]
            security_mark = score.security_mark
            business_visit = score.business_visit
            business_health = score.business_health
            business_situation = (business_visit+business_health)/2
        data = {
            "security_mark": security_mark,
            "security_situation": "安全" if int(security_mark) > 99 else "存在风险",
            "business_situation": "正常" if (business_situation + business_visit) / 2 > 99 else '风险',
            "ssa_company": SSA_COMPANY,
        }
        return Response({
            "status": 200,
            "msg": "获取数据成功",
            "data": data
        })


class GlobaldangerRating(APIView):
    """全局态势感知"""

    def get(self, request):
        """危险等级比例"""
        agent = request.user.userinfo.agent
        score_date = (datetime.datetime.now() - datetime.timedelta(days=1)).date()
        score = SSAScoreSystem.objects.filter(agent=agent, score_date=score_date)
        data = {
            "hole_assets": 0,
            "hole_serious": 0,
            "attack": 0,
            "trojan": 0,
            "business_health": 0,
            "business_visit": 0,
        }
        if score:
            data = {
                "hole_assets": score[0].hole_assets,
                "hole_serious": score[0].hole_serious,
                "attack": score[0].attack,
                "trojan": score[0].trojan,
                "business_health": score[0].business_health,
                "business_visit": score[0].business_visit,
            }
        return Response({
            "status": 200,
            "msg": "获取数据成功",
            "data": data
        })


class GlobalSituationTrend(APIView):
    """全局态势感知"""

    def get(self, request):
        """全网态势发展趋势"""
        agent = request.user.userinfo.agent
        x = []
        y = []
        for i in range(1, 8):
            score_date = (datetime.datetime.now() - datetime.timedelta(days=i)).date()
            x.append(timezone.datetime.strftime(score_date, "%Y-%m-%d"))
            scores = SSAScoreSystem.objects.filter(agent=agent, score_date=score_date)
            security_mark = 0
            if scores:
                security_mark = scores[0].security_mark
            y.append(security_mark)
        x = x[::-1]
        y = y[::-1]
        data = {
            "x": x,
            "y": y
        }

        return Response({
            "status": 200,
            "msg": "获取数据成功",
            "data": data
        })


class GlobalHoleCount(APIView):
    """全局态势感知"""

    def get(self, request):
        """漏洞统计"""
        key = 'vul-vul_total_count'
        field = 'data.vul_total_count'
        end_time = get_str_now()
        start_time = get_cycle()
        hole_total = get_aggs_sum_data(key, field, start_time, end_time)  # hole_total 本周期内的漏洞总数
        last_cycle_end_time = get_cycle()
        now = datetime.datetime.now()
        last_cycle_start_time = timezone.datetime.strftime(now - timezone.timedelta(hours=cycle * 2),
                                                           '%Y-%m-%d %H:%M:%S')
        hole_total_old = get_aggs_sum_data(key, field, last_cycle_start_time,
                                           last_cycle_end_time)  # hole_total 上周期内的漏洞总数

        body = business_es_body("vul-vul_level_count", "data.vul_level")
        result = get_es_data(body, size=0)
        severe = 0  # 严重漏洞个数
        if result.get('aggregations') and result.get('aggregations').get('mydata') and result.get('aggregations').get(
                'mydata').get("buckets"):
            data = result.get('aggregations').get('mydata').get("buckets")
            for da in data:
                if da.get('key') == '严重':
                    severe += da.get('mycount').get('value')

        body = business_es_body("vul-vul_ip_count", "data.vul_ip")
        result = get_es_data(body, size=0)
        hole_ip_count = 0
        if result.get('aggregations') and result.get('aggregations').get('mydata') and result.get('aggregations').get(
                'mydata').get("buckets"):
            data = result.get('aggregations').get('mydata').get("buckets")
            hole_ip_count = len(data)

        data = {
            "hole_count": hole_total,
            "hole_ratio": round(float(hole_total - hole_total_old) * 100 / hole_total_old,
                                2) if hole_total_old else 100,
            "severe": severe,
            "hole_ip_count": hole_ip_count,
        }
        return Response({
            "status": 200,
            "msg": "获取数据成功",
            "data": data
        })


class GlobalLoopholeTop5(APIView):
    """全局态势感知"""

    def get(self, request):
        """最新重大漏洞TOP5"""
        end_time = str(datetime.datetime.now())[:19]
        start_time = get_cycle()
        body = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {"key": "vul-vul_top"}
                        }, {
                            "range": {"time": {"gte": start_time}}
                        },
                        {
                            "match": {"data.vul_level": "严重"}
                        },
                        {
                            "range": {"time": {"lt": end_time}}
                        }
                    ]
                }
            },
            "sort": {"time": {"order": "desc"}},
        }
        result = get_es_data(body, size=5)
        data = result['hits']['hits']
        return_data = []
        for source in data:
            if source.get("_source") and source.get("_source").get('data'):
                es_data = source.get("_source").get('data')
                return_data.append({"name": es_data.get("vul_vuln_name"), "assets": es_data.get("vul_ip"),
                                    "status": es_data.get("vul_level")})
        return Response({
            "status": 200,
            "msg": "获取数据成功",
            "data": return_data
        })


class GlobalAttackNum(APIView):
    """全局态势感知"""

    def get(self, request):
        """攻击次数"""
        body = business_es_body("security-level_count", "data.security_level")
        return_data = []  # 统计严重高中低的次数 去掉info
        result = get_es_data(body, size=0)
        if result.get('aggregations') and result.get('aggregations').get('mydata') and result.get('aggregations').get(
                'mydata').get("buckets"):
            data = result.get('aggregations').get('mydata').get("buckets")
            for da in data:
                if da.get('key') == 'info':
                    continue
                return_data.append({"name": da.get('key'), "value": da.get("mycount").get('value')})

        key = "security-total_count"
        field = 'data.security_total_count'
        now = datetime.datetime.now()
        start_time = get_cycle()
        end_time = get_str_now()
        last_cycle_start_time = timezone.datetime.strftime(now - timezone.timedelta(hours=cycle * 2),
                                                           '%Y-%m-%d %H:%M:%S')
        last_cycle_end_time = start_time
        return_data_total = get_aggs_sum_data(key, field, start_time, end_time)  # 本周期攻击总次数
        return_data_old_total = get_aggs_sum_data(key, field, last_cycle_start_time, last_cycle_end_time)
        # 上周期攻击总次数
        data = {
            "total": return_data_total,
            "proportion": round(float(return_data_total - return_data_old_total) * 100 / return_data_total, 2),
            # 和上一周期比的比例 正负代表上升下降
            "data": return_data
        }
        return Response({
            "status": 200,
            "msg": "获取数据成功",
            "data": data
        })


class GlobalAttackSourceTotal(APIView):
    """全局态势感知"""

    def get(self, request):
        """攻击来源"""
        body = business_es_body("security-source_count", "data.security_src_ip_location")
        return_data = []
        x = []
        y = []
        result = get_es_data(body, size=0)
        if result.get('aggregations') and result.get('aggregations').get('mydata') and result.get('aggregations').get(
                'mydata').get("buckets"):
            data = result.get('aggregations').get('mydata').get("buckets")
            for da in data[:5]:
                x.append(da.get("key"))
                y.append(da.get("mycount").get("value"))
                temp = {'name': da.get("key"), 'value': da.get("mycount").get("value")}
                return_data.append(temp)
        x = x + ['' for i in range(5)]
        y = y + [0 for i in range(5)]
        x = x[:5]
        y = y[:5]
        return Response({
            "status": 200,
            "msg": "获取数据成功",
            "data": {
                "pie": return_data,
                "table": {
                    "x": x,
                    "y": y
                }
            }

        })


class GlobalWormNum(APIView):
    """全局态势感知"""

    def get(self, request):
        """蠕虫感染总数"""
        agent = request.user.userinfo.agent
        company = request.user.userinfo.company
        net_device_count = models.NetDevice.objects.filter(idc__agent=agent, company=company).count()
        server_count = models.Server.objects.filter(idc__agent=agent, company=company).count()
        terminal_count = models.Terminal.objects.filter(asset__agent=agent, company=company).count()
        asset_total = net_device_count + server_count + terminal_count
        # asset_total 资产总数
        body = business_es_body("virus-total_count", "time")
        result = get_es_data(body, size=0)
        worm_total = []
        if result.get('aggregations') and result.get('aggregations').get('mydata') and result.get('aggregations').get(
                'mydata').get("buckets"):
            data = result.get('aggregations').get('mydata').get("buckets")
            for da in data:
                worm_total.append(da.get('mycount').get('value'))
        # worm_total 最近一个周期的漏洞数

        last_cycle_end_time = get_cycle()
        now = datetime.datetime.now()
        last_cycle_start_time = timezone.datetime.strftime(now - timezone.timedelta(hours=cycle * 2), '%Y-%m-%d %H:%M:%S')
        body = business_es_body("virus-total_count", "time", start_time=last_cycle_start_time,end_time=last_cycle_end_time)
        result = get_es_data(body, size=0)
        worm_total_old = []  # worm_total_old 最近一个周期的漏洞数
        if result.get('aggregations') and result.get('aggregations').get('mydata') and result.get('aggregations').get(
                'mydata').get("buckets"):
            data = result.get('aggregations').get('mydata').get("buckets")
            for da in data:
                worm_total_old.append(da.get('mycount').get('value'))

        body = business_es_body("virus-asset_top", "data.virus_host_ip")
        result = get_es_data(body, size=0)
        worm_ips = []
        if result.get('aggregations') and result.get('aggregations').get('mydata') and result.get('aggregations').get(
                'mydata').get("buckets"):
            data = result.get('aggregations').get('mydata').get("buckets")
            worm_ips = len(data)
        # worm_ips 最近24小时感染蠕虫的IP总数

        if worm_ips > asset_total:
            logger.waring('worm_ips more than asset_total')
            worm_ips = asset_total
        proportion = round(float(worm_ips) / asset_total, 2)
        trend = 0
        if sum(worm_total_old):
            trend = round(float((sum(worm_total) - sum(worm_total_old)) * 100) / sum(worm_total_old), 2)
        data = {
            "worm_total": sum(worm_total),  # 最近周期的漏洞数
            "trend": trend,
            # 最近周期和上一个周期相比漏洞变化情况
            "proportion": proportion,  # 漏洞资产占总资产情况
        }
        return Response({
            "status": 200,
            "msg": "获取数据成功",
            "data": data
        })


def sum_25_to_9(a, b):
    # 每三个一组 后一个单独一组
    if not a or not b:
        return a, b
    new_a = [sum(a[i * 3:(i + 1) * 3]) for i in range(8)]
    new_b = [b[i * 3 + 2] for i in range(8)]
    new_a.append(a[-1])
    new_b.append(b[-1])
    return new_a, new_b


def max_25_to_9(a, b):
    # 每三个一组 后一个单独一组
    if not a or not b:
        return a, b
    new_a = [max(a[i * 3:(i + 1) * 3]) for i in range(8)]
    new_b = [b[i * 3 + 2] for i in range(8)]
    new_a.append(a[-1])
    new_b.append(b[-1])
    return new_a, new_b


def sum_25_to_12(a, b):
    # 每2个一组
    if not a or not b:
        return a, b
    a = a[1:]
    b = b[1:]
    new_a = [sum(a[i * 2:(i + 1) * 2]) for i in range(12)]
    new_b = [b[i * 2 + 1] for i in range(12)]
    return new_a, new_b


def max_25_to_12(a, b):
    if not a or not b:
        return a, b
    a = a[1:]
    b = b[1:]
    new_a = [max(a[i * 2:(i + 1) * 2]) for i in range(12)]
    new_b = [b[i * 2 + 1] for i in range(12)]
    return new_a, new_b


class GlobalAssetsOverview(APIView):
    """全局态势感知"""

    def get(self, request):
        """获取全局态势感知"""

        """资产总览"""
        x, y, count = global_es_data("network-throughput", "data.network_out_bytes")
        # y = map(b_to_mb, y)
        y, x = max_25_to_9(y, x)
        max_number = 0
        if y:
            max_number = max(y)
        network_export = {
            "count": max_number,
            "data": {
                'x': x,
                "y": y,
                "total": sum(y)
            }
        }
        x, y, count = global_es_data("ids-total_count", "data.count")
        y, x = sum_25_to_9(y, x)
        network_ids = {
            "count": sum(y),
            "data": {
                "x": x,
                "y": y,
                "total": sum(y)
            }
        }

        x, y, count = global_es_data("firewall-total_count", "data.count")
        y, x = sum_25_to_9(y, x)
        network_firewall = {
            "count": sum(y),
            "data": {
                "x": x,
                "y": y,
                "total": sum(y)
            }
        }

        x, y, count = global_es_data("anti-ddos-max_throughput", "data.anti_ddos_max_throughput")
        # y = map(b_to_mb, y)
        y, x = sum_25_to_9(y, x)
        max_number = 0
        if y:
            max_number = max(y)
        network_ddos = {
            "count": max_number,
            "data": {
                "x": x,
                "y": y,
                "total": sum(y)
            }
        }

        x, y, count = global_es_data("vul-vul_total_count", "data.vul_host_total_count")
        y, x = sum_25_to_12(y, x)
        server_hole = {
            "count": sum(y),
            "data": {
                "x": x,
                "y": y,
                "total": sum(y)
            }
        }

        x, y, count = global_es_data("virus-total_count", "data.count")
        y, x = sum_25_to_12(y, x)
        server_viruses = {
            "count": sum(y),
            "data": {
                "x": x,
                "y": y,
                "total": sum(y)
            }
        }

        x, y, count = global_es_data("weak-password-host_count", "data.count")
        y, x = sum_25_to_12(y, x)
        server_weak_password = {
            "count": sum(y),
            "data": {
                "x": x,
                "y": y,
                "total": sum(y)
            }
        }
        x, y, count = global_es_data("waf-total_count", "data.count")
        y, x = sum_25_to_12(y, x)
        application_waf = {
            "count": sum(y),
            "data": {
                "x": x,
                "y": y,
                "total": sum(y)
            }
        }
        x, y, count = global_es_data("vul-vul_total_count", "data.vul_severe_total_count")
        y, x = sum_25_to_12(y, x)
        application_hole = {
            "count": sum(y),
            "data": {
                "x": x,
                "y": y,
                "total": sum(y)
            }
        }

        x, y, count = global_es_data("db-audit-total_count", "data.count")
        y, x = sum_25_to_12(y, x)
        application_database = {
            "count": sum(y),
            "data": {
                "x": x,
                "y": y,
                "total": sum(y)
            }
        }
        data = {
            "network": {
                "export": network_export,
                "ids": network_ids,
                "firewall": network_firewall,
                "ddos": network_ddos
            },
            "server": {
                "hole": server_hole,
                "viruses": server_viruses,
                "weak_password": server_weak_password
            },
            "application": {
                "waf": application_waf,
                "hole": application_hole,
                "database": application_database
            }
        }
        return Response({
            "status": 200,
            "msg": "获取数据成功",
            "data": data
        })


class GlobalAttackRating(APIView):
    """全局态势感知"""

    def get(self, request):
        """攻击严重比例"""
        start_time = get_cycle()
        end_time = get_str_now()
        body = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {"key": 'security-level_count'}
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
                    "date_histogram": {
                        "field": "time",
                        "interval": "hour",
                        "format": "yyyy-MM-dd HH:mm:ss",
                        "min_doc_count": 0,
                        "extended_bounds": {
                            "min": start_time,
                            "max": end_time
                        }
                    },
                    "aggs": {
                        "mycount": {
                            "terms": {
                                "field": "data.security_level"
                            },
                            "aggs": {
                                "count": {"sum": {"field": "data.count"}}
                            }
                        }
                    }
                }
            }
        }
        return_data = {}
        result = get_es_data(body, size=0)
        if result.get('aggregations') and result.get('aggregations').get('mydata') and result.get('aggregations').get(
                'mydata').get("buckets"):
            data = result.get('aggregations').get('mydata').get("buckets")
            for da in data:
                return_data[da.get('key_as_string')] = {
                    "serious": 0,
                    "high": 0,
                    "middle": 0,
                    "low": 0,
                    "info": 0
                }
                for d in da.get("mycount").get("buckets"):
                    if d.get('key') == "info":
                        return_data[da.get('key_as_string')]['info'] += d.get('count').get("value")
                    elif d.get("key") == '严重':
                        return_data[da.get('key_as_string')]['serious'] += d.get('count').get("value")
                    elif d.get("key") == "高":
                        return_data[da.get('key_as_string')]['high'] += d.get('count').get("value")
                    elif d.get("key") == '中':
                        return_data[da.get('key_as_string')]['middle'] += d.get('count').get("value")
                    elif d.get("key") == '低':
                        return_data[da.get('key_as_string')]['low'] += d.get('count').get("value")
        data1 = [{"time": key, "value": return_data[key]} for key in return_data]
        data1 = sorted(data1, key=lambda b: b["time"])
        x = []
        serious = []
        high = []
        middle = []
        low = []
        info = []
        for da in data1:
            x.append(da.get('time'))
            serious.append(da.get('value').get('serious'))
            high.append(da.get('value').get('high'))
            middle.append(da.get('value').get('middle'))
            low.append(da.get('value').get('low'))
            info.append(da.get('value').get('info'))
        return Response({
            "status": 200,
            "msg": "获取数据成功",
            "data": {
                "x": x,
                "serious": serious,
                "high": high,
                "middle": middle,
                "low": low,
            }
        })
