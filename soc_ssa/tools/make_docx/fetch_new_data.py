# coding=utf-8
from __future__ import unicode_literals
import json
from fetch_new_base import BaseData

from django.db import connection
from django.utils import timezone
import time
from datetime import datetime, timedelta
from elasticsearch import Elasticsearch

from utils.es_select import exec_es_sql
from utils.date import get_today_month

from soc_ssa.models import SelfServiceConf
from soc_assets.models import AssetsType
from soc_assets.models import TermGroup


# "资产-----------------"

class AssetTotalData(BaseData):
    """
    资产总数
    """

    def data(self):
        asset_day_list = []
        day_list = get_day_list(self.cycle)
        for day in day_list:
            sql = "select count(*) as nums from soc_assets where  DATE_FORMAT(add_date,'%Y-%m-%d') <= \'{}\'".format(
                day)
            cursor = connection.cursor()
            cursor.execute(sql)
            raw_data = cursor.fetchall()
            for row in raw_data:
                asset_day_list.append(row[0])
        return {
            "labels": day_list,
            "data": [{"name": "资产总数", "data": asset_day_list}]
        }


class AssetAddTotalData(BaseData):
    """
    新增资产数统计
    """

    def data(self):
        nums_list = []
        data_dict = dict()
        days = get_day_list(self.cycle)
        tuple_days = tuple(days)
        if len(days) == 1:
            tuple_days = '(' + days[0] + ')'
        sql_select = "select DATE_FORMAT(add_date,'%Y-%m-%d') day,count(*) as nums from soc_assets where  DATE_FORMAT(add_date,'%Y-%m-%d') in {} GROUP BY DATE_FORMAT(add_date,'%Y-%m-%d')".format(
            tuple_days)
        cursor = connection.cursor()
        cursor.execute(sql_select)
        raw_data = cursor.fetchall()
        for row in raw_data:
            data_dict[row[0]] = row[1]
        for day in days:
            day_nums = 0
            if day in data_dict:
                day_nums = data_dict[day]
            nums_list.append(day_nums)
        return {
            "labels": days,
            "data": [{"name": "新增资产总数", "data": nums_list}]
        }


class AssetTypeData(BaseData):
    """
    资产类型
    """

    def data(self):
        new_result_list = dict()
        type_data_dict = dict()  # 存放每种类型的数据
        type_list = []
        days = get_day_list(self.cycle)
        for day in days:
            new_result_list[day] = dict()
            sql = "select count(*) as nums,assets_type from soc_assets where  DATE_FORMAT(add_date,'%Y-%m-%d') <= \'{}\' GROUP BY assets_type ".format(
                day)
            cursor = connection.cursor()
            cursor.execute(sql)
            raw_data = cursor.fetchall()
            for row in raw_data:
                type = str(row[1])
                nums = row[0]
                if type not in type_list:
                    type_list.append(type)
                    type_data_dict[type] = []
                new_result_list[day][type] = nums
        for day in days:
            for assets_type in type_list:
                if day in new_result_list:
                    if assets_type in new_result_list[day]:
                        count_nums = new_result_list[day][assets_type]
                    else:
                        count_nums = 0
                    type_data_dict[assets_type].append(count_nums)
                else:
                    type_data_dict[assets_type].append(0)
        type_data_list = []
        for key in type_data_dict:
            assets_type_dict = AssetsType.objects.filter(id=int(key)).values("assets_type_name").first()
            if assets_type_dict:
                type_data_list.append({
                    'name': assets_type_dict["assets_type_name"],
                    'data': type_data_dict[key]
                })
            else:
                type_data_list.append({
                    'name': str(key),
                    'data': type_data_dict[key]
                })
        return {
            "labels": days,
            "data": type_data_list
        }


# "事件-----------------"

class EventAllCountData(BaseData):
    """
    事件统计
    """

    def data(self):
        sql = 'SELECT sum(event_total) nums FROM {} group by date_histogram(field=\'{}\',\'interval\'=\'{}\',\'format\'=\'yyyy-MM-dd\')'
        time_param, sql = get_exec_sql(sql, self.cycle, "all-event", "stastic_time")
        day_list = []
        day_nums_list = []
        result_list = exec_es_sql(sql)
        if len(result_list) > 0:
            for result in result_list:
                day_list.append(result[time_param])
                day_nums_list.append(result['nums'])
        return report_data_rule1(day_nums_list, day_list, "事件统计")


class EventSourceTypeData(BaseData):
    """
    事件来源统计
    """

    def data(self):
        event_source_list = [1, 2, 3, 4, 5, 6, 7]
        event_source_dict = {1: "防火墙", 2: "IDS", 3: "数据库审计", 4: "摆渡设备", 5: "隔离设备", 6: "杀毒软件", 7: "终端"}
        sql = 'SELECT sum(event_total) nums FROM {} group by event_source,date_histogram(field=\'{}\',\'interval\'=\'{}\',\'format\'=\'yyyy-MM-dd\')'
        time_param, sql = get_exec_sql(sql, self.cycle, "all-event", "stastic_time")
        day_list = []  # 存储数据查询出的日期
        event_source_nums_list = dict()  # 存储每种类型的时间数list
        result_list = exec_es_sql(sql)
        new_result_dict = dict()
        data_list = []  # 拼接返回数据data
        for event_source in event_source_list:
            new_result_dict[event_source] = dict()
            event_source_nums_list[event_source] = []
        if len(result_list) > 0:
            for result in result_list:
                result_day = result[time_param]
                result_event_source = result['event_source']
                if result_day not in day_list:
                    day_list.append(result_day)
                new_result_dict[result_event_source][result_day] = result['nums']
        for day in day_list:
            for event_source in event_source_list:
                if day in new_result_dict[event_source]:
                    event_source_nums_list[event_source].append(new_result_dict[event_source][day])
                else:
                    event_source_nums_list[event_source].append(0)
        for event_source in event_source_list:
            data_list.append({'name': event_source_dict[event_source], 'data': event_source_nums_list[event_source]})
        return {
            "labels": day_list,
            "data": data_list
        }


class EventTypeCountData(BaseData):
    """
    事件类型统计
    """

    def data(self):
        start_time, end_time, count_name, index_list_str = get_index_by_count_type(self.cycle, "all-event")
        sql = 'SELECT sum(event_total) as nums FROM {}  group by event_three_type order by nums desc {}'
        top = ""
        if self.top:
            top = "limit " + str(self.top)
        sql = sql.format(",".join(index_list_str), top)
        result_list = exec_es_sql(sql)
        event_type_list = []
        nums_list = []
        if len(result_list) > 0:
            for result in result_list:
                event_type_list.append(result.values()[0])
                nums_list.append(result.values()[1])
        return report_data_rule1(nums_list, event_type_list, "事件类型统计")


class AttackEventTypeCountData(BaseData):
    """
    攻击事件类型统计
    """

    def data(self):
        start_time, end_time, count_name, index_list_str = get_index_by_count_type(self.cycle, "all-event")
        sql = 'SELECT sum(event_total) as nums FROM {} where event_one_type=\'攻击\' group by event_three_type order by nums desc {}'
        top = ""
        if self.top:
            top = "limit " + str(self.top)
        sql = sql.format(",".join(index_list_str), top)
        result_list = exec_es_sql(sql)
        event_type_list = []
        nums_list = []
        if len(result_list) > 0:
            for result in result_list:
                event_type_list.append(result.values()[0])
                nums_list.append(result.values()[1])
        return report_data_rule1(nums_list, event_type_list, "攻击事件类型统计")


class VirusAllEventTypeCountData(BaseData):
    """
    病毒事件类型统计
    """

    def data(self):
        start_time, end_time, count_name, index_list_str = get_index_by_count_type(self.cycle, "all-event")
        sql = 'SELECT sum(event_total) as nums FROM {} where event_one_type=\'病毒\' group by event_three_type order by nums desc {}'
        top = ""
        if self.top:
            top = "limit " + str(self.top)
        sql = sql.format(",".join(index_list_str), top)
        result_list = exec_es_sql(sql)
        event_type_list = []
        nums_list = []
        if len(result_list) > 0:
            for result in result_list:
                event_type_list.append(result.values()[0])
                nums_list.append(result.values()[1])
        return report_data_rule1(nums_list, event_type_list, "病毒事件类型统计")


# "终端----------------"


