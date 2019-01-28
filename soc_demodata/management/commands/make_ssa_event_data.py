# coding: utf-8
import random
import logging
import datetime
from faker import Factory, Faker
from uuid import uuid4
from soc.models import Agent
from common import add_doc_list
from optparse import make_option
from django.utils import timezone
from django.core.management.base import BaseCommand

import time

logger = logging.getLogger('console')
logging.info("script okkkk")

myfake = Factory.create()

"""
python manage.py make_ssa_event_data --agent=Qingsong2
"""


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--agent', dest='agent_name',
                    default='', help='agent name'),
        # make_option('--company', dest='company_name', default='', help='company name'),
    )

    def handle(self, *args, **options):
        agent = options.get('agent_name')
        # company_id = options.get("company_name")
        agent = Agent.objects.get(name=agent)
        logging.info("get agent {0} success ".format(agent))
        obj = DemoData(agent=agent)
        obj.run()


class DemoData(object):
    def __init__(self, agent, company=None):
        self.agent = agent
        self.company = company
        self.fake = Factory.create()
        self.src_ips = [self.fake.ipv4() for i in range(100)]
        self.src_ports = [i for i in range(22, 1000)]
        self.dst_ips = [self.fake.ipv4() for i in range(10)]
        self.dst_ports = [i for i in range(1000, 10000)]
        self.domains = ["www." + self.fake.domain_word() +
                        ".com" for i in range(10)]
        self.cache = {}
        self.location = ['青岛市', '济南市', '曲阜市', '烟台市', '泰安市', '威海市', '蓬莱市', '日照市']
        self.location = ["郑州 ", "开封", "洛阳", "平顶山", "安阳", "鹤壁", "新乡", "焦作", "濮阳", "许昌", "漯河", "三门峡", "南阳", "商丘", "信阳",
                         "周口", "驻马店"]

    def make_data(self, index_name):
        """
        生成数据
        """
        data_fun = getattr(self, "{}_data_func".format(
            index_name.replace('-', '_')))
        print('事件搜索{}数据'.format(index_name))
        datas = []
        # 从10天后 开始往10天前生成数据 共计20天
        start_time = timezone.now() + timezone.timedelta(days=10)
        for i in range(20):
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

    def web_log_data_func(self, index_name, date_time):
        """
        网站访问
        """
        return {
            "time": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "server": random.choice(self.domains),
            "host": random.choice(self.domains),
            "hostname": random.choice(self.domains),
            "remote_ip": random.choice(self.src_ips),
            "src_ip_location": random.choice(self.location),
            "real_ip": random.choice(self.src_ips),
            "ip_loc": "0",
            "server_ip": random.choice(self.dst_ips),
            "status": random.choice([200, 200, 200, 400, 401, 404, 404, 500, 500]),
            "bytes_sent": random.randint(500, 3000),
            "method": random.choice(['POST', 'GET', 'DELETE', 'PUT']),
            "req_uri": self.fake.uri(),
            "uri": self.fake.uri(),
            "scheme": random.randint(50, 120),
            "protocol": random.choice(["HTTP/1.1", 'HTTPS', 'HTTP/1.2']),
            "req_len": str(random.randint(100, 500)),
            "req_time": "0." + str(random.randint(100, 200)),
            "waf_ruleid": random.randint(5, 20),
            "waf_rule": myfake.sha1(),
            "ac_ruleid": random.randint(10000, 50000),
            "ac_auth": "0",
            "ac_defense": "0",
            "con_len": random.randint(5, 20),
            "con_type": "application%2Fx-www-form-urlencoded%3B%20charset%3DUTF-8",
            "accept": self.fake.address(),
            "charset": "-",
            "encoding": random.choice(["gzip", 'tar']),
            "language": "zh-CN",
            "ranges": "-",
            "connection": "keep-alive",
            "upgrade": random.randint(0, 1),
            "pramga": random.randint(5, 20),
            "cache_ctrl": myfake.uri(),
            "cookie": self.fake.sha256(),
            "dev_type": "full",
            "device": "-",
            "osname": self.fake.windows_platform_token(),
            "up_addr": self.fake.ipv4(),
            "up_status": random.choice([200, 200, 200, 400, 401, 404, 404, 500, 500]),
            "up_cache": "-",
            "up_rtime": "0." + str(random.randint(100, 200)),
            "header": "Host%3A%20www.qssec",
            "req_body": "domain%3Dxyqb.com",
            "_type": 'logs',
            "_index": index_name,
        }

    def ids_data_func(self, index_name, date_time):
        """
        IDS
        """
        return {
            "_type": 'logs',
            "_index": index_name,
            "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "time": date_time.strftime('%Y-%m-%d %H:%M:%S'),
            "src_ip": random.choice(self.src_ips),
            "src_ip_location": random.choice(self.location),
            "src_port": random.choice(self.src_ports),
            "dst_ip": random.choice(self.dst_ips),
            "dst_ip_location": random.choice(self.location),
            "dst_port": random.choice(self.dst_ports),
            "protocol": random.choice(['SSH', 'SNMP', 'SMTP', 'SMB', 'HTTP', "TCP"]),
            "type_id": "00{0}00{1}".format(random.randint(1, 9), random.randint(1, 9)),
            "name": random.choice(['SQL注入', '命令注入', '拒绝服务', '远程攻击', '暴力破解']),
            "cve_id": "CVE-{}".format(date_time.strftime("%Y-%m-%d")),
            "fingerprint": "fingerprint",
            "level": random.randint(0, 4),
            "internal_id": random.randint(1, 10),
            "provider_id": random.randint(1, 10),
        }

    def network_data_func(self, index_name, date_time):
        """
        网络数据
        """
        return {
            "_type": 'logs',
            "_index": index_name,
            "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "time": 142113 + random.randint(1000, 9000),
            "src_ip": random.choice(self.src_ips),
            "src_ip_location": random.choice(self.location),
            "src_port": random.choice(self.src_ports),
            "dst_ip": random.choice(self.dst_ips),
            "dst_ip_location": random.choice(self.location),
            "dst_port": random.choice(self.dst_ports),
            "start": 1421138310 + random.randint(1, 1000),
            "end": 1421138319 + random.randint(1, 1000),
            "upload_pkg": random.randint(1, 100),
            "upload_bytes": random.randint(100, 1000),
            "download_pkg": random.randint(10000, 100000),
            "download_bytes": random.randint(1, 100) * 10000,
            "app_proto": random.randint(1, 10),
            "device_type": random.choice(['云防', 'HADES', '思科', '华为', '中兴']),
            "app_names": "qq, 微信",
            "app_name": random.choice(['网页一', 'APP-1', '视频', '音乐', '游戏']),
            "provider_id": myfake.word(),
        }

    def firewall_data_func(self, index_name, date_time):
        """
        防火墙
        """
        return {
            "_type": 'logs',
            "_index": index_name,
            "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "time": date_time.strftime('%Y-%m-%d %H:%M:%S'),
            "src_ip": random.choice(self.src_ips),
            "src_ip_location": random.choice(self.location),
            "src_port": random.choice(self.src_ports),
            "dst_ip": random.choice(self.dst_ips),
            "dst_ip_location": random.choice(self.location),
            "dst_port": random.choice(self.dst_ports),
            "deny_re": random.randint(1, 4),
            "device_type": random.choice(['云防', 'HADES', '思科', '华为', '中兴']),
            "level": random.randint(0, 4),
            "type": random.choice(['包过滤', '代理', '入侵检测', 'VPN', '用户认证']),
            "protocol": random.choice(['SSH', 'SNMP', 'SMTP', 'SMB', 'HTTP', "TCP"]),
            "username": random.choice(['admin', 'root', 'guest', 'test', 'user']),
            "result": random.randint(0, 1),
        }

    def virus_data_func(self, index_name, date_time):
        """病毒"""
        virus_log = {
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
            "time": '',
            "utcms": "",
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

        # virus_log["version"] = random.choice(["天擎6.", '天擎6.3.', '天擎8'])
        # virus_log["log_name"] = random.choice(["病毒分析", '全盘扫描', '深度查杀', '深度清理'])
        # virus_log["log_id"] = myfake.sha1()
        # virus_log["create_time"] = date_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        # virus_log["ip"] = random.choice(['10.10.0.' + str(i) for i in range(20)])
        # virus_log["report_ip"] = random.choice(['10.10.0.'+ str(i) for i in range(20)])
        # virus_log["mac"] = random.choice(['d43d7ec97797', 'oc3d7ev977io', 'p4td7fc91797', 'ddf9fgts797'])
        # virus_log["gid"] = random.randint(100, 200)
        # virus_log["work_group"] = ""
        # virus_log["content"] = {
        #     "name": "Gen:Variant.Zusy.165381",
        #     "type": "木马",
        #     "virus_path": "c:\\windows\\system32\\ntchecktool.dll",
        #     "op": "未处理",
        #     "task": "实时监控查杀"
        # }

        log_i = virus_log
        log_i["infectedfileinfo_cleared"] = 1 if random.randint(
            0, 100) > 80 else 0
        log_i["host_ip"] = random.choice(['192.168.0.' + str(i) for i in range(20)])
        log_i["virustype"] = [0, 1, 2, 3, 4, 5, 6][random.randint(0, 6)]
        return log_i

    def weak_password_data_func(self, index_name, date_time):
        """弱密码"""
        weak_password = {
            "_type": 'logs',
            "_index": index_name,
            "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "scan_start_time": int(time.mktime(date_time.timetuple())) + random.randint(0, 100),
            "scan_end_time": int(time.mktime(date_time.timetuple())) + random.randint(0, 100),
            "port": 22,
            "username": "root",
            "protocol": "SSH"
        }
        log_i = weak_password
        # log_i["scan_start_time"] += index
        # log_i["scan_end_time"] += index
        log_i["ip"] = random.choice(['192.168.0.' + str(i) for i in range(20)])
        log_i["protocol"] = ["SSH", "HTTP", "HTTPS",
                             "SS", "samb"][random.randint(0, 4)]
        return log_i

    def anti_ddos_data_func(self, index_name, date_time):
        "ddos"
        log = {
            "_type": 'logs',
            "_index": index_name,
            "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "time": int(time.mktime(date_time.timetuple())) + random.randint(0, 100),
            "service_name": random.choice(['10.10.0.' + str(i) for i in range(20)]),
            "server_ip": random.choice(['168.18.0.' + str(i) for i in range(20)]),
            "server_type": 'qs',
            "flux_in": random.randint(1000, 2000),
            "flux_out": random.randint(2000, 3000),
            "packet_in": random.randint(20, 90),
            "packet_out": random.randint(20, 90),
            "syn": random.randint(20, 90),
            "ack": random.randint(20, 90),
            "udp": random.randint(20, 90),
            "reset": random.randint(20, 90),
            "other_tcp": random.randint(20, 90),
            "other_ip": random.randint(20, 90),
            "none_ip": random.randint(20, 90),
            "cc_def": random.randint(20, 90),
            "company_name": random.choice([i for i in 'asdfghjklmnbvcxz']) + random.choice(
                [i for i in 'asdfghjklmnbvcxz']),
            "idc_name": myfake.word(),
            "cluster_name": myfake.word(),
            "is_attack": random.choice([0, 1]),
            "attack_type": "syn",
        }
        log_i = log
        log_i["service_name"] = random.choice(['10.10.0.' + str(i) for i in range(20)])
        log_i["server_ip"] = log_i["service_name"]
        log_i["flux_in"] = random.randint(13, 6000000)
        log_i["flux_out"] = random.randint(13, 6000000)
        log_i["packet_in"] = random.randint(13, 6000)
        log_i["packet_out"] = random.randint(13, 60000)
        log_i["syn"] = log_i["flux_in"] / 10 * 4
        log_i["ack"] = log_i["flux_in"] / 10 * 3
        log_i["udp"] = log_i["flux_in"] / 10 * 2
        log_i["reset"] = log_i["flux_in"] / 10 * 1
        log_i["is_attack"] = [1, 0][random.randint(0, 1)]
        return log_i

    def db_audit_data_func(self, index_name, date_time):
        """数据库审计"""
        db_audit_log = {
            "_type": 'logs',
            "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "_index": index_name,
            "src_ip": random.choice(['10.10.0.' + str(i) for i in range(20)]),
            "src_port": random.randint(3000, 6000),
            "dst_ip": random.choice(['10.10.0.' + str(i) for i in range(20)]),
            "dst_port": 80,
            "time": int(time.mktime(date_time.timetuple())) + random.randint(0, 100),
            "level": "严重",
        }
        log_i = db_audit_log
        log_i["level"] = ["严重", "高", "中",
                          "低", "info"][random.randint(0, 4)]
        return log_i

    def host_scan_data_func(self, index_name, date_time):
        """主机扫描"""
        vul_log = {
            "_type": 'logs',
            "_index": index_name,
            "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "ip": "10.1.1.1",
            "scan_start_time": int(time.mktime(date_time.timetuple())) + random.randint(0, 100),
            "scan_end_time": int(time.mktime(date_time.timetuple())) + random.randint(100, 200),
            "provider_id": "bmh",
            "vuln_name": "Redis未授权访问",
            "scan_type": "主机扫描",
            "custom_name": random.choice(['10.10.0.' + str(i) for i in range(20)]),
            "desc": myfake.word(),
            "harm_content": myfake.word(),
            "solution": myfake.word(),
            "threat_type": "其他",
            "port": 80,
        }
        log_i = vul_log
        log_i["ip"] = random.choice(['10.10.0.' + str(i) for i in range(20)])

        log_i["level"] = ["严重", "高", "中",
                          "低", "info"][random.randint(0, 4)]
        log_i["vuln_name"] = ["时序OS命令注入",
                              "SQL注入漏洞",
                              "存在后门",
                              "不安全的客户访问策略",
                              "访问限制旁路源欺骗"][random.randint(0, 4)]
        log_i["threat_type"] = ["AA", "BB",
                                "CC", "DD",
                                "EE", "FF"][random.randint(0, 4)]
        log_i["risk_url"] = random.choice(['10.10.0.' + str(i) for i in range(20)])
        log_i["scan_type"] = ["host-scan",
                              "web-scan", "漏洞专扫"][random.randint(0, 2)]
        return log_i

    def web_scan_data_func(self, index_name, date_time):
        """网站扫描"""
        vul_log = {
            "_type": 'logs',
            "_index": index_name,
            "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "ip": random.choice(['10.10.0.' + str(i) for i in range(20)]),
            "scan_start_time": int(time.mktime(date_time.timetuple())) + random.randint(0, 100),
            "scan_end_time": int(time.mktime(date_time.timetuple())) + random.randint(100, 200),
            "provider_id": "bmh",
            "vuln_name": myfake.word(),
            "scan_type": "网站扫描",
            "level": ["严重", "高", "中",
                      "低", "info"][random.randint(0, 4)],
            "risk_url": random.choice(['10.10.0.' + str(i) for i in range(20)]),
            "custom_name": random.choice(['10.10.0.' + str(i) for i in range(20)]),
            "desc": myfake.word(),
            "harm_content": myfake.word(),
            "solution": myfake.word(),
            "threat_type": "其他",
            "port": 80,
        }
        log_i = vul_log
        log_i["ip"] = random.choice(['10.10.0.' + str(i) for i in range(20)])

        log_i["level"] = ["严重", "高", "中",
                          "低", "info"][random.randint(0, 4)]
        log_i["vuln_name"] = ["时序OS命令注入",
                              "SQL注入漏洞",
                              "存在后门",
                              "不安全的客户访问策略",
                              "访问限制旁路源欺骗"][random.randint(0, 4)]
        log_i["threat_type"] = ["AA", "BB",
                                "CC", "DD",
                                "EE", "FF"][random.randint(0, 4)]
        log_i["risk_url"] = random.choice(['10.10.0.' + str(i) for i in range(20)])
        log_i["scan_type"] = ["host-scan",
                              "web-scan", "漏洞专扫"][random.randint(0, 2)]
        return log_i

    def etl_state_data_func(self, index_name, date_time):
        if not self.cache.get("flows"):
            from soc_ssa import models
            self.cache['flows'] = [i.uuid for i in models.SSASource.objects.all()[:10]]
        inputs = random.randint(1000, 10 * 10000)
        data = {
            "_index": "etl-state",
            "_type": 'logs',
            "time": date_time.strftime('%Y-%m-%d %H:%M:%S'),
            "flow_id": random.choice(self.cache['flows']),
            "flow": "input",
            "state": {
                "input": inputs,
                "output": inputs - random.randint(100, 1000),
                "fix": random.randint(100, 1000),
                "failure": random.randint(100, 1000),
            }
        }
        return data

    def event_firewall_data_func(self, index_name, date_time):
        """防火墙聚合事件"""
        fake = Faker("zh_CN")
        fire_wall = {
            "_type": 'log',
            "_index": index_name,
            "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "src_ip": random.choice(self.src_ips),
            "src_port": random.choice(self.src_ports),
            "attack_user": fake.name(),
            "attack_province": fake.province(),
            "attack_city": fake.city_name(),
            "attack_county": fake.district(),
            "dst_ip": random.choice(self.dst_ips),
            "dst_port": random.choice(self.dst_ports),
            "attacked_user": fake.name(),
            "attacked_province": fake.province(),
            "attacked_city": fake.city_name(),
            "attacked_county": fake.district(),
            "protocol": random.randint(0, 6),
            "total": random.randint(10000, 100000),
            "acc_total": random.randint(100, 1000),
            "acc_type": random.randint(100, 1000),
            "acc_session_type": random.randint(100, 1000),
            "acc_suspicious_type": random.randint(100, 1000),
            "opr_total": random.randint(100, 1000),
            "opr_type": random.randint(100, 1000),
            "sec_total": random.randint(100, 1000),
            "sec_type": random.randint(100, 1000),
            "auth_total": random.randint(100, 1000),
            "auth_authention_type": random.randint(100, 1000),
            "stat_total": random.randint(100, 1000),
            "stat_type": random.randint(100, 1000),
            "stat_info_type": random.randint(100, 1000),
            "score": random.randint(100, 1000),
            "time": date_time.strftime('%Y-%m-%d %H:%M:%S'),
            "date": date_time.strftime('%Y-%m-%d'),
            "opr_cfg_type": random.randint(100, 1000),
            "opr_db_type": random.randint(100, 1000),
            "malware_total": random.randint(100, 1000),
            "malware_type": random.randint(100, 1000),
            "malware_botnet_type": random.randint(100, 1000),
            "malware_virus_type": random.randint(100, 1000),
            "malware_other_type": random.randint(100, 1000),
            "malware_worm_type": random.randint(100, 1000),
            "malware_trojan_type": random.randint(100, 1000),
            "fault_total": random.randint(100, 1000),
            "fault_threshole_type": random.randint(100, 1000),
            "fault_server_type": random.randint(100, 1000),
            "spy_total": random.randint(100, 1000),
            "spy_type": random.randint(100, 1000),
            "spy_vuln_type": random.randint(100, 1000),
            "spy_port_type": random.randint(100, 1000),
            "spy_net_type": random.randint(100, 1000),
            "auth_type": random.randint(100, 1000),
            "auth_accmgr_type": random.randint(100, 1000),
            "att_total": random.randint(100, 1000),
            "att_type": random.randint(100, 1000),
            "att_vul_type": random.randint(100, 1000),
            "att_ddos_type": random.randint(100, 1000),
            "att_pwd_type": random.randint(100, 1000),
            "sec_other_type": random.randint(100, 1000),
            "acc_illegal_type": random.randint(100, 1000),
            "acc_normal_type": random.randint(100, 1000),
            "acc_other_type": random.randint(100, 1000),
            "stat_stop_type": random.randint(100, 1000),
            "stat_conflict_type": random.randint(100, 1000),
            "other_total": random.randint(100, 1000),
            "other_type": random.randint(100, 1000),
            "sec_leak_type": random.randint(100, 1000),
            "harm_total": random.randint(100, 1000),
            "monitor_total": random.randint(100, 1000),
        }
        log_i = fire_wall
        # log_i["protocol"] = ["SSH", "HTTP", "HTTPS",
        #                      "SS", "samb"][random.randint(0, 4)]
        # print(log_i["attack_user"])
        return log_i

    def event_ids_data_func(self, index_name, date_time):
        """防火墙聚合事件"""
        fake = Faker("zh_CN")
        fire_wall = {
            "_type": 'log',
            "_index": index_name,
            "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "src_ip": random.choice(self.src_ips),
            "src_port": random.choice(self.src_ports),
            "attack_user": fake.name(),
            "attack_province": fake.province(),
            "attack_city": fake.city_name(),
            "attack_county": fake.district(),
            "dst_ip": random.choice(self.dst_ips),
            "dst_port": random.choice(self.dst_ports),
            "attacked_user": fake.name(),
            "attacked_province": fake.province(),
            "attacked_city": fake.city_name(),
            "attacked_county": fake.district(),
            "protocol": random.randint(0, 6),
            "total": random.randint(10000, 100000),
            "acc_total": random.randint(100, 1000),
            "acc_type": random.randint(100, 1000),
            "acc_session_type": random.randint(100, 1000),
            "acc_suspicious_type": random.randint(100, 1000),
            "opr_total": random.randint(100, 1000),
            "opr_type": random.randint(100, 1000),
            "sec_total": random.randint(100, 1000),
            "sec_type": random.randint(100, 1000),
            "auth_total": random.randint(100, 1000),
            "auth_authention_type": random.randint(100, 1000),
            "stat_total": random.randint(100, 1000),
            "stat_type": random.randint(100, 1000),
            "stat_info_type": random.randint(100, 1000),
            "score": random.randint(100, 1000),
            "time": date_time.strftime('%Y-%m-%d %H:%M:%S'),
            "date": date_time.strftime('%Y-%m-%d'),
            "opr_cfg_type": random.randint(100, 1000),
            "opr_db_type": random.randint(100, 1000),
            "malware_total": random.randint(100, 1000),
            "malware_type": random.randint(100, 1000),
            "malware_botnet_type": random.randint(100, 1000),
            "malware_virus_type": random.randint(100, 1000),
            "malware_other_type": random.randint(100, 1000),
            "malware_worm_type": random.randint(100, 1000),
            "malware_trojan_type": random.randint(100, 1000),
            "fault_total": random.randint(100, 1000),
            "fault_threshole_type": random.randint(100, 1000),
            "fault_server_type": random.randint(100, 1000),
            "spy_total": random.randint(100, 1000),
            "spy_type": random.randint(100, 1000),
            "spy_vuln_type": random.randint(100, 1000),
            "spy_port_type": random.randint(100, 1000),
            "spy_net_type": random.randint(100, 1000),
            "auth_type": random.randint(100, 1000),
            "auth_accmgr_type": random.randint(100, 1000),
            "att_total": random.randint(100, 1000),
            "att_type": random.randint(100, 1000),
            "att_vul_type": random.randint(100, 1000),
            "att_ddos_type": random.randint(100, 1000),
            "att_pwd_type": random.randint(100, 1000),
            "sec_other_type": random.randint(100, 1000),
            "acc_illegal_type": random.randint(100, 1000),
            "acc_normal_type": random.randint(100, 1000),
            "acc_other_type": random.randint(100, 1000),
            "stat_stop_type": random.randint(100, 1000),
            "stat_conflict_type": random.randint(100, 1000),
            "other_total": random.randint(100, 1000),
            "other_type": random.randint(100, 1000),
            "sec_leak_type": random.randint(100, 1000),
            "harm_total": random.randint(100, 1000),
            "monitor_total": random.randint(100, 1000),
        }
        log_i = fire_wall
        # log_i["protocol"] = ["SSH", "HTTP", "HTTPS",
        #                      "SS", "samb"][random.randint(0, 4)]
        # print(log_i["attack_user"])
        return log_i

    def run(self):
        """
        执行入口
        """
        # self.make_data("ids")
        # self.make_data("network")
        # self.make_data("web-log")
        # self.make_data("firewall")
        # self.make_data("etl-state")

        # self.make_data("anti-ddos")  # 抗DDoS
        # self.make_data("host-scan")  # 主机扫描
        # self.make_data("web-scan")  # 网站扫描
        # self.make_data("weak-password")  # 弱口令扫描
        # self.make_data("virus")  # 病毒
        # self.make_data("db-audit")  # 数据库审计
        # self.make_data("event-firewall")
        self.make_data("event-ids")