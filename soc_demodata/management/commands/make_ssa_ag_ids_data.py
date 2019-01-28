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
two_type = ['信息收集','获取权限','远程控制','数据盗取','系统破坏','隐藏攻击痕迹','有害程序','恶意网站','其他类攻击事件']
three_type = ['系统扫描','端口扫描','漏洞扫描','其他','上传漏洞','上传webshell','远程溢出','3389口令破解','FTP口令破解','SSH口令破解','数据库口令破解','邮件服务口令破解','WEB口令破解','提权','创建用户','更改原有用户密码','其他','Webshell控制','PC木马控制','服务器后门','服务器木马控制','其他','SQL注入','远程拷贝','其他','拒绝服务攻击','格式化磁盘','切断目标主机网络','更改目标主机配置','篡改信息','其他','删除入侵日志','删除rootkit','其他','计算机病毒','蠕虫','计算机木马','僵尸网络','混合攻击程序','网页内嵌恶意代码','其他','钓鱼网站','暴恐网站','色情网站','赌博网站','其他']

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

    def ssa_ag_ids_data_func(self, index_name, date_time):
        '''
        IDS
        '''
        return {
            "_index": index_name,
            "_type": 'logs',
            "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "source": random.choice(self.ips),
            "level": random.choice(level_list),
            "time": date_time.strftime('%Y%m%d%H%M%S'),
            "src_ip": random.choice(self.ips),
            "src_port": random.randint(3000, 6000),
            "dst_ip": random.choice(self.ips),
            "dst_port": random.randint(3000, 6000),
            "type_id": "",
            "name": "",
            "cve_id": "",
            "fingerprint": "",
            "internal_id": "",
            "provider_id": "",
            "event_name": random.choice(['TCP_后门_网络红娘_正向连接', '啦啦啦']),
            "src_mac": "服务器MAC地址",
            "dst_mac": "目的端MAC地址",
            "event_count": random.randint(1, 100000),
            "protocol": random.choice(['tcp', 'udp']),
            "response": "",
            "action": "",
            "description": "",
            "securityid": random.choice(securityid_list),
            "attackid": random.choice(attack_list),
        }

    def event_ids_data_func(self, index_name, date_time):
        '''
        Ids事件统计数据
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
            "event_top_type": "攻击事件",
            "event_type": random.choice(['获取权限', '有害程序', '系统破坏', '远程控制', '恶意网站', '信息收集', '隐藏攻击痕迹',
                                         '数据盗取', '其它']),
            "event_source": "IDS{}".format(random.choice(['213.209.127.64', '160.20.227.90'])),
            "start_time": date_time.strftime('%Y%m%d%H%M%S'),
            "end_time": date_time.strftime('%Y%m%d%H%M%S'),
            "organization": "",
            "event_total": random.randint(0, 100),
            "terminal": random.choice(self.ips),
            "event_level": random.choice([1, 2, 3])
        }

    def statistics_ids_data_func(self, index_name, date_time):
        '''
        IdS日志统计数据
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
            "log_top_type": "IDS日志",
            "log_type": random.choice(['协议分析','网络娱乐','蠕虫病毒','可疑行为','间谍软件','网络设备攻击','网络通讯','缓冲溢出',
                                       '安全审计','脆弱口令','安全漏洞','穷举探测','木马后门','网络数据库攻击','CGI访问',
                                       '分布式拒绝服务','安全扫描','欺骗劫持','CGI攻击','拒绝服务']),
            "log_total": random.randint(500, 1000),
            "start_time": date_time.strftime('%Y%m%d%H%M%S'),
            "end_time": date_time.strftime('%Y%m%d%H%M%S'),
            "organization": "",
            "terminal": random.choice(self.ips),
            "log_flow": "",
            "log_source": "IDS"
        }

    def all_event_data_func(self, index_name, date_time):
        '''
        所有事件
        '''
        event_data = {
            "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "source": random.choice(self.ips),
            "level": random.choice(level_list),
            "time": date_time.strftime('%Y%m%d%H%M%S'),
            "src_ip": random.choice(self.ips),
            "src_port": random.randint(3000, 6000),
            "dst_ip": random.choice(self.ips),
            "dst_port": random.randint(3000, 6000),
            "type_id": "",
            "name": "",
            "cve_id": "",
            "fingerprint": "",
            "internal_id": "",
            "provider_id": "",
            "event_name": random.choice(['TCP_后门_网络红娘_正向连接', '啦啦啦']),
            "src_mac": "服务器MAC地址",
            "dst_mac": "目的端MAC地址",
            "event_count": random.randint(1, 100000),
            "protocol": random.choice(['tcp', 'udp']),
            "response": "",
            "action": "",
            "description": "",
            "securityid": random.choice(securityid_list),
            "attackid": random.choice(attack_list),
        }
        three_types = random.choice(three_type),
        return {
            "_index": index_name,
            "_type": 'logs',
            "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),

            "event_host": event_data['source'],
            "event_one_type": random.choice(['攻击']),
            "event_two_type": random.choice(two_type),
            "event_three_type": three_types,
            "event_source": 2,
            "src_ip": event_data['src_ip'],
            "dst_ip": event_data['dst_ip'],
            "src_port": event_data['src_port'],
            "dst_port": event_data['dst_port'],
            "tran_protocol": event_data['protocol'],
            "app_protocol": '',
            "start_time": date_time.strftime('%Y%m%d%H%M%S'),
            "end_time": date_time.strftime('%Y%m%d%H%M%S'),
            "stastic_time": date_time.strftime('%Y%m%d%H%M%S'),
            "opt_result": random.choice([0, 1]),
            "flow": '',
            "event_level": random.choice([1, 2, 3]),
            "organization": '',  # 单位
            "event_total": random.randint(0, 5),
            "event_detail": json.dumps(event_data),
            "event_contents": "{}发生{},{}".format(event_data['source'],three_types,
                                                 event_data['description']),
        }

    def run(self):
        # IDS
        # self.make_data('ssa-ag-ids')
        # self.make_data('event-ids')
        # self.make_data('statistics-ids')
        self.make_data('all-event')

