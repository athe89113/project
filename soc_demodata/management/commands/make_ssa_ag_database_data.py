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


class Command(BaseCommand):
    def handle(self, *args, **options):
        obj = DemoData()
        obj.run()


class DemoData(object):
    def __init__(self):
        self.fake = Factory.create()
        self.ips = [self.fake.ipv4() for i in range(100)]
        self.macs = [self.fake.mac_address() for i in range(100)]

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

    def ssa_ag_database_data_func(self, index_name, date_time):
        '''
        数据库审计
        '''
        return {
            "_index": index_name,
            "_type": 'logs',
            "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),

            "event_time": date_time.strftime('%Y%m%d%H%M%S'),
            "id": str(uuid.uuid4()),
            "provider_id": "qimingxingchen",
            "transport_protocol": random.choice(['tcp', 'udp']),
            "app_protocol": random.choice(['ORACLE', 'MYSQL', "SQL SERVER"]),
            "level": random.choice(['urgent', 'High', "middle", "low"]),
            "dev_ip": random.choice(["171.234.220.213"]),
            "server_ip": random.choice(self.ips),
            "client_ip": random.choice(self.ips),
            "server_port": random.randint(3000, 6000),
            "redirect_port": random.randint(3000, 6000),
            "client_port": random.randint(3000, 6000),
            "server_mac": random.choice(self.macs),
            "client_mac": random.choice(self.macs),
            "ruleset_name": random.choice(["规则集{}".format(str(index)) for index in range(10)]),
            "rule_name": random.choice(["规则{}".format(str(index)) for index in range(10)]),
            "bizaccout": random.choice(["资源账号{}".format(str(index)) for index in range(10)]),
            "auth_account": random.choice(["认证账号{}".format(str(index)) for index in range(10)]),
            "policy_id": random.randint(1, 1000),
            "rule_id": random.randint(1, 1000),
            "rule_templet_id": random.randint(1, 1000),
            "direction": random.choice(["request", "response"]),
            "response_time": random.randint(1, 100000),
            "error_code": random.randint(1, 10),
            "block": random.choice(["yes", "no"]),
            "record_rows": random.randint(1, 100),
            "sql": random.choice(["select * from user", "delete from user", "update user set name='张三' where id =1"]),
            "client_host": random.choice(["源主机名称{}".format(str(index)) for index in range(10)]),
            "server_host": random.choice(["目的主机名称{}".format(str(index)) for index in range(10)]),
            "library": random.choice(["ODBC", "JDBC"]),
            "client_software": random.choice(["客户端软件{}".format(str(index)) for index in range(10)]),
            "client_user": random.choice(["客户端用户名{}".format(str(index)) for index in range(10)]),
            "instance_name": random.choice(["实例名{}".format(str(index)) for index in range(10)]),
            "db_name": random.choice(["数据库{}".format(str(index)) for index in range(10)]),
            "table_name": random.choice(["表名{}".format(str(index)) for index in range(10)]),
            "object_name": random.choice(["对象名{}".format(str(index)) for index in range(10)]),
            "cmd": random.choice(["命令{}".format(str(index)) for index in range(10)]),
            "subcmd": random.choice(["子命令{}".format(str(index)) for index in range(10)]),
        }

    def event_db_audit_data_func(self, index_name, date_time):
        '''
        数据库审计事件统计数据
        '''
        return {
            "_index": index_name,
            "_type": 'logs',
            "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "src_ip": random.choice(self.ips),
            "dst_ip": random.choice(self.ips),
            "src_port": random.randint(3000, 6000),
            "dst_port": random.randint(3000, 6000),
            "protocol": random.choice(['tcp', 'udp']),
            "event_top_type": "违规事件",
            "event_type": random.choice(["规则{}".format(str(index)) for index in range(10)]),
            "event_source": "数据库审计",
            "start_time": date_time.strftime('%Y%m%d%H%M%S'),
            "end_time": date_time.strftime('%Y%m%d%H%M%S'),
            "organization": "",
            "event_total": random.randint(0, 100),
            "terminal": random.choice(self.ips),
            "event_level": 2
        }

    def statistics_db_audit_data_func(self, index_name, date_time):
        '''
        数据库审计日志统计数据
        '''
        return {
            "_index": index_name,
            "_type": 'logs',
            "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "src_ip": random.choice(self.ips),
            "dst_ip": random.choice(self.ips),
            "src_port": random.randint(3000, 6000),
            "dst_port": random.randint(3000, 6000),
            "protocol": random.choice(['tcp', 'udp']),
            "log_top_type": "数据库审计",
            "log_type": random.choice(['ORACLE', 'MYSQL', "SQL SERVER"]),
            "log_total": random.randint(500, 1000),
            "start_time": date_time.strftime('%Y%m%d%H%M%S'),
            "end_time": date_time.strftime('%Y%m%d%H%M%S'),
            "organization": "",
            "terminal": random.choice(self.ips),
            "log_flow": "",
            "log_source": "数据库审计"
        }

    def all_event_data_func(self, index_name, date_time):
        '''
        所有事件
        '''
        event_data = {
            "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "event_time": date_time.strftime('%Y%m%d%H%M%S'),
            "id": str(uuid.uuid4()),
            "provider_id": "qimingxingchen",
            "transport_protocol": random.choice(['tcp', 'udp']),
            "app_protocol": random.choice(['ORACLE', 'MYSQL', "SQL SERVER"]),
            "level": random.choice(['urgent', 'High', "middle", "low"]),
            "dev_ip": random.choice(["171.234.220.213"]),
            "server_ip": random.choice(self.ips),
            "client_ip": random.choice(self.ips),
            "server_port": random.randint(3000, 6000),
            "redirect_port": random.randint(3000, 6000),
            "client_port": random.randint(3000, 6000),
            "server_mac": random.choice(self.macs),
            "client_mac": random.choice(self.macs),
            "ruleset_name": random.choice(["规则集{}".format(str(index)) for index in range(10)]),
            "rule_name": random.choice(["规则{}".format(str(index)) for index in range(10)]),
            "bizaccout": random.choice(["资源账号{}".format(str(index)) for index in range(10)]),
            "auth_account": random.choice(["认证账号{}".format(str(index)) for index in range(10)]),
            "policy_id": random.randint(1, 1000),
            "rule_id": random.randint(1, 1000),
            "rule_templet_id": random.randint(1, 1000),
            "direction": random.choice(["request", "response"]),
            "response_time": random.randint(1, 100000),
            "error_code": random.randint(1, 10),
            "block": random.choice(["yes", "no"]),
            "record_rows": random.randint(1, 100),
            "sql": random.choice(["select * from user", "delete from user", "update user set name='张三' where id =1"]),
            "client_host": random.choice(["源主机名称{}".format(str(index)) for index in range(10)]),
            "server_host": random.choice(["目的主机名称{}".format(str(index)) for index in range(10)]),
            "library": random.choice(["ODBC", "JDBC"]),
            "client_software": random.choice(["客户端软件{}".format(str(index)) for index in range(10)]),
            "client_user": random.choice(["客户端用户名{}".format(str(index)) for index in range(10)]),
            "instance_name": random.choice(["实例名{}".format(str(index)) for index in range(10)]),
            "db_name": random.choice(["数据库{}".format(str(index)) for index in range(10)]),
            "table_name": random.choice(["表名{}".format(str(index)) for index in range(10)]),
            "object_name": random.choice(["对象名{}".format(str(index)) for index in range(10)]),
            "cmd": random.choice(["命令{}".format(str(index)) for index in range(10)]),
            "subcmd": random.choice(["子命令{}".format(str(index)) for index in range(10)]),

        }

        return {
            "_index": index_name,
            "_type": 'logs',
            "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),

            "event_host": event_data['dev_ip'],
            "event_one_type": random.choice(['违规']),
            "event_two_type": event_data['ruleset_name'],
            "event_three_type": event_data['rule_name'],
            "event_source": 3,
            "src_ip": event_data['server_ip'],
            "dst_ip": event_data['client_ip'],
            "src_port": event_data['server_port'],
            "dst_port": event_data['client_port'],
            "tran_protocol": event_data['transport_protocol'],
            "app_protocol": event_data['app_protocol'],
            "start_time": date_time.strftime('%Y%m%d%H%M%S'),
            "end_time": date_time.strftime('%Y%m%d%H%M%S'),
            "stastic_time": date_time.strftime('%Y%m%d%H%M%S'),
            "opt_result": 1,
            "flow": '',
            "event_level": random.choice([1, 2, 3]),
            "organization": '',  # 单位
            "event_total": random.randint(0, 5),
            "event_detail": json.dumps(event_data),
            "event_contents": "{}请求sql:{}触发规则{}".format(event_data['dev_ip'],event_data['sql'],
                                                          event_data['rule_name']),
        }

    def run(self):
        # # 数据库审计
        # self.make_data('ssa-ag-database')
        # self.make_data('event-db-audit')
        # self.make_data('statistics-db-audit')
        self.make_data('all-event')
