# coding=utf-8
from django.utils import timezone
from fetch_new_base import BaseData
from utils.es_select import exec_es_sql
import time
import json
from datetime import datetime, timedelta
from soc_assets.models import TermGroup
from elasticsearch import Elasticsearch
from soc_ssa.models import SelfServiceConf


class EventAllCountData(BaseData):
    """
    事件统计
    """
    def data(self):
        count_type = 1
        day_list = get_day_list(count_type)
        new_result_dict = dict()
        data_tag = "all-event"
        for day in day_list:
            index = data_tag + "-" + day + "*"
            sql = "SELECT sum(event_total) nums FROM {}".format(index)
            result_list = exec_es_sql(sql)
            if len(result_list) > 0:
                nums = result_list[0]['nums']
            else:
                nums = 0
            if day in new_result_dict and new_result_dict[day]:
                new_result_dict[day] = int(nums) + int(new_result_dict[day])
            else:
                new_result_dict[day] = int(nums)
        day_nums_list = []
        for day in day_list:
            if day in new_result_dict:
                day_nums = new_result_dict[day]
            else:
                day_nums = 0
            day_nums_list.append(day_nums)
        return {
            "labels": day_list,
            "data": [{"name": "事件统计", "data": day_nums_list}]
        }


class EventSourceTypeData(BaseData):
    """
    事件来源统计
    """
    def data(self):
        count_type = 1
        day_list = get_day_list(count_type)
        new_result_dict = dict()
        data_tag_list = ["event-firewall", "event-ids", "event-terminal",
                         "event-db-audit", "event-anti"]
        data_tag_name = {"event-firewall": "防火墙", "event-ids": "IDS", "event-terminal": "终端", "event-db-audit": "数据库审计",
                         "event-anti": "360杀毒软件"}
        for data_tag in data_tag_list:
            new_result_dict[data_tag] = []
        new_result_dict["隔离设备"] = []
        new_result_dict["摆渡设备"] = []
        for day in day_list:
            for data_tag in data_tag_list:
                index = data_tag + "-" + day + "*"
                sql = "SELECT sum(event_total) nums FROM {}".format(index)
                result_list = exec_es_sql(sql)
                if len(result_list) > 0:
                    new_result_dict[data_tag].append(int(result_list[0]['nums']))
                else:
                    new_result_dict[data_tag].append(0)
            index = "event-security" + "-" + day + "*"
            sql = "SELECT sum(event_total) nums FROM {} where event_source like \'%隔离设备%\' ".format(index)
            result_list = exec_es_sql(sql)
            if len(result_list) > 0:
                new_result_dict["隔离设备"].append(int(result_list[0]['nums']))
            else:
                new_result_dict["隔离设备"].append(0)
            index = "event-security" + "-" + day + "*"
            sql = "SELECT sum(event_total) nums FROM {} where event_source like '%摆渡设备%' ".format(index)
            result_list = exec_es_sql(sql)
            if len(result_list) > 0:
                new_result_dict["摆渡设备"].append(int(result_list[0]['nums']))
            else:
                new_result_dict["摆渡设备"].append(0)
        event_type_list = []
        for data_tag in data_tag_list:
            event_type_list.append({'name': data_tag_name[data_tag], 'data': new_result_dict[data_tag]})
        event_type_list.append({'name': "隔离设备", 'data': new_result_dict["隔离设备"]})
        event_type_list.append({'name': "摆渡设备", 'data': new_result_dict["摆渡设备"]})
        return {
            "labels": day_list,
            "data": event_type_list
        }


