# coding=utf-8
from datetime import datetime

from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
# from datetime import datetime

from soc_ssa import models
from soc_ssa.serializers import IpEventSerializer, EventSerializer, EventLineSerializer
from soc_ssa.ssa_common import prase_event_result
from utils.es_select import exec_es_sql, exec_es_sql_total
import requests
from hashlib import md5
from django.conf import settings
import time
import json

"""
事件时间线，暂定移植安审事件时间线逻辑
数据当前不够完善。暂定接口。
"""

EVENT_TYPE = {
    "acc": u"网络访问",
    "opr": u"操作记录",
    "sec": u"安全预警",
    "auth": u"认证总数",
    "stat": u"系统状态",
    "malware": u"恶意代码",
    "fault": u"设备故障",
    "spy": u"信息刺探",
    "att": u"攻击入侵",
    "other": u"其他",
    "harm": u"信息危害",
    "monitor": u"信息监控"
}


ANOMALY_TYPE = {
    "acc": {"event_type": u"网络访问", "desc": u"一般的网络访问事件"},
    "acc_session": {"event_type": u"网络访问/会话连接", "desc": u"网络访问时出现的链接请求"},
    "acc_suspicious": {"event_type": u"网络访问/可疑访问", "desc": u"出现了可疑的网络访问请求"},
    "acc_illegal": {"event_type": u"网络访问/违规访问", "desc": u"出现了不合规的网络访问请求"},
    "acc_normal": {"event_type": u"网络访问/正常访问", "desc": u"正常的网络请求"},
    "acc_other": {"event_type": u"网络访问/其他", "desc": u"其他类别的网络请求内容"},
    "opr": {"event_type": u"操作记录", "desc": u"记录某些用户或系统的操作内容"},
    "opr_cfg": {"event_type": u"操作记录/系统维护", "desc": u"对系统进行维护的信息"},
    "opr_db": {"event_type": u"操作记录/数据操作", "desc": u"对数据进行操作的内容"},
    "sec": {"event_type": u"安全预警", "desc": u"安全设备（软件）给出的预警信息"},
    "sec_other": {"event_type": u"安全预警/病毒预警", "desc": u"上报有关病毒信息的预警内容"},
    "sec_leak": {"event_type": u"安全预警/漏洞预警", "desc": u"上报有关漏洞信息的预警内容"},
    "auth": {"event_type": u"认证授权", "desc": u"有关账号认证的信息"},
    "auth_authention": {"event_type": u"认证授权/安全认证", "desc": u"账号进行认证的动作"},
    "auth_accmgr": {"event_type": u"认证授权/账号管理", "desc": u"更改账号配置的信息"},
    "stat": {"event_type": u"系统状态", "desc": u"有关系统工作状态的信息"},
    "stat_info": {"event_type": u"系统状态/运行报告", "desc": u"系统、设备、软件上报的工作报告"},
    "stat_stop": {"event_type": u"系统状态/系统关闭或宕机", "desc": u"系统停止的信息"},
    "stat_conflict": {"event_type": u"系统状态/地址冲突", "desc": u"出现了冲突的IP地址"},
    "malware": {"event_type": u"恶意代码", "desc": u"上报有关恶意代码的相关信息"},
    "malware_botnet": {"event_type": u"恶意代码/僵尸软件", "desc": u"发现了僵尸软件相关的信息"},
    "malware_virus": {"event_type": u"恶意代码/病毒", "desc": u"发现了病毒相关的信息"},
    "malware_other": {"event_type": u"恶意代码/其他", "desc": u"其他类别的恶意代码"},
    "malware_worm": {"event_type": u"恶意代码/网络蠕虫", "desc": u"发现了蠕虫相关的信息"},
    "malware_trojan": {"event_type": u"恶意代码/木马", "desc": u"发现了木马相关的信息"},
    "fault_threshole": {"event_type": u"设备故障/阈值告警", "desc": u"触发了某些设备的阈值告警信息"},
    "fault_server": {"event_type": u"设备故障/服务故障", "desc": u"某些服务无法正常提供"},
    "spy": {"event_type": u"信息刺探", "desc": u"获取敏感内容以进行下一步攻击动作"},
    "spy_vuln": {"event_type": u"信息刺探/漏洞扫描", "desc": u"尝试扫描触发可能出现的漏洞"},
    "spy_port": {"event_type": u"信息刺探/服务探测", "desc": u"可能对服务相关端口进行了扫描"},
    "spy_net": {"event_type": u"信息刺探/网络扫描", "desc": u"尝试获取网络基本信息"},
    "att": {"event_type": u"攻击入侵", "desc": u"对系统发生攻击的动作"},
    "att_vul": {"event_type": u"攻击入侵/漏洞利用", "desc": u"发现利用漏洞进行的攻击动作"},
    "att_ddos": {"event_type": u"攻击入侵/拒绝服务", "desc": u"发现了拒绝服务攻击"},
    "att_pwd": {"event_type": u"攻击入侵/口令猜测", "desc": u"破解某些账户的密码"},
    "other": {"event_type": u"其他事件", "desc": u"其他事件"},
}


