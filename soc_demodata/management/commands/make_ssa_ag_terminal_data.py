# -*- coding:utf-8 -*-
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
dst_ips = ['250.52.233.8', '230.188.33.94', '87.6.55.243', '161.52.23.152', '95.16.80.30', '46.178.15.155',
           '171.150.92.188', '107.58.102.71', '171.230.5.6', '136.164.56.196', '177.162.18.235', '202.251.94.55',
           '147.5.45.0', '224.13.212.84', '145.165.15.54', '68.198.99.56', '75.39.207.95', '111.220.214.239',
           '52.203.149.50', '26.161.244.24', '42.217.34.8', '240.159.155.188', '243.21.228.104', '231.248.12.252',
           '67.204.139.139', '35.112.134.192', '221.16.88.254', '102.51.108.64', '59.245.233.15', '224.236.224.197',
           '135.117.250.27', '28.17.9.231', '93.137.162.86', '224.177.220.254', '4.236.149.152', '21.51.121.198',
           '165.65.5.109', '198.232.126.0', '225.171.2.16', '215.66.188.241', '180.247.79.128', '188.131.254.189',
           '64.14.178.18', '143.3.29.62', '255.163.124.197', '148.38.252.91', '122.34.187.112', '247.12.177.79',
           '66.93.182.199', '135.74.16.40']