class EventTypeCountData(BaseData):
    """
    事件类型统计
    """
    def data(self):
        count_type = 1
        data = []
        data_tag_list = ["event-firewall", "event-ids", "event-terminal",
                         "event-db-audit", "event-anti", "event-security"]
        event_type_list = []
        new_result_dict = dict()
        for data_tag in data_tag_list:
            start_time, end_time, indexs = get_index_by_count_type(count_type, data_tag)
            sql = "SELECT sum(event_total) nums FROM {} group by event_type".format(",".join(indexs))
            result_list = exec_es_sql(sql)
            if len(result_list) > 0:
                for result in result_list:
                    event_type = result['event_type']
                    if event_type != "正常事件":
                        new_result_dict[event_type] = int(result['nums'])
        new_result_dict = sorted(new_result_dict.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
        if self.top != "":
            new_result_dict = new_result_dict[0:self.top]
        for k, v in new_result_dict:
            event_type_list.append(k)
            data.append(v)
        return report_data_rule1(data, event_type_list, "事件类型统计")


class AttackEventTypeCountData(BaseData):
    """
    攻击事件类型统计
    """
    def data(self):
        count_type = 1
        data = []
        data_tag_list = ["event-firewall", "event-ids"]
        event_type_list = []
        new_result_dict = dict()
        for data_tag in data_tag_list:
            start_time, end_time, indexs = get_index_by_count_type(count_type, data_tag)
            sql = "SELECT sum(event_total) nums FROM {} group by event_type".format(",".join(indexs))
            result_list = exec_es_sql(sql)
            if len(result_list) > 0:
                for result in result_list:
                    event_type = result['event_type']
                    if event_type != "正常事件":
                        new_result_dict[event_type] = int(result['nums'])
        new_result_dict = sorted(new_result_dict.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
        if self.top != "":
            new_result_dict = new_result_dict[0:self.top]
        for k, v in new_result_dict:
            event_type_list.append(k)
            data.append(v)
        return report_data_rule1(data, event_type_list, "攻击事件类型统计")


class VirusAllEventTypeCountData(BaseData):
    """
    病毒事件类型统计
    """
    def data(self):
        count_type = 1
        data = []
        data_tag_list = ["event-anti"]
        event_type_list = []
        new_result_dict = dict()
        for data_tag in data_tag_list:
            start_time, end_time, indexs = get_index_by_count_type(count_type, data_tag)
            sql = "SELECT sum(event_total) nums FROM {} group by event_type".format(",".join(indexs))
            result_list = exec_es_sql(sql)
            if len(result_list) > 0:
                for result in result_list:
                    event_type = result['event_type']
                    if event_type != "正常事件":
                        new_result_dict[event_type] = int(result['nums'])
        new_result_dict = sorted(new_result_dict.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
        if self.top != "":
            new_result_dict = new_result_dict[0:self.top]
        for k, v in new_result_dict:
            event_type_list.append(k)
            data.append(v)
        return report_data_rule1(data, event_type_list, "病毒事件类型统计")


def get_day_list(count_type):
    date_list = []
    if count_type == 1:
        start_time = (datetime.now() - timedelta(days=6)).strftime("%Y-%m-%d")
        end_time = time.strftime("%Y-%m-%d")
        date_list = []
        begin_date = datetime.strptime(start_time, "%Y-%m-%d")
        end_date = datetime.strptime(end_time, "%Y-%m-%d")
        while begin_date <= end_date:
            date_str = begin_date.strftime("%Y-%m-%d")
            date_list.append(date_str)
            begin_date += timedelta(days=1)
    return date_list


def get_index_by_count_type(count_type, data_tag):
    try:
        es_host = SelfServiceConf.objects.get(service="es")
    except SelfServiceConf.DoesNotExist:
        raise ValueError("ES服务未配置")
    start_time = (datetime.now() - timedelta(days=6)).strftime("%Y-%m-%d") + " 00:00:00"
    end_time = time.strftime("%Y-%m-%d") + " 23:59:59"
    indexs = ""
    if data_tag:
        indexs = generate_index(datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"),
                                datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S"), data_tag, es_host.host)
    return start_time, end_time, indexs


def generate_index(start_time, end_time, data_tag, es_hosts):
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


def get_term_duty_by_ip(ip):
    sql = 'SELECT term_duty from ssa-ag-zd* where login_ip = {} order act_time limit 1'.format(ip)
    result = exec_es_sql(sql)
    term_duty = ""
    if len(result) > 0:
        term_duty = result[0]['term_duty']
    return term_duty


def only_generate_index(start_time, end_time, data_tag):
    """
    生成需要搜索的indexs
    """
    try:
        es_host = SelfServiceConf.objects.get(service="es")
    except SelfServiceConf.DoesNotExist:
        raise ValueError("ES服务未配置")
    es = Elasticsearch(hosts=es_host.host)
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


def is_json(json_str):
    try:
        a = json.loads(json_str)
        return True
    except Exception as e:
        return False


def report_data_rule1(data, labels, name):
    if len(data) > 0:
        data_dict = [{
            'name': name,
            'data': data
        }]
    else:
        data_dict = []
    return {
        "labels": labels,
        "data": data_dict
    }


def report_data_table(data, labels):
    if len(data) == 0:
        labels = []
    return {
        "labels": labels,
        "data": data
    }


def get_term_name(term_id):
    term_name = TermGroup.objects.filter(term_group_id=term_id).first()
    if term_name:
        return term_name.term_group_name
    else:
        return ""