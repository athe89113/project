# -*- coding:utf-8 -*-

from datetime import datetime, timedelta
from soc_assets.models import TermGroup, Assets
from utils.es_select import exec_es_sql


def security_count(days):
    '''
    违规总量占比
    '''
    index = ['event-terminal-{}-*'.format(day) for day in days]
    sql = 'SELECT organization,sum(event_total) count_ FROM  {} ' \
          'group by organization order by count_ desc'.format(','.join(index))

    count_list = exec_es_sql(sql=sql)
    labels, data = [], []
    for item in count_list:
        labels.append(item['organization'])
        data.append(item['count_'])
    result = {
        "labels": labels,
        "data": [{"name": u"单位违规总量占比", "data": data}]
    }
    return result


def security_type_count(days):
    '''
    各单位违规总量型统计
    '''
    index = ['event-terminal-{}-*'.format(day) for day in days]
    sql = 'SELECT organization,event_type,sum(event_total) count_ FROM {} ' \
          'group by organization,event_type order by count_ desc'.format(','.join(index))
    count_list = exec_es_sql(sql=sql)
    labels, event_types, data = [], [], []
    for item in count_list:
        if item['organization'] not in labels:
            labels.append(item['organization'])
        if item['event_type'] not in event_types:
            event_types.append(item['event_type'])

    for et in event_types:
        row_data = [0 for i in range(len(labels))]
        for lab in labels:
            for item in count_list:
                if et == item['event_type'] and lab == item['organization']:
                    row_data[labels.index(lab)] = item['count_']
                    continue
        data.append({"name": et, "data": row_data})

    result = {
        "labels": labels,
        "data": data
    }
    return result


def security_terminal_count(days):
    '''
    违规类型详情统计
    '''
    index = ['event-terminal-{}-*'.format(day) for day in days]
    sql = 'SELECT organization,event_type,terminal,count(*) count_ FROM {} ' \
          'group by organization,event_type,terminal order by count_ desc'.format(','.join(index))

    count_list = exec_es_sql(sql=sql)

    data = dict()
    index = 0
    for item in count_list:
        index += 1
        if item['organization'] not in data:
            data[item['organization']] = dict()
        if item['event_type'] in data[item['organization']]:
            data[item['organization']][item['event_type']] += 1
        else:
            data[item['organization']][item['event_type']] = 1
    row = []
    for org in data:
        count_ = 0
        for et in data[org]:
            count_ += data[org][et]
        for et in data[org]:
            row.append([org, count_, et, data[org][et]])

    result = {
        "labels": [u"部门名称", u"违规终端总数", u"违规类型", u"违规终端数"],
        "data": row
    }
    return result


def get_term_list():
    '''
    获取所有部门
    '''
    return TermGroup.objects.all()


def get_assets_by_ip(ip, org):
    '''
    获取ip资产信息
    '''
    assets_set = Assets.objects.filter(ip=ip)
    if org:
        term_set = TermGroup.objects.filter(term_group_name=org)
        if term_set:
            group_id = term_set.first().term_group_id
            assets_set = assets_set.filter(term_group_id=group_id)
    if assets_set:
        return assets_set.first()
    else:
        return dict()


def org_security_terminal_count(days, org):
    '''
    某单位终端违规情况统计
    '''
    index = ['event-terminal-{}-*'.format(day) for day in days]
    sql = 'SELECT terminal,event_type,count(*) count_ FROM {} ' \
          'where organization=\'{}\' ' \
          'group by terminal,event_type order by count_ desc'.format(','.join(index), org)

    count_list = exec_es_sql(sql=sql)

    labels, event_types, data = [], [], []
    for item in count_list:
        if item['terminal'] not in labels:
            labels.append(item['terminal'])
        if item['event_type'] not in event_types:
            event_types.append(item['event_type'])
    labels = labels[0:10]
    for et in event_types:
        row_data = [0 for i in range(len(labels))]
        for lab in labels:
            for item in count_list:
                if et == item['event_type'] and lab == item['terminal']:
                    row_data[labels.index(lab)] = item['count_']
                    continue
        data.append({"name": et, "data": row_data})

    result = {
        "labels": labels,
        "data": data
    }
    return result


def org_security_terminal_detail_count(days, org):
    '''
    某单位终端违规情况统计
    '''
    index = ['event-terminal-{}-*'.format(day) for day in days]
    sql = 'SELECT terminal,event_type,count(*) count_ FROM {} ' \
          'where organization=\'{}\' ' \
          'group by terminal,event_type order by count_ desc'.format(','.join(index), org)

    count_list = exec_es_sql(sql=sql)

    data = dict()
    index = 0
    for item in count_list:
        index += 1
        if item['terminal'] not in data:
            data[item['terminal']] = dict()
        if item['event_type'] in data[item['terminal']]:
            data[item['terminal']][item['event_type']] += 1
        else:
            data[item['terminal']][item['event_type']] = 1

    row = []
    ips = []
    for ip in data:
        ips.append(ip)
        term = get_assets_by_ip(ip=ip, org=org)
        duty = ''  # 负责人
        if term:
            duty = term.term_duty
        count_ = 0
        for et in data[ip]:
            count_ += data[ip][et]
        for et in data[ip]:
            row.append([ip, duty, count_, et, data[ip][et]])

    result = {
        "labels": [u"终端ip", u"负责人姓名", u"违规终端总数", u"违规类型", u"违规终端数"],
        "data": row,
        "ips": ips
    }
    return result