three_type = ['系统共享未关闭', '系统未禁用guest用户', '未安装终端安全管理系统', '未安装网盾桌面安全套件', '未安装杀毒软件', '明文存储', '非工作时段操作',
              'USB存储设备使用', '手机充电记录', '终端安全管理系统卸载记录', '程序试图运行']


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

    #
    #
    # def ssa_ag_zd_data_func(self, index_name, date_time):
    #     '''
    #     终端日志
    #     '''
    #     return {
    #         "_index": index_name,
    #         "_type": 'logs',
    #         "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
    #         "agent_id": str(uuid.uuid4()),
    #         "log_type": random.randint(1, 7),
    #         "act_ip": random.choice(self.ips),
    #         "act_time": date_time.strftime('%Y%m%d%H%M%S'),
    #         "act_type": random.randint(0, 7),
    #         "app_path": "app_path",
    #         "app_name": "app_name",
    #         "login_ip": random.choice(self.ips),
    #         "login_name": random.choice(
    #             ['古志用', '王盼芙', '夏景山', "员慧巧", "王寄云", "务冰凡", "军飞白", "力云泽", "王莹玉", "董水之", "王梓美", "王代巧"]),
    #         "os_username": random.choice(
    #             ['admin', 'user', 'agent', "go", 'test', 'qqq', 'superuser', 'superadmin', 'super123', 'aaa']),
    #         "login_type": random.randint(1, 7),
    #         "login_result": random.randint(0, 1),
    #         "ie_name": random.choice(
    #             ['http://192.168.0.1:808/wss', 'http://192.168.2.11:8080/index', 'http://192.168.3.1/home',
    #              'http://192.168.0.1/wss', 'http://192.168.12.1:8088/wssa']),
    #         "file_name": random.choice(
    #             ['E:/技术资料/信息安全/PKI/PKI体系.doc', 'E:/人员资料/办公室人员.doc', 'D:/系统资料/人口体系说明.doc', 'E:/技术资料/程序配置/config.xml',
    #              'E:/项目/OA/test.py', 'E:/项目/PKI/说明.doc']),
    #         "user_ip": random.choice(self.ips),
    #         "request_type": random.randint(1, 10),
    #         "request_name": random.choice(
    #             ['打印文件', '打印图片', '刻录系统镜像', "刻录文件", "连接蓝牙aaa", "红外操作", "手机充电", "移动盘拷贝文件", "移动盘拷贝系统", "刻录系统资料"]),
    #         "request_time": date_time.strftime('%Y%m%d%H%M%S'),
    #         "approver_name": random.choice(
    #             ['刘琼芳', '王盼芙', '李余妍', "李星汉", "刘青旋", "务冰凡", "张欣怿", "张白玉", "王莹玉", "李力勤", "张向露", "王代巧"]),
    #         "approve_time": date_time.strftime('%Y%m%d%H%M%S'),
    #         "dev_name": random.choice(
    #             ['HP LASERJET PROFESSIONAL P1606DN', 'FX XPS', 'SanDisk', "WD", "TOSHIBA", "Lenovo", "ASUS", "PHILIPS",
    #              "DACOM K6P"]),
    #         "print_doc": random.choice(
    #             ['公司人员结构分析.doc', '单位工作人员个人简历表.doc', '人员名单.doc', "年度人员需求预测报告.doc", "员工类型分析与管理.doc", "RFID技术说明.doc",
    #              "资质.JPG", "工资单.doc", "CARD.JPG"]),
    #         "file_path": random.choice(
    #             ['C:/Windows/system32', 'H:/', 'H:/elk部署', "H:/360Downloads", "E:/技术资料/程序配置", "D:/系统资料/", "E:/项目/PKI/",
    #              "E:/人员资料/", "J:/logs"]),
    #         "act_info": random.choice(
    #             ['J:/printelselist.xml', 'H:/webservice.log', 'H:/elk部署/manage.py', "H:/360Downloads/说明.doc",
    #              "E:/技术资料/程序配置/RFID技术说明.doc", "D:/系统资料/RFID技术说明.doc", "E:/人员资料/工资单.doc", "E:/人员资料/", "J:/人员名单.doc"]),
    #         "term_ip": random.choice(self.ips),
    #         "term_computer_name": random.choice(
    #             ['WORKGROUP', 'LIUZZ-2', 'MACBOOK-PRO', "USER-20170916HL", "FX-CE787E", "QQQ-PC", "PC-LIUJINGJING",
    #              "MACBOOKPRO-65B8", "MACBOOKPRO-A883"]),
    #         "term_duty": random.choice(
    #             ['许欣艳', '金问薇', '李余妍', "李星汉", "孔秀筠", "孔寻春", "熊叶嘉", "金弘致", "王莹玉", "成博远", "孔秀慧", "金长莹"]),
    #         "term_group_id": random.choice(['001', '002', 'xzbgs', "jsbgs", "xzbgs", "zcbgs", "005"]),
    #         "term_group_name": random.choice(['研发办公室', '财务办公室', '行政办公室', "技术办公室", "刑侦办公室", "驻场办公室", "人事办公室"]),
    #     }

    def ssa_ag_zd_cx_data_func(self, index_name, date_time):
        """
        终端程序日志
        :param index_name:
        :param date_time:
        :return:
        """
        return {
            "_index": index_name,
            "_type": 'logs',
            "log_type": "程序日志",
            "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "agent_id": str(uuid.uuid4()),
            "term_ip": random.choice(self.ips),
            "term_computer_name": random.choice(
                ['WORKGROUP', 'LIUZZ-2', 'MACBOOK-PRO', "USER-20170916HL", "FX-CE787E", "QQQ-PC", "PC-LIUJINGJING",
                 "MACBOOKPRO-65B8", "MACBOOKPRO-A883"]),
            "term_duty": random.choice(
                ['许欣艳', '金问薇', '李余妍', "李星汉", "孔秀筠", "孔寻春", "熊叶嘉", "金弘致", "王莹玉", "成博远", "孔秀慧", "金长莹"]),
            "term_group_id": random.choice(['001', '002', 'xzbgs', "jsbgs", "xzbgs", "zcbgs", "005"]),
            "term_group_name": random.choice(['研发办公室', '财务办公室', '行政办公室', "技术办公室", "刑侦办公室", "驻场办公室", "人事办公室"]),
            "act_ip": random.choice(self.ips),
            "act_time": date_time.strftime('%Y%m%d%H%M%S'),
            "act_type": random.choice([2, 3, 5]),
            "app_path": "app_path",
            "app_name": "app_name",
            "log_id": random.randint(1, 1000),
        }

    def ssa_ag_zd_dl_data_func(self, index_name, date_time):
        """
        终端登录日志
        :param index_name:
        :param date_time:
        :return:
        """
        return {
            "_index": index_name,
            "_type": 'logs',
            "log_type": "登录日志",
            "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "agent_id": str(uuid.uuid4()),
            "term_ip": random.choice(self.ips),
            "term_computer_name": random.choice(
                ['WORKGROUP', 'LIUZZ-2', 'MACBOOK-PRO', "USER-20170916HL", "FX-CE787E", "QQQ-PC", "PC-LIUJINGJING",
                 "MACBOOKPRO-65B8", "MACBOOKPRO-A883"]),
            "term_duty": random.choice(
                ['许欣艳', '金问薇', '李余妍', "李星汉", "孔秀筠", "孔寻春", "熊叶嘉", "金弘致", "王莹玉", "成博远", "孔秀慧", "金长莹"]),
            "term_group_id": random.choice(['001', '002', 'xzbgs', "jsbgs", "xzbgs", "zcbgs", "005"]),
            "term_group_name": random.choice(['研发办公室', '财务办公室', '行政办公室', "技术办公室", "刑侦办公室", "驻场办公室", "人事办公室"]),
            "login_ip": random.choice(self.ips),
            "login_name": random.choice(
                ['古志用', '王盼芙', '夏景山', "员慧巧", "王寄云", "务冰凡", "军飞白", "力云泽", "王莹玉", "董水之", "王梓美", "王代巧"]),
            "os_username": random.choice(
                ['admin', 'user', 'agent', "go", 'test', 'qqq', 'superuser', 'superadmin', 'super123', 'aaa']),
            "login_type": random.randint(1, 7),
            "login_result": random.randint(0, 1),
            "act_time": date_time.strftime('%Y%m%d%H%M%S'),
            "log_id": random.randint(1, 1000),
        }

    def ssa_ag_zd_ll_data_func(self, index_name, date_time):
        """
        终端浏览网页日志
        :param index_name:
        :param date_time:
        :return:
        """
        return {
            "_index": index_name,
            "_type": 'logs',
            "log_type": "浏览网页",
            "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "agent_id": str(uuid.uuid4()),
            "term_ip": random.choice(self.ips),
            "term_computer_name": random.choice(
                ['WORKGROUP', 'LIUZZ-2', 'MACBOOK-PRO', "USER-20170916HL", "FX-CE787E", "QQQ-PC", "PC-LIUJINGJING",
                 "MACBOOKPRO-65B8", "MACBOOKPRO-A883"]),
            "term_duty": random.choice(
                ['许欣艳', '金问薇', '李余妍', "李星汉", "孔秀筠", "孔寻春", "熊叶嘉", "金弘致", "王莹玉", "成博远", "孔秀慧", "金长莹"]),
            "term_group_id": random.choice(['001', '002', 'xzbgs', "jsbgs", "xzbgs", "zcbgs", "005"]),
            "term_group_name": random.choice(['研发办公室', '财务办公室', '行政办公室', "技术办公室", "刑侦办公室", "驻场办公室", "人事办公室"]),
            "ie_name": random.choice(
                ['http://192.168.0.1:808/wss', 'http://192.168.2.11:8080/index', 'http://192.168.3.1/home',
                 'http://192.168.0.1/wss', 'http://192.168.12.1:8088/wssa']),
            "act_time": date_time.strftime('%Y%m%d%H%M%S'),
            "log_id": random.randint(1, 1000),
            "act_ip": random.choice(self.ips),
        }

    def ssa_ag_zd_ls_data_func(self, index_name, date_time):
        """
        终端历史文件浏览日志
        :param index_name:
        :param date_time:
        :return:
        """
        return {
            "_index": index_name,
            "_type": 'logs',
            "log_type": "历史文件浏览",
            "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "agent_id": str(uuid.uuid4()),
            "term_ip": random.choice(self.ips),
            "term_computer_name": random.choice(
                ['WORKGROUP', 'LIUZZ-2', 'MACBOOK-PRO', "USER-20170916HL", "FX-CE787E", "QQQ-PC", "PC-LIUJINGJING",
                 "MACBOOKPRO-65B8", "MACBOOKPRO-A883"]),
            "term_duty": random.choice(
                ['许欣艳', '金问薇', '李余妍', "李星汉", "孔秀筠", "孔寻春", "熊叶嘉", "金弘致", "王莹玉", "成博远", "孔秀慧", "金长莹"]),
            "term_group_id": random.choice(['001', '002', 'xzbgs', "jsbgs", "xzbgs", "zcbgs", "005"]),
            "term_group_name": random.choice(['研发办公室', '财务办公室', '行政办公室', "技术办公室", "刑侦办公室", "驻场办公室", "人事办公室"]),
            "file_name": random.choice(
                ['E:/技术资料/信息安全/PKI/PKI体系.doc', 'E:/人员资料/办公室人员.doc', 'D:/系统资料/人口体系说明.doc', 'E:/技术资料/程序配置/config.xml',
                 'E:/项目/OA/test.py', 'E:/项目/PKI/说明.doc']),
            "act_time": date_time.strftime('%Y%m%d%H%M%S'),
            "log_id": random.randint(1, 1000),
            "act_ip": random.choice(self.ips),
        }

    def ssa_ag_zd_sp_data_func(self, index_name, date_time):
        """
        终端设备审批日志
        :param index_name:
        :param date_time:
        :return:
        """
        return {
            "_index": index_name,
            "_type": 'logs',
            "log_type": "设备审批",
            "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "agent_id": str(uuid.uuid4()),
            "term_ip": random.choice(self.ips),
            "term_computer_name": random.choice(
                ['WORKGROUP', 'LIUZZ-2', 'MACBOOK-PRO', "USER-20170916HL", "FX-CE787E", "QQQ-PC", "PC-LIUJINGJING",
                 "MACBOOKPRO-65B8", "MACBOOKPRO-A883"]),
            "term_duty": random.choice(
                ['许欣艳', '金问薇', '李余妍', "李星汉", "孔秀筠", "孔寻春", "熊叶嘉", "金弘致", "王莹玉", "成博远", "孔秀慧", "金长莹"]),
            "term_group_id": random.choice(['001', '002', 'xzbgs', "jsbgs", "xzbgs", "zcbgs", "005"]),
            "term_group_name": random.choice(['研发办公室', '财务办公室', '行政办公室', "技术办公室", "刑侦办公室", "驻场办公室", "人事办公室"]),
            "user_ip": random.choice(self.ips),
            "request_type": random.randint(1, 10),
            "request_name": random.choice(
                ['打印文件', '打印图片', '刻录系统镜像', "刻录文件", "连接蓝牙aaa", "红外操作", "手机充电", "移动盘拷贝文件", "移动盘拷贝系统", "刻录系统资料"]),
            "act_type": random.randint(0, 7),
            "request_time": date_time.strftime('%Y%m%d%H%M%S'),
            "approver_name": random.choice(
                ['刘琼芳', '王盼芙', '李余妍', "李星汉", "刘青旋", "务冰凡", "张欣怿", "张白玉", "王莹玉", "李力勤", "张向露", "王代巧"]),
            "approve_time": date_time.strftime('%Y%m%d%H%M%S'),
            "dev_name": random.choice(
                ['HP LASERJET PROFESSIONAL P1606DN', 'FX XPS', 'SanDisk', "WD", "TOSHIBA", "Lenovo", "ASUS", "PHILIPS",
                 "DACOM K6P"]),
            "print_doc": random.choice(
                ['公司人员结构分析.doc', '单位工作人员个人简历表.doc', '人员名单.doc', "年度人员需求预测报告.doc", "员工类型分析与管理.doc", "RFID技术说明.doc",
                 "资质.JPG",
                 "工资单.doc", "CARD.JPG"]),
        }

    def ssa_ag_zd_kl_data_func(self, index_name, date_time):
        """
        终端终端刻录日志
        :param index_name:
        :param date_time:
        :return:
        """
        return {
            "_index": index_name,
            "_type": 'logs',
            "log_type": "刻录文件",
            "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "agent_id": str(uuid.uuid4()),
            "term_ip": random.choice(self.ips),
            "term_computer_name": random.choice(
                ['WORKGROUP', 'LIUZZ-2', 'MACBOOK-PRO', "USER-20170916HL", "FX-CE787E", "QQQ-PC", "PC-LIUJINGJING",
                 "MACBOOKPRO-65B8", "MACBOOKPRO-A883"]),
            "term_duty": random.choice(
                ['许欣艳', '金问薇', '李余妍', "李星汉", "孔秀筠", "孔寻春", "熊叶嘉", "金弘致", "王莹玉", "成博远", "孔秀慧", "金长莹"]),
            "term_group_id": random.choice(['001', '002', 'xzbgs', "jsbgs", "xzbgs", "zcbgs", "005"]),
            "term_group_name": random.choice(['研发办公室', '财务办公室', '行政办公室', "技术办公室", "刑侦办公室", "驻场办公室", "人事办公室"]),
            "act_time": date_time.strftime('%Y%m%d%H%M%S'),
            "file_path": random.choice(
                ['C:/Windows/system32', 'H:/', 'H:/elk部署', "H:/360Downloads", "E:/技术资料/程序配置", "D:/系统资料/", "E:/项目/PKI/",
                 "E:/人员资料/", "J:/logs"]),
            "file_name": random.choice(
                ['E:/技术资料/信息安全/PKI/PKI体系.doc', 'E:/人员资料/办公室人员.doc', 'D:/系统资料/人口体系说明.doc', 'E:/技术资料/程序配置/config.xml',
                 'E:/项目/OA/test.py', 'E:/项目/PKI/说明.doc']),
            "log_id": random.randint(1, 1000),
            "act_ip": random.choice(self.ips),
        }

    def ssa_ag_zd_uc_data_func(self, index_name, date_time):
        """
        终端移动盘拷文件日志
        :param index_name:
        :param date_time:
        :return:
        """
        return {
            "_index": index_name,
            "_type": 'logs',
            "log_type": "移动盘拷贝",
            "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "agent_id": str(uuid.uuid4()),
            "term_ip": random.choice(self.ips),
            "term_computer_name": random.choice(
                ['WORKGROUP', 'LIUZZ-2', 'MACBOOK-PRO', "USER-20170916HL", "FX-CE787E", "QQQ-PC", "PC-LIUJINGJING",
                 "MACBOOKPRO-65B8", "MACBOOKPRO-A883"]),
            "term_duty": random.choice(
                ['许欣艳', '金问薇', '李余妍', "李星汉", "孔秀筠", "孔寻春", "熊叶嘉", "金弘致", "王莹玉", "成博远", "孔秀慧", "金长莹"]),
            "term_group_id": random.choice(['001', '002', 'xzbgs', "jsbgs", "xzbgs", "zcbgs", "005"]),
            "term_group_name": random.choice(['研发办公室', '财务办公室', '行政办公室', "技术办公室", "刑侦办公室", "驻场办公室", "人事办公室"]),
            "act_time": date_time.strftime('%Y%m%d%H%M%S'),
            "act_type": random.randint(4, 6),
            "act_info": random.choice(
                ['J:/printelselist.xml', 'H:/webservice.log', 'H:/elk部署/manage.py', "H:/360Downloads/说明.doc",
                 "E:/技术资料/程序配置/RFID技术说明.doc", "D:/系统资料/RFID技术说明.doc", "E:/人员资料/工资单.doc", "E:/人员资料/", "J:/人员名单.doc"]),
            "log_id": random.randint(1, 1000),
            "act_ip": random.choice(self.ips),
        }

    def ssa_ag_zt_basic_data_func(self, index_name, date_time):
        '''
        终端基本信息表
        '''
        return {
            "_index": index_name,
            "_type": 'logs',
            "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),

            "agent_id": str(uuid.uuid4()),
            "log_type": "终端基本信息",
            "term_ip": random.choice(self.ips),
            "term_computer_name": random.choice(
                ['WORKGROUP', 'LIUZZ-2', 'MACBOOK-PRO', "USER-20170916HL", "FX-CE787E", "QQQ-PC", "PC-LIUJINGJING",
                 "MACBOOKPRO-65B8", "MACBOOKPRO-A883"]),
            "term_duty": random.choice(
                ['许欣艳', '金问薇', '李余妍', "李星汉", "孔秀筠", "孔寻春", "熊叶嘉", "金弘致", "王莹玉", "成博远", "孔秀慧", "金长莹"]),
            "term_group_id": random.choice(['001', '002', 'xzbgs', "jsbgs", "xzbgs", "zcbgs", "005"]),
            "term_group_name": random.choice(['研发办公室', '财务办公室', '行政办公室', "技术办公室", "刑侦办公室", "驻场办公室", "人事办公室"]),
            "devip": random.choice(self.ips),
            "computer_name": "主机名",
            "current_user_name": "当前登录用户",
            "cpu_info": "CPU信息",
            "os_info": "操作系统",
            "memory_info": "内存信息",
            "mac_address": "MAC地址",
            "act_time": date_time.strftime('%Y%m%d%H%M%S'),
        }

    def ssa_ag_zt_soft_data_func(self, index_name, date_time):
        '''
        终端安装软件表
        '''
        return {
            "_index": index_name,
            "_type": 'logs',
            "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),

            "agent_id": str(uuid.uuid4()),
            "log_type": "终端安装软件",
            "term_ip": random.choice(self.ips),
            "term_computer_name": random.choice(
                ['WORKGROUP', 'LIUZZ-2', 'MACBOOK-PRO', "USER-20170916HL", "FX-CE787E", "QQQ-PC", "PC-LIUJINGJING",
                 "MACBOOKPRO-65B8", "MACBOOKPRO-A883"]),
            "term_duty": random.choice(
                ['许欣艳', '金问薇', '李余妍', "李星汉", "孔秀筠", "孔寻春", "熊叶嘉", "金弘致", "王莹玉", "成博远", "孔秀慧", "金长莹"]),
            "term_group_id": random.choice(['001', '002', 'xzbgs', "jsbgs", "xzbgs", "zcbgs", "005"]),
            "term_group_name": random.choice(['研发办公室', '财务办公室', '行政办公室', "技术办公室", "刑侦办公室", "驻场办公室", "人事办公室"]),
            "devip": random.choice(self.ips),
            "software_name": random.choice(['软件1', '软件2']),
            "act_time": date_time.strftime('%Y%m%d%H%M%S'),
        }

    def ssa_ag_zt_share_data_func(self, index_name, date_time):
        '''
        终端共享信息表
        '''
        return {
            "_index": index_name,
            "_type": 'logs',
            "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),

            "agent_id": str(uuid.uuid4()),
            "log_type": "终端共享信息",
            "term_ip": random.choice(self.ips),
            "term_computer_name": random.choice(
                ['WORKGROUP', 'LIUZZ-2', 'MACBOOK-PRO', "USER-20170916HL", "FX-CE787E", "QQQ-PC", "PC-LIUJINGJING",
                 "MACBOOKPRO-65B8", "MACBOOKPRO-A883"]),
            "term_duty": random.choice(
                ['许欣艳', '金问薇', '李余妍', "李星汉", "孔秀筠", "孔寻春", "熊叶嘉", "金弘致", "王莹玉", "成博远", "孔秀慧", "金长莹"]),
            "term_group_id": random.choice(['001', '002', 'xzbgs', "jsbgs", "xzbgs", "zcbgs", "005"]),
            "term_group_name": random.choice(['研发办公室', '财务办公室', '行政办公室', "技术办公室", "刑侦办公室", "驻场办公室", "人事办公室"]),
            "devip": random.choice(self.ips),
            "share_name": "共享名称",
            "folder_path": "文件夹路径",
            "share_des": "共享描述",
            "act_time": date_time.strftime('%Y%m%d%H%M%S'),
        }

    def ssa_ag_zt_user_data_func(self, index_name, date_time):
        '''
        终端用户信息表
        '''
        return {
            "_index": index_name,
            "_type": 'logs',
            "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),

            "agent_id": str(uuid.uuid4()),
            "log_type": "终端用户信息",
            "term_ip": random.choice(self.ips),
            "term_computer_name": random.choice(
                ['WORKGROUP', 'LIUZZ-2', 'MACBOOK-PRO', "USER-20170916HL", "FX-CE787E", "QQQ-PC", "PC-LIUJINGJING",
                 "MACBOOKPRO-65B8", "MACBOOKPRO-A883"]),
            "term_duty": random.choice(
                ['许欣艳', '金问薇', '李余妍', "李星汉", "孔秀筠", "孔寻春", "熊叶嘉", "金弘致", "王莹玉", "成博远", "孔秀慧", "金长莹"]),
            "term_group_id": random.choice(['001', '002', 'xzbgs', "jsbgs", "xzbgs", "zcbgs", "005"]),
            "term_group_name": random.choice(['研发办公室', '财务办公室', '行政办公室', "技术办公室", "刑侦办公室", "驻场办公室", "人事办公室"]),
            "devip": random.choice(self.ips),
            "group_name": random.choice(['组1', '组2', '组3']),
            "user_name": random.choice(['许欣艳', '金问薇', '李余妍']),
            "act_time": date_time.strftime('%Y%m%d%H%M%S'),
        }

    def ssa_event_terminal_data_func(self, index_name, date_time):
        """
        终端事件归并表
        :param index_name:
        :param date_time:
        :return:
        """
        return {
            "_index": index_name,
            "_type": 'logs',
            "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "event_id": str(uuid.uuid4()),
            "event_top_type": '违规事件',  # 事件大类: 病毒，违规，攻击
            "event_type": random.choice(['明文存储', '程序试图运行', 'TMS卸载', '手机充电', '违规插入移动盘', '非工作时间操作']),
            # 事件小类: 程序试图运行,TMS卸载,手机充电,违规插入移动盘,涉密文件,非工作时间操作
            "event_source": random.choice(['审批', '终端程序日志', '刻录', '移动盘', '终端登录日志']),  # 事件来源:程序，登录，审批'
            "event_index": random.choice(
                ['ssa-ag-zd-sp', 'ssa-ag-zd-cx', 'ssa-ag-zd-kl', 'ssa-ag-zd-uc', 'ssa-ag-zd-dl']),  # 原始日志在es中index
            "term_duty": random.choice(
                ['许欣艳', '金问薇', '李余妍', "李星汉", "孔秀筠", "孔寻春", "熊叶嘉", "金弘致", "王莹玉", "成博远", "孔秀慧", "金长莹"]),  # 终端责任人
            "remark": random.choice(['{"sm_content": "D:/系统资料/RFID技术说明.doc","word": "doc"}',
                                     '{"sm_content": "J:/人员名单.doc","word": "doc"}',
                                     '{"sm_content": "E:/人员资料/工资单.doc","word": "doc"}']),  # 备注字段
            "terminal": random.choice(self.ips),  # 终端
            "organization": random.choice(['研发办公室', '财务办公室', '行政办公室', "技术办公室", "刑侦办公室", "驻场办公室", "人事办公室"]),  # 单位
            "event_time": date_time.strftime('%Y%m%d%H%M%S'),  # 事件发生时间
            "event_level": random.randint(1, 3)  # 事件级别
        }

    def event_terminal_data_func(self, index_name, date_time):
        '''
        终端事件统计数据
        '''
        return {
            "_index": index_name,
            "_type": 'logs',
            "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "src_ip": '',
            "dst_ip": '',
            "dst_port": '',
            "protocol": '',
            "event_top_type": "违规事件",
            "event_type": random.choice(['终端卸载', '试图运行', '违规接入U盘', '手机充电']),
            "event_source": "终端-{}".format(random.choice(['登录日志', '程序日志', '设备审批'])),
            "start_time": date_time.strftime('%Y%m%d%H%M%S'),
            "end_time": date_time.strftime('%Y%m%d%H%M%S'),
            "organization": random.choice(['技术办公室', '驻场办公室', '财务办公室', '人事办公室', '刑侦办公室', '行政办公室', '研发办公室']),
            "event_total": random.randint(0, 100),
            "terminal": random.choice(self.ips),
            "event_level": random.choice([1, 2, 3])
        }

    def statistics_terminal_data_func(self, index_name, date_time):
        '''
        终端日志统计数据
        '''
        return {
            "_index": index_name,
            "_type": 'logs',
            "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "src_ip": '',
            "dst_ip": '',
            "src_port": '',
            "dst_port": '',
            "protocol": '',
            "log_top_type": "终端",
            "log_type": random.choice(['登录日志', '浏览网页', '刻录文件', '历史文件浏览', '移动盘拷贝', '程序日志', '设备审批']),
            "log_total": random.randint(500, 1000),
            "start_time": date_time.strftime('%Y%m%d%H%M%S'),
            "end_time": date_time.strftime('%Y%m%d%H%M%S'),
            "organization": random.choice(['技术办公室', '驻场办公室', '财务办公室', '人事办公室', '刑侦办公室', '行政办公室', '研发办公室']),
            "terminal": random.choice(self.ips),
            "log_flow": "",
            "log_source": random.choice(['终端登录日志', '终端浏览网页', '终端刻录文件', '终端历史文件浏览', '终端移动盘拷贝', '终端程序日志', '终端设备审批'])
        }

    def ssa_ag_all_terminal_data_func(self, index_name, date_time):
        '''
        终端日志数据
        '''
        log_type = random.randint(1, 7)
        # 1 = 程序日志
        # 2 = 登录日志
        # 3 = 浏览网页日志
        # 4 = 历史文件日志
        # 5 = 设备审批使用日志
        # 6 = 刻录文件日志
        # 7 = 移动盘拷贝文件日志
        if log_type == 1:
            log_data = {
                "log_type": 1,
                "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
                "agent_id": str(uuid.uuid4()),
                "term_ip": random.choice(self.ips),
                "term_computer_name": random.choice(
                    ['WORKGROUP', 'LIUZZ-2', 'MACBOOK-PRO', "USER-20170916HL", "FX-CE787E", "QQQ-PC", "PC-LIUJINGJING",
                     "MACBOOKPRO-65B8", "MACBOOKPRO-A883"]),
                "term_duty": random.choice(
                    ['许欣艳', '金问薇', '李余妍', "李星汉", "孔秀筠", "孔寻春", "熊叶嘉", "金弘致", "王莹玉", "成博远", "孔秀慧", "金长莹"]),
                "term_group_id": random.choice(['001', '002', 'xzbgs', "jsbgs", "xzbgs", "zcbgs", "005"]),
                "term_group_name": random.choice(['研发办公室', '财务办公室', '行政办公室', "技术办公室", "刑侦办公室", "驻场办公室", "人事办公室"]),
                "act_ip": random.choice(self.ips),
                "act_time": date_time.strftime('%Y%m%d%H%M%S'),
                "act_type": random.choice([2, 3, 5]),
                "app_path": "app_path",
                "app_name": "app_name",
                "log_id": random.randint(1, 1000),
            }
        elif log_type == 2:
            log_data = {
                "log_type": 2,
                "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
                "agent_id": str(uuid.uuid4()),
                "term_ip": random.choice(self.ips),
                "term_computer_name": random.choice(
                    ['WORKGROUP', 'LIUZZ-2', 'MACBOOK-PRO', "USER-20170916HL", "FX-CE787E", "QQQ-PC", "PC-LIUJINGJING",
                     "MACBOOKPRO-65B8", "MACBOOKPRO-A883"]),
                "term_duty": random.choice(
                    ['许欣艳', '金问薇', '李余妍', "李星汉", "孔秀筠", "孔寻春", "熊叶嘉", "金弘致", "王莹玉", "成博远", "孔秀慧", "金长莹"]),
                "term_group_id": random.choice(['001', '002', 'xzbgs', "jsbgs", "xzbgs", "zcbgs", "005"]),
                "term_group_name": random.choice(['研发办公室', '财务办公室', '行政办公室', "技术办公室", "刑侦办公室", "驻场办公室", "人事办公室"]),
                "login_ip": random.choice(self.ips),
                "login_name": random.choice(
                    ['古志用', '王盼芙', '夏景山', "员慧巧", "王寄云", "务冰凡", "军飞白", "力云泽", "王莹玉", "董水之", "王梓美", "王代巧"]),
                "os_username": random.choice(
                    ['admin', 'user', 'agent', "go", 'test', 'qqq', 'superuser', 'superadmin', 'super123', 'aaa']),
                "login_type": random.randint(1, 7),
                "login_result": random.randint(0, 1),
                "act_time": date_time.strftime('%Y%m%d%H%M%S'),
                "log_id": random.randint(1, 1000),
            }
        elif log_type == 3:
            log_data = {
                "log_type": 3,
                "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
                "agent_id": str(uuid.uuid4()),
                "term_ip": random.choice(self.ips),
                "term_computer_name": random.choice(
                    ['WORKGROUP', 'LIUZZ-2', 'MACBOOK-PRO', "USER-20170916HL", "FX-CE787E", "QQQ-PC", "PC-LIUJINGJING",
                     "MACBOOKPRO-65B8", "MACBOOKPRO-A883"]),
                "term_duty": random.choice(
                    ['许欣艳', '金问薇', '李余妍', "李星汉", "孔秀筠", "孔寻春", "熊叶嘉", "金弘致", "王莹玉", "成博远", "孔秀慧", "金长莹"]),
                "term_group_id": random.choice(['001', '002', 'xzbgs', "jsbgs", "xzbgs", "zcbgs", "005"]),
                "term_group_name": random.choice(['研发办公室', '财务办公室', '行政办公室', "技术办公室", "刑侦办公室", "驻场办公室", "人事办公室"]),
                "ie_name": random.choice(
                    ['http://192.168.0.1:808/wss', 'http://192.168.2.11:8080/index', 'http://192.168.3.1/home',
                     'http://192.168.0.1/wss', 'http://192.168.12.1:8088/wssa']),
                "act_time": date_time.strftime('%Y%m%d%H%M%S'),
                "log_id": random.randint(1, 1000),
                "act_ip": random.choice(self.ips),
            }
        elif log_type == 4:
            log_data = {
                "log_type": 4,
                "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
                "agent_id": str(uuid.uuid4()),
                "term_ip": random.choice(self.ips),
                "term_computer_name": random.choice(
                    ['WORKGROUP', 'LIUZZ-2', 'MACBOOK-PRO', "USER-20170916HL", "FX-CE787E", "QQQ-PC", "PC-LIUJINGJING",
                     "MACBOOKPRO-65B8", "MACBOOKPRO-A883"]),
                "term_duty": random.choice(
                    ['许欣艳', '金问薇', '李余妍', "李星汉", "孔秀筠", "孔寻春", "熊叶嘉", "金弘致", "王莹玉", "成博远", "孔秀慧", "金长莹"]),
                "term_group_id": random.choice(['001', '002', 'xzbgs', "jsbgs", "xzbgs", "zcbgs", "005"]),
                "term_group_name": random.choice(['研发办公室', '财务办公室', '行政办公室', "技术办公室", "刑侦办公室", "驻场办公室", "人事办公室"]),
                "file_name": random.choice(
                    ['E:/技术资料/信息安全/PKI/PKI体系.doc', 'E:/人员资料/办公室人员.doc', 'D:/系统资料/人口体系说明.doc', 'E:/技术资料/程序配置/config.xml',
                     'E:/项目/OA/test.py', 'E:/项目/PKI/说明.doc']),
                "act_time": date_time.strftime('%Y%m%d%H%M%S'),
                "log_id": random.randint(1, 1000),
                "act_ip": random.choice(self.ips),
            }
        elif log_type == 5:
            log_data = {
                "log_type": 5,
                "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
                "agent_id": str(uuid.uuid4()),
                "term_ip": random.choice(self.ips),
                "term_computer_name": random.choice(
                    ['WORKGROUP', 'LIUZZ-2', 'MACBOOK-PRO', "USER-20170916HL", "FX-CE787E", "QQQ-PC", "PC-LIUJINGJING",
                     "MACBOOKPRO-65B8", "MACBOOKPRO-A883"]),
                "term_duty": random.choice(
                    ['许欣艳', '金问薇', '李余妍', "李星汉", "孔秀筠", "孔寻春", "熊叶嘉", "金弘致", "王莹玉", "成博远", "孔秀慧", "金长莹"]),
                "term_group_id": random.choice(['001', '002', 'xzbgs', "jsbgs", "xzbgs", "zcbgs", "005"]),
                "term_group_name": random.choice(['研发办公室', '财务办公室', '行政办公室', "技术办公室", "刑侦办公室", "驻场办公室", "人事办公室"]),
                "user_ip": random.choice(self.ips),
                "request_type": random.randint(1, 10),
                "request_name": random.choice(
                    ['打印文件', '打印图片', '刻录系统镜像', "刻录文件", "连接蓝牙aaa", "红外操作", "手机充电", "移动盘拷贝文件", "移动盘拷贝系统", "刻录系统资料"]),
                "act_type": random.randint(0, 7),
                "request_time": date_time.strftime('%Y%m%d%H%M%S'),
                "approver_name": random.choice(
                    ['刘琼芳', '王盼芙', '李余妍', "李星汉", "刘青旋", "务冰凡", "张欣怿", "张白玉", "王莹玉", "李力勤", "张向露", "王代巧"]),
                "approve_time": date_time.strftime('%Y%m%d%H%M%S'),
                "dev_name": random.choice(
                    ['HP LASERJET PROFESSIONAL P1606DN', 'FX XPS', 'SanDisk', "WD", "TOSHIBA", "Lenovo", "ASUS", "PHILIPS",
                     "DACOM K6P"]),
                "print_doc": random.choice(
                    ['公司人员结构分析.doc', '单位工作人员个人简历表.doc', '人员名单.doc', "年度人员需求预测报告.doc", "员工类型分析与管理.doc", "RFID技术说明.doc",
                     "资质.JPG",
                     "工资单.doc", "CARD.JPG"]),
                "act_time": date_time.strftime('%Y%m%d%H%M%S'),
            }
        elif log_type == 6:
            log_data = {
                "log_type": 6,
                "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
                "agent_id": str(uuid.uuid4()),
                "term_ip": random.choice(self.ips),
                "term_computer_name": random.choice(
                    ['WORKGROUP', 'LIUZZ-2', 'MACBOOK-PRO', "USER-20170916HL", "FX-CE787E", "QQQ-PC", "PC-LIUJINGJING",
                     "MACBOOKPRO-65B8", "MACBOOKPRO-A883"]),
                "term_duty": random.choice(
                    ['许欣艳', '金问薇', '李余妍', "李星汉", "孔秀筠", "孔寻春", "熊叶嘉", "金弘致", "王莹玉", "成博远", "孔秀慧", "金长莹"]),
                "term_group_id": random.choice(['001', '002', 'xzbgs', "jsbgs", "xzbgs", "zcbgs", "005"]),
                "term_group_name": random.choice(['研发办公室', '财务办公室', '行政办公室', "技术办公室", "刑侦办公室", "驻场办公室", "人事办公室"]),
                "act_time": date_time.strftime('%Y%m%d%H%M%S'),
                "file_path": random.choice(
                    ['C:/Windows/system32', 'H:/', 'H:/elk部署', "H:/360Downloads", "E:/技术资料/程序配置", "D:/系统资料/", "E:/项目/PKI/",
                     "E:/人员资料/", "J:/logs"]),
                "file_name": random.choice(
                    ['E:/技术资料/信息安全/PKI/PKI体系.doc', 'E:/人员资料/办公室人员.doc', 'D:/系统资料/人口体系说明.doc', 'E:/技术资料/程序配置/config.xml',
                     'E:/项目/OA/test.py', 'E:/项目/PKI/说明.doc']),
                "log_id": random.randint(1, 1000),
                "act_ip": random.choice(self.ips),
            }
        elif log_type == 7:
            log_data = {
                "log_type": 7,
                "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
                "agent_id": str(uuid.uuid4()),
                "term_ip": random.choice(self.ips),
                "term_computer_name": random.choice(
                    ['WORKGROUP', 'LIUZZ-2', 'MACBOOK-PRO', "USER-20170916HL", "FX-CE787E", "QQQ-PC", "PC-LIUJINGJING",
                     "MACBOOKPRO-65B8", "MACBOOKPRO-A883"]),
                "term_duty": random.choice(
                    ['许欣艳', '金问薇', '李余妍', "李星汉", "孔秀筠", "孔寻春", "熊叶嘉", "金弘致", "王莹玉", "成博远", "孔秀慧", "金长莹"]),
                "term_group_id": random.choice(['001', '002', 'xzbgs', "jsbgs", "xzbgs", "zcbgs", "005"]),
                "term_group_name": random.choice(['研发办公室', '财务办公室', '行政办公室', "技术办公室", "刑侦办公室", "驻场办公室", "人事办公室"]),
                "act_time": date_time.strftime('%Y%m%d%H%M%S'),
                "act_type": random.randint(4, 6),
                "act_info": random.choice(
                    ['J:/printelselist.xml', 'H:/webservice.log', 'H:/elk部署/manage.py', "H:/360Downloads/说明.doc",
                     "E:/技术资料/程序配置/RFID技术说明.doc", "D:/系统资料/RFID技术说明.doc", "E:/人员资料/工资单.doc", "E:/人员资料/", "J:/人员名单.doc"]),
                "log_id": random.randint(1, 1000),
                "act_ip": random.choice(self.ips),
            }
        return {
            "_index": index_name,
            "_type": 'logs',
            "@timestamp": log_data.get('@timestamp', ''),
            "agent_id": log_data.get('agent_id', ''),
            "log_type": log_data.get('log_type', ''),
            "act_ip": log_data.get('act_ip', ''),
            "act_time": log_data.get('act_time', ''),
            "act_type": log_data.get('act_type', ''),
            "app_path": log_data.get('app_path', ''),
            "app_name": log_data.get('app_name', ''),
            "login_ip": log_data.get('login_ip', ''),
            "login_name": log_data.get('login_name', ''),
            "os_username": log_data.get('os_username', ''),
            "login_type": log_data.get('login_type', ''),
            "login_result": log_data.get('login_result', ''),
            "ie_name": log_data.get('ie_name', ''),
            "file_name": log_data.get('file_name', ''),
            "user_ip": log_data.get('user_ip', ''),
            "request_type": log_data.get('request_type', ''),
            "request_name": log_data.get('request_name', ''),
            "approver_name": log_data.get('approver_name', ''),
            "approve_time": log_data.get('approve_time', ''),
            "dev_name": log_data.get('dev_name', ''),
            "print_doc": log_data.get('print_doc', ''),
            "file_path": log_data.get('file_path', ''),
            "act_info": log_data.get('act_info', ''),
            "term_ip": log_data.get('term_ip', ''),
            "term_computer_name": log_data.get('term_computer_name', ''),
            "term_duty": log_data.get('term_duty', ''),
            "term_group_id": log_data.get('term_group_id', ''),
            "term_group_name": log_data.get('term_group_name', ''),
        }
        # return {
        #     "_index": index_name,
        #     "_type": 'logs',
        #     "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
        #     "agent_id": uuid.uuid4(),
        #     "log_type": random.randint(1, 7),
        #     "act_ip": random.choice(self.ips),
        #     "act_time": date_time.strftime('%Y%m%d%H%M%S'),
        #     "act_type": random.randint(1, 10),
        #     "app_path": random.choice(['C:\Windows\system32', 'D:\doc']),
        #     "app_name": random.choice(['notepad.exe', 'qq.exe']),
        #     "login_ip": random.choice(self.ips),
        #     "login_name": random.choice(['ADMINISTRATOR', 'guest']),
        #     "os_username": random.choice(['admin', 'user']),
        #     "login_type": random.randint(1, 7),
        #     "login_result": random.randint(0, 1),
        #     "ie_name": random.choice(['http://192.168.0.1:808/wss', 'http://127.0.0.1:80/ie']),
        #     "file_name": random.choice(['E:/技术资料/信息安全/PKI/ PKI体系.doc', 'E://abc/涉密.doc']),
        #     "user_ip": random.choice(self.ips),
        #     "request_type": random.randint(1, 10),
        #     "request_name": random.choice(['admin', 'user']),
        #     "approver_name": random.choice(['admin', 'user']),
        #     "approve_time": date_time.strftime('%Y%m%d%H%M%S'),
        #     "dev_name": random.choice(['dev1', 'dev2', 'dev3']),
        #     "print_doc": random.choice(['文档1', '文档2', '文档3']),
        #     "file_path": random.choice(['C:\Windows\system32', 'D:\cbc']),
        #     "act_info": random.choice(['J:\printelselist.xml', 'D:\cbc.conf']),
        #     "term_ip": random.choice(self.ips),
        #     "term_computer_name": random.choice(['window7', 'window10']),
        #     "term_duty": random.choice(['张三', '李四', '王五']),
        #     "term_group_id": random.choice(['1', '2', '3', "4", "5", "6", "7"]),  # 单位
        #     "term_group_name": random.choice(['研发办公室', '财务办公室', '行政办公室', "技术办公室", "刑侦办公室", "驻场办公室", "人事办公室"]),  # 单位
        # }

    def all_event_data_func(self, index_name, date_time):
        '''
        所有事件
        '''
        # ['系统共享未关闭', '系统未禁用guest用户', '未安装终端安全管理系统', '未安装网盾桌面安全套件', '未安装杀毒软件',
        # '明文存储', '非工作时段操作','USB存储设备使用', '手机充电记录', '终端安全管理系统卸载记录', '程序试图运行']
        # "{}的{}的{}设备发生{}事件".format(event_data['organization'], event_data['src_ip'],
        #                           event_data['dev_name'], event_data['three_type']),
        event_data = {
            "src_ip": random.choice(dst_ips),
            "remark": random.choice(['{"sm_content": "D:/系统资料/RFID技术说明.doc","word": "doc"}',
                                     '{"sm_content": "J:/人员名单.doc","word": "doc"}',
                                     '{"sm_content": "E:/人员资料/工资单.doc","word": "doc"}']),
            "three_type": random.choice(three_type),
            "dev_name": random.choice(
                ['HP LASERJET PROFESSIONAL P1606DN', 'FX XPS', 'SanDisk', "WD", "TOSHIBA", "Lenovo", "ASUS", "PHILIPS",
                 "DACOM K6P"]),
            "organization": random.choice(['研发办公室', '财务办公室', '行政办公室', "技术办公室", "刑侦办公室", "驻场办公室", "人事办公室"]),  # 单位
            "start_time": date_time.strftime('%Y%m%d%H%M%S'),
            "end_time": date_time.strftime('%Y%m%d%H%M%S'),
            "app_path": random.choice(['C:\Windows\system32', 'D:\doc']),
            "app_name": random.choice(['notepad.exe', 'qq.exe']),

        }
        if event_data['three_type'] == "明文存储":
            content = "{}的{}出现明文存储:{}".format(event_data['organization'], event_data['src_ip'],
                                                            event_data['remark'])
        elif event_data['three_type'] == "非工作时段操作":
            content = "{}的{}在{}到{}内非工作时间操作".format(event_data['organization'],event_data['src_ip'],
                                                                 event_data['start_time'],event_data['end_time'])
        elif event_data['three_type'] in ["USB存储设备使用",'手机充电记录']:
            content = "{}的{}的{}设备发生{}事件".format(event_data['organization'], event_data['src_ip'],
                                  event_data['dev_name'], event_data['three_type'])
        elif event_data['three_type'] == '程序试图运行':
            content = "{}的{}的{}程序视图运行".format(event_data['organization'], event_data['src_ip'],
                                  event_data['app_name'] )
        else:
            content = "{}的{}发生{}事件".format(event_data['organization'], event_data['src_ip'],
                                                         event_data['three_type'])

        return {
            "_index": index_name,
            "_type": 'logs',
            "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),

            "event_host": random.choice(dst_ips),
            "event_one_type": random.choice(['违规']),
            "event_two_type": random.choice(['安全策略', '必装安全软件', '痕迹检查']),
            "event_three_type": event_data['three_type'],
            "event_source": 7,
            "src_ip": event_data['src_ip'],
            "dst_ip": '',
            "src_port": '',
            "dst_port": '',
            "tran_protocol": '',
            "app_protocol": '',
            "start_time": date_time.strftime('%Y%m%d%H%M%S'),
            "end_time": date_time.strftime('%Y%m%d%H%M%S'),
            "stastic_time": date_time.strftime('%Y%m%d%H%M%S'),
            "opt_result": random.randint(0, 1),
            "flow": '',
            "event_level": random.randint(1, 3),
            "organization": event_data['organization'],
            "event_total": random.randint(0, 5),
            "event_detail": '',
            "event_contents": content,
        }

    def run(self):



        # 终端基本信息表
        # self.make_data('ssa-ag-zt-basic')
        # # # 终端安装软件表
        # self.make_data('ssa-ag-zt-soft')
        # # # 终端共享信息表
        # self.make_data('ssa-ag-zt-share')
        # # # 终端用户信息表
        # self.make_data('ssa-ag-zt-user')
        # #
        # self.make_data('ssa-event-terminal')
        # self.make_data('event-terminal')
        # self.make_data('statistics-terminal')
        #
        # self.make_data('ssa-ag-all-terminal')
        self.make_data('all-event')

        # self.make_data('ssa-ag-all-terminal')