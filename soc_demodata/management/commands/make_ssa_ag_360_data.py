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

    def ssa_ag_360_data_func(self, index_name, date_time):
        '''
        360
        '''
        return {
            # "_index": index_name,
            # "_type": 'logs',
            # "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            #
            # "version": "天擎6.3.0.6000",
            # "log_name": random.choice(["漏洞管理", "其他漏洞"]),
            # "log_id": str(uuid.uuid4()),
            # "create_time": date_time.strftime('%Y%m%d%H%M%S'),
            # "ip": random.choice(self.ips),
            # "report_ip": random.choice(self.ips),
            # "mac": random.choice(self.macs),
            # "gid": random.randint(1, 6000),
            # "work_group": random.choice([""]),
            # "content": random.choice(['{"name":"IE“秘狐”安全漏洞","type":"高危漏洞","action":"忽略漏洞"}',
            #                           '{"name":"Windows主题文件远程代码执行漏洞","type":"高危漏洞","action":"用户卸载漏洞补丁"}',
            #                           '{"name":"Windows 安全更新","type":"高危漏洞","action":"用户卸载漏洞补丁"}']),
            # "name": random.choice(["IE“秘狐”安全漏洞", "Windows主题文件远程代码执行漏洞", "Windows 安全更新"]),
            # "type": random.choice(["高危漏洞", "中危漏洞", "低危漏洞"]),
            "_type": 'logs',
            "_index": index_name,
            "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "host_ip": ["192.168.1.107", "192.168.2.107", "192.168.1.110", "192.168.1.120",
                        "192.168.3.107", "192.168.3.108", "192.168.3.109", "192.168.3.110"][random.randint(0, 7)],
            "computer_name": "",
            "infectedfileinfo_code": "",
            "infectedfileinfo_cleared": random.randint(0, 1),
            "infectedfileinfo_filehash": "",
            "infectedfileinfo_filepath": "c:\\windows\\system32\\ntchecktool.dll",
            "infectedfileinfo_custommediatype": "",
            "infectedfileinfo_mediatype": "",
            "time":  date_time.strftime('%Y%m%d%H%M%S'),
            "utcms":  date_time.strftime('%Y%m%d%H%M%S'),
            "custominitiativedefencesource": "",
            "initiativedefencecode": "",
            "customsource": "",
            "mainsourcecode": "",
            "taskid": "",
            "custommediatype": random.choice(["天擎6.", '天擎6.3.', '天擎8']),
            "mediatype": '',
            "clearedfilenumber": random.randint(1, 10),
            "infectedfilenumber": random.randint(1, 10),
            "customtype": '',
            "virusfingerprint": "",
            "virustype": random.choice(['木马', 'sql注入', '危险数据', '病毒']),
            "virusname": random.choice(["Gen:Variant.Zusy.165381",
                                        "Variant.Zusy"]),
            "provider_id": random.choice(['360']),
        }

    def event_anti_data_func(self, index_name, date_time):
        '''
        360事件统计数据
        '''
        return {
            "_index": index_name,
            "_type": 'logs',
            "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "src_ip": "",
            "dst_ip": "",
            "src_port": "",
            "dst_port": "",
            "protocol": "",
            "event_top_type": "病毒事件",
            "event_type": random.choice(["漏洞管理", "其他漏洞"]),
            "event_source": "360杀毒软件",
            "start_time": date_time.strftime('%Y%m%d%H%M%S'),
            "end_time": date_time.strftime('%Y%m%d%H%M%S'),
            "organization": "",
            "event_total": random.randint(0, 100),
            "terminal": random.choice(self.ips),
            "event_level": 2
        }

    def statistics_anti_data_func(self, index_name, date_time):
        '''
        360日志统计数据
        '''
        return {
            "_index": index_name,
            "_type": 'logs',
            "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "src_ip": "",
            "dst_ip": "",
            "src_port": "",
            "dst_port": "",
            "protocol": "",
            "log_top_type": "杀毒软件",
            "log_type": random.choice(["漏洞管理", "其他漏洞"]),
            "log_total": random.randint(500, 1000),
            "start_time": date_time.strftime('%Y%m%d%H%M%S'),
            "end_time": date_time.strftime('%Y%m%d%H%M%S'),
            "organization": "",
            "terminal": random.choice(self.ips),
            "log_flow": "",
            "log_source": "360"
        }

    def all_event_data_func(self, index_name, date_time):
        '''
        所有事件
        '''
        event_data = {
            "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "host_ip": ["192.168.1.107", "192.168.2.107", "192.168.1.110", "192.168.1.120",
                        "192.168.3.107", "192.168.3.108", "192.168.3.109", "192.168.3.110"][random.randint(0, 7)],
            "computer_name": "",
            "infectedfileinfo_code": "",
            "infectedfileinfo_cleared": random.randint(0, 1),
            "infectedfileinfo_filehash": "",
            "infectedfileinfo_filepath": "c:\\windows\\system32\\ntchecktool.dll",
            "infectedfileinfo_custommediatype": "",
            "infectedfileinfo_mediatype": "",
            "time": date_time.strftime('%Y%m%d%H%M%S'),
            "utcms": date_time.strftime('%Y%m%d%H%M%S'),
            "custominitiativedefencesource": "",
            "initiativedefencecode": "",
            "customsource": "",
            "mainsourcecode": "",
            "taskid": "",
            "custommediatype": random.choice(["天擎6.", '天擎6.3.', '天擎8']),
            "mediatype": '',
            "clearedfilenumber": random.randint(1, 10),
            "infectedfilenumber": random.randint(1, 10),
            "customtype": '',
            "virusfingerprint": "",
            "virustype": random.choice(['木马', 'sql注入', '危险数据', '病毒']),
            "virusname": random.choice(["Gen:Variant.Zusy.165381",
                                        "Variant.Zusy"]),
            "provider_id": random.choice(['360']),
            "two_type": random.choice(['有害程序', '漏洞', '其它'])
        }
        return {
            "_index": index_name,
            "_type": 'logs',
            "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),

            "event_host": event_data['host_ip'],
            "event_one_type": random.choice(['病毒']),
            "event_two_type": event_data['two_type'],
            "event_three_type": event_data['virustype'],
            "event_source": 6,
            "src_ip": event_data['host_ip'],
            "dst_ip": '',
            "src_port": '',
            "dst_port": '',
            "tran_protocol": '',
            "app_protocol": '',
            "start_time": date_time.strftime('%Y%m%d%H%M%S'),
            "end_time": date_time.strftime('%Y%m%d%H%M%S'),
            "stastic_time": date_time.strftime('%Y%m%d%H%M%S'),
            "opt_result": event_data['infectedfileinfo_cleared'],
            "flow": '',
            "event_level": 2,
            "organization": '',  # 单位
            "event_total": random.randint(0, 100),
            "event_detail": json.dumps(event_data),
            "event_contents": "{}发现{}:{}感染路径{}".format(event_data['host_ip'],event_data['two_type'],event_data['virustype'],event_data['infectedfileinfo_filepath'])
,
        }

    def run(self):
        # # 360
        # self.make_data('ssa-ag-360')
        # # 360事件
        # self.make_data('event-anti')
        # # 360日志
        # self.make_data('statistics-anti')
        # 事件
        self.make_data('all-event')