def get_score_level(score):
    """通过评分获取级别"""
    if score <= 0:
        lv = 1
    if 0 < score <= 25:
        lv = 2
    elif 25 < score <= 50:
        lv = 3
    elif 50 < score <= 75:
        lv = 4
    elif 75 < score <= 100:
        lv = 5
    else:
        lv = 5
    return lv


def get_index(tag):
    """
    获取事件index前缀
    :param tag:
    :return:
    """
    data_index = models.SECDataTag.objects.filter(id=tag).values("path", "diff_field", "diff_value").first()
    return data_index


def get_field_map(tag):
    """
    获取事件中的IP字段
    :param tag:
    :return:
    """
    ip_field = models.SECFieldMap.objects.filter(data_tag_id=tag).values("key", "name", "items", "field_priority").all()
    return ip_field


class EventIpList(APIView):
    """
    IP事件信息
    """

    def get(self, request):
        """
        查询人员信息
        """
        search = request.query_params.get("search")
        tag = request.query_params.get("data_tag")
        index = get_index(tag)
        base_sql = "select * from {}* ".format(index)
        where_sql = ""
        if search:
            where_sql = "where src_ip like '%%%s%%' " \
                        "or attack_user like '%%%s%%'" % (search, search)
        # 取前五
        query_sql = base_sql + where_sql + "limit 5"
        result = exec_es_sql(query_sql)
        data = []
        for i in result[:5]:
            data.append({
                "name": i.get('attack_user'),
                "ip": i.get('src_ip'),
                "port": i.get('src_port'),
                "location": i.get('attack_city'),
                "dst_ip": i.get('dst_ip'),
                "dst_port": i.get('dst_port'),
                "dst_location": i.get('attacked_city'),
                "ip_addr": "--",
                "device_type": "--",
                "device": "--",
                "asset": "--"
            })
        return Response({"status": 200, "msg": "成功", "data": data})


class EventIpDetail(APIView):
    """
    IP详情信息
    """

    def get(self, request):
        """
        查询人员信息
        """
        name = request.query_params.get("name")
        ip = request.query_params.get('ip')
        port = request.query_params.get('port')
        tag = request.query_params.get('tag')
        index = get_index(tag)
        # 查询
        sql = "select * from {}* where src_ip='%s' and src_port='%s' and attack_user='%s' limit 1".format(index)
        query_sql = sql % (ip, port, name)
        result = exec_es_sql(query_sql)
        if not result:
            return Response({"status": 500, "msg": "查询不到数据"})
        res = result[0]
        data = {
            "name": res.get('username'),
            "ip": res.get('src_ip'),
            "port": res.get('src_port'),
            "location": res.get('attack_city'),
            "dst_ip": res.get('dst_ip'),
            "dst_port": res.get('dst_port'),
            "dst_location": res.get('attacked_city'),
            "ip_addr": "--",
            "device_type": "--",
            "device": "--",
            "asset": "--"
        }
        return Response({"status": 200, "msg": "成功", "data": data})