class TerminalDetailData(BaseData):
    """
    终端行为详情
    """

    def data(self):
        start_time, end_time, count_name, index_list_str = get_index_by_count_type(self.cycle, "ssa-ag-all-terminal")
        term, top = self.structure_term_sql_param()
        sql = 'SELECT term_group_name,login_ip,term_duty,act_time,login_type FROM {} where log_type = 2' \
              ' and (login_type=4 or login_type=5) {} order by act_time desc '.format(", ".join(index_list_str), term)
        result_list = exec_es_sql(sql)
        new_result_list = []
        for log in result_list:
            data_dict = dict()
            if log['login_type'] == 4:
                data_dict['login_ip'] = log['login_ip']
                data_dict['term_group_name'] = log['term_group_name']
                data_dict['term_duty'] = log['term_duty']
                if 'close_time' not in data_dict:
                    data_dict['close_time'] = ''
                data_dict['start_time'] = datetime.strptime(log['act_time'], "%Y%m%d%H%M%S").strftime(
                    "%Y-%m-%d %H:%M:%S")
                new_result_list.append(data_dict)
            if log['login_type'] == 5:
                data_dict['login_ip'] = log['login_ip']
                data_dict['term_group_name'] = log['term_group_name']
                data_dict['term_duty'] = log['term_duty']
                data_dict['close_time'] = datetime.strptime(log['act_time'], "%Y%m%d%H%M%S").strftime(
                    "%Y-%m-%d %H:%M:%S")
                if 'start_time' not in data_dict:
                    data_dict['start_time'] = ''
                new_result_list.append(data_dict)
        data_list = []
        for item in new_result_list:
            if self.term and self.term[0]['id']:
                term_name = get_term_name(self.term[0]['id'])
            else:
                term_name = item['term_group_name']
            data_list.append({
                'name': '终端行为',
                'data': [item['login_ip'], item['term_duty'], term_name, item['start_time'],
                         item['close_time']],
            })
        labels = ['IP', '终端负责人', '用户组名称', '开机时间', '关机时间']
        return report_data_table(data_list, labels)


class TerminalLoginNumsData(BaseData):
    """
    登录次数统计
    """

    def data(self):
        start_time, end_time, count_name, index_list_str = get_index_by_count_type(self.cycle, "ssa-ag-all-terminal")
        term, top = self.structure_term_sql_param()
        sql = 'SELECT login_ip,count(*) as nums FROM {} where log_type=2 and login_type in (1,2,3) {} group by login_ip order by nums desc {}'.format(
            ", ".join(index_list_str), term, top)
        result_list = exec_es_sql(sql)
        labels = []
        data = []
        for item in result_list:
            labels.append(item['login_ip'])
            data.append(item['nums'])
        name = '登录次数'
        return report_data_rule1(data, labels, name)


class TerminalFailLoginNumsData(BaseData):
    """
    登录失败次数统计
    """

    def data(self):
        start_time, end_time, count_name, index_list_str = get_index_by_count_type(self.cycle, "ssa-ag-all-terminal")
        term, top = self.structure_term_sql_param()
        sql = 'SELECT login_ip,count(*) as nums FROM {} where log_type=2 and login_result=0 {}' \
              'group by login_ip order by nums desc {}'.format(", ".join(index_list_str), term, top)
        result_list = exec_es_sql(sql)
        labels = []
        data = []
        for item in result_list:
            labels.append(item['login_ip'])
            data.append(item['nums'])
        name = '登录失败次数'
        return report_data_rule1(data, labels, name)


class OutPrintData(BaseData):
    """
    打印情况统计
    """

    def data(self):
        start_time, end_time, count_name, index_list_str = get_index_by_count_type(self.cycle, "ssa-ag-all-terminal")
        term, top = self.structure_term_sql_param()
        sql = 'SELECT term_ip,count(*) as nums FROM {} where log_type=5 and request_type=1 and act_type in (0,1,2,3,4,5,7) {} group by term_ip,act_type order by nums desc {}'.format(
            ", ".join(index_list_str), term, top)
        result_list = exec_es_sql(sql)
        labels = []
        act_type_list = []
        act_type_name_list = {"0": "拒绝打印", "1": "同意打印", "2": "打印审计", "3": "强制使用",
                              "4": "自行取消", "5": "中心超时取消", "7": "离线使用"}
        new_result_dict = dict()
        for item in result_list:
            if item['term_ip'] not in labels:
                labels.append(item['term_ip'])
                new_result_dict[item['term_ip']] = dict()
            if item['act_type'] not in act_type_list:
                act_type_list.append(item['act_type'])
            new_result_dict[item['term_ip']][item['act_type']] = item['nums']
        data_list_dict = {}
        for act_type in act_type_list:
            data_list_dict[act_type] = []
            for term_ip in labels:
                if act_type in new_result_dict[term_ip]:
                    data_list_dict[act_type].append(new_result_dict[term_ip][act_type])
                else:
                    data_list_dict[act_type].append(0)
        data = []
        for act_type in act_type_list:
            if str(act_type) in act_type_name_list:
                data.append({"name": act_type_name_list[str(act_type)], "data": data_list_dict[act_type]})
            else:
                data.append({"name": str(act_type), "data": data_list_dict[act_type]})
        return {
            "labels": labels,
            "data": data
        }


# class OutLinePrintData(BaseData):
#     """
#     违规打印统计
#     """
#
#     def data(self):
#         count_type = 1
#         start_time, end_time, indexs = get_index_by_count_type(count_type, "ssa-ag-zd-sp")
#         term, top = self.structure_term_sql_param()
#         sql = 'SELECT term_ip,count(*) as nums FROM {} where (request_type=1 or request_type=2 or request_type=3) ' \
#               'and (act_type = 3 or act_type=7) {} group by term_ip order by nums desc {}'.format(", ".join(indexs),
#                                                                                                   term, top)
#         result_list = exec_es_sql(sql)
#         labels = []
#         data = []
#         for item in result_list:
#             labels.append(item['term_ip'])
#             data.append(item['nums'])
#         name = '违规打印次数'
#         return report_data_rule1(data, labels, name)


