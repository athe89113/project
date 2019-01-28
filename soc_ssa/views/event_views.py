# coding: utf-8
"""
事件检测
"""
import logging
from collections import Counter
from datetime import datetime
from elasticsearch import Elasticsearch

from django.conf import settings
from django.utils import timezone
from django.db.models import Q

from soc_ssa import models
from soc_knowledge.models import VulStore
from soc_ssa.models import SSADataTag
from utils.select2 import select2_filter
from rest_framework.views import APIView
from rest_framework.response import Response
from common import localtime_to_timestamp
from soc_ssa.ssa_common import prase_es_result, AGG_MAP, ESSQL, exec_elasticsearch_sql, prase_log_result

from utils.es_select import exec_es_sql


ES_HOSTS = settings.ELASTICSEARCH_HOSTS

es_hosts = ES_HOSTS
es = Elasticsearch(hosts=es_hosts)
ES_TIMEOUT = 60

logger = logging.getLogger("soc_ssa")


class FieldMapList(APIView):
    """
    字段信息
    """

    def get(self, request):
        """
        获取字段信息
        """
        data_tag_id = request.query_params.get('data_tag_id', '')
        if data_tag_id:
            field_map = models.SSAFieldMap.get_field_map(data_tag_id=data_tag_id)
        else:
            field_map = models.SSAFieldMap.get_field_map()
        return Response({"status": 200, "data": field_map, "msg": "获取数据成功"})


class SelectFilterSelect2(APIView):
    """事件检测"""

    def post(self, request):
        """获取事件检测字段"""
        data_tag = request.DATA.get('tag')
        agent = request.data.get("agent")
        company = request.data.get("company")
        try:
            data_tag = models.SSADataTag.objects.filter(
                Q(agent=agent, company=company) | Q(agent=None, company=None)).get(id=data_tag)
        except models.SSADataTag.DoesNotExist:
            return Response({"status": 500, "msg": "数据源错误"})
        mapping = es.indices.get_mapping(
            index="{}-*".format(data_tag.path)).values()
        if not mapping:
            return Response({"status": 500, "msg": "无数据", "items": []})
        mapping = mapping[-1]
        # 取第一个type
        try:
            mapping = mapping.values()[0].values()[0]['properties']
        except Exception:
            data = select2_filter(request, [])
            return Response(data)
        data_list = []
        field_map = models.SSAFieldMap.get_field_map(data_tag)
        for key, value in mapping.items():
            if key in field_map:
                if 'type' in value:
                    k_type = value['type']
                    if k_type == "long":
                        k_type = "int"
                    if k_type in ['keyword', 'text']:
                        k_type = "string"
                    data_list.append({
                        "id": key,
                        "type": k_type,
                        "name": field_map.get(key, {"name": key})['name'],
                        "precedence": field_map.get(key, {"precedence": 0}).get("precedence", 0),
                    })
                # else:
                #     for key1, value1 in value.items():
                #         for key2, value2 in value1.items():
                #             k_type = value2['type']
                #             if k_type == 'long':
                #                 k_type = 'int'
                #             if k_type in ['keyword', 'text']:
                #                 k_type = "string"
                #             data_list.append({
                #                 "id": key + '.' + key2,
                #                 "type": k_type,
                #                 "name": field_map.get(key + '.' + key2, {"name": key + '.' + key2})['name'],
                #                 "precedence": field_map.get(key + '.' + key2, {"precedence": 0}).get("precedence", 0),
                #             })
        data_list = sorted(
            data_list, key=lambda k: k['precedence'], reverse=True)
        data = select2_filter(request, data_list)
        return Response(data)