# class IpScoreLine(APIView):
#     """
#     用户风险值曲线图
#     """
#
#     def fetch_today_score(self, ip, index):
#         """当天评分值"""
#         today = timezone.now().strftime("%Y-%m-%d")
#         sql = "select max(score) as score from {}* where src_ip={} and time > {} ".format(index, ip, today)
#         data = exec_es_sql(sql)
#         score = data[0].get('score', 0) if data else 0
#         return today, score
#
#     def parsed_data(self, data):
#         """
#         生成曲线图日期评分数据
#         data: [
#             {
#             "date": "2018-05-16",
#             "score": 21
#             },
#             {
#             "date": "2018-05-18",
#             "score": 30
#             },
#         ]
#         """
#         times = []
#         scores = []
#         min_date, max_date = "", ""
#
#         active_data = filter(lambda x: x['score'] > 0, data)
#         active_data = [i['date'] for i in active_data]
#         if active_data:
#             min_date = min(active_data)
#             max_date = max(active_data)
#
#         for i in data:
#             date = i['date']
#             score = i['score']
#             # 去重
#             if date in times:
#                 index = times.index(date)
#                 scores[index] = score
#             else:
#                 times.append(date)
#                 scores.append(score)
#         # 补漏
#         start_day = datetime.strptime(times[0], "%Y-%m-%d")
#         end_day = datetime.strptime(times[-1], "%Y-%m-%d")
#         days = (end_day - start_day).days
#         new_times = []
#         new_scores = []
#         for i in range(days + 1):
#             day = (start_day + timedelta(days=i))
#             day_str = day.strftime("%Y-%m-%d")
#             new_times.append(day_str)
#             if day_str in times:
#                 index = times.index(day_str)
#                 score = scores[index]
#             else:
#                 score = 0
#             score = math.ceil(score)
#             if score > 100:
#                 score = 100
#             new_scores.append(score)
#         return new_times, new_scores, min_date, max_date
#
#     def get(self, request):
#
#         query_time = request.query_params.get("days", 30)
#         src_ip = request.query_params.get("ip")
#         tag = request.query_params.get("tag")
#         index = get_index(tag)
#         start_time = timezone.now() - timedelta(days=query_time)
#         sql = "select date, max(score) as score from {}* where src_ip='%s' and date > '%s' group by date".format(index)
#         sql = sql % (src_ip, start_time)
#         data = exec_es_sql(sql)
#         today, today_score = self.fetch_today_score(src_ip, index)
#         data.append({"date": today, "score": today_score})
#         times, scores, first_day, last_day = self.parsed_data(data)
#         rsp_data = {
#             "times": times,
#             "first_day": first_day,
#             "last_day": last_day,
#             "scores": scores,
#             "now_score": today_score
#         }
#         return Response({"status": 200, "msg": "成功", "data": rsp_data})



class IpEventReport(APIView):
    """IP事件上报事件处置"""

    def post(self, request):
        serializer = IpEventSerializer(data=request.data)
        if not serializer.is_valid():
            errors = serializer.errors
            return Response({"status": 500, "msg": list(errors.items())})
        validated_data = serializer.validated_data
        # 整理上传数据
        warn_time = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        timestamp = str(int(time.time()))
        secret_token = md5(timestamp + settings.EVENT_TOKEN).hexdigest()
        level = validated_data.get("level")
        if 0 <= level <= 2:
            urgent_level = 1
            danger_level = 1
        else:
            urgent_level = 2
            danger_level = 2
        data = {
            "urgent_level": urgent_level,
            "danger_level": danger_level,
            "warn_time": warn_time,
            "secret_token": secret_token,
            "timestamp": timestamp
        }
        for k, v in validated_data.items():
            data[k] = v
        # 请求事件处置接口
        try:
            req = requests.post(settings.EVENT_REPORT_URL, data=data, timeout=3)
            if json.loads(req.content).get("return_code", 0) == 1:
                return Response({"status": 200, "msg": "上报事件成功"})
            else:
                return Response({"status": 200, "msg": "上报事件错误"})
        except Exception as e:
            return Response({"status": 500, "msg": "上报事件错误"})

