# coding: utf-8

import datetime
from soc import models
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from .es_common import get_cycle, get_es_data, business_es_body, cycle, get_str_now, get_aggs_sum_data, global_es_data


class SourceHole(APIView):
    """资源态势感知"""

    def get(self, request):
        """漏洞统计"""
        start_time = get_cycle()
        end_time = get_str_now()
        hole_total = get_aggs_sum_data(key='vul-vul_total_count', field='data.vul_total_count', start_time=start_time,
                                       end_time=end_time)  # 总漏洞数

        body = business_es_body('vul-vul_ip_count', 'data.vul_ip', start_time=start_time, end_time=end_time)
        result = get_es_data(body, size=0)
        x = []  # 漏洞IP分类
        y = []  # 漏洞IP分类后的总数
        if result.get('aggregations') and result.get('aggregations').get('mydata') and result.get("aggregations").get(
                "mydata").get("buckets"):
            data = result.get("aggregations").get("mydata").get("buckets")
            for da in data:
                x.append(da.get('key'))
                y.append(da.get('mycount').get('value'))
        x = x + ['' for i in range(5)]
        y = y + [0 for i in range(5)]
        x = x[:5]
        y = y[:5]

        # agent = request.user.userinfo.agent
        # company = request.user.userinfo.company
        # net_device_count = models.NetDevice.objects.filter(idc__agent=agent, company=company).count()
        # server_count = models.Server.objects.filter(idc__agent=agent, company=company).count()
        # terminal_count = models.Terminal.objects.filter(asset__agent=agent, company=company).count()
        data = {
            "hole_total": hole_total,  # 总漏洞数
            # "asset_total": net_device_count + server_count + terminal_count,  # 资产总数
            # "proportion": round(float(hole_total)*100/(net_device_count + server_count + terminal_count), 4),  # 资产漏洞占比
            "data": {
                "x": x,
                "y": y
            }
        }
        return Response({
            "status": 200,
            "msg": "获取数据成功",
            "data": data
        })


class SourceHoleRating(APIView):
    """资源态势感知"""

    def get(self, request):
        """漏洞严重级别"""
        body = business_es_body('vul-vul_level_count', 'data.vul_level')
        result = get_es_data(body, size=0)
        return_data = []
        if result.get('aggregations') and result.get('aggregations').get('mydata') and result.get("aggregations").get(
                "mydata").get("buckets"):
            data = result.get("aggregations").get("mydata").get("buckets")
            for da in data:
                if da.get('key') == 'info':
                    continue
                return_data.append({"name": da.get("key"), "value": da.get("mycount").get('value')})
        return Response({
            "status": 200,
            "msg": "获取数据成功",
            "data": return_data[:6]
        })


class SourceHoleClass(APIView):
    """资源态势感知"""

    def get(self, request):
        """漏洞类别"""
        body = business_es_body("vul-vul_threat_type_count", "data.vul_threat_type")
        result = get_es_data(body, size=0)
        return_data = []
        if result.get('aggregations') and result.get('aggregations').get('mydata') and result.get("aggregations").get(
                "mydata").get("buckets"):
            data = result.get("aggregations").get("mydata").get("buckets")
            for da in data:
                return_data.append({"name": da.get("key"), "value": da.get("mycount").get('value')})
        return Response({
            "status": 200,
            "msg": "获取数据成功",
            "data": return_data[:6]
        })


class SourceBusinessRisk(APIView):
    """资源态势感知"""

    def get(self, request):
        """风险业务网站统计"""
        start_time = get_cycle()
        end_time = get_str_now()
        body = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {"key": "vul-vul_risk_url_count"}
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
                        "field": "data.vul_threat_type"
                    },
                    "aggs": {
                        "mycount": {
                            "terms": {
                                "field": "data.vul_risk_url"
                            },
                            "aggs": {
                                "count": {"sum": {"field": "data.count"}}
                            }
                        }
                    }
                }
            }
        }
        return_data = []
        result = get_es_data(body, size=0)
        if result.get('aggregations') and result.get('aggregations').get('mydata') and result.get("aggregations").get(
                "mydata").get("buckets"):
            data = result.get("aggregations").get("mydata").get("buckets")
            for da in data:
                for d in da.get('mycount').get('buckets'):
                    temp = {"domain": d.get("key"), "status": da.get('key'), "count": d.get("count").get("value")}
                    return_data.append(temp)
        return_data = sorted(return_data, key=lambda b: b["count"], reverse=True)[:5]
        return Response({
            "status": 200,
            "msg": "获取数据成功",
            "data": return_data
        })


