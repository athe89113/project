# -*- coding:utf-8 -*-
import json

from datetime import datetime

from soc_assets.models import Assets, TermGroup
from soc_ssa.tools.make_docx.fetch_new_data import only_generate_index

from utils.es_select import exec_es_sql


def asset_status(days):
    '''
    资产状态
    '''
    index = ['statistics-*-{}-*'.format(day) for day in days]
    sql = 'select log_source,count(distinct terminal) count_ from {}  ' \
          'group by log_source'.format(','.join(index))
    result = exec_es_sql(sql=sql)
    labes = [u'数据库审计', u'IDS', u'隔离设备', u'摆渡设备', u'360', u'终端']
    event_source_type = [3, 2, 5, 4, 6, 7]
    for item in result:
        log_source = item['log_source']
        if u'防火墙' in log_source and log_source not in labes:
            labes.append(log_source)
            event_source_type.append(1)

    data = []
    for index, lab in enumerate(labes):
        assets_num, normal, off, abnormal = 0, 0, 0, 0
        for item in result:
            if item['log_source'] == lab:
                assets_num = item['count_']
                continue
        # 防火墙
        where = ''
        if event_source_type[index] == 1:
            where = ' and event_host=\'\' '.format(lab.replace(u'防火墙', ''))
        event_index = ['all-event-{}-*'.format(day) for day in days]
        assets_sql = 'SELECT event_source,count(distinct event_host) count_,sum(event_total) sum_ ' \
                     'FROM {} where event_source={} {} group by event_source ' \
                     ''.format(','.join(event_index), event_source_type[index], where)
        assets_count = exec_es_sql(sql=assets_sql)
        if assets_count:
            normal = assets_count[0]['count_']
            abnormal = assets_count[0]['sum_']

        if normal > assets_num:
            assets_num = normal
            off = 0
        else:
            off = assets_num - normal
        if lab == '360':
            data.append([u'杀毒软件', assets_num, normal, off, abnormal])
        else:
            data.append([lab, assets_num, normal, off, abnormal])
    results = {"labels": [u'类型', u'数量 ', u'采集正常', u'采集断开', u'异常事件数'], "data": data}

    return results


def event_num_count(days):
    '''
    设备事件量占比
    '''
    index = ['all-event-{}-*'.format(day) for day in days]
    event_source_sql = 'select event_source,sum(event_total) count_ from {}  ' \
                       'where event_level>0 group by event_source order by count_ desc'.format(','.join(index))
    event_source_result = exec_es_sql(sql=event_source_sql)

    event_source_data = []
    source_name = [u'数据库审计', u'IDS', u'隔离设备', u'摆渡设备', u'终端', u'杀毒软件']
    source_type = [3, 2, 5, 4, 7, 6]
    source_data = [0, 0, 0, 0, 0, 0]
    for item in event_source_result:
        if item['event_source'] in source_type:
            i = source_type.index(item['event_source'])
            source_data[i] += item['count_']
            continue
    for i in range(len(source_name)):
        event_source_data.append({
            'name': source_name[i],
            'data': [source_data[i]]
        })
    # 防火墙
    event_source_fw_sql = 'select event_host,sum(event_total) count_ from {}  ' \
                          'where event_level>0 and event_source=1 ' \
                          'group by event_host order by count_ desc'.format(','.join(index))
    event_source_fw_result = exec_es_sql(sql=event_source_fw_sql)
    for fw in event_source_fw_result:
        event_source_data.append({
            'name': u'防火墙{}'.format(fw['event_host']),
            'data': [fw['count_']]
        })
    result = {
        "labels": u"事件来源",
        "data": event_source_data
    }
    return result


def event_thred_count(days):
    '''
    事件趋势统计
    '''
    index = ['all-event-{}-*'.format(day) for day in days]
    sql = 'select event_source,event_host,sum(event_total) count_ from {} ' \
          'where event_level>0 ' \
          'group by date_histogram(field=\'start_time\',\'interval\'=\'1d\') ' \
          ',event_source,event_host order by  start_time'.format(','.join(index))
    result = exec_es_sql(sql=sql)
    days, data_list = [], []

    source_name = [u'数据库审计', u'IDS', u'隔离设备', u'摆渡设备', u'终端', u'杀毒软件']
    source_type = [3, 2, 5, 4, 7, 6]
    for item in result:
        day = item['date_histogram(field=start_time,interval=1d)'][0:10]
        if day not in days:
            days.append(day)
        if item['event_source'] == 1:
            event_source = u'防火墙{}'.format(item['event_host'])
            if event_source not in source_name:
                source_name.append(event_source)

    for index, source in enumerate(source_name):
        data_dict = {
            'name': source,
            'data': []
        }
        for d in range(len(days)):
            event_count = 0
            for item in result:
                if item['event_source'] == 1:
                    event_source = u'防火墙{}'.format(item['event_host'])
                else:
                    event_source = source_name[source_type.index(item['event_source'])]

                day = item['date_histogram(field=start_time,interval=1d)'][0:10]
                if day == days[d] and source == event_source:
                    event_count += item['count_']
            data_dict['data'].append(event_count)
        data_list.append(data_dict)
    data = {'labels': days, 'data': data_list}
    return data


def risk_event_count(days):
    '''
    风险事件统计
    '''
    index = ['all-event-{}-*'.format(day) for day in days]
    sql = 'select event_two_type,event_level,count(*) count_ ' \
          'from {} where event_level>0 ' \
          'group by event_two_type,event_level ' \
          'order by event_two_type,event_level'.format(','.join(index))
    count_list = exec_es_sql(sql=sql)
    row = []
    for item in count_list:
        event_level = ''
        if item['event_level'] == 1:
            event_level = u'一般'
        elif item['event_level'] == 2:
            event_level = u'危险'
        elif item['event_level'] == 3:
            event_level = u'非常危险'
        else:
            pass
        row.append([item['event_two_type'], event_level, item['count_']])
    result = {
        "labels": [u"事件名称", u"事件级别", u"事件数量"],
        "data": row
    }
    return result