class SSAEventSearchBase(APIView):
    """
    事件监测
    """

    def _generate_sql(self, query):
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

    def generate_sql(self, querys, query_string, path, ip):
        """
        生成SQL语句
        """
        sql_list = []
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
                        _or_sql = self._generate_sql(i)
                        _or_sqls.append(_or_sql)
                    _sql = " OR ".join(_or_sqls)
                    _sql = "({})".format(_sql)
                # 单个语句
                else:
                    _sql = self._generate_sql(i)

                sql_list.append(_sql)
        # 用AND 合并所有语句
        sql = " AND ".join(sql_list)
        ip_param = {"ssa-ag-360": "host_ip", "ssa-ag-database": "server_ip,dev_ip,client_ip",
                    "ssa-ag-ids": "src_ip,source,dst_ip", "ssa-ag-fw": "src_ip,dst_ip,device_name",
                    "ssa-ag-all-terminal": "act_ip,term_ip,user_ip", "ssa-ag-bd": "src_ip,comp_ip,dst_ip",
                    "ssa-ag-gl": "src_ip,dst_ip"
                    }
        ip_sql = ""
        if ip:
            ip = ip.strip()
            ip_param_list = ip_param[path].split(',')
            ip_sql = "("
            length = len(ip_param_list) - 1
            for i, ip_param_name in enumerate(ip_param_list):
                operate_str = " or "
                if i == length:
                    operate_str = ")"
                ip_sql = ip_sql + ip_param_name + " = '" + ip + "'" + operate_str
        if sql and ip_sql:
            sql = sql + " and " + ip_sql
        elif ip_sql:
            sql = ip_sql
        if sql:
            param_name = self.request.data.get("param_name", "")
            if param_name:
                param_value = self.request.data.get("param_value", "")
                sql = sql + " and " + param_name + " = '" + param_value + "'"
        else:
            param_name = self.request.data.get("param_name", "")
            if param_name:
                param_value = self.request.data.get("param_value", "")
                sql = param_name + " = '" + param_value + "'"
        if sql:
            sql = "WHERE {}".format(sql)
        return sql

    def generate_index(self, start_time, end_time, data_tag, es_hosts):
        """
        生成需要搜索的indexs
        """
        es = Elasticsearch(hosts=es_hosts)
        all_indexs = es.indices.get_alias("*").keys()
        indexs = []
        while True:
            index = "{}-{}".format(data_tag, start_time.strftime("%Y-%m-%d-%H"))
            if index in all_indexs:
                indexs.append(index)
            start_time = start_time + timezone.timedelta(hours=1)
            if start_time > end_time:
                break
        return indexs

    def fetch_table_data(self, es_sql_url, sql, indexs, start, length, data_tag="", data_type=""):
        """
        查询表格数据
        """
        _sql = "select * from {} {} limit {}, {} ".format(", ".join(indexs), sql, start, length)
        is_ok, result = self.fetch_es(es_sql_url, _sql)
        if not is_ok:
            return is_ok, result
        all_count = result['hits']['total']
        return True, {"recordsTotal": all_count, "data": prase_log_result(result, data_tag, data_type)}

    def fetch_line_data(self, es_sql_url, sql, indexs, interval):
        """
        查询折线图数据
        """
        if interval == "day":
            date_format = "yyyy-MM-dd"
        elif interval == "hour":
            date_format = "MM-dd HH:mm"
        else:
            date_format = "HH:mm:ss"
        _sql = "select count(*) from {} {} " \
               "GROUP BY date_histogram(field='@timestamp', 'interval'='{}', 'format'='{}')" \
            .format(", ".join(indexs), sql, interval, date_format)
        is_ok, result = self.fetch_es(es_sql_url, _sql)
        if not is_ok:
            return is_ok, result
        result = prase_es_result(result)
        x = []
        y = []
        for i in result:
            if "key_as_string" in i:
                x.append(i['key_as_string'])
                y.append(i['COUNT(*)'])

        return True, {"times": x, "counts": y}

    def fetch_es(self, es_sql_url, sql):
        """
        查询ES
        """
        return exec_elasticsearch_sql(es_sql_url, sql)

    def parsed_post(self, request):
        """
        事件搜索
        """
        agent = request.user.userinfo.agent
        company = request.user.userinfo.company
        data_tag = request.data.get("data_tag")
        start_time = self.request.data.get("start_time")
        end_time = self.request.data.get("end_time")
        querys = self.request.data.get("query")
        query_string = self.request.data.get("query_string")
        ip = self.request.data.get("src_ip", "")


        try:
            es_host = models.SelfServiceConf.objects.get(agent=agent, company=company, service="es")
        except models.SelfServiceConf.DoesNotExist:
            raise ValueError("ES服务未配置")
        try:
            data_tag = models.SSADataTag.objects.filter(Q(agent=agent, company=company) |
                                                        Q(agent=None, company=None)).get(id=data_tag)
        except models.SSADataTag.DoesNotExist:
            raise ValueError("事件源错误")
        datetime_format = '%Y-%m-%d %H:%M:%S'
        # 时间为空，采用默认时间 最近1天
        if not any([start_time, end_time]):
            start_time = timezone.now() - timezone.timedelta(hours=1)
            end_time = timezone.now()
        else:
            try:
                start_time = timezone.get_current_timezone().localize(
                    datetime.strptime(start_time, datetime_format))
                end_time = timezone.get_current_timezone().localize(
                    datetime.strptime(end_time, datetime_format))
            # 时间格式错误
            except(ValueError, TypeError):
                raise ValueError("时间格式错误")

        indexs = self.generate_index(start_time, end_time, data_tag.path, es_host.host)
        if not indexs:
            raise ValueError("无数据")
        sql = self.generate_sql(querys, query_string, data_tag.path, ip)
        return start_time, end_time, es_host.host, sql, indexs, data_tag.path


