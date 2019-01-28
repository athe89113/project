# -*- coding:utf-8 -*-
import logging
import random
import time
import datetime
import uuid
from faker import Factory

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

    def make_data(self, index_name):
        data_fun = getattr(self, "{}_data_func".format(index_name.replace('-', '_')))
        datas = []
        # 从10天后 开始往10天前生成数据 共计20天
        start_time = timezone.now() + timezone.timedelta(days=15)
        for i in range(15):
            random_time = timezone.timedelta(minutes=random.randint(1, 1440))
            date_time = timezone.localtime(
                start_time - timezone.timedelta(days=i + 1) - random_time)
            index = "{0}-{1}".format(index_name, date_time.strftime('%Y-%m-%d-%H'))
            for j in range(random.randint(100, 200)):
                starttime = datetime.datetime.strptime(str(date_time)[
                                                       :10] + ' 00:00:00', '%Y-%m-%d %H:%M:%S') + timezone.timedelta(
                    minutes=random.randint(1, 1440))
                data = data_fun(index, starttime)
                datas.append(data)
        add_doc_list(datas)

    def score_data_func(self, index_name, date_time):
        '''
        安全事件评分
        '''
        return {
            "_index": index_name,
            "_type": 'logs',
            "@timestamp": date_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "ip": random.choice(self.ips),
            "event_time": str(date_time.strftime('%Y%m%d%H')),
            "source": random.choice(['终端','防火墙','隔离设备','摆渡设备','SM扫描','数据库审计','IDS','360杀毒软件']),
            "level": random.randint(1, 3),
            "num": random.randint(100, 2000),
            "score": random.randint(0, 100),
        }

    def run(self):
        self.make_data('score')