class OutLinePrintTableData(BaseData):
    """
    打印详情
    """

    def data(self):
        start_time, end_time, count_name, index_list_str = get_index_by_count_type(self.cycle, "ssa-ag-all-terminal")
        term, top = self.structure_term_sql_param()
        sql = 'SELECT term_ip,term_duty,term_group_name,act_time,act_type FROM {} where log_type=5 and request_type=1 and act_type in (0,1,2,3,4,5,7) {}' \
              ' order by act_time desc'.format(", ".join(index_list_str), term)
        result_list = exec_es_sql(sql)
        data_list = []
        act_type_name_list = {"0": "拒绝打印", "1": "同意打印", "2": "打印审计", "3": "强制使用",
                              "4": "自行取消", "5": "中心超时取消", "7": "离线使用"}
        for item in result_list:
            item['act_time'] = datetime.strptime(item['act_time'], "%Y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
            act_type = item['act_type']
            if str(act_type) in act_type_name_list:
                item['act_type'] = act_type_name_list[str(act_type)]
            else:
                item['act_type'] = str(act_type)
            if self.term and self.term[0]['id']:
                term_name = get_term_name(self.term[0]['id'])
            else:
                term_name = item['term_group_name']
            data_list.append({
                'name': '打印',
                'data': [item['term_ip'], item['term_duty'], term_name, item['act_time'],
                         item['act_type']]
            })
        labels = ['IP', '终端负责人', '用户组名称', '打印时间', '违规类型']
        return report_data_table(data_list, labels)


class GoWorkData(BaseData):
    """
    下班打印统计
    """

    def data(self):
        act_type_name_list = {"0": "拒绝打印", "1": "同意打印", "2": "打印审计", "3": "强制使用",
                              "4": "自行取消", "5": "中心超时取消", "7": "离线使用"}
        day_list = get_day_list(self.cycle)
        ip_nums_dict = dict()
        act_type_list = []
        data_list_dict = dict()
        ip_list = []
        term, top = self.structure_term_sql_param()
        for day in day_list:
            start_time = datetime.strptime((day + " 00:00:00"), "%Y-%m-%d %H:%M:%S")
            end_time = datetime.strptime((day + " 23:59:59"), "%Y-%m-%d %H:%M:%S")
            indexs = only_generate_index(start_time, end_time, "ssa-ag-all-terminal")
            if indexs == []:
                continue
            start_time_one = datetime.strptime((day + " 00:00:00"), "%Y-%m-%d %H:%M:%S")
            start_time_one = int(start_time_one.strftime("%Y%m%d%H%M%S"))
            end_time_one = datetime.strptime((day + " 08:00:00"), "%Y-%m-%d %H:%M:%S")
            end_time_one = int(end_time_one.strftime("%Y%m%d%H%M%S"))
            start_time_two = datetime.strptime((day + " 18:00:00"), "%Y-%m-%d %H:%M:%S")
            start_time_two = int(start_time_two.strftime("%Y%m%d%H%M%S"))
            end_time_two = int(end_time.strftime("%Y%m%d%H%M%S"))
            sql = 'SELECT term_ip,count(*) as nums FROM {0} where log_type=5 and request_type =1 and act_type in (0,1,2,3,4,5,7) and ((act_time > {1} and act_time < {2}) or (act_time > {3} and act_time < {4})) {5} group by term_ip,act_type'.format(
                ", ".join(indexs), start_time_one, end_time_one, start_time_two, end_time_two, term)
            result_list = exec_es_sql(sql)
            for data in result_list:
                act_type = data['act_type']
                if act_type not in act_type_list:
                    act_type_list.append(act_type)
                if data['term_ip']:
                    if data['term_ip'] not in ip_list:
                        ip_list.append(data['term_ip'])
                        ip_nums_dict[data['term_ip']] = dict()
                    if data['term_ip'] in ip_nums_dict and "all_nums" in ip_nums_dict[data['term_ip']]:
                        ip_nums_dict[data['term_ip']]["all_nums"] = ip_nums_dict[data['term_ip']]["all_nums"] + data[
                            'nums']
                    else:
                        ip_nums_dict[data['term_ip']]["all_nums"] = 0
                    if data['term_ip'] in ip_nums_dict and act_type in ip_nums_dict[data['term_ip']]:
                        ip_nums_dict[data['term_ip']][act_type] = int(ip_nums_dict[data['term_ip']][act_type]) + data[
                            'nums']
                    else:
                        ip_nums_dict[data['term_ip']][act_type] = data['nums']
        ip_nums_dict = sorted(ip_nums_dict.items(), lambda x, y: cmp(x[1]['all_nums'], y[1]['all_nums']), reverse=True)
        ip_nums_dict = ip_nums_dict[0:self.top]
        data = []
        new_ip_list = []
        for k, v in ip_nums_dict:
            new_ip_list.append(k)
        for act_type in act_type_list:
            data_list_dict[act_type] = []
        for act_type in act_type_list:
            for i in range(len(new_ip_list)):
                if act_type in ip_nums_dict[i][1]:
                    data_list_dict[act_type].append(ip_nums_dict[i][1][act_type])
                else:
                    data_list_dict[act_type].append(0)
        for act_type in act_type_list:
            if str(act_type) in act_type_name_list:
                data.append({"name": act_type_name_list[str(act_type)], "data": data_list_dict[act_type]})
            else:
                data.append({"name": str(act_type), "data": data_list_dict[act_type]})
        return {
            "labels": new_ip_list,
            "data": data
        }


class GoWorkTableData(BaseData):
    """
    下班打印详情
    """

    def data(self):
        all_day_result_list = []
        term, top = self.structure_term_sql_param()
        day_list = get_day_list(self.cycle)
        for day in day_list:
            start_time = datetime.strptime((day + " 00:00:00"), "%Y-%m-%d %H:%M:%S")
            end_time = datetime.strptime((day + " 23:59:59"), "%Y-%m-%d %H:%M:%S")
            indexs = only_generate_index(start_time, end_time, "ssa-ag-all-terminal")
            if indexs == []:
                continue
            start_time_one = datetime.strptime((day + " 00:00:00"), "%Y-%m-%d %H:%M:%S")
            start_time_one = int(start_time_one.strftime("%Y%m%d%H%M%S"))
            end_time_one = datetime.strptime((day + " 08:00:00"), "%Y-%m-%d %H:%M:%S")
            end_time_one = int(end_time_one.strftime("%Y%m%d%H%M%S"))
            start_time_two = datetime.strptime((day + " 18:00:00"), "%Y-%m-%d %H:%M:%S")
            start_time_two = int(start_time_two.strftime("%Y%m%d%H%M%S"))
            end_time_two = int(end_time.strftime("%Y%m%d%H%M%S"))
            sql = 'SELECT term_ip,term_duty,act_time,term_group_name as nums FROM {0} where   log_type=5 and request_type=1 and ((act_time > {1} and act_time < {2}) or (act_time > {3} and act_time < {4})) {5} '.format(
                ", ".join(indexs), start_time_one, end_time_one, start_time_two, end_time_two, term)
            result_list = exec_es_sql(sql)
            all_day_result_list.extend(result_list)
        data_list = []
        for item in all_day_result_list:
            item['act_time'] = datetime.strptime(item['act_time'], "%Y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
            if self.term and self.term[0]['id']:
                term_name = get_term_name(self.term[0]['id'])
            else:
                term_name = item['term_group_name']
            data_list.append({
                'name': '下班打印',
                'data': [item['term_ip'], item['term_duty'], term_name, item['act_time']]
            })
        labels = ['IP', '终端负责人', '用户组名称', '打印时间']
        return report_data_table(data_list, labels)


class DiskData(BaseData):
    """
    移动盘统计
    """

    def data(self):
        start_time, end_time, count_name, index_list_str = get_index_by_count_type(self.cycle, "ssa-ag-all-terminal")
        term, top = self.structure_term_sql_param()
        sql = 'SELECT term_ip,count(*) as nums FROM {} where log_type=5 and request_type=2 and act_type in (3,8,9,10,11,12) {} group by term_ip,act_type order by nums desc {}'.format(
            ", ".join(index_list_str), term, top)
        result_list = exec_es_sql(sql)
        labels = []
        act_type_list = []
        act_type_name_list = {"8": "拒绝", "9": "同意", "3": "强制使用",
                              "10": "禁用", "11": "插入", "12": "拔出"}
        new_result_dict = dict()
        for item in result_list:
            if item['term_ip'] not in labels:
                labels.append(item['term_ip'])
                new_result_dict[item['term_ip']] = dict()
            if item['act_type'] not in act_type_list:
                act_type_list.append(item['act_type'])
            new_result_dict[item['term_ip']][item['act_type']] = item['nums']
        data_list_dict = {}
        for act_type in act_type_list:
            data_list_dict[act_type] = []
            for term_ip in labels:
                if act_type in new_result_dict[term_ip]:
                    data_list_dict[act_type].append(new_result_dict[term_ip][act_type])
                else:
                    data_list_dict[act_type].append(0)
        data = []
        for act_type in act_type_list:
            if str(act_type) in act_type_name_list:
                data.append({"name": act_type_name_list[str(act_type)], "data": data_list_dict[act_type]})
            else:
                data.append({"name": str(act_type), "data": data_list_dict[act_type]})
        return {
            "labels": labels,
            "data": data
        }


class DiskTableData(BaseData):
    """
    移动盘使用详情
    """

    def data(self):
        act_type_name_list = {"8": "拒绝", "9": "同意", "3": "强制使用",
                              "10": "禁用", "11": "插入", "12": "拔出"}
        start_time, end_time, count_name, index_list_str = get_index_by_count_type(self.cycle, "ssa-ag-all-terminal")
        term, top = self.structure_term_sql_param()
        sql = 'SELECT term_ip,term_duty,term_group_name,act_time,act_type FROM {} where log_type=5 and request_type=2 and act_type in (3,8,9,10,11,12) {} ' \
              ' order by act_time desc '.format(", ".join(index_list_str), term)
        result_list = exec_es_sql(sql)
        data_list = []
        for item in result_list:
            item['act_time'] = datetime.strptime(item['act_time'], "%Y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
            act_type = item['act_type']
            if str(act_type) in act_type_name_list:
                item['act_type'] = act_type_name_list[str(act_type)]
            else:
                item['act_type'] = str(act_type)
            if self.term and self.term[0]['id']:
                term_name = get_term_name(self.term[0]['id'])
            else:
                term_name = item['term_group_name']
            data_list.append({
                'name': '',
                'data': [item['term_ip'], item['term_duty'], term_name, item['act_time'],
                         item['act_type']]
            })
        labels = ['IP', '终端负责人', '用户组名称', '使用时间', '使用类型']
        return report_data_table(data_list, labels)


class OutLineDiskData(BaseData):
    """
    移动盘违规统计
    """

    def data(self):
        start_time, end_time, count_name, index_list_str = get_index_by_count_type(self.cycle, "ssa-event-terminal")
        term, top = self.structure_term_sql_param()
        sql = 'SELECT terminal,count(*) as nums FROM {} where event_type in (\'违规插入移动盘\') {} group by terminal,event_type order by nums desc {}'.format(
            ", ".join(index_list_str), term, top)
        result_list = exec_es_sql(sql)
        labels = []
        event_type_list = []
        new_result_dict = dict()
        data_list_dict = {}
        for item in result_list:
            if item['terminal'] not in labels:
                labels.append(item['terminal'])
                new_result_dict[item['terminal']] = dict()
            if item['event_type'] not in event_type_list:
                data_list_dict[item['event_type']] = []
                event_type_list.append(item['event_type'])
            new_result_dict[item['terminal']][item['event_type']] = item['nums']
        for event_type in event_type_list:
            for terminal in labels:
                if event_type in new_result_dict[terminal]:
                    data_list_dict[event_type].append(new_result_dict[terminal][event_type])
                else:
                    data_list_dict[event_type].append(0)
        data = []
        for event_type in event_type_list:
            data.append({"name": event_type, "data": data_list_dict[event_type]})
        return {
            "labels": labels,
            "data": data
        }

    def structure_term_sql_param(self):
        if self.term != "":
            if self.term[0]['name'] != '全部部门':
                term = " and organization in ('" + '\',\''.join([item['name'] for item in self.term]) + "')"
            else:
                term = ""
        else:
            term = ""
        if self.top != "":
            top = "limit " + str(self.top)
        else:
            top = ""
        return term, top


class OutLineDiskTableData(BaseData):
    """
    移动盘违规使用详情
    """

    def data(self):
        start_time, end_time, count_name, index_list_str = get_index_by_count_type(self.cycle, "ssa-event-terminal")
        term, top = self.structure_term_sql_param()
        sql = 'SELECT terminal,organization,term_duty ,event_time,event_type from {} where event_type in (\'违规插入移动盘\') {} order by event_time desc {}'.format(
            ", ".join(index_list_str), term, top)
        result_list = exec_es_sql(sql)
        data_list = []
        for item in result_list:
            item['event_time'] = datetime.strptime(item['event_time'], "%Y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
            data_list.append({
                'name': '',
                'data': [item['terminal'], item['term_duty'], item['organization'], item['event_time'],
                         item['event_type']]
            })
        labels = ['IP', '终端负责人', '用户组名称', '使用时间', '使用类型']
        return report_data_table(data_list, labels)

    def structure_term_sql_param(self):
        if self.term != "":
            if self.term[0]['name'] != '全部部门':
                term = " and organization in ('" + '\',\''.join([item['name'] for item in self.term]) + "')"
            else:
                term = ""
        else:
            term = ""
        if self.top != "":
            top = "limit " + str(self.top)
        else:
            top = ""
        return term, top


class RecordCountData(BaseData):
    """
    刻录情况统计
    """

    def data(self):
        start_time, end_time, count_name, index_list_str = get_index_by_count_type(self.cycle, "ssa-ag-all-terminal")
        term, top = self.structure_term_sql_param()
        sql = 'SELECT term_ip,count(*) as nums FROM {} where log_type=5 and request_type=3 and act_type in (8,9,3) {} group by term_ip,act_type order by nums desc {}'.format(
            ", ".join(index_list_str), term, top)
        result_list = exec_es_sql(sql)
        labels = []
        act_type_list = []
        act_type_name_list = {"8": "拒绝", "9": "同意", "3": "强制使用"}
        new_result_dict = dict()
        for item in result_list:
            if item['term_ip'] not in labels:
                labels.append(item['term_ip'])
                new_result_dict[item['term_ip']] = dict()
            if item['act_type'] not in act_type_list:
                act_type_list.append(item['act_type'])
            new_result_dict[item['term_ip']][item['act_type']] = item['nums']
        data_list_dict = {}
        for act_type in act_type_list:
            data_list_dict[act_type] = []
            for term_ip in labels:
                if act_type in new_result_dict[term_ip]:
                    data_list_dict[act_type].append(new_result_dict[term_ip][act_type])
                else:
                    data_list_dict[act_type].append(0)
        data = []
        for act_type in act_type_list:
            if str(act_type) in act_type_name_list:
                data.append({"name": act_type_name_list[str(act_type)], "data": data_list_dict[act_type]})
            else:
                data.append({"name": str(act_type), "data": data_list_dict[act_type]})
        return {
            "labels": labels,
            "data": data
        }


class RecordTableData(BaseData):
    """
    刻录使用详情
    """

    def data(self):
        start_time, end_time, count_name, index_list_str = get_index_by_count_type(self.cycle, "ssa-ag-all-terminal")
        term, top = self.structure_term_sql_param()
        sql = 'SELECT term_ip,term_duty,term_group_name,act_time,file_name FROM {} where log_type=5 and request_type=3 and act_type in (8,9,3) {}' \
              ' order by act_time desc'.format(", ".join(index_list_str), term)
        result_list = exec_es_sql(sql)
        data_list = []
        for item in result_list:
            item['act_time'] = datetime.strptime(item['act_time'], "%Y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
            if self.term and self.term[0]['id']:
                term_name = get_term_name(self.term[0]['id'])
            else:
                term_name = item['term_group_name']
            data_list.append({
                'name': '刻录',
                'data': [item['term_ip'], item['term_duty'], term_name, item['act_time'],
                         item['file_name']]
            })
        labels = ['IP', '终端负责人', '用户组名称', '刻录时间', '文件名']
        return report_data_table(data_list, labels)


class PlaintextSaveCountData(BaseData):
    """
    明文存储
    """

    def data(self):
        start_time, end_time, count_name, index_list_str = get_index_by_count_type(self.cycle, "ssa-event-terminal")
        term, top = self.structure_term_sql_param()
        sql = 'SELECT count(*) nums,terminal FROM {} where event_type = \'明文存储\' {} group by terminal order by nums desc {}'.format(
            ", ".join(index_list_str), term, top)
        result_list = exec_es_sql(sql)
        labels = []
        data = []
        for item in result_list:
            labels.append(item['terminal'])
            data.append(item['nums'])
        name = '明文存储'
        return report_data_rule1(data, labels, name)

    def structure_term_sql_param(self):
        if self.term != "":
            if self.term[0]['name'] != '全部部门':
                term = " and organization in ('" + '\',\''.join([item['name'] for item in self.term]) + "')"
            else:
                term = ""
        else:
            term = ""
        if self.top != "":
            top = "limit " + str(self.top)
        else:
            top = ""
        return term, top


class PlaintextSaveTableData(BaseData):
    """
    明文存储
    """

    def data(self):
        start_time, end_time, count_name, index_list_str = get_index_by_count_type(self.cycle, "ssa-event-terminal")
        term, top = self.structure_term_sql_param()
        sql = 'SELECT terminal,remark,organization,term_duty FROM {} where event_type = \'明文存储\' {}  order by event_time desc'.format(
            ", ".join(index_list_str), term)
        result_list = exec_es_sql(sql)
        data_list = []
        for item in result_list:
            remark = item['remark']
            if is_json(remark):
                remark = json.loads(remark)
                if isinstance(remark, dict):
                    if self.term and self.term[0]['id']:
                        term_name = get_term_name(self.term[0]['id'])
                    else:
                        term_name = item['organization']
                    data_list.append({
                        'name': '明文存储',
                        'data': [item['terminal'], item['term_duty'], term_name, remark['word'],
                                 remark['sm_content']]
                    })
        labels = ['IP', '终端负责人', '用户组名称', '明文', '文件目录']
        return report_data_table(data_list, labels)

    def structure_term_sql_param(self):
        if self.term != "":
            if self.term[0]['name'] != '全部部门':
                term = " and organization in ('" + '\',\''.join([item['name'] for item in self.term]) + "')"
            else:
                term = ""
        else:
            term = ""
        if self.top != "":
            top = "limit " + str(self.top)
        else:
            top = ""
        return term, top


class OutreachCountData(BaseData):
    """
    外联接口统计
    """

    def data(self):
        start_time, end_time, count_name, index_list_str = get_index_by_count_type(self.cycle, "ssa-ag-all-terminal")
        term, top = self.structure_term_sql_param()
        sql = 'SELECT term_ip,count(*) as nums FROM {} where log_type=5 and request_type in (4,5,6,7,8,9) {} group by term_ip,request_type order by nums desc {}'.format(
            ", ".join(index_list_str), term, top)
        result_list = exec_es_sql(sql)
        labels = []
        request_type_list = []
        request_type_name_list = {"4": "红外", "5": "蓝牙", "6": "1394", "7": "Modem",
                                  "8": "802.1x", "9": "PCMCIA"}
        new_result_dict = dict()
        for item in result_list:
            if item['term_ip'] not in labels:
                labels.append(item['term_ip'])
                new_result_dict[item['term_ip']] = dict()
            if item['request_type'] not in request_type_list:
                request_type_list.append(item['request_type'])
            new_result_dict[item['term_ip']][item['request_type']] = item['nums']
        data_list_dict = {}
        for request_type in request_type_list:
            data_list_dict[request_type] = []
            for term_ip in labels:
                if request_type in new_result_dict[term_ip]:
                    data_list_dict[request_type].append(new_result_dict[term_ip][request_type])
                else:
                    data_list_dict[request_type].append(0)
        data = []
        for request_type in request_type_list:
            data.append({"name": request_type_name_list[str(request_type)], "data": data_list_dict[request_type]})
        return {
            "labels": labels,
            "data": data
        }


# class PhoneChargeCountData(BaseData):
#     """
#     手机充电情况统计
#     """
#     def data(self):
#         count_type = 1
#         start_time, end_time, indexs = get_index_by_count_type(count_type, "ssa-ag-all-terminal")
#         term, top = self.structure_term_sql_param()
#         sql = 'SELECT term_ip,count(*) as nums FROM {} where log_type=5 and request_type=10 {} group by term_ip,act_type order by nums desc {}'.format(
#             ", ".join(indexs), term, top)
#         result_list = exec_es_sql(sql)
#         labels = []
#         act_type_list = []
#         act_type_name_list = {"15": "插入手机", "16": "拔出手机"}
#         new_result_dict = dict()
#         for item in result_list:
#             if item['term_ip'] not in labels:
#                 labels.append(item['term_ip'])
#                 new_result_dict[item['term_ip']] = dict()
#             if item['act_type'] not in act_type_list:
#                 act_type_list.append(item['act_type'])
#             new_result_dict[item['term_ip']][item['act_type']] = item['nums']
#         data_list_dict = {}
#         for act_type in act_type_list:
#             data_list_dict[act_type] = []
#             for term_ip in labels:
#                 if act_type in new_result_dict[term_ip]:
#                     data_list_dict[act_type].append(new_result_dict[term_ip][act_type])
#                 else:
#                     data_list_dict[act_type].append(0)
#         data = []
#         for act_type in act_type_list:
#             if str(act_type) in act_type_name_list:
#                 data.append({"name": act_type_name_list[str(act_type)], "data": data_list_dict[act_type]})
#             else:
#                 data.append({"name": str(act_type), "data": data_list_dict[act_type]})
#         return {
#             "labels": labels,
#             "data": data
#         }
#
#
# class PhoneChargeTableData(BaseData):
#     """
#     手机充电详情
#     """
#
#     def data(self):
#         count_type = 1
#         act_type_name_list = {"15": "插入手机", "16": "拔出手机"}
#         start_time, end_time, indexs = get_index_by_count_type(count_type, "ssa-ag-all-terminal")
#         term, top = self.structure_term_sql_param()
#         sql = 'SELECT term_ip,term_duty,term_group_name,act_time,act_type FROM {} where log_type=5 and request_type=10 {} ' \
#               ' order by act_time desc'.format(", ".join(indexs), term)
#         result_list = exec_es_sql(sql)
#         data_list = []
#         for item in result_list:
#             item['act_time'] = datetime.strptime(item['act_time'], "%Y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
#             act_type = item['act_type']
#             if str(act_type) in act_type_name_list:
#                 item['act_type'] = act_type_name_list[str(act_type)]
#             else:
#                 item['act_type'] = str(act_type)
#             if self.term:
#                 term_name = get_term_name(self.term)
#             else:
#                 term_name = item['term_group_name']
#             data_list.append({
#                 'name': '手机充电',
#                 'data': [item['term_ip'], item['term_duty'], term_name, item['act_time'],
#                          item['act_type']]
#             })
#         labels = ['IP', '终端负责人', '用户组名称', '操作时间', '操作']
#         return report_data_table(data_list, labels)
class PhoneChargeCountData(BaseData):
    """
    手机充电统计
    """

    def data(self):
        start_time, end_time, count_name, index_list_str = get_index_by_count_type(self.cycle, "ssa-event-terminal")
        term, top = self.structure_term_sql_param()
        sql = 'SELECT terminal,count(*) as nums FROM {} where event_type in (\'手机充电\') {} group by terminal,event_type order by nums desc {}'.format(
            ", ".join(index_list_str), term, top)
        result_list = exec_es_sql(sql)
        labels = []
        event_type_list = []
        new_result_dict = dict()
        data_list_dict = {}
        for item in result_list:
            if item['terminal'] not in labels:
                labels.append(item['terminal'])
                new_result_dict[item['terminal']] = dict()
            if item['event_type'] not in event_type_list:
                data_list_dict[item['event_type']] = []
                event_type_list.append(item['event_type'])
            new_result_dict[item['terminal']][item['event_type']] = item['nums']
        for event_type in event_type_list:
            for terminal in labels:
                if event_type in new_result_dict[terminal]:
                    data_list_dict[event_type].append(new_result_dict[terminal][event_type])
                else:
                    data_list_dict[event_type].append(0)
        data = []
        for event_type in event_type_list:
            data.append({"name": event_type, "data": data_list_dict[event_type]})
        return {
            "labels": labels,
            "data": data
        }

    def structure_term_sql_param(self):
        if self.term != "":
            if self.term[0]['name'] != '全部部门':
                term = " and organization in ('" + '\',\''.join([item['name'] for item in self.term]) + "')"
            else:
                term = ""
        else:
            term = ""
        if self.top != "":
            top = "limit " + str(self.top)
        else:
            top = ""
        return term, top


class PhoneChargeTableData(BaseData):
    """
    手机充电使用详情
    """

    def data(self):
        start_time, end_time, count_name, index_list_str = get_index_by_count_type(self.cycle, "ssa-event-terminal")
        term, top = self.structure_term_sql_param()
        sql = 'SELECT terminal,organization,term_duty ,event_time,event_type from {} where event_type in (\'手机充电\') {} order by event_time desc {}'.format(
            ", ".join(index_list_str), term, top)
        result_list = exec_es_sql(sql)
        data_list = []
        for item in result_list:
            item['event_time'] = datetime.strptime(item['event_time'], "%Y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
            data_list.append({
                'name': '',
                'data': [item['terminal'], item['term_duty'], item['organization'], item['event_time'],
                         item['event_type']]
            })
        labels = ['IP', '终端负责人', '用户组名称', '使用时间', '使用类型']
        return report_data_table(data_list, labels)

    def structure_term_sql_param(self):
        if self.term != "":
            if self.term[0]['name'] != '全部部门':
                term = " and organization in ('" + '\',\''.join([item['name'] for item in self.term]) + "')"
            else:
                term = ""
        else:
            term = ""
        if self.top != "":
            top = "limit " + str(self.top)
        else:
            top = ""
        return term, top


class TmsInstallCountData(BaseData):
    """
    TMS安装卸载统计
    """

    def data(self):
        start_time, end_time, count_name, index_list_str = get_index_by_count_type(self.cycle, "ssa-ag-all-terminal")
        term, top = self.structure_term_sql_param()
        sql = 'SELECT count(*) nums FROM {} where log_type=2 and (login_type=6 or login_type=7) {} group by term_ip,login_type order by nums desc {}'.format(
            ", ".join(index_list_str), term, top)
        result_list = exec_es_sql(sql)
        labels = []
        login_type_list = []
        act_type_name_list = {"6": "卸载", "7": "安装"}
        new_result_dict = dict()
        for item in result_list:
            if item['term_ip'] not in labels:
                labels.append(item['term_ip'])
                new_result_dict[item['term_ip']] = dict()
            if item['login_type'] not in login_type_list:
                login_type_list.append(item['login_type'])
            new_result_dict[item['term_ip']][item['login_type']] = item['nums']
        data_list_dict = {}
        for login_type in login_type_list:
            data_list_dict[login_type] = []
            for term_ip in labels:
                if login_type in new_result_dict[term_ip]:
                    data_list_dict[login_type].append(new_result_dict[term_ip][login_type])
                else:
                    data_list_dict[login_type].append(0)
        data = []
        for login_type in login_type_list:
            data.append({"name": act_type_name_list[str(login_type)], "data": data_list_dict[login_type]})
        return {
            "labels": labels,
            "data": data
        }


class TmsInstallTableData(BaseData):
    """
    TMS安装详情
    """

    def data(self):
        act_type_name_list = {"6": "卸载", "7": "安装"}
        start_time, end_time, count_name, index_list_str = get_index_by_count_type(self.cycle, "ssa-ag-all-terminal")
        term, top = self.structure_term_sql_param()
        sql = 'SELECT term_ip,term_duty,term_group_name,act_time,login_type FROM {} where log_type=2 and (login_type=6 or login_type=7) {} order by act_time desc'.format(
            ", ".join(index_list_str), term)
        result_list = exec_es_sql(sql)
        data_list = []
        for item in result_list:
            item['act_time'] = datetime.strptime(item['act_time'], "%Y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
            login_type = item['login_type']
            item['login_type'] = act_type_name_list[str(login_type)]
            if self.term and self.term[0]['id']:
                term_name = get_term_name(self.term[0]['id'])
            else:
                term_name = item['term_group_name']
            data_list.append({
                'name': 'TMS安装卸载',
                'data': [item['term_ip'], item['term_duty'], term_name, item['act_time'],
                         item['login_type']]
            })
        labels = ['IP', '终端负责人', '用户组名称', '操作时间', '操作']
        return report_data_table(data_list, labels)


# ------网络


class FirewallFlowData(BaseData):
    """
    流量统计
    """

    def data(self):
        sql = 'SELECT sum(flow) flow_total FROM {} group by date_histogram(field=\'{}\',\'interval\'=\'{}\',\'format\'=\'yyyy-MM-dd\')'
        time_param, sql = get_exec_sql(sql, self.cycle, "ssa-ag-fw", "time")
        day_list = []
        day_flow_total_list = []
        result_list = exec_es_sql(sql)
        if len(result_list) > 0:
            for result in result_list:
                day_list.append(result[time_param])
                day_flow_total_list.append(result['flow_total'])
        return report_data_rule1(day_flow_total_list, day_list, "流量统计")


class FirewallSrcIpFlowData(BaseData):
    """
    源IP流量统计
    """

    def data(self):
        start_time, end_time, count_name, index_list_str = get_index_by_count_type(self.cycle, "ssa-ag-fw")
        sql = 'SELECT sum(flow) as flow_total FROM {}  group by src_ip order by flow_total desc {}'
        top = ""
        if self.top:
            top = "limit " + str(self.top)
        sql = sql.format(",".join(index_list_str), top)
        result_list = exec_es_sql(sql)
        labels = []
        data = []
        for item in result_list:
            labels.append(item['src_ip'])
            data.append(item['flow_total'])
        name = "源IP流量"
        return report_data_rule1(data, labels, name)


class FirewallDstIpFlowData(BaseData):
    """
    目的IP流量统计
    """

    def data(self):
        start_time, end_time, count_name, index_list_str = get_index_by_count_type(self.cycle, "ssa-ag-fw")
        sql = 'select sum(flow) flow_total from {} group by dst_ip  order by flow_total desc {}'
        top = ""
        if self.top:
            top = "limit " + str(self.top)
        sql = sql.format(",".join(index_list_str), top)
        result_list = exec_es_sql(sql)
        labels = []
        data = []
        for item in result_list:
            labels.append(item['dst_ip'])
            data.append(item['flow_total'])
        name = "目的IP流量"
        return report_data_rule1(data, labels, name)


class FirewallProFlowData(BaseData):
    """
    协议流量统计
    """

    def data(self):
        sql = 'select sum(flow) flow from {} group by protocol,date_histogram(field=\'{}\',\'interval\'=\'{}\',\'format\'=\'yyyy-MM-dd\')'
        time_param, sql = get_exec_sql(sql, self.cycle, "ssa-ag-fw", "time")
        day_list = []  # 存储数据查询出的日期
        protocol_list = []
        protocol_data_dict = dict()  # 存储每种类型的时间数list
        result_list = exec_es_sql(sql)
        new_result_dict = dict()
        data_list = []  # 拼接返回数据data
        if len(result_list) > 0:
            for result in result_list:
                result_day = result[time_param]
                protocol = result['protocol']
                if result_day not in day_list:
                    day_list.append(result_day)
                if protocol not in protocol_list:
                    protocol_list.append(protocol)
                    new_result_dict[protocol] = dict()
                    protocol_data_dict[protocol] = []
                new_result_dict[protocol][result_day] = result['flow']
        for day in day_list:
            for protocol in protocol_list:
                if day in new_result_dict[protocol]:
                    protocol_data_dict[protocol].append(new_result_dict[protocol][day])
                else:
                    protocol_data_dict[protocol].append(0)
        for protocol in protocol_list:
            data_list.append({'name': protocol, 'data': protocol_data_dict[protocol]})
        return {
            "labels": day_list,
            "data": data_list
        }


class ConRefuseData(BaseData):
    """
    会话拒绝统计
    """

    def data(self):
        sql = 'select count(*) nums from {} group by protocol,date_histogram(field=\'{}\',\'interval\'=\'{}\',\'format\'=\'yyyy-MM-dd\')'
        time_param, sql = get_exec_sql(sql, self.cycle, "ssa-ag-fw", "time")
        day_list = []  # 存储数据查询出的日期
        protocol_list = []
        protocol_data_dict = dict()  # 存储每种类型的时间数list
        result_list = exec_es_sql(sql)
        new_result_dict = dict()
        data_list = []  # 拼接返回数据data
        if len(result_list) > 0:
            for result in result_list:
                result_day = result[time_param]
                protocol = result['protocol']
                if result_day not in day_list:
                    day_list.append(result_day)
                if protocol not in protocol_list:
                    protocol_list.append(protocol)
                    new_result_dict[protocol] = dict()
                    protocol_data_dict[protocol] = []
                new_result_dict[protocol][result_day] = result['nums']
        for day in day_list:
            for protocol in protocol_list:
                if day in new_result_dict[protocol]:
                    protocol_data_dict[protocol].append(new_result_dict[protocol][day])
                else:
                    protocol_data_dict[protocol].append(0)
        for protocol in protocol_list:
            data_list.append({'name': protocol, 'data': protocol_data_dict[protocol]})
        return {
            "labels": day_list,
            "data": data_list
        }


class IsolationFlowCountData(BaseData):
    """
    隔离流量统计
    """

    def data(self):
        sql = 'SELECT sum(send_flow_statis) send_flow,sum(recv_flow_statis) recv_flow FROM {} group by date_histogram(field=\'{}\',\'interval\'=\'{}\',\'format\'=\'yyyy-MM-dd\')'
        time_param, sql = get_exec_sql(sql, self.cycle, "ssa-ag-gl", "starttime")
        day_list = []
        day_flow_total_list = []
        result_list = exec_es_sql(sql)
        if len(result_list) > 0:
            for result in result_list:
                day_list.append(result[time_param])
                day_flow_total_list.append(result['send_flow'] + result['recv_flow'])
        return report_data_rule1(day_flow_total_list, day_list, " 隔离流量统计")


class IsolationSrcFlowCountData(BaseData):
    """
    隔离源流量统计
    """

    def data(self):
        start_time, end_time, count_name, index_list_str = get_index_by_count_type(self.cycle, "ssa-ag-gl")
        sql = 'SELECT sum(send_flow_statis) flow FROM {} group by src_ip order by flow desc {}'
        top = ""
        if self.top:
            top = "limit " + str(self.top)
        sql = sql.format(",".join(index_list_str), top)
        result_list = exec_es_sql(sql)
        src_ip_list = []
        data_list = []
        for count in result_list:
            src_ip_list.append(count['src_ip'])
            data_list.append(count['flow'])
        return report_data_rule1(data_list, src_ip_list, "流量")


class IsolationDstFlowCountData(BaseData):
    """
    隔离目的流量统计
    """

    def data(self):
        start_time, end_time, count_name, index_list_str = get_index_by_count_type(self.cycle, "ssa-ag-gl")
        sql = 'SELECT sum(recv_flow_statis) flow FROM {} group by dst_ip order by flow desc {}'
        top = ""
        if self.top:
            top = "limit " + str(self.top)
        sql = sql.format(",".join(index_list_str), top)
        result_list = exec_es_sql(sql)
        dst_ip_list = []
        data_list = []
        for count in result_list:
            dst_ip_list.append(count['dst_ip'])
            data_list.append(count['flow'])
        return report_data_rule1(data_list, dst_ip_list, "流量")


# 攻击事件-----------------
class AttackEventCountData(BaseData):
    """
    攻击事件统计
    """

    def data(self):
        sql = 'SELECT sum(event_total) nums FROM {} where event_one_type = \'攻击\' group by date_histogram(field=\'{}\',\'interval\'=\'{}\',\'format\'=\'yyyy-MM-dd\')'
        time_param, sql = get_exec_sql(sql, self.cycle, "all-event", "stastic_time")
        day_list = []
        day_nums_list = []
        result_list = exec_es_sql(sql)
        if len(result_list) > 0:
            for result in result_list:
                day_list.append(result[time_param])
                day_nums_list.append(result['nums'])
        return report_data_rule1(day_nums_list, day_list, "攻击事件统计")


class SecurityTypeData(BaseData):
    """
    安全类型统计
    """

    def data(self):
        sql = 'SELECT sum(event_total) nums FROM {} where event_one_type = \'攻击\' group by event_three_type,date_histogram(field=\'{}\',\'interval\'=\'{}\',\'format\'=\'yyyy-MM-dd\')'
        time_param, sql = get_exec_sql(sql, self.cycle, "all-event", "stastic_time")
        day_list = []  # 存储数据查询出的日期
        event_type_list = []
        event_type_nums_list = dict()  # 存储每种类型的时间数list
        result_list = exec_es_sql(sql)
        new_result_dict = dict()
        data_list = []  # 拼接返回数据data
        if len(result_list) > 0:
            for result in result_list:
                result_day = result[time_param]
                result_event_type = result['event_three_type']
                if result_event_type not in event_type_nums_list:
                    event_type_list.append(result_event_type)
                    new_result_dict[result_event_type] = dict()
                    event_type_nums_list[result_event_type] = []
                if result_day not in day_list:
                    day_list.append(result_day)
                new_result_dict[result_event_type][result_day] = result['nums']
        for day in day_list:
            for event_type in event_type_list:
                if day in new_result_dict[event_type]:
                    event_type_nums_list[event_type].append(new_result_dict[event_type][day])
                else:
                    event_type_nums_list[event_type].append(0)
        for event_type in event_type_list:
            data_list.append({'name': event_type, 'data': event_type_nums_list[event_type]})
        return {
            "labels": day_list,
            "data": data_list
        }


class AttackLevelCountData(BaseData):
    """
    攻击严重等级事件数统计
    """

    def data(self):
        start_time, end_time, count_name, index_list_str = get_index_by_count_type(self.cycle, "all-event")
        sql = 'SELECT sum(event_total) nums FROM {} where event_one_type = \'攻击\' group by event_level order by nums desc {}'
        top = ""
        if self.top:
            top = "limit " + str(self.top)
        sql = sql.format(",".join(index_list_str), top)
        level_list = []
        data = []
        result_list = exec_es_sql(sql)
        if len(result_list) > 0:
            for result in result_list:
                level = result['event_level']
                nums = result['nums']
                level_list.append(level)
                data.append(nums)
        level_name_dict = {"1": "低", "2": "中", "3": "高"}
        level_name_list = []
        for level in level_list:
            level = str(level)
            if level in level_name_dict:
                level_name_list.append(level_name_dict[level])
            else:
                level_name_list.append(level)
        data_dict = [{
            'name': "攻击严重等级事件数统计",
            'data': data
        }]
        return {
            "labels": level_name_list,
            "data": data_dict
        }


class AttackSrcIpCountData(BaseData):
    """
    攻击源IP统计
    """

    def data(self):
        start_time, end_time, count_name, index_list_str = get_index_by_count_type(self.cycle, "all-event")
        sql = 'SELECT sum(event_total) nums FROM {} where event_one_type = \'攻击\' group by src_ip order by nums desc {}'
        top = ""
        if self.top:
            top = "limit " + str(self.top)
        sql = sql.format(",".join(index_list_str), top)
        src_ip_list = []
        data = []
        result_list = exec_es_sql(sql)
        if len(result_list) > 0:
            for result in result_list:
                src_ip = result['src_ip']
                nums = result['nums']
                src_ip_list.append(src_ip)
                data.append(nums)

        data_dict = [{
            'name': "攻击源IP统计",
            'data': data
        }]
        return {
            "labels": src_ip_list,
            "data": data_dict
        }


class AttackDstIpCountData(BaseData):
    """
    攻击目标IP统计
    """

    def data(self):
        start_time, end_time, count_name, index_list_str = get_index_by_count_type(self.cycle, "all-event")
        sql = 'SELECT sum(event_total) nums FROM {} where event_one_type = \'攻击\' group by dst_ip order by nums desc {}'
        top = ""
        if self.top:
            top = "limit " + str(self.top)
        sql = sql.format(",".join(index_list_str), top)
        dst_ip_list = []
        data = []
        result_list = exec_es_sql(sql)
        if len(result_list) > 0:
            for result in result_list:
                dst_ip = result['dst_ip']
                nums = result['nums']
                dst_ip_list.append(dst_ip)
                data.append(nums)
        data_dict = [{
            'name': "攻击源IP统计",
            'data': data
        }]
        return {
            "labels": dst_ip_list,
            "data": data_dict
        }


# 违规事件-----------------

class ViolationEventCountData(BaseData):
    """
    违规事件统计
    """

    def data(self):
        sql = 'SELECT sum(event_total) nums FROM {} where event_one_type = \'违规\' group by date_histogram(field=\'{}\',\'interval\'=\'{}\',\'format\'=\'yyyy-MM-dd\')'
        time_param, sql = get_exec_sql(sql, self.cycle, "all-event", "stastic_time")
        day_list = []
        day_nums_list = []
        result_list = exec_es_sql(sql)
        if len(result_list) > 0:
            for result in result_list:
                day_list.append(result[time_param])
                day_nums_list.append(result['nums'])
        return report_data_rule1(day_nums_list, day_list, "违规事件统计")


class ViolationTypeCountData(BaseData):
    """
    终端违规类型统计
    """

    def data(self):
        term = self.structure_org_sql_param()
        sql = 'SELECT sum(event_total) nums FROM {} where event_one_type = \'违规\' and event_source = 7 {} group by event_three_type,date_histogram(field=\'stastic_time\',\'interval\'=\'{}\',\'format\'=\'yyyy-MM-dd\')'
        start_time, end_time, count_name, index_list_str = get_index_by_count_type(self.cycle, "all-event")
        if index_list_str:
            sql = sql.format(','.join(index_list_str), term, count_name)
        day_list = []  # 存储数据查询出的日期
        event_type_list = []
        event_type_nums_list = dict()  # 存储每种类型的时间数list
        result_list = exec_es_sql(sql)
        new_result_dict = dict()
        data_list = []  # 拼接返回数据data
        if len(result_list) > 0:
            for result in result_list:
                result_day = result.values()[1]
                result_event_type = result.values()[0]
                if result_event_type not in event_type_nums_list:
                    event_type_list.append(result_event_type)
                    new_result_dict[result_event_type] = dict()
                    event_type_nums_list[result_event_type] = []
                if result_day not in day_list:
                    day_list.append(result_day)
                new_result_dict[result_event_type][result_day] = result.values()[2]
        for day in day_list:
            for event_type in event_type_list:
                if day in new_result_dict[event_type]:
                    event_type_nums_list[event_type].append(new_result_dict[event_type][day])
                else:
                    event_type_nums_list[event_type].append(0)
        for event_type in event_type_list:
            data_list.append({'name': event_type, 'data': event_type_nums_list[event_type]})
        return {
            "labels": day_list,
            "data": data_list
        }

    def structure_org_sql_param(self):
        if self.term != "":
            term = " and organization = '" + str(self.term) + "'"
        else:
            term = ""
        return term


class TermViolationEventCountData(BaseData):
    """
    终端违规事件统计TOP5
    """

    def data(self):
        term, top = self.structure_org_sql_param()
        event_type_list = []
        data = []
        start_time, end_time, count_name, index_list_str = get_index_by_count_type(self.cycle, "all-event")
        sql = "SELECT sum(event_total) nums FROM {} where event_one_type = \'违规\' and event_source = 7 {} group by event_three_type order by nums desc {}".format(
            ",".join(index_list_str), term, top)
        result_list = exec_es_sql(sql)
        if len(result_list) > 0:
            for result in result_list:
                event_type = result['event_three_type']
                event_type_list.append(event_type)
                data.append(result['nums'])
        return report_data_rule1(data, event_type_list, "终端违规事件统计")

    def structure_org_sql_param(self):
        if self.term != "":
            term = " and organization = '" + str(self.term) + "'"
        else:
            term = ""
        if self.top != "":
            top = "limit " + str(self.top)
        else:
            top = ""
        return term, top


class DbViolationEventCountData(BaseData):
    """
    数据库违规事件统计
    """

    def data(self):
        sql = 'SELECT sum(event_total) nums FROM {} where event_one_type = \'违规\' and event_source = 3 group by date_histogram(field=\'{}\',\'interval\'=\'{}\',\'format\'=\'yyyy-MM-dd\')'
        time_param, sql = get_exec_sql(sql, self.cycle, "all-event", "stastic_time")
        day_list = []
        day_nums_list = []
        result_list = exec_es_sql(sql)
        if len(result_list) > 0:
            for result in result_list:
                day_list.append(result[time_param])
                day_nums_list.append(result['nums'])
        return report_data_rule1(day_nums_list, day_list, "数据库违规事件统计")


class DbViolationTypeCountData(BaseData):
    """
    违规操作数据库类型事件统计
    """

    def data(self):
        sql = 'SELECT sum(event_total) nums FROM {} where event_one_type = \'违规\' and event_source = 3 group by event_three_type,date_histogram(field=\'{}\',\'interval\'=\'{}\',\'format\'=\'yyyy-MM-dd\')'
        time_param, sql = get_exec_sql(sql, self.cycle, "all-event", "stastic_time")
        day_list = []  # 存储数据查询出的日期
        event_type_list = []
        event_type_nums_list = dict()  # 存储每种类型的时间数list
        result_list = exec_es_sql(sql)
        new_result_dict = dict()
        data_list = []  # 拼接返回数据data
        if len(result_list) > 0:
            for result in result_list:
                result_day = result[time_param]
                result_event_type = result['event_three_type']
                if result_event_type not in event_type_nums_list:
                    event_type_list.append(result_event_type)
                    new_result_dict[result_event_type] = dict()
                    event_type_nums_list[result_event_type] = []
                if result_day not in day_list:
                    day_list.append(result_day)
                new_result_dict[result_event_type][result_day] = result['nums']
        for day in day_list:
            for event_type in event_type_list:
                if day in new_result_dict[event_type]:
                    event_type_nums_list[event_type].append(new_result_dict[event_type][day])
                else:
                    event_type_nums_list[event_type].append(0)
        for event_type in event_type_list:
            data_list.append({'name': event_type, 'data': event_type_nums_list[event_type]})
        return {
            "labels": day_list,
            "data": data_list
        }


class DbViolationProCountData(BaseData):
    """
    数据库操作协议统计
    """

    def data(self):
        start_time, end_time, count_name, index_list_str = get_index_by_count_type(self.cycle, "all-event")
        sql = 'SELECT sum(event_total) nums FROM {} where event_one_type = \'违规\' and event_source = 3 group by app_protocol order by nums desc {}'
        top = ""
        if self.top:
            top = "limit " + str(self.top)
        sql = sql.format(",".join(index_list_str), top)
        protocol_list = []
        data = []
        result_list = exec_es_sql(sql)
        if len(result_list) > 0:
            for result in result_list:
                protocol = result['app_protocol']
                protocol_list.append(protocol)
                data.append(result['nums'])
        return report_data_rule1(data, protocol_list, "数据库操作协议统计")


class DbViolationLevelCountData(BaseData):
    """
    数据库操作严重等级事件数统计
    """

    def data(self):
        event_level_list = []
        event_level_name_dict = {"1": "低", "2": "中", "3": "高"}
        event_level_name_list = []
        data = []
        start_time, end_time, count_name, index_list_str = get_index_by_count_type(self.cycle, "all-event")
        sql = 'SELECT sum(event_total) nums FROM {} where event_one_type = \'违规\' and event_source = 3 group by event_level order by nums desc {}'
        top = ""
        if self.top:
            top = "limit " + str(self.top)
        sql = sql.format(",".join(index_list_str), top)
        result_list = exec_es_sql(sql)
        if len(result_list) > 0:
            for result in result_list:
                event_level = result['event_level']
                event_level_list.append(event_level)
                data.append(result['nums'])
        for level in event_level_list:
            level = str(level)
            if level in event_level_name_dict:
                event_level_name_list.append(event_level_name_dict[level])
            else:
                event_level_name_list.append(level)
        return report_data_rule1(data, event_level_name_list, "数据库操作严重等级事件数统计")


# 病毒数据分析---------------------------

class VirusEventCountData(BaseData):
    """
    病毒事件统计
    """

    def data(self):
        sql = 'SELECT sum(event_total) nums FROM {} where event_one_type = \'病毒\' group by date_histogram(field=\'{}\',\'interval\'=\'{}\',\'format\'=\'yyyy-MM-dd\')'
        time_param, sql = get_exec_sql(sql, self.cycle, "all-event", "stastic_time")
        day_list = []
        day_nums_list = []
        result_list = exec_es_sql(sql)
        if len(result_list) > 0:
            for result in result_list:
                day_list.append(result[time_param])
                day_nums_list.append(result['nums'])
        return report_data_rule1(day_nums_list, day_list, "病毒事件统计")


class VirusEventTypeCountData(BaseData):
    """
    病毒类型统计
    """

    def data(self):
        sql = 'SELECT sum(event_total) nums FROM {} where event_one_type = \'病毒\' group by event_three_type,date_histogram(field=\'{}\',\'interval\'=\'{}\',\'format\'=\'yyyy-MM-dd\')'
        time_param, sql = get_exec_sql(sql, self.cycle, "all-event", "stastic_time")
        day_list = []  # 存储数据查询出的日期
        event_type_list = []
        event_type_nums_list = dict()  # 存储每种类型的时间数list
        result_list = exec_es_sql(sql)
        new_result_dict = dict()
        data_list = []  # 拼接返回数据data
        if len(result_list) > 0:
            for result in result_list:
                result_day = result[time_param]
                result_event_type = result['event_three_type']
                if result_event_type not in event_type_nums_list:
                    event_type_list.append(result_event_type)
                    new_result_dict[result_event_type] = dict()
                    event_type_nums_list[result_event_type] = []
                if result_day not in day_list:
                    day_list.append(result_day)
                new_result_dict[result_event_type][result_day] = result['nums']
        for day in day_list:
            for event_type in event_type_list:
                if day in new_result_dict[event_type]:
                    event_type_nums_list[event_type].append(new_result_dict[event_type][day])
                else:
                    event_type_nums_list[event_type].append(0)
        for event_type in event_type_list:
            data_list.append({'name': event_type, 'data': event_type_nums_list[event_type]})
        return {
            "labels": day_list,
            "data": data_list
        }


class VirusIpCountData(BaseData):
    """
    病毒IP统计
    """

    def data(self):
        src_ip_list = []
        data = []
        data_tag = "all-event"
        start_time, end_time, count_name, index_list_str = get_index_by_count_type(self.cycle, data_tag)
        sql = "SELECT sum(event_total) nums FROM {} where event_one_type = \'病毒\' group by src_ip order by nums desc {}"
        top = ""
        if self.top:
            top = "limit " + str(self.top)
        sql = sql.format(",".join(index_list_str), top)
        result_list = exec_es_sql(sql)
        if len(result_list) > 0:
            for result in result_list:
                src_ip = result['src_ip']
                src_ip_list.append(src_ip)
                data.append(result['nums'])
        return report_data_rule1(data, src_ip_list, "病毒IP统计")


def demo_data():
    data = {
        "labels": ['01-01', '01-02', '01-03', '01-04', '01-05', '01-06', '01-07'],
        "data": [
            {"name": "数据一", "data": [19, 33, 88, 22, 66, 44, 11]},
            {"name": "数据二", "data": [4, 22, 55, 99, 77, 22, 77]},
            {"name": "数据三", "data": [12, 1, 88, 33, 99, 221, 88]}
        ]
    }
    return data


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
    elif count_type == 7:
        for i in xrange(0, 6):
            start_time = (datetime.now() - timedelta(weeks=i)).strftime("%Y-%m-%d")
            date_list.append(start_time)
        date_list.reverse()
    elif count_type == 30:
        for i in xrange(0, 5):
            start_time = get_today_month(-i)
            date_list.append(start_time)
        date_list.reverse()
    elif count_type == 90:
        for i in xrange(0, 3):
            start_time = get_today_month(-3 * i)
            date_list.append(start_time)
        date_list.reverse()
    elif count_type == 365:
        for i in xrange(0, 3):
            start_time = get_today_month(-12 * i)
            date_list.append(start_time)
        date_list.reverse()
    return date_list


def get_index_by_count_type(count_type, data_tag):
    try:
        es_host = SelfServiceConf.objects.get(service="es")
    except SelfServiceConf.DoesNotExist:
        raise ValueError("ES服务未配置")
    start_time = (datetime.now() - timedelta(days=6)).strftime("%Y-%m-%d") + " 00:00:00"
    count_name = "day"
    if count_type == 7:
        count_name = "week"
        start_time = (datetime.now() - timedelta(weeks=6)).strftime("%Y-%m-%d") + " 00:00:00"
    elif count_type == 30:
        count_name = "month"
        start_time = get_today_month(-5) + " 00:00:00"
    elif count_type == 90:
        count_name = "quarter"
        start_time = get_today_month(-11) + " 00:00:00"
    elif count_type == 365:
        count_name = "year"
        start_time = get_today_month(-47) + " 00:00:00"
    end_time = time.strftime("%Y-%m-%d") + " 23:59:59"
    index_list_str = ""
    if data_tag:
        # 查询出周期内的所有索引
        index_list_str = generate_index(datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"),
                                        datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S"), data_tag, es_host.host)
    return start_time, end_time, count_name, index_list_str


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


def get_exec_sql(sql, count_type, data_tag, time_field):
    """
    通过传递的周期类型和索引进行拼接sql
    :param sql:
    :param count_type:
    :param data_tag:
    :return:
    """
    start_time, end_time, count_name, index_list_str = get_index_by_count_type(count_type, data_tag)
    if index_list_str:
        sql = sql.format(','.join(index_list_str), time_field, count_name)
    time_param = "date_histogram(field={},interval={},format=yyyy-MM-dd)".format(time_field, count_name)
    return time_param, sql


if __name__ == "__main__":
    pass