class SSAEventSearchLine(SSAEventSearchBase):
    """
    事件搜索
    """

    def post(self, request):
        """
        图表接口
        """
        try:
            start_time, end_time, es_sql_url, sql, indexs, data_tag = self.parsed_post(request)
        except ValueError as e:
            return Response({"status": 500, "data": [], "msg": e.message})
        diff_time = (end_time - start_time)
        if diff_time > timezone.timedelta(days=7):
            interval = "day"
        elif diff_time > timezone.timedelta(hours=8):
            interval = "hour"
        else:
            interval = "minute"
        x = request.data.get("x")
        y = request.data.get("y")
        query_time = request.data.get("query_time", 30)

        if x and y:
            es_sql = ESSQL(userinfo=request.user.userinfo,
                           indices=indexs,
                           x=x,
                           y=y,
                           ssa_data_tag=data_tag,
                           query_time=query_time)
            try:
                is_ok, data = es_sql.exec_serach(wheres=sql, data_tag=data_tag, data_type=1)
            except ValueError as e:
                return Response({"status": 500, "msg": e.message})
        else:
            is_ok, data = self.fetch_line_data(es_sql_url, sql, indexs, interval)
        if not is_ok:
            return Response({"status": 500, "msg": "查询失败", "error": data})
        return Response({"status": 200, "msg": "查询成功", "data": data})


class SSAEventSearchDts(SSAEventSearchBase):
    """
    事件搜索
    """

    def post(self, request):
        """
        图表接口
        """
        start = self.request.data.get("start", 0)
        length = self.request.data.get("length", 10)
        if start >= 10000:
            return Response({"status": 500, "msg": "只能查看前10000条数据，请修改查询条件", "error": ""})
        elif start + length > 10000:
            length = 10000 - start
        else:
            try:
                start_time, end_time, es_sql_url, sql, indexs, data_tag = self.parsed_post(request)
            except ValueError as e:
                return Response({"status": 200, "data": [], "msg": e.message})
        is_ok, data = self.fetch_table_data(es_sql_url, sql, indexs, start, length, data_tag, 1)
        if not is_ok:
            return Response({"status": 500, "msg": "查询失败", "error": data})
        data['recordsFiltered'] = data['recordsTotal']
        return Response(data)


class SSAEventSearchValuePercent(SSAEventSearchBase):
    """
    事件搜索
    """

    def percent_of_data(self, data):
        percent_data = {}
        all_key_data = {}
        for i in data:
            for k, v in i.items():
                all_key_data[k] = all_key_data.get(k, [])
                all_key_data[k].append(v)

        for k, v in all_key_data.items():
            wordcount = Counter(v)
            all_count = sum(wordcount.values())
            percent_data[k] = {
                "key_count": len(wordcount.keys()),
                "keys": []
            }
            all_count = float(all_count)
            for w_k, w_c in wordcount.items():
                percent = w_c / all_count if all_count != 0 else 0
                percent = round(percent * 100, 1)
                percent_data[k]['keys'].append({"name": w_k, "count": percent})
            percent_data[k]['keys'] = sorted(
                percent_data[k]['keys'], key=lambda k: k['count'], reverse=True)[:5]
        return percent_data

    def post(self, request):
        """
        事件搜索-值分布
        取前500 条数据 计算各列值占比
        """
        try:
            start_time, end_time, es_sql_url, sql, indexs, data_tag = self.parsed_post(request)
        except ValueError as e:
            return Response({"status": 500, "data": [], "msg": e.message})
        is_ok, data = self.fetch_table_data(es_sql_url, sql, indexs, 0, 500)
        if not is_ok:
            return Response({"status": 500, "msg": "查询失败", "error": data})
        data = self.percent_of_data(data['data'])
        return Response({"status": 200, "msg": "查询成功", "data": data})


