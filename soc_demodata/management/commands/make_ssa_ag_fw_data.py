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

    def ssa_ag_fw_data_func(self, index_name, date_time):
        """
        防火墙
        """
        deny_result = random.randint(0, 1)
        if deny_result == 0:
            deny_event = ""
        else:
            deny_event = random.choice(['被规则拒绝','应用识别不符','应用动作违规'])
        return {
            "_type": 'logs',
            "_index": index_name,
            "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "time": date_time.strftime('%Y%m%d%H%M%S'),
            "src_ip": random.choice(self.ips),
            "src_port": random.randint(3000, 6000),
            "dst_ip": random.choice(self.ips),
            "dst_port": random.randint(3000, 6000),
            "provider_id": "",
            "device_name": random.choice(['59.27.14.159', '84.79.73.154']),
            "level": random.randint(1, 3),
            "event_type": "",
            "event_name": "",
            "event_digest": "",
            "protocol": random.choice(['tcp', 'udp', 'icmp', 'http', 'ftp', 'telnet', 'pop3']),
            "src_mac": "00-23-24-AF-D7-E2",
            "dst_mac": "00-23-24-AF-D7-E2",
            "username": "",
            "program": "",
            "operation": "",
            "object": "",
            "result": deny_result,
            "response": "",
            "msg": "",
            "flow": random.randint(100, 1002400),
            "deny_re": deny_event
        }

    def event_firewall_data_func(self, index_name, date_time):
        '''
        防火墙事件统计数据
        '''
        return {
            "_index": index_name,
            "_type": 'logs',
            "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "src_ip": random.choice(self.ips),
            "dst_ip": random.choice(self.ips),
            "src_port": random.randint(3000, 6000),
            "dst_port": random.randint(3000, 6000),
            "protocol": random.choice(['tcp', 'udp', 'icmp', 'http', 'ftp', 'telnet', 'pop3']),
            "event_top_type": "攻击事件",
            "event_type": random.choice(['应用识别不符','被规则拒绝','应用动作违规']),
            "event_source": "防火墙{}".format(random.choice(['59.27.14.159', '84.79.73.154'])),
            "start_time": date_time.strftime('%Y%m%d%H%M%S'),
            "end_time": date_time.strftime('%Y%m%d%H%M%S'),
            "organization": "",
            "event_total": random.randint(0, 100),
            "terminal": ['59.27.14.159', '84.79.73.154'],
            "event_level": random.choice([1, 2, 3])
        }

    def statistics_firewall_data_func(self, index_name, date_time):
        '''
        防火墙日志统计数据
        '''
        return {
            "_index": index_name,
            "_type": 'logs',
            "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "src_ip": random.choice(self.ips),
            "dst_ip": random.choice(self.ips),
            "src_port": random.randint(3000, 6000),
            "dst_port": random.randint(3000, 6000),
            "protocol": random.choice(['tcp', 'udp', 'icmp', 'http', 'ftp', 'telnet', 'pop3']),
            "log_top_type": "防火墙",
            "log_type": "防火墙{}".format(random.choice(['59.27.14.159', '84.79.73.154'])),
            "log_total": random.randint(500, 1000),
            "start_time": date_time.strftime('%Y%m%d%H%M%S'),
            "end_time": date_time.strftime('%Y%m%d%H%M%S'),
            "organization": "",
            "terminal": random.choice(self.ips),
            "log_flow": random.randint(100, 1000),
            "log_source": "防火墙{}".format(random.choice(['59.27.14.159', '84.79.73.154']))
        }

    def all_event_data_func(self, index_name, date_time):
        '''
        所有事件
        '''
        event_data = {
            "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "time": date_time.strftime('%Y%m%d%H%M%S'),
            "src_ip": random.choice(self.ips),
            "src_port": random.randint(3000, 6000),
            "dst_ip": random.choice(self.ips),
            "dst_port": random.randint(3000, 6000),
            "provider_id": "",
            "device_name": random.choice(['59.27.14.159', '84.79.73.154']),
            "level": random.randint(1, 3),
            "event_type": "",
            "event_name": "",
            "event_digest": "",
            "protocol": random.choice(['tcp', 'udp', 'icmp', 'http', 'ftp', 'telnet', 'pop3']),
            "src_mac": "00-23-24-AF-D7-E2",
            "dst_mac": "00-23-24-AF-D7-E2",
            "username": "",
            "program": "",
            "operation": "",
            "object": "",
            "result": random.randint(0, 1),
            "response": "",
            "msg": "",
            "flow": random.randint(100, 1002400),
            "type": random.choice(['被规则拒绝', '应用识别不符', '应用动作违规'])

        }
        if event_data['result'] == 1:
            content = "{}请求{}被放行".format(event_data['src_ip'],event_data['dst_ip'])
        else:
            content = "{}请求{}被阻断，阻断原因:{}".format(event_data['src_ip'],
                                                                     event_data['dst_ip'], event_data['type'])
        return {
            "_index": index_name,
            "_type": 'logs',
            "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),

            "event_host": event_data['device_name'],
            "event_one_type": random.choice(['攻击']),
            "event_two_type": random.choice(['阻断策略']),
            "event_three_type": random.choice(['被规则拒绝', '应用识别不符', '应用动作违规']),
            "event_source": 1,
            "src_ip": event_data['src_ip'],
            "dst_ip": event_data['dst_ip'],
            "src_port": event_data['src_port'],
            "dst_port": event_data['dst_port'],
            "tran_protocol": event_data['protocol'],
            "app_protocol": '',
            "start_time": date_time.strftime('%Y%m%d%H%M%S'),
            "end_time": date_time.strftime('%Y%m%d%H%M%S'),
            "stastic_time": date_time.strftime('%Y%m%d%H%M%S'),
            "opt_result": event_data['result'],
            "flow": random.randint(10, 1000),
            "event_level": random.choice([1, 2, 3]),
            "organization": '',  # 单位
            "event_total": random.randint(0, 5),
            "event_detail": json.dumps(event_data),
            "event_contents": content,
        }

    def run(self):
        # FW
        # self.make_data('ssa-ag-fw')
        # self.make_data('event-firewall')
        # self.make_data('statistics-firewall')
        self.make_data('all-event')