# class EventTimeLineDts(APIView):
#     """
#     事件时间线
#     查询单个实体的事件信息
#     """
#
#     def base_data(self, data):
#         new_data = []
#         for item in data:
#             base_dict = dict()
#             event_dict = dict()
#             for k, v in item.items():
#                 if '_total' in k and v > 0:
#                     k_event = k.split('_total')[0]
#                     base_dict[k_event] = dict()
#
#             for k, v in item.items():
#                 if '_type' in k and v > 0:
#                     for bk in base_dict:
#                         if k.startswith(bk):
#                             base_dict[bk][k] = v
#                             break
#             event_dict['start_time'] = item['time']
#             event_dict['score'] = item['score']
#             event_dict['event'] = base_dict
#             new_data.append(event_dict)
#         return new_data
#
#
#     def parsed_data(self, data):
#         new_data = []
#         for item in data:
#             if "T" in item['start_time']:
#                 d = "T"
#             else:
#                 d = " "
#             if "@timestamp" in item:
#                 del item['@timestamp']
#             s_date, s_time = item['start_time'].split(d)
#             e_date, e_time = item['start_time'].split(d)
#             s_time = s_time.split(".")[0]
#             e_time = e_time.split(".")[0]
#             # 一个IP聚合后只有一个评分级别
#             level = get_score_level(item['score'])
#             event = item['event']
#             for k, v in event.items():
#                 event_type = EVENT_TYPE.get(k, '其它')
#                 event_item = []
#                 for i, j in v.items():
#                     time_event = dict()
#                     time_event['start_date'] = s_date
#                     time_event['start_time'] = s_time
#                     time_event['end_date'] = e_date
#                     time_event['end_time'] = e_time
#                     anomaly = ANOMALY_TYPE.get(i.split('_type')[0], {})
#                     time_event['anomaly_type'] = anomaly.get('event_type', '其它')
#                     time_event['count'] = j
#                     time_event['threat_level'] = level
#                     time_event['anomaly_desc'] = anomaly.get('desc', '其它')
#                     event_item.append(time_event)
#                 new_item = {
#                     "items": event_item,
#                     "start_date": s_date,
#                     "start_time": s_time,
#                     "event_type": event_type,
#                     "threat_level": level
#                 }
#                 new_data.append(new_item)
#
#         for i in new_data:
#             i['start_time'] = ":".join(i['start_time'].split(":")[:2])
#         return new_data
#
#     def post(self, request):
#         """
#         查询时间线
#         """
#         serializer = EventTimeLineSerializer(data=request.data)
#         if not serializer.is_valid():
#             errors = serializer.errors
#             return Response({"status": 500, "msg": list(errors.items())})
#         validated_data = serializer.validated_data
#         tag = validated_data.get('tag')
#         index = get_index(tag)
#         ip = validated_data.get('ip')
#         start = validated_data.get('start', 0)
#         length = validated_data.get('length', 10)
#         # 级别
#         min_level = validated_data.get('min_level', 0)
#         max_level = validated_data.get('max_level', 5)
#         # 操作类型
#         event_type = validated_data.get('event_type')
#         event_type_dict = dict()
#         for k, v in EVENT_TYPE.items():
#             event_type_dict[v] = k
#
#         wheres = []
#         wheres_sql = "select * from {}* where src_ip = '{}' ".format(index, ip)
#         if event_type and event_type != "全部操作":
#             event_str = event_type_dict.get(event_type, 'acc') + "*"
#             wheres_sql = "select {}, time, score from {}* where src_ip = '{}' ".format(event_str, index, ip)
#         if not min_level == 0:
#             min_score = min_level * 25
#             wheres.append("score >= {}".format(min_score))
#         if not max_level == 5:
#             max_score = max_level * 25
#             wheres.append("score <= {}".format(max_score))
#         if wheres:
#             wheres_sql = wheres_sql + " and " + " and ".join(wheres)
#         wheres_sql = wheres_sql + " order by time desc limit {}, {}".format(start, length)
#
#         data = exec_es_sql_total(wheres_sql)
#         total = data['total']
#         base_data = self.base_data(data['data_list'])
#         new_data = self.parsed_data(base_data)
#         return Response({
#             "status": 200,
#             "msg": "成功",
#             "data": new_data,
#             "recordsFiltered": total,
#             "recordsTotal": total})


