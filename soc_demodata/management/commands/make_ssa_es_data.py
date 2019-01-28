# coding:utf-8
from __future__ import unicode_literals, print_function
import json
import logging
import random
import time
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from faker import Factory
from hashlib import md5
from optparse import make_option
from utils import ip as geoip

es_hosts = getattr(settings, "ELASTICSEARCH_HOSTS", ["http://127.0.0.1:9200/"])
logger = logging.getLogger('console')


class Command(BaseCommand):
    help = "生成态势感知demo数据"
    option_list = BaseCommand.option_list + (
        make_option('--days', dest='days', default=1, type=int,
                    help='Days, day'),
    )

    def handle(self, *args, **options):
        """生成数据
        1. 时间周期为当天0点到24点
        """
        days = options.get("days")
        today_zero = timezone.localtime(timezone.now()).replace(
            hour=0, minute=0, second=0, microsecond=0)
        for i in range(days):
            SSAEsData(today_zero-timezone.timedelta(days=i)).make_data()


def random_shuffle(x):
    random.shuffle(x)
    return x


def fil(ip):
    try:
        location = geoip.find_ip_location(ip)
        if len(location) == 4:
            location = location[1]
    except Exception as e:
        location = "未知"
    return location


class SSAEsData(object):
    """SSA ES Data
    """

    def __init__(self, day_zero):
        self.datas = None
        self.hosts = [
            "10.1.1.1", "10.1.1.2", "10.1.1.3", "10.1.1.4", "10.1.1.5",
            "10.1.1.6", "10.1.1.6", "10.1.1.8", "10.1.1.9", "10.1.1.10",
            "10.2.1.6", "10.2.1.6", "10.2.1.8", "10.2.1.9", "10.2.1.10",
            "10.3.1.6", "10.3.1.6", "10.3.1.8", "10.3.1.9", "10.3.1.10",
            "10.4.1.6", "10.5.1.6", "10.6.1.8", "10.7.1.9", "10.8.1.10",
        ]
        self.src_ips = [
            "45.45.45.45", "37.123.43.55", "34.88.88.123", "139.23.45.4",
            "50.67.45.45", "211.123.55.55", "34.88.88.222", "138.23.45.42",
            "50.69.45.45", "211.143.55.55", "34.77.88.222", "139.3.45.42",
            "50.67.45.99", "213.123.55.55", "34.66.88.222", "138.203.45.42",
        ]
        self.dst_ips = ["23.97.72.204", "23.97.72.205",
                        "23.97.72.206", "23.97.72.207"]
        self.supported_keys = [
            ["network", [
                "throughput",
                "abnormal_throughput_peak"
            ]],
            ["ids", [
                # 不要改变顺序
                "level_count",
                "source_count",
                "total_count",
            ]],
            ["firewall", [
                "total_count"
            ]],
            ["anti-ddos", [
                "max_throughput"
            ]],
            ["vul", [
                "vul_total_count",
                "vul_count",
                "vul_level_count",
                "vul_threat_type_count",
                "vul_risk_url_count",
                "vul_ip_count",
                "vul_top"
            ]],
            ["virus", [
                # 不要改变顺序
                "total_count",
                "btw_count",
                "btw_cleared",
                "asset_top",
                "btw_asset_top"
            ]],
            ["waf", [
                # 不要改变顺序
                "attack_type_count",
                "total_count",
            ]],
            ["db-audit", [
                "total_count"
            ]],
            ["web-log", [
                # 不要改变顺序
                "uv",
                "http_status_count",
                "location_count",
                "browser_count",
                "ip_count",
                "pv",
                "os_count"
            ]],
            ["weak-password", [
                "host_count"
            ]],
            ["security", [
                "total_count",
                "source_count",
                "level_count",
                "dst_ip_count",
                "events"
            ]]
        ]
        # 当天0时
        self.today_zero = day_zero

        #
        self.flux_ins = None
        self.flux_outs = None

    def make_24hour_data(self, key, data_24):
        """添加时间到数据中
        """
        docs = []
        if len(data_24) != 24:
            import pdb
            pdb.set_trace()
        for idx, one_hour in enumerate(data_24):
            local_time = self.today_zero + timezone.timedelta(hours=idx)
            timestamp = int(time.mktime(local_time.timetuple()))
            time_string = local_time.strftime("%Y-%m-%d %H:%M:%S")
            date_string = local_time.strftime("%Y%m%d")
            ones = []
            if isinstance(one_hour, list):
                # 24组数据
                ones += one_hour
            elif isinstance(one_hour, dict):
                ones.append(one_hour)

            for one in ones:
                docs.append({
                    "key": key,
                    "timestamp": timestamp,
                    "time": time_string,
                    "data": one,
                    "_index": "ssa-result-{}".format(date_string),
                    "_type": "result"
                })

        return docs

    def make_data(self):
        """make data
        """
        print("==> {}".format(self.today_zero.strftime("%Y-%m-%d")))
        doc_list = []
        for idx, ks in enumerate(self.supported_keys):
            key = ks[0]
            sub_keys = ks[1]
            for sk in sub_keys:
                doc_key = "{}-{}".format(key, sk)
                func_name = "{}__{}".format("_".join(key.split("-")), sk)
                func = getattr(self, func_name, None)
                if func:
                    # print(func_name)
                    # 生成连续24个点的数据
                    data_hour24 = func()
                    # 对上24小时时间
                    if data_hour24:
                        doc_list += self.make_24hour_data(doc_key, data_hour24)
                else:
                    print("No target for key: {}".format(doc_key))
        doc_len = len(doc_list)
        print("total: {}".format(doc_len))
        for idx in range(0, doc_len, 500):
            # print(idx)
            es = Elasticsearch(
                hosts=es_hosts
            )
            helpers.bulk(es, doc_list[idx:min(idx+500, doc_len)])
        print("Done")

    def network__throughput(self):
        """网络流量
        network_in_bytes
        network_out_bytes
        """
        basedata = [
            3, 3, 4, 6, 8, 9, 9, 8, 3, 0, 0, 0, 0, 0, 0, 0, 0, 5, 6, 4, 5, 4, 4, 5,
            5, 4, 6, 5, 0, 0, 0, 0, 6, 7, 6, 6, 7, 8, 9, 8, 9, 4, 5, 4, 5, 6, 5, 6,
            6, 5, 3, 4, 3, 4, 3, 4, 6, 7, 6, 8, 7, 7, 0, 0, 0, 0, 0, 5, 9, 9, 8, 7,
            6, 6, 6, 6, 6, 5, 5, 4, 2, 1, 1, 1, 1, 0, 0, 0, 0, 0, 5, 6, 6, 6, 6, 6,
            6, 7, 8, 8, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 1, 0, 0, 0, 0, 0, 0, 2, 3, 2,
            2, 3, 2, 2, 3, 3, 2, 0, 0, 0, 0, 0, 5, 6, 5, 6, 5, 5, 7, 8, 9, 9, 9, 9,
            8, 2, 1, 0, 0, 0, 0, 1, 1, 2, 1, 2, 2, 2, 1, 4, 5, 6, 6, 6, 6, 5, 5, 4,
            3, 3, 4, 6, 8, 9, 9, 8, 3, 0, 0, 0, 0, 0, 0, 0, 6, 5, 6, 4, 5, 4, 4, 5,
            5, 4, 6, 5, 0, 0, 0, 0, 6, 7, 6, 6, 7, 8, 9, 0, 0, 4, 5, 4, 5, 6, 5, 0,
            0, 0, 3, 4, 3, 4, 3, 4, 6, 7, 6, 8, 7, 7, 0, 0, 0, 0, 0, 5, 9, 9, 8, 7,
            6, 6, 6, 6, 6, 5, 5, 4, 2, 1, 1, 1, 1, 0, 0, 0, 0, 0, 5, 6, 6, 6, 6, 6,
            6, 7, 8, 8, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 1, 0, 0, 0, 0, 0, 0, 2, 3, 2,
            2, 3, 2, 2, 3, 3, 2, 0, 0, 0, 0, 0, 5, 6, 5, 6, 5, 5, 7, 8, 9, 9, 9, 9,
            8, 2, 1, 0, 0, 0, 0, 1, 1, 2, 1, 2, 2, 2, 1, 4, 5, 6, 6, 6, 6, 6, 6, 6,
            7, 8, 8, 8, 7, 6, 5]
        flow_base = {
            "16": 5 * 1 * 1024 * 1024,  # 1M - 8M 0
            "17": 4 * 1 * 1024 * 1024,
            "18": 3 * 1 * 1024 * 1024,
            "19": 2 * 1 * 1024 * 1024,
            "20": 1 * 1 * 1024 * 1024,
            "21": 1 * 1 * 1024 * 1024,
            "22": 2 * 1 * 1024 * 1024,
            "23": 3 * 1 * 1024 * 1024,
            "00": 4 * 1 * 1024 * 1024,
            "01": 5 * 1 * 1024 * 1024,
            "02": 6 * 1 * 1024 * 1024,
            "03": 6 * 1 * 1024 * 1024,
            "04": 5 * 1 * 1024 * 1024,
            "05": 4 * 1 * 1024 * 1024,
            "06": 3 * 1 * 1024 * 1024,
            "07": 3 * 1 * 1024 * 1024,
            "08": 4 * 1 * 1024 * 1024,
            "09": 4 * 1 * 1024 * 1024,
            "10": 5 * 1 * 1024 * 1024,
            "11": 6 * 1 * 1024 * 1024,
            "12": 7 * 1 * 1024 * 1024,
            "13": 8 * 1 * 1024 * 1024,
            "14": 8 * 1 * 1024 * 1024,
            "15": 7 * 1 * 1024 * 1024,
        }
        BW_500M = 500 * 1024 * 1024
        flux_ins = []
        flux_outs = []
        timestamp_zero = int(time.mktime(self.today_zero.timetuple()))
        for t in range(24*60*60*0, 24*60*60*1, 60):
            # 一分钟一条数据
            bd = (basedata[int(t/1800)])
            if bd:
                flux_in = (bd + 5) * BW_500M * 2 * (random.random()+0.5)
            else:
                flux_in = 0
            flux_out = flux_in * \
                random.choice(
                    [0.0003, 0.00033, 0.0004, 0.00045, 0.0005])

            now_time = timezone.localtime(timezone.datetime.fromtimestamp(
                timestamp_zero + t).replace(tzinfo=timezone.get_current_timezone())).strftime("%H")
            # print(now_time)
            flux_out = flux_out + \
                flow_base[now_time] * \
                random.randint(80, 120)/100.0  # 基础业务流量

            flux_ins.append(flux_out)
            flux_outs.append(flux_in)

        self.flux_ins = flux_ins
        self.flux_outs = flux_outs
        datas = [
            {
                "network_in_bytes": int(sum(flux_ins[60*i:60*(i+1)])/3600),
                "network_out_bytes": int(sum(flux_outs[60*i:60*(i+1)])/3600)
            } for i in range(24)
        ]
        return datas

    def network__abnormal_throughput_peak(self):
        """异常网络流量
        network_max_in_bytes
        network_max_out_bytes
        """
        datas = [
            {
                "network_max_in_bytes": int(max(self.flux_ins[60*i:60*(i+1)])),
                "network_max_out_bytes": int(max(self.flux_outs[60*i:60*(i+1)]))
            } for i in range(24)
        ]
        return datas

    def ids__total_count(self):
        """攻击数量
        count
        """
        datas_count = [{
            "count": sum(item["count"] for item in data)
        } for data in self.datas
        ]
        self.datas = None
        self.ids_datas = datas_count
        return datas_count

    def ids__level_count(self):
        """危险等级
        ids_level
        count
        """
        p = [0.02, 0.03, 0.05, 0.1, 0.8]

        datas = [
            [{
                "ids_level": ["严重", "高", "中", "低", "info"][idx],
                "count": int(random.randint(7000, 10000) * p[idx])
            } for idx in range(5)
            ] for i in range(24)
        ]
        self.datas = datas
        self.ids_level_count = datas
        return datas

    def ids__source_count(self):
        """攻击来源
        ids_src_ip
        ids_src_ip_location
        count
        """
        datas = []
        for i in range(24):
            data_list = []
            for ip in self.src_ips:
                data = {
                    "ids_src_ip": ip,
                    "count": random.randint(13, 1000)
                }
                try:
                    location = geoip.find_ip_location(ip)
                    if len(location) == 4:
                        location = location[1]
                except Exception as e:
                    location = "未知"
                data["ids_src_ip_location"] = location
                data_list.append(data)
            datas.append(data_list)
        self.ids_source_count = datas
        return datas

    def firewall__total_count(self):
        """防火墙总数
        count
        """
        datas = [
            {
                "count": random.randint(100, 10000)
            } for i in range(24)
        ]
        self.firewall_datas = datas
        return datas

    def anti_ddos__max_throughput(self):
        """DDoS
        anti_ddos_max_throughput
        """
        datas = [
            {
                "anti_ddos_max_throughput": int(max(self.flux_ins[60*i:60*(i+1)]))
            } for i in range(24)
        ]
        return datas

    def vul__vul_total_count(self):
        """漏洞总数
        vul_total_count 总个数
        vul_host_total_count 主机漏洞个数
        vul_web_total_count 网站漏斗管个数
        vul_severe_total_count 严重级漏洞
        vul_high_total_count 高等级漏洞
        vul_severe_rate 严重比例
        """
        datas = []
        for i in range(24):
            total = random.randint(1000, 10000)
            datas.append(
                {
                    "vul_total_count": total,
                    "vul_web_total_count": int(total*0.45),
                    "vul_host_total_count": int(total*0.45),
                    "vul_severe_total_count": int(total*0.1),
                    "vul_high_total_count": int(total*0.2),
                    "vul_severe_rate": 0.3
                }
            )
        return datas

    def vul__vul_count(self):
        """主机漏洞
        vul_vuln_name
        count
        """
        vuls = [
            "WordPress read-and-understood插件跨站请求伪造漏洞",
            "iJoomla com_adagency插件SQL注入漏洞",
            "WordPress booking-calendar插件跨站请求伪造漏洞",
            "Libav 安全漏洞",
            "AMAX Winmail Server 安全漏洞",
            "SAP Solution Manager 安全漏洞",
            "Google Chrome V8引擎和Digia Qt QtWebEngineCore 安全漏洞",
            "BarCodeWiz Barcode ActiveX control（BarcodeWiz.DLL）缓冲区错误漏洞",
            "Melody SQL注入漏洞",
            "General Motors和Shanghai OnStar iOS Client 安全漏洞",
            "Security Key Lifecycle Manager SQL注入漏洞",
            "Rockwell Automation Allen-Bradley MicroLogix 1400 Controllers Series B和C 缓冲区错误漏洞	",
            "Cobham Sea Tel 安全漏洞",
            "NewsBee CMS SQL注入漏洞",
            "Citrix XenApp和XenDesktop 安全漏洞",
            "Artifex MuPDF 基于堆的缓冲区溢出漏洞",
            "Apache Sentry 不完整的黑名单漏洞",
            "多款I-O DATA DEVICE产品跨站请求伪造漏洞",
            "vBulletin 安全漏洞",
            "Haxx libcurl 释放后重用漏洞",
            "Sophos Mobile Control EAS Proxy 安全漏洞",
            "Red Hat Enterprise Linux 基于栈的缓冲区溢出漏洞",
            "Microsoft Windows ActiveSyncProvider组件信息泄露漏洞",
            "Google Chrome Blink 安全漏洞",
            "多款Symantec和Norton产品整数溢出漏洞",
            "Symantec Endpoint Protection Manager 安全漏洞",
            "phpMyAdmin SQL注入漏洞",
            "phpMyAdmin 安全漏洞",
            "多款NTT Hikari Denwa产品跨站请求伪造漏洞",
            "Pivotal Cloud Foundry Ops Manager vCloud和vSphere 安全漏洞",
            "ImageMagick 整数溢出漏洞",
            "Fortinet FortiWeb 跨站请求伪造漏洞",
            "PHP zip扩展释放后重用漏洞",
            "多款Openstack产品安全漏洞",
            "Red Hat Jgroups 安全漏洞",
            "PHP‘mcrypt_generic’函数整数溢出漏洞",
            "PHP WDDX扩展双重释放漏洞",
            "PHP‘_gd2GetHeader()’函数整数溢出漏洞",
            "PHP mbstring扩展整数溢出漏洞",
            "Apple iOS WebKit Canvas 安全漏洞",
            "Moodle 跨站请求伪造漏洞",
            "VMware Workstation和VMware Player 安全漏洞",
            "Katello SQL注入漏洞",
            "多款Meteocontrol WEB'log产品跨站请求伪造漏洞",
            "Chef Manage 任意代码执行漏洞",
            "IBM TRIRIGA Application Platform 提权漏洞",
            "Symantec Anti-virus Engine 拒绝服务漏洞",
        ]

        datas = [
            [{
                "vul_vuln_name": vul,
                "count": random.randint(10, 200)
            } for vul in random_shuffle(vuls)[:random.randint(5, 30)]] for i in range(24)
        ]
        return datas

    def vul__vul_level_count(self):
        """漏洞等级
        vul_level
        count
        """
        p = [0.02, 0.03, 0.05, 0.1, 0.8]

        datas = [
            [{
                "vul_level": ["严重", "高", "中", "低", "info"][idx],
                "count": int(random.randint(7000, 10000) * p[idx])
            } for idx in range(5)
            ] for i in range(24)
        ]
        self.datas = datas
        return datas

    def vul__vul_threat_type_count(self):
        """攻击类型
        vul_threat_type
        count
        """
        types = [
            # 主机
            "权限许可和访问控制",
            "缓冲区错误",
            "跨站请求伪造",
            "SQL注入",
            "操作系统命令注入",
            "输入验证",
            "缓冲区溢出",
            "代码注入",
            "授权问题",
            "信任管理",
            "信息泄露",
            "数字错误",
            "格式化字符串",
            "路径遍历",
            "加密问题",
            "配置错误",
            "命令注入",
            "跨站脚本",
            "资源管理错误",
            "后置链接",
            "访问控制错误",
            # url
            "代码注入",
            "跨站请求伪造",
            "文件包含",
            "LDAP注入",
            "NoSQL注入",
            "OS命令注入",
            "目录遍历",
            "HTTP应答拆分注入",
            "远程文件包含",
            "固定会话攻击",
            "源代码暴露",
            "SQL注入",
            "未验证的重定向",
            "未验证的DOM重定向",
            "Xpath注入",
            "跨站脚本",
            "XML外部实体注入",
            "后门",
            "备份目录",
            "备份文件",
            "常见管理接口",
            "常见目录",
            "常见文件",
            "目录列表",
            ".htacess LIMIT 错误配置",
            "PUT文件上传",
            "不安全的客户访问策略",
            "不安全的跨域访问策略",
            "localstart.asp页面暴露",
            "限制绕道源欺骗",
            "跨站跟踪攻击",
            "Web分布式创作和版本管理",
            "允许的HTTP方法",
        ]
        datas = [
            [{
                "vul_threat_type": t,
                "count": random.randint(10, 1000)
            } for t in random_shuffle(types)[:random.randint(5, len(types))]] for i in range(24)
        ]
        return datas

    def vul__vul_risk_url_count(self):
        """风险URL
        vul_risk_url
        vul_threat_type
        count
        """
        urls = ["/login"] + \
            ["/home/study/{}.html".format(i) for i in range(510, 600)] + \
            ["/profile/settings/{}.html".format(i) for i in range(45646, 45746)] + \
            ["/working/{}.html".format(i) for i in range(444533, 444633)] + \
            ["/asset/{}.html".format(i) for i in range(444533, 444633)]

        types = [
            "代码注入",
            "跨站请求伪造",
            "文件包含",
            "LDAP注入",
            "NoSQL注入",
            "OS命令注入",
            "目录遍历",
            "HTTP应答拆分注入",
            "远程文件包含",
            "固定会话攻击",
            "源代码暴露",
            "SQL注入",
            "未验证的重定向",
            "未验证的DOM重定向",
            "Xpath注入",
            "跨站脚本",
            "XML外部实体注入",
            "后门",
            "备份目录",
            "备份文件",
            "常见管理接口",
            "常见目录",
            "常见文件",
            "目录列表",
            ".htacess LIMIT 错误配置",
            "PUT文件上传",
            "不安全的客户访问策略",
            "不安全的跨域访问策略",
            "localstart.asp页面暴露",
            "限制绕道源欺骗",
            "跨站跟踪攻击",
            "Web分布式创作和版本管理",
            "允许的HTTP方法",
        ]
        datas = [
            [{
                "vul_risk_url": url,
                "vul_threat_type": random.choice(types),
                "count": random.randint(1, 40)
            } for url in random_shuffle(urls)[:random.randint(20, 200)]] for i in range(24)
        ]
        return datas

    def vul__vul_ip_count(self):
        """风险资产
        vul_ip
        count
        """
        types = [
            # 主机
            "权限许可和访问控制",
            "缓冲区错误",
            "跨站请求伪造",
            "SQL注入",
            "操作系统命令注入",
            "输入验证",
            "缓冲区溢出",
            "代码注入",
            "授权问题",
            "信任管理",
            "信息泄露",
            "数字错误",
            "格式化字符串",
            "路径遍历",
            "加密问题",
            "配置错误",
            "命令注入",
            "跨站脚本",
            "资源管理错误",
            "后置链接",
            "访问控制错误",
        ]
        datas = [
            [{
                "vul_ip": host,
                "count": random.randint(1, 500)
            } for host in self.hosts
            ] for i in range(24)
        ]
        return datas

    def vul__vul_top(self):
        """严重漏洞
        vul_vuln_name
        vul_ip
        count
        vul_level
        """

        tops = [
            "多款NTT Hikari Denwa产品跨站请求伪造漏洞",
            "Pivotal Cloud Foundry Ops Manager vCloud和vSphere 安全漏洞",
            "ImageMagick 整数溢出漏洞",
            "Fortinet FortiWeb 跨站请求伪造漏洞",
            "PHP zip扩展释放后重用漏洞",
            "多款Openstack产品安全漏洞",
            "Red Hat Jgroups 安全漏洞",
            "PHP‘mcrypt_generic’函数整数溢出漏洞",
            "PHP WDDX扩展双重释放漏洞",
            "PHP‘_gd2GetHeader()’函数整数溢出漏洞",
            "PHP mbstring扩展整数溢出漏洞",
            "Apple iOS WebKit Canvas 安全漏洞",
            "Moodle 跨站请求伪造漏洞",
            "VMware Workstation和VMware Player 安全漏洞",
            "Katello SQL注入漏洞",
            "多款Meteocontrol WEB'log产品跨站请求伪造漏洞",
            "Chef Manage 任意代码执行漏洞",
            "IBM TRIRIGA Application Platform 提权漏洞",
            "Symantec Anti-virus Engine 拒绝服务漏洞",
        ]
        datas = []
        for i in range(24):
            ds = []
            for host in random_shuffle(self.hosts)[:int(len(self.hosts)/2)]:
                for top in random_shuffle(tops)[:random.randint(1, int(len(tops)/2))]:
                    ds.append({
                        "vul_vuln_name": top,
                        "vul_ip": host,
                        "count": random.randint(1, 20),
                        "vul_level": "严重"
                    })
            datas.append(ds)
        self.vul_top = datas
        return datas

    def virus__total_count(self):
        """病毒总数
        count
        """
        datas = [
            {
                "count": random.randint(10, 1000),
            } for i in range(24)
        ]
        self.datas = datas
        return datas

    def virus__btw_count(self):
        """僵木蠕统计
        virus_total_count
        virus_btw_count
        """
        datas = [
            {
                "virus_btw_count": int(self.datas[i]["count"]*random.randint(35, 78)/100.0),
                "virus_total_count": self.datas[i]["count"],
            } for i in range(24)
        ]
        self.datas = datas
        return datas

    def virus__btw_cleared(self):
        """僵木蠕查杀率
        """
        datas = []
        for i in range(24):
            rate = random.randint(1, 100) / 100.0
            cleared = int(self.datas[i]["virus_btw_count"] * rate)

            datas.append(
                {
                    "virus_btw_cleared_1": cleared,
                    "virus_btw_cleared_0": self.datas[i]["virus_btw_count"] - cleared,
                }
            )
        self.datas = None
        return datas

    def virus__asset_top(self):
        """蠕虫感染资产数量
        virus_btw_count
        virus_host_ip
        virus_total_count
        """
        datas = []
        for i in range(24):
            ds = []
            for host in random_shuffle(self.hosts)[:random.randint(5, len(self.hosts)-3)]:
                r = random.randint(1, 10)
                ds.append({
                    "virus_btw_count": r,
                    "virus_host_ip": host,
                    "virus_total_count": int(r*100.0/random.randint(35, 78))
                })
            datas.append(ds)
        self.datas = datas
        return datas

    def virus__btw_asset_top(self):
        """严重蠕虫
        """
        # https://share.anva.org.cn/web/publicity/listMalware?type=malware
        virus = [
            "Worm/Win32.Debris.h",
            "Trojan/Win32.Kovter.nup",
            "Worm[P2P]/Win32.Picsys.c",
            "Worm[Net]/Win32.Allaple.b",
            "Worm[Net]/Win32.Allaple.e",
            "Worm/Win32.Vobfus.aiqu",
            "Worm[Net]/Win32.Allaple.b",
            "Trojan/Win32.Kovter.nup",
            "Trojan/Win32.Bublik.cred",
            "Trojan[Backdoor]/Win32.Zegost.mtbdv",
            "Trojan[Backdoor]/Win32.Farfli.alem",
            "Trojan/Win32.Swisyn.bner",
            "Trojan[Downloader]/JS.Cryptoload.abv",
            "Trojan[Backdoor]/Win32.Poison.fnqe",
            "GrayWare[AdWare]/Win32.DealPly.gen",
            "Trojan/Win32.Pakes.wtk",
            "Worm/Win32.Wenper.b",
        ]
        datas = []
        for i in range(24):
            ds = []
            for h in self.datas[i]:
                for v in random_shuffle(virus)[:len(virus)]:
                    ds.append({
                        "virus_btw_count": h["virus_btw_count"],
                        "virus_host_ip": h["virus_host_ip"],
                        "virus_total_count": h["virus_total_count"],
                        "virus_virusname": v
                    })
            datas.append(ds)
        return datas

    def db_audit__total_count(self):
        """数据库审计
        count
        """
        datas = [
            {
                "count": random.randint(10, 1000),
            } for i in range(24)
        ]
        self.db_audit_datas = datas
        return datas

    def web_log__uv(self):
        """UV
        count
        web_log_ip
        """
        def _gen_ips(num=1):
            ips = []
            if len(self.src_ips) >= num:
                return self.src_ips[:num]

            for i in range(num-len(self.src_ips)):
                ip = ".".join([str(s) for s in [
                    random.randint(1, 244), random.randint(1, 244),
                    random.randint(1, 244), random.randint(1, 244)]])
                ips.append(ip)
            return self.src_ips + ips
        datas = [
            [{
                "web_log_ip": ip,
                "count": random.randint(1, 40),
            } for ip in _gen_ips(random.randint(20, 300))
            ] for i in range(24)
        ]
        self.datas = datas
        return datas

    def web_log__http_status_count(self):
        """HTTP状态
        web_log_host
        web_log_http_status_total_count
        web_log_http_status_count
            - web_log_http_status
            - count
        """
        status = {
            200: 0.73,
            201: 0.01,
            301: 0.13,
            400: 0.01,
            401: 0.01,
            404: 0.02,
            500: 0.02,
            501: 0.04,
            502: 0.01,
            503: 0.02,
        }

        datas = []
        for i in range(24):
            for ip in self.dst_ips:
                data = {
                    "web_log_http_status_count": [
                        {
                            "count": int(random.randint(1500, 2000)*rate),
                            "web_log_http_status": s
                        } for s, rate in status.items()
                    ],
                    "web_log_host": ip
                }
                data["web_log_http_status_total_count"] = sum(
                    d["count"] for d in data["web_log_http_status_count"])
            datas.append(data)
        return datas

    def web_log__location_count(self):
        """位置
        web_log_location
        count
        """
        location_count = []
        for data in self.datas:
            ls = {}
            for d in data:
                try:
                    location = geoip.find_ip_location(d["web_log_ip"])
                    if len(location) == 4:
                        location = location[1]
                except Exception as e:
                    location = "unknown"
                location_hash = md5(str(location.encode("utf8"))).hexdigest()
                if location_hash in ls:
                    ls[location_hash][1] += d["count"]
                else:
                    ls[location_hash] = [location, 1]
            lc = [{
                "count": c[1],
                "web_log_location": c[0]
            } for l, c in ls.items()]
            location_count.append(lc)
        return location_count

    def web_log__browser_count(self):
        """浏览器
        web_log_browser
        count
        """
        browsers = {
            "Seamonkey": 0.01,
            "Firefox": 0.1,
            "Chromium": 0.1,
            "Chrome": 0.4,
            "Opera": 0.02,
            "Opera": 0.03,
            "Internet Explorer": 0.3,
            "Edge": 0.01,
            "Safari": 0.03,
        }
        datas = [
            [{
                "count": int(random.randint(1000, 15000) * rate),
                "web_log_browser": browser
            } for browser, rate in browsers.items()
            ] for i in range(24)
        ]
        return datas

    def web_log__ip_count(self):
        """IP及地址
        web_log_ip
        web_log_location
        count
        """
        location_count = []
        for data in self.datas:
            ls = {}
            for d in data:
                try:
                    location = geoip.find_ip_location(d["web_log_ip"])
                    if len(location) == 4:
                        location = location[1]
                except Exception as e:
                    location = "未知"
                if d["web_log_ip"] in ls:
                    ls[d["web_log_ip"]][1] += d["count"]
                else:
                    ls[d["web_log_ip"]] = [location, d["count"]]
            lc = [{
                "count": c[1],
                "web_log_ip": k,
                "web_log_location": c[0]
            } for k, c in ls.items()]
            location_count.append(lc)
        self.datas = None
        return location_count

    def web_log__pv(self):
        """访问
        web_log_url
        count
        """

        htmls = ["/login"] + \
            ["/home/{}.html".format(i) for i in range(10, 100)] + \
            ["/profile/{}.html".format(i) for i in range(4566, 4766)] + \
            ["/work/{}.html".format(i) for i in range(4444533, 4444633)]
        datas = [
            [{
                "count": random.randint(1, 100),
                "web_log_url": html
            } for html in htmls
            ] for i in range(24)
        ]
        return datas

    def web_log__os_count(self):
        """操作系统
        web_log_os
        count
        """
        oses = {
            "Windows": 0.75,
            "Mac OS X": 0.1,
            "Linux": 0.1,
            "Unknown": 0.05
        }
        datas = [
            [{
                "count": int(random.randint(1000, 15000) * rate),
                "web_log_os": os
            } for os, rate in oses.items()
            ] for i in range(24)
        ]
        return datas

    def security__total_count(self):
        """总数
        security_total_count
        security_waf_count
        security_db_audit_count
        security_firewall_count
        security_ids_count
        """
        datas = [
            {
                "security_waf_count": self.waf_datas[i]["count"],
                "security_db_audit_count": self.db_audit_datas[i]["count"],
                "security_total_count": sum([
                    self.waf_datas[i]["count"],
                    self.db_audit_datas[i]["count"],
                    self.firewall_datas[i]["count"],
                    self.ids_datas[i]["count"]
                ]),
                "security_firewall_count": self.firewall_datas[i]["count"],
                "security_ids_count": self.ids_datas[i]["count"]
            } for i in range(24)
        ]
        return datas

    def security__source_count(self):
        """来源
        security_src_ip
        security_src_ip_location
        count
        """
        datas = []
        for d in self.ids_source_count:
            ds = [{
                "count": int(k["count"] * random.randint(100, 120)/100.0),
                "security_src_ip_location": k["ids_src_ip_location"],
                "security_src_ip": k["ids_src_ip"]} for k in d
            ]
            datas.append(ds)

        return datas

    def security__level_count(self):
        """危险等级
        security_level
        count
        """
        datas = []
        for d in self.ids_level_count:
            ds = [{
                "count": int(k["count"] * random.randint(130, 160)/100.0),
                "security_level": k["ids_level"]} for k in d
            ]
            datas.append(ds)

        return datas

    def security__dst_ip_count(self):
        """目标IP
        security_dst_ip
        security_dst_ip_location
        count
        """
        datas = []
        for idx in range(24):
            ds = []
            # vul_top
            for vul in self.vul_top[idx]:
                # src_ip = random.choice(self.src_ips)
                ds.append({
                    "count": random.randint(10, 1000),
                    "security_dts_ip_location": fil(vul["vul_ip"]),
                    "security_dst_ip": vul["vul_ip"],
                })
            datas.append(ds)
        return datas

    def security__events(self):
        """严重事件
        security_time
        security_src_ip
        security_dst_ip
        security_dst_ip_location
        security_level
        """
        datas = []
        for idx in range(24):
            local_time = self.today_zero + timezone.timedelta(hours=idx)
            timestamp = int(time.mktime(local_time.timetuple()))
            ds = []
            # vul_top
            for vul in self.vul_top[idx]:
                src_ip = random.choice(self.src_ips)
                ds.append({
                    "security_src_ip": src_ip,
                    "security_src_ip_location": fil(src_ip),
                    "security_time": timezone.localtime(timezone.datetime.fromtimestamp(random.randint(timestamp, timestamp+3599)).replace(tzinfo=timezone.get_current_timezone())).strftime("%Y-%m-%d %H:%M:%S"),
                    "security_dst_ip_location": fil(vul["vul_ip"]),
                    "security_dst_ip": vul["vul_ip"],
                    "security_level": "严重"
                })
            # TODO: 添加其他攻击事件

            datas.append(ds)
        return datas

    def waf__total_count(self):
        """waf攻击
        count
        """
        # 依赖 waf__attack_type_count
        datas_count = [{
            "count": sum(item["count"] for item in data)
        } for data in self.datas
        ]
        self.datas = None
        self.waf_datas = datas_count
        return datas_count

    def waf__attack_type_count(self):
        """WAF攻击类型
        waf_attack_type
        count
        """
        attack_types = [
            "代码注入",
            "跨站请求伪造",
            "文件包含漏洞",
            "OS命令注入",
            "目录遍历漏洞",
            "远程文件包含漏洞",
            "固定会话攻击",
            "源代码暴露",
            "SQL注入漏洞",
            "未验证的重定向漏洞",
            "未验证的DOM重定向漏洞",
            "Xpath注入",
            "跨站脚本攻击",
            "DOM跨站脚本攻击",
            "脚本上下文中的DOM跨站脚本攻击",
            "HTML元素的事件属性中的跨站脚本攻击",
            "路径中的跨站脚本攻击",
            "脚本上下文中的跨站脚本攻击",
            "HTML标签中的跨站脚本攻击",
            "XML外部实体注入",
            "存在后门",
            "存在备份目录",
            "存在备份文件",
            "常见管理接口",
            "常见目录",
            "常见敏感文件",
            "目录列表暴露",
            ".htacess文件LIMIT指令的错误配置",
            "PUT文件上传",
            "不安全的客户访问策略",
            "不安全的跨域访问策略(allow-access-from)",
            "localstart.asp页面暴露",
            "访问限制旁路源欺骗",
            "HTTP TRACE跨站攻击",
            "Web分布式创作和版本管理",
            "允许的HTTP方法",
        ]

        datas = [
            [
                {
                    "count": random.randint(1, 10),
                    "waf_attack_type": attack_types[idx]
                } for idx in range(random.randint(1, 20))
            ] for i in range(24)
        ]
        self.datas = datas
        return datas

    def weak_password__host_count(self):
        """弱口令主机数量
        count
        weak_password_ip
        weak_password_protocol
        weak_password_end_time
        """
        protocols = [
            "FTP",
            "SSH",
            "MSSQL",
            "MYSQL",
            "PostGreSQL",
            "REDIS",
            "EiasticSearch",
            "MONGODB",
        ]
        datas = []
        for idx in range(24):
            local_time = self.today_zero + timezone.timedelta(hours=idx)
            timestamp = int(time.mktime(local_time.timetuple()))
            datas.append(
                [{
                    "count": random.randint(0, 13),
                    "weak_password_protocol": key,
                    "weak_password_ip": self.hosts[random.randint(0, len(self.hosts)-1)],
                    "weak_password_end_time": random.randint(timestamp, timestamp+3599)
                } for key in protocols]
            )
        return datas
