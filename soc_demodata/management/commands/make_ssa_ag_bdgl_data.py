# -*- coding:utf-8 -*-
import json
import logging
import random
import time
import datetime
import uuid
from faker import Factory, Faker

from django.utils import timezone
from django.core.management.base import BaseCommand

from common import add_doc_list

logger = logging.getLogger('console')

level_list = [10, 20, 30, 40]
securityid_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 17, 18, 19, 20, 24, 25, 26]
attack_list = [1001, 1002, 1003, 1004, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013,
               3001, 3002, 3003, 3004, 3005, 4001, 4002, 4003, 5001, 5002, 5003, 5004, 5005, 5006, 6001, 6002, 6003,
               7001, 7002, 7003, 7004, 7005, 7006, 7007, 8001, 8002, 8003, 8004, 9000]
event_ids = ['0x71010000', '0x71020000', '0x71030000', '0x72010000', '0x72020000']
dst_ips = ['250.52.233.8', '230.188.33.94', '87.6.55.243', '161.52.23.152', '95.16.80.30', '46.178.15.155',
           '171.150.92.188', '107.58.102.71', '171.230.5.6', '136.164.56.196', '177.162.18.235', '202.251.94.55',
           '147.5.45.0', '224.13.212.84', '145.165.15.54', '68.198.99.56', '75.39.207.95', '111.220.214.239',
           '52.203.149.50', '26.161.244.24', '42.217.34.8', '240.159.155.188', '243.21.228.104', '231.248.12.252',
           '67.204.139.139', '35.112.134.192', '221.16.88.254', '102.51.108.64', '59.245.233.15', '224.236.224.197',
           '135.117.250.27', '28.17.9.231', '93.137.162.86', '224.177.220.254', '4.236.149.152', '21.51.121.198',
           '165.65.5.109', '198.232.126.0', '225.171.2.16', '215.66.188.241', '180.247.79.128', '188.131.254.189',
           '64.14.178.18', '143.3.29.62', '255.163.124.197', '148.38.252.91', '122.34.187.112', '247.12.177.79',
           '66.93.182.199', '135.74.16.40']
class Command(BaseCommand):
    def handle(self, *args, **options):
        obj = DemoData()
        obj.run()