def risk_assets_count(days):
    '''
    风险资产统计
    '''
    index = ['all-event-{}-*'.format(day) for day in days]
    sql = 'select event_host,count(*) count_,sum(event_total) sum_ ' \
          'from {} where event_level>0 group by event_host '.format(','.join(index))
    count_list = exec_es_sql(sql=sql)
    row = []
    for item in count_list:
        row.append([item['event_host'], item['count_'], item['sum_']])
    result = {
        "labels": [u"资产IP", u"风险值", u"事件数量"],
        "data": row
    }
    return result


def risk_org_count(days):
    '''
    风险部门统计
    '''
    index = ['all-event-{}-*'.format(day) for day in days]
    sql = 'select organization,count(*) count_,sum(event_total) sum_,count(distinct event_host) count_ip ' \
          'from {} where event_level>0 and organization<>\'\' ' \
          'group by organization'.format(','.join(index))
    count_list = exec_es_sql(sql=sql)
    row = []
    for item in count_list:
        row.append([item['organization'], item['count_'], item['sum_'], item['count_ip']])
    result = {
        "labels": [u"部门名称", u"风险值", u"事件数量", u"涉及终端数"],
        "data": row
    }
    return result


def irregularly_source_count(days):
    '''
    违规来源统计
    '''
    index = ['all-event-{}-*'.format(day) for day in days]
    sql = 'select event_source,count(*) count_ ' \
          'from {} where event_level>0 and event_one_type=\'违规\' ' \
          'group by event_source'.format(','.join(index))
    count_list = exec_es_sql(sql=sql)
    source_name = [u'防火墙', u'数据库审计', u'IDS', u'隔离设备', u'摆渡设备', u'终端', u'杀毒软件']
    source_type = [1, 3, 2, 5, 4, 7, 6]
    row = []
    for item in count_list:
        i = source_type.index(item['event_source'])
        row.append({
            'name': source_name[i],
            'data': [item['count_']]
        })
    result = {
        "labels": [u"违规来源"],
        "data": row
    }
    return result


def irregularly_type_count(days):
    '''
    违规类型统计
    '''
    index = ['all-event-{}-*'.format(day) for day in days]
    sql = 'select event_source,event_three_type,count(*) count_,count(distinct event_host) count_ip ' \
          'from {} where event_level>0 and event_one_type=\'违规\' ' \
          'group by event_source,event_three_type order by event_source'.format(','.join(index))
    count_list = exec_es_sql(sql=sql)
    source_name = [u'防火墙', u'数据库审计', u'IDS', u'隔离设备', u'摆渡设备', u'终端', u'杀毒软件']
    source_type = [1, 3, 2, 5, 4, 7, 6]
    row = []
    for item in count_list:
        i = source_type.index(item['event_source'])
        row.append([source_name[i], item['event_three_type'], item['count_'], item['count_ip']])
    result = {
        "labels": [u"违规事件来源", u"违规类型", u"违规事件数", u"涉及终端数"],
        "data": row
    }
    return result


def irregularly_ip_count(days):
    '''
    违规终端统计
    '''
    index = ['all-event-{}-*'.format(day) for day in days]
    sql = 'select event_host,event_three_type,count(*) count_ ' \
          'from {} where event_level>0 and event_one_type=\'违规\' ' \
          'group by event_host,event_three_type'.format(','.join(index))
    count_list = exec_es_sql(sql=sql)
    row = []
    for item in count_list:
        row.append([item['event_host'], item['event_three_type'], item['count_']])
    result = {
        "labels": [u"终端IP", u"违规类型", u"违规事件数"],
        "data": row
    }
    return result


def irregularly_org_count(days):
    '''
    违规单位统计
    '''
    index = ['all-event-{}-*'.format(day) for day in days]
    sql = 'select organization,event_three_type,count(*) count_,count(distinct event_host) count_ip ' \
          'from {} where event_level>0 and event_one_type=\'违规\' and organization<> \'\' ' \
          'group by organization,event_three_type'.format(','.join(index))
    count_list = exec_es_sql(sql=sql)
    row = []
    for item in count_list:
        row.append([item['organization'], item['event_three_type'], item['count_'], item['count_ip']])
    result = {
        "labels": [u"单位名称", u"违规类型", u"违规事件数", u"涉及终端数"],
        "data": row
    }
    return result


def viruses_type_count(days):
    '''
    病毒类型统计
    '''
    index = ['all-event-{}-*'.format(day) for day in days]
    sql = 'select event_three_type,count(*) count_ ' \
          'from {} where event_level>0 and event_one_type=\'病毒\' ' \
          'group by event_three_type'.format(','.join(index))
    count_list = exec_es_sql(sql=sql)
    row = []
    for item in count_list:
        row.append({
            'name': item['event_three_type'],
            'data': [item['count_']]
        })
    result = {
        "labels": [u"病毒类型"],
        "data": row
    }
    return result