def terminal_info_os(days):
    '''
    终端操作系统名称
    '''
    yesterday = datetime.strftime(datetime.now() - timedelta(days=1), "%Y-%m-%d")
    sql = 'SELECT os_info,term_ip FROM ssa-ag-zt-basic-{0}-* group by os_info,term_ip'.format(days[-1])
    result = exec_es_sql(sql=sql)
    return result


def terminal_info_share(days):
    '''
    终端共享
    '''
    # yesterday = datetime.strftime(datetime.now() - timedelta(days=1), "%Y-%m-%d")
    sql = 'SELECT term_ip,count(*) FROM ssa-ag-zt-share-{0}-* group by term_ip '.format(days[-1])
    result = exec_es_sql(sql=sql)
    return result


def terminal_info_guest_user(days):
    '''
    是否禁用guest
    '''
    # yesterday = datetime.strftime(datetime.now() - timedelta(days=1), "%Y-%m-%d")
    sql = 'SELECT term_ip,count(*) FROM ssa-ag-zt-user-{0}-* ' \
          'where (user_name like \'%{1}%\' or  user_name like \'%{2}%\') ' \
          'group by term_ip'.format(days[-1], 'Guest', 'guest')
    result = exec_es_sql(sql=sql)
    return result


def terminal_info_security_app(days):
    '''
    是否安装终端安全管理系统
    '''
    # yesterday = datetime.strftime(datetime.now() - timedelta(days=1), "%Y-%m-%d")
    sql = 'SELECT term_ip,count(*) FROM ssa-ag-zt-soft-{0}-* ' \
          'where software_name like \'%{1}%\' group by term_ip'.format(days[-1], 'TmsAgent')
    result = exec_es_sql(sql=sql)
    return result


def terminal_info_security_shield(days):
    '''
    是否安装网盾桌面安全套件
    '''
    # yesterday = datetime.strftime(datetime.now() - timedelta(days=1), "%Y-%m-%d")
    sql = 'SELECT term_ip,count(*) FROM ssa-ag-zt-soft-{0}-* ' \
          'where  software_name like \'%{1}%\' group by term_ip'.format(days[-1], '网盾')
    result = exec_es_sql(sql=sql)
    return result


def terminal_info_security_loophole(days):
    '''
    是否安装杀毒软件
    '''
    # yesterday = datetime.strftime(datetime.now() - timedelta(days=1), "%Y-%m-%d")
    sql = 'SELECT term_ip,count(*) FROM ssa-ag-zt-soft-{0}-* ' \
          'where (software_name like \'%{1}%\' or  software_name like \'%{2}%\' ' \
          'or  software_name like \'%{3}%\') group by term_ip'.format(days[-1], '360', '天擎', '瑞星')
    result = exec_es_sql(sql=sql)
    return result


def terminal_info_plaintext(days):
    '''
    明文存储
    '''

    lastHour = datetime.strftime(datetime.now(), "%H")
    sql = 'select event_time,remark,terminal from ssa-event-terminal-{}-{} ' \
          'where event_type=\'明文存储\' '.format(days[-1], lastHour)
    result = exec_es_sql(sql=sql)
    return result


def terminal_info_usb(days):
    '''
    USB存储设备使用痕迹
    '''
    # noday = datetime.strftime(datetime.now(), "%Y-%m-%d")
    sql = 'select act_time,dev_name,term_ip from ssa-ag-all-terminal-{0}-* ' \
          'where act_type=10'.format(days[-1])
    result = exec_es_sql(sql=sql)
    return result


def terminal_info_phone(days):
    '''
    手机充电情况
    '''
    # noday = datetime.strftime(datetime.now(), "%Y-%m-%d")
    sql = 'select act_time,dev_name,term_ip from ssa-ag-all-terminal-{0}-* ' \
          'where act_type=9'.format(days[-1])
    result = exec_es_sql(sql=sql)
    return result


def terminal_info_uninstall(days):
    '''
    终端安全管理系统卸载记录
    '''
    # noday = datetime.strftime(datetime.now(), "%Y-%m-%d")
    sql = 'select act_time,term_ip from ssa-ag-all-terminal-{0}-* ' \
          'where login_type=7'.format(days[-1])
    result = exec_es_sql(sql=sql)
    return result


def get_terminal_os(data, ip):
    '''
    查找终端操作系统
    '''
    os_info = ''
    for item in data:
        if item['term_ip'] == ip:
            os_info = item['os_info']
            break
    return os_info


def get_terminal_info(data, key, ip):
    '''
    判断是否存在数据
    '''
    count = 0
    for item in data:
        if item[key] == ip:
            count += 1
            break
    return '是' if count > 0 else '否'


def get_terminal_plaintext_data(data, ip):
    '''
    获取终端数据-明文存储
    '''
    result = []
    for item in data:
        if item['terminal'] == ip:
            result.append([u'明文存储情况', item['remark'], item['event_time']])
    return result


def get_terminal_usb_data(data, ip):
    '''
    获取终端数据-USB存储设备使用痕迹
    '''
    result = []
    for item in data:
        if item['term_ip'] == ip:
            result.append([u'USB存储设备使用痕迹', u'违规插入移动盘{0}'.format(item['dev_name']), item['act_time']])
    return result


def get_terminal_phone_data(data, ip):
    '''
    获取终端数据-手机充电情况
    '''
    result = []
    for item in data:
        if item['term_ip'] == ip:
            result.append([u'手机充电情况', u'违规插入手机{0}'.format(item['dev_name']), item['act_time']])
    return result


def get_terminal_uninstall_data(data, ip):
    '''
    获取终端数据-系统卸载记录
    '''
    result = []
    for item in data:
        if item['term_ip'] == ip:
            result.append([u'终端安全管理系统卸载记录', u'卸载软件', item['act_time']])
    return result