class DemoData(object):
    def __init__(self):
        self.fake = Factory.create()
        self.ips = [self.fake.ipv4() for i in range(100)]

    def make_data(self, index_name):
        data_fun = getattr(self, "{}_data_func".format(index_name.replace('-', '_')))
        datas = []
        # 从10天后 开始往10天前生成数据 共计20天
        start_time = timezone.now() + timezone.timedelta(days=30)
        for i in range(60):
            random_time = timezone.timedelta(minutes=random.randint(1, 1440))
            date_time = timezone.localtime(
                start_time - timezone.timedelta(days=i + 1) - random_time)
            index = "{0}-{1}".format(index_name,
                                     date_time.strftime('%Y-%m-%d-%H'))
            for j in range(random.randint(100, 200)):
                starttime = datetime.datetime.strptime(str(date_time)[
                                                       :10] + ' 00:00:00', '%Y-%m-%d %H:%M:%S') + timezone.timedelta(
                    minutes=random.randint(1, 1440))
                data = data_fun(index, starttime)
                datas.append(data)
        add_doc_list(datas)

    def ssa_ag_bd_data_func(self, index_name, date_time):
        '''
        摆渡设备流量日志
        '''
        return {
            "_index": index_name,
            "_type": 'logs',
            "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "comp_ip": random.choice(self.ips),
            "task_id": str(uuid.uuid4()),
            "src_ip": random.choice(self.ips),
            "src_port": random.randint(3000, 6000),
            "dst_ip": random.choice(self.ips),
            "dst_port": random.randint(3000, 6000),
            "file_name": random.choice(
                ['20180111.doc', 'app.xml', '数据报告.doc', '人员名单.xlsx', '异常情况报告.doc', '季度报告.doc', '20180622.doc',
                 '数据信息.doc', '风险人员.doc']),
            "file_size": random.randint(1, 10000),
            "is_success": random.randint(0, 1),
            "starttime": date_time.strftime('%Y%m%d%H%M%S'),
            "endtime": date_time.strftime('%Y%m%d%H%M%S'),
            "note": ''
        }

    def ssa_ag_gl_data_func(self, index_name, date_time):
        '''
        隔离设备文件日志
        '''
        return {
            "_index": index_name,
            "_type": 'logs',
            "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "comp_ip": random.choice(self.ips),
            "task_id": str(uuid.uuid4()),
            "proto": random.choice([6, 17]),
            "src_ip": random.choice(self.ips),
            "src_port": random.randint(3000, 6000),
            "dst_ip": random.choice(self.ips),
            "dst_port": random.randint(3000, 6000),
            "send_flow_statis": random.randint(1, 10000),
            "recv_flow_statis": random.randint(1, 10000),
            "is_normal": random.randint(0, 1),
            "starttime": date_time.strftime('%Y%m%d%H%M%S'),
            "endtime": date_time.strftime('%Y%m%d%H%M%S'),
            "note": ''
        }

    def ssa_event_bdgl_data_func(self, index_name, date_time):
        """
        摆渡机隔离设备事件日志
        """
        f = Faker(locale='zh_CN')
        return {
            "_type": 'logs',
            "_index": index_name,
            "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "event_id": uuid.uuid4(),
            "type": random.randint(1, 2),
            "app": random.choice(['测试1', '测试2', '测试3']),
            "event_path": random.choice(self.ips),
            "app_name": random.choice(['测试1','测试2']),
            "level": random.randint(1, 3),
            "event_time": date_time.strftime('%Y%m%d%H%M%S'),
            "subject": random.choice(['主体1', '主体2', '主体3']),
            "content": random.choice(['内容1', '内容2', '内容3'])
        }

    def event_security_data_func(self, index_name, date_time):
        '''
        摆渡隔离事件统计数据
        '''
        return {
            "_index": index_name,
            "_type": 'logs',
            "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "src_ip": '',
            "dst_ip": "",
            "src_port": "",
            "dst_port": '',
            "protocol": '',
            "event_top_type": "攻击事件",
            "event_type": random.choice(['违反IPMAC绑定的连接请求', '违反访问规则的连接请求', '非法协议数据', '非法登录', 'DDOS攻击']),
            "event_source": random.choice(['隔离设备', '隔离设备']),
            "start_time": date_time.strftime('%Y%m%d%H%M%S'),
            "end_time": date_time.strftime('%Y%m%d%H%M%S'),
            "organization": "",
            "event_total": random.randint(0, 100),
            "terminal": random.choice(self.ips),
            "event_level": random.choice([1, 2, 3])
        }

    def statistics_security_bd_data_func(self, index_name, date_time):
        '''
        摆渡日志统计数据
        '''
        return {
            "_index": index_name,
            "_type": 'logs',
            "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "src_ip": random.choice(self.ips),
            "dst_ip": random.choice(self.ips),
            "src_port": random.randint(3000, 6000),
            "dst_port": random.randint(3000, 6000),
            "protocol": "",
            "log_top_type": "摆渡设备",
            "log_type": "摆渡设备",
            "log_total": random.randint(500, 1000),
            "start_time": date_time.strftime('%Y%m%d%H%M%S'),
            "end_time": date_time.strftime('%Y%m%d%H%M%S'),
            "organization": "",
            "terminal": random.choice(self.ips),
            "log_flow": "",
            "log_source": "摆渡设备"
        }

    def statistics_security_gl_data_func(self, index_name, date_time):
        '''
        隔离设备日志统计数据
        '''
        return {
            "_index": index_name,
            "_type": 'logs',
            "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "src_ip": random.choice(self.ips),
            "dst_ip": random.choice(self.ips),
            "src_port": random.randint(3000, 6000),
            "dst_port": random.randint(3000, 6000),
            "protocol": "",
            "log_top_type": "隔离设备",
            "log_type": "隔离设备",
            "log_total": random.randint(500, 1000),
            "start_time": date_time.strftime('%Y%m%d%H%M%S'),
            "end_time": date_time.strftime('%Y%m%d%H%M%S'),
            "organization": "",
            "terminal": random.choice(self.ips),
            "log_flow": "",
            "log_source": "隔离设备"
        }

    def all_event_data_func(self, index_name, date_time):
        '''
        所有事件
        '''
        event_data = {
            "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "event_source": random.choice(dst_ips),
            "event_id": random.choice(event_ids),
            "event_type": random.randint(1, 2),
            "app": random.choice(['测试1', '测试2', '测试3']),
            "event_path": random.choice(dst_ips),
            "app_name": random.choice(['系统1', '系统2', '系统3']),
            "level": random.randint(1, 3),
            "event_time": str(date_time.strftime('%Y%m%d%H%M%S')),
            "subject": random.choice(['主体1', '主体2', '主体3']),
            "content": random.choice(['内容1', '内容2', '内容3'])
        }
        return {
            "_index": index_name,
            "_type": 'logs',
            "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),

            "event_host": event_data['event_source'],
            "event_one_type": random.choice(['违规']),
            "event_two_type": random.choice(['阻断策略', '访问控制', '防攻击']),
            "event_three_type": random.choice(['违反IPMAC绑定的连接请求', '违反访问规则的连接请求', '非法协议数据', '非法登录', 'DDOS攻击']),
            "event_source": random.choice([4, 5]),
            "src_ip": event_data['event_path'],
            "dst_ip": '',
            "src_port": '',
            "dst_port": '',
            "tran_protocol": '',
            "app_protocol": '',
            "start_time": date_time.strftime('%Y%m%d%H%M%S'),
            "end_time": date_time.strftime('%Y%m%d%H%M%S'),
            "stastic_time": date_time.strftime('%Y%m%d%H%M%S'),
            "opt_result": 1,
            "flow": '',
            "event_level": random.choice([1, 2, 3]),
            "organization": '',  # 单位
            "event_total": random.randint(0, 5),
            "event_contents": event_data['content'],
            "event_detail": json.dumps(event_data),
        }

    def run(self):
        # IDS
        # self.make_data('ssa-ag-bd')
        # self.make_data('ssa-ag-gl')
        # self.make_data('ssa-event-bdgl')
        # self.make_data('event-security')
        # self.make_data('statistics-security-bd')
        # self.make_data('statistics-security-gl')

        self.make_data('all-event')