def _generate_sql(query):
    """
    生成子语句
    """
    field = query.get('field')
    value = query.get('value', "")
    if not field:
        raise ValueError("筛选字段不能为空")
    if value == "":
        raise ValueError("筛选值不能为空")
    expression = query['expression']
    if expression == "!=":
        expression = "<>"
    if expression == "in":
        expression = " LIKE "
        value = "%{}%".format(value)
    return "{}{}'{}'".format(field, expression, value)


def generate_sql(ip_where, index_pre, querys, query_string):
    """
    生成SQL语句
    :param ip_where:
    :param index_pre:
    :param querys:
    :param query_string:
    :return:
    """
    sql_list = []
    if ip_where:
        sql_list.append(ip_where)
    if index_pre:
        sql_list.append(index_pre)

    # 处理关键字搜索
    if query_string:
        sql_list.append("q=query('{}')".format(query_string))
    # 处理条件搜索
    if querys:
        for query in querys:
            # 多个语句用OR合并
            if isinstance(query, list):
                _or_sqls = []
                for i in query:
                    _or_sql = _generate_sql(i)
                    _or_sqls.append(_or_sql)
                _sql = " OR ".join(_or_sqls)
                _sql = "({})".format(_sql)
            # 单个语句
            else:
                _sql = _generate_sql(i)

            sql_list.append(_sql)
    # 用AND 合并所有语句
    sql = " AND ".join(sql_list)
    if sql:
        sql = "WHERE {}".format(sql)
    return sql