class SourceWeak(APIView):
    """资源态势感知"""

    def get(self, request):
        """主机弱口令统计"""
        start_time = get_cycle()
        end_time = get_str_now()
        body = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {"key": "weak-password-host_count"}
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
                        "field": "data.weak_password_protocol"
                    },
                    "aggs": {
                        "mycount": {
                            "terms": {
                                "field": "data.weak_password_ip"
                            },
                            "aggs": {
                                "count": {"sum": {"field": "data.count"}}
                            }
                        }
                    }
                }
            },
        }
        return_data = []
        result = get_es_data(body, size=0)
        if result.get('aggregations') and result.get('aggregations').get('mydata') and result.get("aggregations").get(
                "mydata").get("buckets"):
            data = result.get("aggregations").get("mydata").get("buckets")
            for da in data:
                for d in da.get('mycount').get('buckets'):
                    temp = {"ip": d.get("key"), "protocal": da.get('key'), "count": d.get("count").get("value")}
                    return_data.append(temp)
        return_data = sorted(return_data, key=lambda b: b["count"], reverse=True)[:5]
        return Response({
            "status": 200,
            "msg": "获取数据成功",
            "data": return_data
        })


class SourceSourceRisk(APIView):
    """资源态势感知"""

    def get(self, request):
        """资产和风险分布"""
        agent = request.user.userinfo.agent
        company = request.user.userinfo.company
        locations = {"未知":0}
        locations_ip = {"未知":[]}
        # 做一个location_ip = {"济南":[ip1,ip2,ip3]} 方便后面查询ip的地理位置

        def get_location(locations, locations_ip, models, idcs):

            for idc in idcs:
                if models == 'server':
                    host_list = idc.server_set.all()
                elif models == 'netdevice':
                    host_list = idc.netdevice_set.all()
                else:
                    host_list = idc.terminal_set.all()
                if not idc.location:
                    locations['未知'] = locations['未知'] + idc.mynum
                    locations_ip['未知'] = locations_ip['未知'] + [x.ip for x in host_list]
                else:
                    if idc.location.name not in locations:
                        locations[idc.location.name] = 0
                        locations_ip[idc.location.name] = []
                    locations[idc.location.name] = locations[idc.location.name] + idc.mynum
                    locations_ip[idc.location.name] = locations_ip[idc.location.name] + [x.ip for x in host_list]

        idcs = models.Idc.objects.filter(agent=agent).annotate(mynum=Count("netdevice"))
        get_location(locations, locations_ip, 'netdevice', idcs)
        idcs = models.Idc.objects.filter(agent=agent).annotate(mynum=Count("server"))
        get_location(locations, locations_ip, 'server', idcs)
        groups = models.AssetGroup.objects.filter(agent=agent).annotate(mynum=Count("terminal"))
        get_location(locations, locations_ip, 'terminal', groups)

        source = []
        for lo in locations:
            source.append({"name": lo, "value": locations[lo]})
        start_time = get_cycle()
        end_time = get_str_now()
        body = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {"key": "vul-vul_ip_count"}
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
                    "terms": {"field": "data.vul_ip"}
                }
            },
        }

        locations = {"未知":0}
        result = get_es_data(body=body, size=0)
        if result.get('aggregations') and result.get('aggregations').get('mydata') and result.get("aggregations").get(
                "mydata").get("buckets"):
            data = result.get("aggregations").get("mydata").get("buckets")
            for da in data:
                no_lo = True
                for ips in locations_ip:
                    # 从 locations_ip里查询ip位置 如果没查到  归为未知IP
                    if ips not in locations:
                        locations[ips] = 0
                    if da.get('key') in locations_ip[ips]:
                        locations[ips] = locations[ips] + 1
                        no_lo = False
                        break
                if no_lo:
                    locations['未知'] += 1
        risk = []
        for lo in locations:
            risk.append({"name": lo, "value": locations[lo]})
        data = {
            "source": source,
            "risk": risk,
        }
        # data = {
        #     "source": [
        #         {"name": "济南", "value": 89},
        #         {"name": "聊城", "value": 65},
        #     ],
        #     "risk": [
        #         {"name": "青岛", "value": 39},
        #         {"name": "烟台", "value": 55},
        #     ]
        # }
        return Response({
            "status": 200,
            "msg": "获取数据成功",
            "data": data
        })