def viruses_ip_count(days):
    '''
    感染病毒终端统计
    '''
    index = ['ssa-ag-360-{}-*'.format(day) for day in days]
    sql = 'select host_ip,virustype,infectedfileinfo_filepath,count(*) ' \
          'from {} group by host_ip,virustype,infectedfileinfo_filepath ' \
          'order by host_ip,virustype,infectedfileinfo_filepath'.format(','.join(index))
    count_list = exec_es_sql(sql=sql)
    ips, orgs = [], []
    for item in count_list:
        host_ip = item['host_ip']
        if host_ip not in ips:
            ips.append(host_ip)
            org = ''
            assets_list = Assets.objects.filter(ip=host_ip).values('term_group_id')
            if assets_list:
                term_list = TermGroup.objects.filter(term_group_id=assets_list.first()['term_group_id']).values(
                    'term_group_name')
                if term_list:
                    org = term_list.first()['term_group_name']
            orgs.append(org)
    row = []
    for item in count_list:
        i = ips.index(item['host_ip'])
        if orgs[i]:
            row.append([orgs[i], item['host_ip'], item['virustype'], item['infectedfileinfo_filepath']])
    result = {
        "labels": [u"单位名称", u"终端IP", u"病毒类型", u"感染目录"],
        "data": row
    }
    return result


def attack_type_count(days):
    '''
    攻击类型统计
    '''
    index = ['all-event-{}-*'.format(day) for day in days]
    sql = 'select event_three_type,count(*) count_ ' \
          'from {} where event_level>0 and event_one_type=\'攻击\' ' \
          'group by event_three_type'.format(','.join(index))
    count_list = exec_es_sql(sql=sql)
    row = []
    for item in count_list:
        row.append({
            'name': item['event_three_type'],
            'data': [item['count_']]
        })
    result = {
        "labels": [u"攻击类型"],
        "data": row
    }
    return result


def attack_source_count(days):
    '''
    攻击源统计
    '''
    index = ['all-event-{}-*'.format(day) for day in days]
    sql = 'select src_ip,count(*) count_ ' \
          'from {} where event_level>0 and event_one_type=\'攻击\' ' \
          'group by src_ip order by count_ desc limit 10'.format(','.join(index))
    count_list = exec_es_sql(sql=sql)
    labels = []
    for item in count_list:
        if item['src_ip'] not in labels:
            labels.append(item['src_ip'])
    flow_count = {
        'name': u'次数',
        'data': []
    }
    for lab in labels:
        count_ = 0
        for item in count_list:
            if lab == item['src_ip']:
                count_ = item['count_']
                continue
        flow_count['data'].append(count_)
    result = {
        "labels": labels,
        "data": [flow_count] if len(labels) > 0 else []
    }
    return result


def attack_ip_count(days):
    '''
    被攻击终端统计
    '''
    index = ['all-event-{}-*'.format(day) for day in days]
    sql = 'select dst_ip,event_three_type,count(*) count_ ' \
          'from {} where event_level>0 and event_one_type=\'攻击\' ' \
          'group by dst_ip,event_three_type order by count_ desc'.format(','.join(index))
    count_list = exec_es_sql(sql=sql)
    ips, orgs = [], []
    for item in count_list:
        dst_ip = item['dst_ip']
        if dst_ip not in ips:
            ips.append(dst_ip)
            org = ''
            assets_list = Assets.objects.filter(ip=dst_ip).values('term_group_id')
            if assets_list:
                term_list = TermGroup.objects.filter(term_group_id=assets_list.first()['term_group_id']).values(
                    'term_group_name')
                if term_list:
                    org = term_list.first()['term_group_name']
            orgs.append(org)
    row = []
    for item in count_list:
        i = ips.index(item['dst_ip'])
        if orgs[i]:
            row.append([orgs[i], item['dst_ip'], item['event_three_type']])
    result = {
        "labels": [u"单位名称", u"终端IP", u"攻击类型"],
        "data": row
    }
    return result


def terminal_on_off_count(days, term_id):
    '''
    终端开关机情况
    '''
    index = ['ssa-ag-all-terminal-{}-*'.format(day) for day in days]
    sql = 'SELECT term_group_name,login_ip,term_duty,act_time,login_type ' \
          'FROM {} where log_type = 2 and (login_type=4 or login_type=5) ' \
          'and term_group_id=\'{}\' order by act_time desc'.format(','.join(index), term_id)
    count_list = exec_es_sql(sql=sql)
    row = []
    for i, item in enumerate(count_list):
        act_time = datetime.strptime(item['act_time'], "%Y%m%d%H%M%S").strftime(
            "%Y-%m-%d %H:%M:%S")
        term_name = "其他部门"
        term_list = TermGroup.objects.filter(term_group_id=term_id).values('term_group_name')
        if term_list:
            term_name = term_list.first()['term_group_name']
        if item['login_type'] == 4:
            row.append([i + 1, item['login_ip'], item['term_duty'], term_name, act_time, ""])
        elif item['login_type'] == 5:
            row.append([i + 1, item['login_ip'], item['term_duty'], term_name, "", act_time])
    result = {
        "labels": [u"序号", u"IP", u"终端负责人", u"用户组名称", u"开机时间", u"关机时间"],
        "data": row
    }
    return result


def terminal_login_fail_count(days):
    '''
    登录失败统计
    '''
    index = ['ssa-ag-all-terminal-{}-*'.format(day) for day in days]
    sql = 'SELECT login_ip,count(*) count_ FROM {} where log_type=2 and login_result=0 ' \
          'group by login_ip order by count_ desc limit 10'.format(','.join(index))
    count_list = exec_es_sql(sql=sql)
    labels = []
    for item in count_list:
        if item['login_ip'] not in labels:
            labels.append(item['login_ip'])
    flow_count = {
        'name': u'登录失败次数',
        'data': []
    }
    for lab in labels:
        count_ = 0
        for item in count_list:
            if lab == item['login_ip']:
                count_ = item['count_']
                continue
        flow_count['data'].append(count_)
    result = {
        "labels": labels,
        "data": [flow_count] if len(labels) > 0 else []
    }
    return result