class ETLDataTagSelect2(SSAEventSearchBase):
    """数据标签列表"""

    def post(self, request):
        """
        数据标签列表
        """
        agent_now = request.user.userinfo.agent
        company_now = request.user.userinfo.company
        q = request.DATA.get("q", '')
        data_list = models.SSADataTag.objects.filter(name__contains=q) \
            .filter(Q(agent=agent_now, company=company_now) | Q(agent=None, company=None)) \
            .values("id", "name")
        new_data_list = []
        for data in data_list:
            try:
                start_time, end_time, es_sql_url, sql, indexs, data_tag = self.parsed_post(request, data['id'])
                sql = "select count(*) nums from {} {} ".format(", ".join(indexs), sql)
                result_list = exec_es_sql(sql)
                if len(result_list) == 1:
                    all_count = result_list[0]['nums']
                else:
                    all_count = 0
                data['all_count'] = all_count
                new_data_list.append(data)
            except ValueError as e:
                data['all_count'] = 0
                new_data_list.append(data)
                print(e)
        result = select2_filter(request, new_data_list)
        return Response(result)

    def parsed_post(self, request, data_tag):
        """
        事件搜索
        """
        agent = request.user.userinfo.agent
        company = request.user.userinfo.company
        start_time = self.request.data.get("start_time")
        end_time = self.request.data.get("end_time")
        querys = self.request.data.get("query")
        query_string = self.request.data.get("query_string")
        ip = self.request.data.get("src_ip", "")

        try:
            es_host = models.SelfServiceConf.objects.get(agent=agent, company=company, service="es")
        except models.SelfServiceConf.DoesNotExist:
            raise ValueError("ES服务未配置")
        try:
            data_tag = models.SSADataTag.objects.filter(Q(agent=agent, company=company) |
                                                        Q(agent=None, company=None)).get(id=data_tag)
        except models.SSADataTag.DoesNotExist:
            raise ValueError("事件源错误")
        datetime_format = '%Y-%m-%d %H:%M:%S'
        # 时间为空，采用默认时间 最近1天
        if not any([start_time, end_time]):
            start_time = timezone.now() - timezone.timedelta(days=1)
            end_time = timezone.now()
        else:
            try:
                start_time = timezone.get_current_timezone().localize(
                    datetime.strptime(start_time, datetime_format))
                end_time = timezone.get_current_timezone().localize(
                    datetime.strptime(end_time, datetime_format))
            # 时间格式错误
            except(ValueError, TypeError):
                raise ValueError("时间格式错误")

        indexs = self.generate_index(start_time, end_time, data_tag.path, es_host.host)
        if not indexs:
            raise ValueError("无数据")
        sql = self.generate_sql(querys, query_string, data_tag.path, ip)
        return start_time, end_time, es_host.host, sql, indexs, data_tag.path


class SelectParamSelect2(APIView):
    """事件检测"""

    def post(self, request):
        """获取事件检测字段"""
        data_list = [{"id": 'src_ip', "name": '源IP地址'}, {"id": 'src_port', "name": '源端口'},
                     {"id": 'dst_ip', "name": '目标IP地址'},
                     {"id": 'dst_port', "name": '目标端口'}]
        data = select2_filter(request, data_list)
        return Response(data)


class SelectVulStore(APIView):
    """
    获取漏洞信息
    """
    def post(self, request):
        cve_id = request.data.get("cve_id")
        vul_name = request.data.get("vul_name")
        data = ""
        vul_list = VulStore.objects.all()
        if cve_id:
            data = vul_list.filter(vul_name=vul_name).values().first()
        if vul_name:
            data = vul_list.filter(vul_name=vul_name).values().first()
        return Response(data)