class EventTimeLineInfo(APIView):
    """
    事件时间线信息
    """

    def base_data(self, data, event_fields, ip_field, time_field, event_type_infos):
        """
        处理数据
        :param data:
        :param event_fields:
        :param ip_field:
        :param time_field:
        :param event_type_infos:
        :return:
        """
        new_data = []
        for item in data:
            new_one_data = dict()
            new_data_tan = dict()
            new_one_data["event_name"] = "正常操作"

            # 处理字段翻译
            field_map_list = models.SECFieldMap.objects.filter(~Q(items=''), ~Q(items='[]'), ).values("items", "key")
            key_list = []
            for field_map in field_map_list:
                key_list.append(field_map['key'])
            for i in range(len(key_list)):
                desc_dict = json.loads(field_map_list[i]['items'])
                if key_list[i] in item:
                    if isinstance(desc_dict, list):
                        for desc in desc_dict:
                            if isinstance(desc['id'], int) and isinstance(item[key_list[i]], int) and desc['id'] \
                                    == item[key_list[i]]:
                                item[key_list[i]] = desc['name']
                                break
                            elif desc['id'] == item[key_list[i]]:
                                item[key_list[i]] = desc['name']
                                break

            for k, v in item.items():
                # 判断事件类型
                if k in event_type_infos['key']:
                    # 判断是什么事件
                    str = json.loads(event_type_infos.get("items"))
                    for i in str:
                        if v == i["id"]:
                            new_one_data["event_name"] = i["name"]
                            continue
                    continue
                # 标记时间字段
                if k == time_field:
                    new_one_data["time"] = v
                    continue
                # 标记被攻击方
                if ip_field and k == ip_field:
                    new_one_data["dst_ip"] = v
                    continue
                # 判断入库时间，去掉格式
                if k == "@timestamp":
                    v = v.replace("T", " ").replace("Z", "")


                # 字段名翻译
                if k in event_fields:
                    new_data_tan[event_fields.get(k, {"name": k})['name']] = v

                new_one_data['precedence'] = event_fields.get(k, {"precedence": 9}).get("precedence", 9)
                new_one_data['tran_data'] = new_data_tan

            new_data.append(new_one_data)
        return new_data

    def post(self, request):
        """
        事件时间线信息
        :param request:
        :return:
        """
        querys = self.request.data.get("query", "")
        query_string = self.request.data.get("query_string", "")
        serializer = EventSerializer(data=request.data)
        if not serializer.is_valid():
            errors = serializer.errors
            return Response({"status": 500, "msg": list(errors.items())})
        validated_data = serializer.validated_data
        start = validated_data.get("start")
        length = validated_data.get("length")
        # 事件地址
        ip = validated_data.get("ip")
        # 事件数据标签
        tag = validated_data.get("tag")
        # 事件时间
        event_time = validated_data.get("event_time")
        if len(event_time) == 19:
            time_value = datetime.strptime(str(event_time), "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
        else:
            time_value = datetime.strptime(str(event_time), "%Y%m%d%H%M%S").strftime("%Y-%m-%d")

        # 获取事件前缀
        event_index = get_index(tag)
        event_index_pre = "{}-{}".format(event_index["path"], time_value)
        # 获取事件字段标签对照信息
        event_field_map = get_field_map(tag)
        event_type_infos = event_field_map.filter(field_priority__contains="event").first()
        ip_field = event_field_map.filter(field_priority__contains="src_ip").values("key").first()['key']
        time_field = event_field_map.filter(field_priority__contains="time").values("key").first()['key']
        dst_ip_field = event_field_map.filter(field_priority__contains="dst_ip").values("key")
        if dst_ip_field:
            dst_ip_field = dst_ip_field.first()['key']
        else:
            dst_ip_field = ''
        event_fields = models.SECFieldMap.get_field_map(tag)
        # ip条件
        ip_where = '{} = "{}" '.format(ip_field, str(ip))

        # 同一个index，不同类型数据
        index_pre = ''
        if event_index["diff_field"] is not None and event_index['diff_field'] != '':
            index_pre = "{} = {}".format(event_index["diff_field"], event_index["diff_value"])
        sql = generate_sql(ip_where, index_pre, querys, query_string)

        wheres_sql = "select * from {}* {}".format(event_index_pre, sql)
        wheres_sql = wheres_sql + " order by {} desc limit {}, {}".format(time_field, start, length)
        data = exec_es_sql_total(wheres_sql)
        #data = prase_event_result(data)
        total = data['total']
        base_data = self.base_data(data['data_list'], event_fields, dst_ip_field, time_field, event_type_infos)
        return Response({
            "status": 200,
            "msg": "成功",
            "data": base_data,
            "recordsFiltered": total,
            "recordsTotal": total})


class IpScoreLine(APIView):
    """
    攻击次数曲线图
    """
    def post(self, request):
        """
        攻击次数折线图
        :param request:
        :return:
        """
        querys = self.request.data.get("query", "")
        query_string = self.request.data.get("query_string", "")
        serializer = EventLineSerializer(data=request.data)
        if not serializer.is_valid():
            errors = serializer.errors
            return Response({"status": 500, "msg": list(errors.items())})
        validated_data = serializer.validated_data
        event_time = validated_data.get("event_time")
        if len(event_time) == 19:
            time_value = datetime.strptime(str(event_time), "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
        else:
            time_value = datetime.strptime(str(event_time), "%Y%m%d%H%M%S").strftime("%Y-%m-%d")
        src_ip = validated_data.get("ip")
        tag = validated_data.get("tag")
        event_field_map = get_field_map(tag)
        ip_field = event_field_map.filter(field_priority__contains="src_ip").values("key").first()['key']
        time_field = event_field_map.filter(field_priority__contains="time").values("key").first()['key']
        event_index = get_index(tag)
        event_index_pre = "{}-{}".format(event_index["path"], time_value)
        ip_where = '{} = "{}" '.format(ip_field, str(src_ip))
        # 同一个index，不同类型数据
        index_pre = ''
        if event_index["diff_field"] is not None and event_index['diff_field'] != '':
            index_pre = "{} = {}".format(event_index["diff_field"], event_index["diff_value"])
        sql = generate_sql(ip_where, index_pre, querys, query_string)
        group_field = 'date_histogram(field="{}","interval"="hour",format="yyyy-MM-dd-HH")'.format(time_field)

        sql = 'select count(*) as total from {}* {} group by {} '.format(event_index_pre, sql, group_field)
        data = exec_es_sql(sql)
        for one_data in data:
            one_data.update(data_time=one_data.pop(group_field.replace('"', '')))

        return Response({"status": 200, "msg": "成功", "data": data})