def terminal_print_count(days):
    '''
    打印情况统计
    '''
    index = ['ssa-ag-all-terminal-{}-*'.format(day) for day in days]
    sql = 'SELECT term_ip,act_type,count(*) count_ FROM {} ' \
          'where log_type=5 and request_type=1 and act_type in (0,1,2,3,4,5,7) ' \
          'group by term_ip,act_type order by count_ desc limit 10'.format(','.join(index))
    count_list = exec_es_sql(sql=sql)
    act_type_name = [u"拒绝打印", u"同意打印", u"打印审计", u"强制使用", u"自行取消", u"中心超时取消", u"离线使用"]
    act_type_value = ['0', '1', '2', '3', '4', '5', '7']
    ips = []
    for item in count_list:
        if item['term_ip'] not in ips:
            ips.append(item['term_ip'])
    row = []
    for i, act_type in enumerate(act_type_value):
        act_type_count_list = []
        for ip in ips:
            act_type_count = 0
            for item in count_list:
                if ip == item['term_ip'] and act_type == str(item['act_type']):
                    act_type_count = item['count_']
                    continue
            act_type_count_list.append(act_type_count)
        row.append({
            'name': act_type_name[i],
            'data': act_type_count_list
        })
    result = {
        "labels": ips,
        "data": row
    }
    return result


def terminal_print_list(days, term_id):
    '''
    各部门打印详情
    '''
    index = ['ssa-ag-all-terminal-{}-*'.format(day) for day in days]
    sql = 'SELECT term_ip,term_duty,term_group_name,act_time,act_type FROM {} ' \
          'where log_type=5 and request_type=1 and act_type in (0,1,2,3,4,5,7) ' \
          'and term_group_id=\'{}\' order by act_time desc'.format(','.join(index), term_id)
    count_list = exec_es_sql(sql=sql)
    act_type_name = [u"拒绝打印", u"同意打印", u"打印审计", u"强制使用", u"自行取消", u"中心超时取消", u"离线使用"]
    act_type_value = ['0', '1', '2', '3', '4', '5', '7']
    row = []
    for i, item in enumerate(count_list):
        act_time = datetime.strptime(item['act_time'], "%Y%m%d%H%M%S").strftime(
            "%Y-%m-%d %H:%M:%S")
        term_name = "其他部门"
        term_list = TermGroup.objects.filter(term_group_id=term_id).values('term_group_name')
        if term_list:
            term_name = term_list.first()['term_group_name']
        act_type = act_type_name[act_type_value.index(str(item['act_type']))]
        row.append([i + 1, item['term_ip'], item['term_duty'], term_name, act_time, act_type])
    result = {
        "labels": [u"序号", u"IP", u"终端负责人", u"用户组名称", u"打印时间", u"违规类型"],
        "data": row
    }
    return result


def terminal_offwork_print_count(days):
    '''
    下班打印统计TOP10
    '''
    all_day_result_list = []
    for day in days:
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
        sql = 'SELECT term_ip,count(*) count_ FROM {0} ' \
              'where log_type=5 and request_type=1 and ' \
              '((act_time > {1} and act_time < {2}) or (act_time > {3} and act_time < {4})) ' \
              'group by term_ip'.format(", ".join(indexs), start_time_one, end_time_one,
                                        start_time_two, end_time_two)
        result_list = exec_es_sql(sql)
        all_day_result_list.extend(result_list)
    ip_count = dict()
    for item in all_day_result_list:
        if item['term_ip'] not in ip_count:
            ip_count[item['term_ip']] = item['count_']
        else:
            ip_count[item['term_ip']] += item['count_']
    ip_list = sorted(ip_count.items(), key=lambda ip_count: ip_count[1], reverse=True)
    labels = []
    term_count = {'name': "IP", 'data': []}
    for item in ip_list[0:10]:
        labels.append(item[0])
        term_count['data'].append(item[1])
    result = {
        "labels": labels,
        "data": [term_count] if len(labels) > 0 else []
    }
    return result


def terminal_offwork_print_list(days):
    '''
    下班打印详情
    '''
    all_day_result_list = []
    for day in days:
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
        sql = 'SELECT term_ip,term_duty,act_time,term_group_name as nums FROM {0} ' \
              'where log_type=5 and request_type=1 and ((act_time > {1} and act_time < {2}) or (act_time > {3} and act_time < {4}))'.format(
            ", ".join(indexs), start_time_one, end_time_one, start_time_two, end_time_two)
        result_list = exec_es_sql(sql)
        all_day_result_list.extend(result_list)
    row = []
    for i, item in enumerate(all_day_result_list):
        act_time = datetime.strptime(item['act_time'], "%Y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
        row.append([i + 1, item['term_ip'], item['term_duty'], item['term_group_name'], act_time])
    result = {
        "labels": [u"序号", u"终端IP", u"终端负责人", u"所属单位", u"打印时间"],
        "data": row
    }
    return result


'''
def terminal_usb_count(days):
    ''
    移动盘违规使用统计
    ''
    index = ['ssa-ag-all-terminal-{}-*'.format(day) for day in days]
    sql = 'SELECT term_ip,act_type,count(*) count_ FROM {} ' \
          'where log_type=5 and request_type=2 and act_type in (8,10) ' \
          'group by term_ip,act_type order by count_ desc limit 10'.format(','.join(index))
    count_list = exec_es_sql(sql=sql)
    act_type_name = [u"强制使用", u"拒绝", u"同意", u"禁用", u"插入", u"拔出"]
    act_type_value = ['3', '8', '9', '10', '11', '12']
    ips = []
    for item in count_list:
        if item['term_ip'] not in ips:
            ips.append(item['term_ip'])
    row = []

    for i, act_type in enumerate(act_type_value):
        act_type_count_list = []
        for ip in ips:
            act_type_count = 0
            for item in count_list:
                if ip == item['term_ip'] and act_type == str(item['act_type']):
                    act_type_count = item['count_']
                    continue
            act_type_count_list.append(act_type_count)
        row.append({
            'name': act_type_name[i],
            'data': act_type_count_list
        })
    result = {
        "labels": ips,
        "data": row
    }
    return result


def terminal_usb_list(days, term_id):
    ''
    移动盘违规使用详情
    ''
    index = ['ssa-ag-all-terminal-{}-*'.format(day) for day in days]
    sql = 'SELECT term_ip,term_duty,term_group_name,act_time,act_type FROM {} ' \
          'where log_type=5 and request_type=2 and act_type in (8,10) ' \
          'and term_group_id=\'{}\' order by act_time desc'.format(','.join(index), term_id)
    count_list = exec_es_sql(sql=sql)
    act_type_name = [u"强制使用", u"拒绝", u"同意", u"禁用", u"插入", u"拔出"]
    act_type_value = ['3', '8', '9', '10', '11', '12']
    ips = []
    for item in count_list:
        if item['term_ip'] not in ips:
            ips.append(item['term_ip'])
    row = []
    for i, item in enumerate(count_list):
        act_time = datetime.strptime(item['act_time'], "%Y%m%d%H%M%S").strftime(
            "%Y-%m-%d %H:%M:%S")
        term_name = "其他部门"
        term_list = TermGroup.objects.filter(term_group_id=term_id).values('term_group_name')
        if term_list:
            term_name = term_list.first()['term_group_name']
        act_type = act_type_name[act_type_value.index(str(item['act_type']))]
        row.append([i + 1, item['term_ip'], item['term_duty'], term_name, act_time, act_type])
    result = {
        "labels": [u"序号", u"IP", u"终端负责人", u"用户组名称", u"使用时间", u"使用类型"],
        "data": row
    }
    return result
'''


def terminal_usb_count(days):
    '''
    移动盘违规使用统计
    '''
    index = ['ssa-event-terminal-{}-*'.format(day) for day in days]
    sql = 'SELECT terminal,count(*) count_ FROM {} ' \
          'where event_type = \'违规插入移动盘\' ' \
          'group by terminal order by count_ desc limit 10'.format(','.join(index))
    count_list = exec_es_sql(sql=sql)
    labels = []
    for item in count_list:
        if item['terminal'] not in labels:
            labels.append(item['terminal'])
    term_count = {'name': "次数", 'data': []}
    for lab in labels:
        count_ = 0
        for item in count_list:
            if item['terminal'] == lab:
                count_ = item['count_']
        term_count['data'].append(count_)
    result = {
        "labels": labels,
        "data": [term_count] if len(labels) > 0 else []
    }
    return result


def terminal_usb_list(days, term_id):
    '''
    移动盘违规使用详情
    '''
    index = ['ssa-event-terminal-{}-*'.format(day) for day in days]
    sql = 'SELECT terminal,organization,term_duty FROM {} ' \
          'where event_type = \'违规插入移动盘\' and term_group_id=\'{}\' ' \
          'order by event_time desc'.format(','.join(index), term_id)
    count_list = exec_es_sql(sql=sql)

    row = []
    for i, item in enumerate(count_list):
        term_name = "其他部门"
        term_list = TermGroup.objects.filter(term_group_id=term_id).values('term_group_name')
        if term_list:
            term_name = term_list.first()['term_group_name']
        row.append([i + 1, item['terminal'], item['term_duty'], term_name, u'违规插入移动盘'])
    result = {
        "labels": [u"序号", u'IP', u'终端负责人', u'用户组名称', u'操作'],
        "data": row
    }
    return result


def terminal_txt_count(days):
    '''
    明文存储统计
    '''
    index = ['ssa-event-terminal-{}-*'.format(day) for day in days]
    sql = 'SELECT terminal,count(*) count_ FROM {} ' \
          'where event_type = \'明文存储\' ' \
          'group by terminal order by count_ desc limit 10'.format(','.join(index))
    count_list = exec_es_sql(sql=sql)
    labels = []
    for item in count_list:
        if item['terminal'] not in labels:
            labels.append(item['terminal'])
    term_count = {'name': "次数", 'data': []}
    for lab in labels:
        count_ = 0
        for item in count_list:
            if item['terminal'] == lab:
                count_ = item['count_']
        term_count['data'].append(count_)
    result = {
        "labels": labels,
        "data": [term_count] if len(labels) > 0 else []
    }
    return result


def terminal_txt_list(days, term_id):
    '''
    明文存储详情
    '''
    index = ['ssa-event-terminal-{}-*'.format(day) for day in days]
    sql = 'SELECT terminal,remark,organization,term_duty FROM {} ' \
          'where event_type = \'明文存储\' and term_group_id=\'{}\' ' \
          'order by event_time desc'.format(','.join(index), term_id)
    count_list = exec_es_sql(sql=sql)

    row = []
    for i, item in enumerate(count_list):
        remark = item['remark']
        if is_json(remark):
            remark = json.loads(remark)
            if isinstance(remark, dict):
                term_name = "其他部门"
                term_list = TermGroup.objects.filter(term_group_id=term_id).values('term_group_name')
                if term_list:
                    term_name = term_list.first()['term_group_name']
                row.append([i + 1, item['terminal'], item['term_duty'],
                            term_name, remark['word'], remark['sm_content']])
    result = {
        "labels": [u"序号", u'IP', u'终端负责人', u'用户组名称', u'明文', u'文件目录'],
        "data": row
    }
    return result


def terminal_battery_count(days):
    '''
    手机充电统计
    '''
    index = ['ssa-event-terminal-{}-*'.format(day) for day in days]
    sql = 'SELECT terminal,count(*) count_ FROM {} ' \
          'where event_type = \'手机充电\' ' \
          'group by terminal order by count_ desc limit 10'.format(','.join(index))
    count_list = exec_es_sql(sql=sql)
    labels = []
    for item in count_list:
        if item['terminal'] not in labels:
            labels.append(item['terminal'])
    term_count = {'name': "次数", 'data': []}
    for lab in labels:
        count_ = 0
        for item in count_list:
            if item['terminal'] == lab:
                count_ = item['count_']
        term_count['data'].append(count_)
    result = {
        "labels": labels,
        "data": [term_count] if len(labels) > 0 else []
    }
    return result


def terminal_battery_list(days, term_id):
    '''
    手机充电详情
    '''
    index = ['ssa-event-terminal-{}-*'.format(day) for day in days]
    sql = 'SELECT terminal,organization,term_duty FROM {} ' \
          'where event_type = \'手机充电\' and term_group_id=\'{}\' ' \
          'order by event_time desc'.format(','.join(index), term_id)
    count_list = exec_es_sql(sql=sql)

    row = []
    for i, item in enumerate(count_list):
        term_name = "其他部门"
        term_list = TermGroup.objects.filter(term_group_id=term_id).values('term_group_name')
        if term_list:
            term_name = term_list.first()['term_group_name']
        row.append([i + 1, item['terminal'], item['term_duty'], term_name, u'手机充电'])
    result = {
        "labels": [u"序号", u'IP', u'终端负责人', u'用户组名称', u'操作'],
        "data": row
    }
    return result


def terminal_uninstall_count(days):
    '''
    卸载统计
    '''
    index = ['ssa-event-terminal-{}-*'.format(day) for day in days]
    sql = 'SELECT terminal,count(*) count_ FROM {} ' \
          'where event_type = \'TMS卸载\' ' \
          'group by terminal order by count_ desc limit 10'.format(','.join(index))
    count_list = exec_es_sql(sql=sql)
    labels = []
    for item in count_list:
        if item['terminal'] not in labels:
            labels.append(item['terminal'])
    term_count = {'name': "次数", 'data': []}
    for lab in labels:
        count_ = 0
        for item in count_list:
            if item['terminal'] == lab:
                count_ = item['count_']
        term_count['data'].append(count_)
    result = {
        "labels": labels,
        "data": [term_count] if len(labels) > 0 else []
    }
    return result


def terminal_uninstall_list(days, term_id):
    '''
    卸载详情
    '''
    index = ['ssa-event-terminal-{}-*'.format(day) for day in days]
    sql = 'SELECT terminal,organization,term_duty FROM {} ' \
          'where event_type = \'TMS卸载\' and term_group_id=\'{}\' ' \
          'order by event_time desc'.format(','.join(index), term_id)
    count_list = exec_es_sql(sql=sql)

    row = []
    for i, item in enumerate(count_list):
        term_name = "其他部门"
        term_list = TermGroup.objects.filter(term_group_id=term_id).values('term_group_name')
        if term_list:
            term_name = term_list.first()['term_group_name']
        row.append([i + 1, item['terminal'], item['term_duty'], term_name, u'TMS卸载'])
    result = {
        "labels": [u"序号", u'IP', u'终端负责人', u'用户组名称', u'操作'],
        "data": row
    }
    return result


def detabase_terminal_opt_count(days):
    '''
    数据库违规终端操作统计
    '''
    index = ['all-event-{}-*'.format(day) for day in days]
    sql = 'SELECT src_ip,sum(event_total) sum_ FROM {} ' \
          'where event_source=3 and event_level>0 ' \
          'group by src_ip order by sum_ desc limit 10'.format(','.join(index))
    count_list = exec_es_sql(sql=sql)
    labels = []
    for item in count_list:
        if item['src_ip'] not in labels:
            labels.append(item['src_ip'])

    opt_count = {'name': u"事件总数", 'data': []}
    for lab in labels:
        count_ = 0
        for item in count_list:
            if item['src_ip'] == lab:
                count_ = item['sum_']
                continue
        opt_count['data'].append(count_)
    result = {
        "labels": labels,
        "data": [opt_count] if len(labels) > 0 else []
    }
    return result


def detabase_type_opt_count(days):
    '''
    数据库操作违规类型统计
    '''
    index = ['all-event-{}-*'.format(day) for day in days]
    sql = 'SELECT event_two_type,count(*) count_ FROM {} ' \
          'where event_source=3 and event_level>0 ' \
          'group by event_two_type order by count_ desc'.format(','.join(index))
    count_list = exec_es_sql(sql=sql)
    row = []
    for item in count_list:
        row.append({
            'name': item['event_two_type'],
            'data': [item['count_']]
        })
    result = {
        "labels": [u"违规类型"],
        "data": row
    }
    return result


def firewall_flow_count(days):
    '''
    防火墙流量趋势
    '''
    index = ['all-event-{}-*'.format(day) for day in days]
    sql = 'SELECT sum(flow) sum_ FROM {} where event_source=1 and event_level>0 ' \
          'group by date_histogram(field=\'@timestamp\', \'interval\'=\'day\', \'format\'=\'yyyy-MM-dd\')' \
          ''.format(','.join(index))
    count_list = exec_es_sql(sql=sql)
    labels = []
    for item in count_list:
        day = item['date_histogram(field=@timestamp,interval=day,format=yyyy-MM-dd)']
        if day not in labels:
            labels.append(day)
    flow_count = {
        'name': u'流量',
        'data': []
    }
    for lab in labels:
        sum_ = 0
        for item in count_list:
            day = item['date_histogram(field=@timestamp,interval=day,format=yyyy-MM-dd)']
            if lab == day:
                sum_ = item['sum_']
                continue
        flow_count['data'].append(sum_)

    result = {
        "labels": labels,
        "data": [flow_count] if len(labels) > 0 else []
    }
    return result


def firewall_prot_flow_count(days):
    '''
    防火墙协议流量统计
    '''
    index = ['ssa-ag-fw-{}-*'.format(day) for day in days]
    sql = 'select protocol,sum(flow) sum_ from {} ' \
          'group by protocol order by sum_ desc'.format(','.join(index))
    count_list = exec_es_sql(sql=sql)
    labels = []
    for item in count_list:
        if item['protocol'] not in labels:
            labels.append(item['protocol'])
    flow_count = {
        'name': u'流量',
        'data': []
    }
    for lab in labels:
        sum_ = 0
        for item in count_list:
            if lab == item['protocol']:
                sum_ = item['sum_']
                continue
        flow_count['data'].append(sum_)

    result = {
        "labels": labels,
        "data": [flow_count] if len(labels) > 0 else []
    }
    return result


def firewall_src_ip_count(days):
    '''
    防火墙源IP流量排行TOP10
    '''
    index = ['ssa-ag-fw-{}-*'.format(day) for day in days]
    sql = 'select src_ip,sum(flow) sum_ from {} ' \
          'group by src_ip order by sum_ desc limit 10'.format(','.join(index))
    count_list = exec_es_sql(sql=sql)
    labels = []
    for item in count_list:
        if item['src_ip'] not in labels:
            labels.append(item['src_ip'])
    flow_count = {
        'name': u'流量',
        'data': []
    }
    for lab in labels:
        sum_ = 0
        for item in count_list:
            if lab == item['src_ip']:
                sum_ = item['sum_']
                continue
        flow_count['data'].append(sum_)

    result = {
        "labels": labels,
        "data": [flow_count] if len(labels) > 0 else []
    }
    return result


def firewall_dst_ip_count(days):
    '''
    防火墙目标IP流量排行TOP10
    '''
    index = ['ssa-ag-fw-{}-*'.format(day) for day in days]
    sql = 'select dst_ip,sum(flow) sum_ from {} ' \
          'group by dst_ip order by sum_ desc limit 10'.format(','.join(index))
    count_list = exec_es_sql(sql=sql)
    labels = []
    for item in count_list:
        if item['dst_ip'] not in labels:
            labels.append(item['dst_ip'])
    flow_count = {
        'name': u'流量',
        'data': []
    }
    for lab in labels:
        sum_ = 0
        for item in count_list:
            if lab == item['dst_ip']:
                sum_ = item['sum_']
                continue
        flow_count['data'].append(sum_)

    result = {
        "labels": labels,
        "data": [flow_count] if len(labels) > 0 else []
    }
    return result


def firewall_type_count(days):
    '''
    防火墙事件类型统计
    '''
    index = ['all-event-{}-*'.format(day) for day in days]
    sql = 'SELECT event_three_type,count(*) count_ FROM {} ' \
          'where event_source=1 and event_level>0 ' \
          'group by event_three_type'.format(','.join(index))
    count_list = exec_es_sql(sql=sql)
    labels = []
    for item in count_list:
        if item['event_three_type'] not in labels:
            labels.append(item['event_three_type'])
    type_count = {
        'name': u'数量',
        'data': []
    }
    for lab in labels:
        sum_ = 0
        for item in count_list:
            if lab == item['event_three_type']:
                sum_ = item['count_']
                continue
        type_count['data'].append(sum_)

    result = {
        "labels": labels,
        "data": [type_count] if len(labels) > 0 else []
    }
    return result


def gl_flow_count(days):
    '''
    隔离设备接收发送流量趋势
    '''
    index = ['ssa-ag-gl-{}-*'.format(day) for day in days]
    sql = 'select sum(recv_flow_statis) sum_recv,sum(send_flow_statis) sum_send from {} ' \
          'group by date_histogram(field=\'@timestamp\', \'interval\'=\'day\', \'format\'=\'yyyy-MM-dd\')' \
          ''.format(','.join(index))
    count_list = exec_es_sql(sql=sql)
    labels = []
    for item in count_list:
        day = item['date_histogram(field=@timestamp,interval=day,format=yyyy-MM-dd)']
        if day not in labels:
            labels.append(day)
    row = [{"name": u"接收流量", "data": []}, {"name": u"发送流量", "data": []}]
    for lab in labels:
        sum_recv, sum_send = 0, 0
        for item in count_list:
            day = item['date_histogram(field=@timestamp,interval=day,format=yyyy-MM-dd)']
            if lab == day:
                sum_recv = item['sum_recv']
                sum_send = item['sum_send']
                continue
        row[0]['data'].append(sum_recv)
        row[1]['data'].append(sum_send)
    result = {
        "labels": labels,
        "data": row
    }
    return result


def gl_src_ip_flow_count(days):
    '''
    隔离设备源IP发送流量统计TOP10
    '''
    index = ['ssa-ag-gl-{}-*'.format(day) for day in days]
    sql = 'select src_ip,sum(send_flow_statis) sum_ from {} ' \
          'group by src_ip order by sum_ desc limit 10'.format(','.join(index))
    count_list = exec_es_sql(sql=sql)
    labels = []
    for item in count_list:
        if item['src_ip'] not in labels:
            labels.append(item['src_ip'])
    flow_count = {
        "name": u"流量",
        "data": []
    }
    for lab in labels:
        count_ = 0
        for item in count_list:
            if lab == item['src_ip']:
                count_ = item['sum_']
                continue
        flow_count['data'].append(count_)
    result = {
        "labels": labels,
        "data": [flow_count] if len(labels) > 0 else []
    }
    return result


def gl_dst_ip_flow_count(days):
    '''
    隔离设备目标IP接收流量统计TOP10
    '''
    index = ['ssa-ag-gl-{}-*'.format(day) for day in days]
    sql = 'select dst_ip,sum(recv_flow_statis) sum_ from {} ' \
          'group by dst_ip order by sum_ desc limit 10'.format(','.join(index))
    count_list = exec_es_sql(sql=sql)
    labels = []
    for item in count_list:
        if item['dst_ip'] not in labels:
            labels.append(item['dst_ip'])
    flow_count = {
        "name": u"流量",
        "data": []
    }
    for lab in labels:
        count_ = 0
        for item in count_list:
            if lab == item['dst_ip']:
                count_ = item['sum_']
                continue
        flow_count['data'].append(count_)
    result = {
        "labels": labels,
        "data": [flow_count] if len(labels) > 0 else []
    }
    return result


def gl_type_count(days):
    '''
    隔离事件类型统计
    '''
    index = ['all-event-{}-*'.format(day) for day in days]
    sql = 'SELECT event_three_type,count(*) count_ FROM {} ' \
          'where event_source=5 and event_level>0 ' \
          'group by event_three_type'.format(','.join(index))
    count_list = exec_es_sql(sql=sql)
    labels = []
    for item in count_list:
        if item['event_three_type'] not in labels:
            labels.append(item['event_three_type'])
    type_count = {
        'name': u'数量',
        'data': []
    }
    for lab in labels:
        sum_ = 0
        for item in count_list:
            if lab == item['event_three_type']:
                sum_ = item['count_']
                continue
        type_count['data'].append(sum_)

    result = {
        "labels": labels,
        "data": [type_count] if len(labels) > 0 else []
    }
    return result


def ids_attack_count(days):
    '''
    IDS监测攻击趋势
    '''
    index = ['ssa-ag-ids-{}-*'.format(day) for day in days]
    sql = 'SELECT sum(event_count) sum_ FROM {} ' \
          'group by date_histogram(field=\'@timestamp\', \'interval\'=\'day\', \'format\'=\'yyyy-MM-dd\')' \
          ''.format(','.join(index))
    count_list = exec_es_sql(sql=sql)
    labels = []
    for item in count_list:
        day = item['date_histogram(field=@timestamp,interval=day,format=yyyy-MM-dd)']
        if day not in labels:
            labels.append(day)
    flow_count = {
        'name': u'攻击次数',
        'data': []
    }
    for lab in labels:
        sum_ = 0
        for item in count_list:
            day = item['date_histogram(field=@timestamp,interval=day,format=yyyy-MM-dd)']
            if lab == day:
                sum_ = item['sum_']
                continue
        flow_count['data'].append(sum_)

    result = {
        "labels": labels,
        "data": [flow_count] if len(labels) > 0 else []
    }
    return result


def ids_event_count(days):
    '''
    IDS监测事件名称占比
    '''
    index = ['ssa-ag-ids-{}-*'.format(day) for day in days]
    sql = 'SELECT event_name,count(*) count_ FROM {} ' \
          'group by event_name'.format(','.join(index))
    count_list = exec_es_sql(sql=sql)
    labels = []
    for item in count_list:
        if item['event_name'] not in labels:
            labels.append(item['event_name'])
    flow_count = {
        'name': u'事件名称',
        'data': []
    }
    for lab in labels:
        count_ = 0
        for item in count_list:
            if lab == item['event_name']:
                count_ = item['count_']
                continue
        flow_count['data'].append(count_)

    result = {
        "labels": labels,
        "data": [flow_count] if len(labels) > 0 else []
    }
    return result


def ids_attack_src_count(days):
    '''
    IDS监测攻击源攻击次数统计TOP10
    '''
    index = ['ssa-ag-ids-{}-*'.format(day) for day in days]
    sql = 'SELECT source,sum(event_count) sum_ FROM {} ' \
          'group by source order by sum_ desc limit 10'.format(','.join(index))
    count_list = exec_es_sql(sql=sql)
    labels = []
    for item in count_list:
        if item['source'] not in labels:
            labels.append(item['source'])
    flow_count = {
        'name': u'攻击次数',
        'data': []
    }
    for lab in labels:
        sum_ = 0
        for item in count_list:
            if lab == item['source']:
                sum_ = item['sum_']
                continue
        flow_count['data'].append(sum_)

    result = {
        "labels": labels,
        "data": [flow_count] if len(labels) > 0 else []
    }
    return result


def ids_attack_dst_count(days):
    '''
    IDS监测终端被攻击次数统计TOP10
    '''
    index = ['ssa-ag-ids-{}-*'.format(day) for day in days]
    sql = 'SELECT src_ip,sum(event_count) sum_ FROM {} ' \
          'group by src_ip order by sum_ desc limit 10'.format(','.join(index))
    count_list = exec_es_sql(sql=sql)
    labels = []
    for item in count_list:
        if item['src_ip'] not in labels:
            labels.append(item['src_ip'])
    flow_count = {
        'name': u'被攻击次数',
        'data': []
    }
    for lab in labels:
        sum_ = 0
        for item in count_list:
            if lab == item['src_ip']:
                sum_ = item['sum_']
                continue
        flow_count['data'].append(sum_)

    result = {
        "labels": labels,
        "data": [flow_count] if len(labels) > 0 else []
    }
    return result


def is_json(json_str):
    try:
        a = json.loads(json_str)
        return True
    except Exception as e:
        return False
