# coding=utf-8
from __future__ import print_function
from __future__ import unicode_literals
import time
import json
import redis
import psutil
import datetime


class BaseSetting(object):
    pass


if __name__ == '__main__':
    settings = BaseSetting()
    setattr(settings, 'SYS_REDIS_HOST', '127.0.0.1')
    setattr(settings, 'SYS_REDIS_DB', 1)
    setattr(settings, 'SYS_REDIS_PORT', 6379)
    setattr(settings, 'SYS_REDIS_PASSWORD', None)
else:
    from django.conf import settings


class OS(object):

    def disk(self):
        pass

    def mem(self):
        pass

    def cpu(self):
        pass

    def network(self):
        pass


class RedisDb(object):
    def __init__(self, redis_host, redis_port=6379, redis_db=2, redis_password=None):
        self.redis_pipline = redis.Redis(host=redis_host, port=redis_port,
                                         db=redis_db, password=redis_password).pipeline()
        self.redis_cli = redis.Redis(host=redis_host, port=redis_port,
                                     db=redis_db, password=redis_password)

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_inst'):
            cls._inst = super(RedisDb, cls).__new__(cls, *args, **kwargs)
        return cls._inst

    def set(self, key, data, timeout=60*60):
        data = json.dumps(data)
        self.redis_cli.set(key, data)
        self.redis_cli.expire(key, time=timeout)

    def get(self, key):
        return self.redis_cli.get(key)

    def keys(self, pattern):
        return self.redis_cli.keys(pattern)

    def get_last(self, key):
        key_list = self.redis_cli.keys(key)
        if key_list:
            return self.redis_cli.get(max(key_list))
        return None

    def execute(self):
        self.redis_pipline.execute()


class BaseMonitor(object):

    def __init__(self, threshold=None, key='soc_monitor', hostname=None):
        self.threshold = threshold
        self.key = key
        self.hostname = hostname
        redis_db = getattr(settings, "SYS_REDIS_DB")
        redis_host = getattr(settings, "SYS_REDIS_HOST")
        redis_port = getattr(settings, "SYS_REDIS_PORT")
        redis_password = getattr(settings, "SYS_REDIS_PASSWORD")

        self.db = RedisDb(redis_host=redis_host, redis_port=redis_port,
                          redis_db=redis_db, redis_password=redis_password)

    def fetch(self, *args, **kwargs):
        pass

    def __key(self, all=False):
        if all:
            timestamp = '*'
        else:
            timestamp = int(time.mktime(datetime.datetime.now().timetuple()))

        return "{}_{}_{}_{}".format(self.key, self.hostname, self.__class__.__name__.lower(), timestamp)

    def save(self, data=None):
        return self.db.set(self.__key(), data)

    def read(self, db):
        return db.get(self.__key())

    def read_history(self, *args, **kwargs):
        pass

    def last(self):
        return self.db.get_last(self.__key(all=True))

    def alert(self, data):
        pass

    def get_line_chart(self):
        db = self.db
        keys = db.keys(self.__key(all=True))
        keys.sort()
        data = []
        key_list = []
        for key in keys:
            times = datetime.datetime.fromtimestamp(int(key.split('_')[-1])).strftime("%H:%M:%S")
            key_list.append(times)
            item = db.get(key)
            if item:
                item = json.loads(item)
            data.append(item)
        datas = {
            "time": key_list,
            "data": data
        }
        return datas


class CpuMonitor(BaseMonitor):

    def __init__(self, threshold=80, *args, **kwargs):
        super(CpuMonitor, self).__init__(threshold, *args, **kwargs)

    def fetch(self, *args, **kwargs):
        # total_cpu = psutil.cpu_times().user + psutil.cpu_times().idle
        # user_cpu = psutil.cpu_times().user
        # cpu_syl = user_cpu / total_cpu * 100
        cpu_syl = psutil.cpu_percent()
        return round(cpu_syl, 1)


class MenMonitor(BaseMonitor):

    def __init__(self, threshold=80, *args, **kwargs):
        super(MenMonitor, self).__init__(threshold, *args, **kwargs)

    def fetch(self):
        mem = psutil.virtual_memory()  # 使用psutil.virtual_memory方法获取内存完整信息
        mem_total = mem.total
        mem_used = mem.used

        mem_syl = mem_used / float(mem_total) * 100
        return round(mem_syl, 1)


class DiskMonitor(BaseMonitor):

    def __init__(self, threshold=80, *args, **kwargs):
        super(DiskMonitor, self).__init__(threshold, *args, **kwargs)

    def fetch(self):
        data = list()
        data.append({"name": "系统盘", "used": psutil.disk_usage('/').used, "all": psutil.disk_usage('/').total})
        data.append({"name": "数据盘", "used": psutil.disk_usage('/opt').used, "all": psutil.disk_usage('/opt').total})
        return data


class NetMonitor(BaseMonitor):

    def __init__(self, threshold=80, *args, **kwargs):
        super(NetMonitor, self).__init__(threshold, *args, **kwargs)

    @classmethod
    def get_key(cls):
        key_info = psutil.net_io_counters(pernic=True).keys()  # 获取网卡名称

        recv = 0
        sent = 0
        for key in key_info:

            recv += psutil.net_io_counters(pernic=True).get(key).bytes_recv  # 各网卡接收的字节数
            sent += psutil.net_io_counters(pernic=True).get(key).bytes_sent  # 各网卡发送的字节数
        return recv, sent

    def fetch(self):
        recv, sent = self.get_key()
        return {"in": recv, "out": sent}

    def __key(self, all=False):
        if all:
            timestamp = '*'
        else:
            timestamp = int(time.mktime(datetime.datetime.now().timetuple()))

        return "{}_{}_{}_{}".format(self.key, self.hostname, self.__class__.__name__.lower(), timestamp)

    def get_line_chart(self):

        db = self.db
        keys = db.keys(self.__key(all=True))
        keys.sort()
        data = []
        key_list = []
        old_time = None
        old_in = None
        old_out = None

        for key in keys:
            time = datetime.datetime.fromtimestamp(int(key.split('_')[-1]))
            item = db.get(key)
            if item:
                item = json.loads(item)
            new_in = item.get("in")
            new_out = item.get("out")
            if old_time:
                s = (time - old_time).seconds
                if not s:
                    s = 1
                item['in'] = (abs(new_in - old_in))/s
                item['out'] = (abs(new_out - old_out))/s

                key_list.append(time.strftime("%H:%M:%S"))
                data.append(item)
            old_time = time
            old_in = new_in
            old_out = new_out
        datas = {
            "time": key_list,
            "data": data
        }
        return datas


class MysqlMonitor(BaseMonitor):
    def fetch(self, *args, **kwargs):
        import MySQLdb
        sql = "select round(sum(DATA_LENGTH/1024/1024),2)" \
              " as data, truncate(sum(index_length)/1024/1024,2) as index_size  from TABLES;"
        db = MySQLdb.connect("127.0.0.1", "root", "root", 'information_schema')
        cursor = db.cursor()
        cursor.execute(sql)
        data = cursor.fetchone()
        data = sum(data)
        return data


class VrrpdMonitor(BaseMonitor):

    def __init__(self, threshold=80, *args, **kwargs):
        super(VrrpdMonitor, self).__init__(threshold, *args, **kwargs)
        self._is_master_key = "soc:nids:{}:is_master".format(self.hostname)
        self._is_vrrpd_runnig_key = "soc:nids:{}:is_vrrpd_runnig".format(self.hostname)
        self._is_runnig_key = "soc:nids:{}:is_runnig".format(self.hostname)
        self._is_worker_key = "soc:nids:{}:is_runnig".format(self.hostname)
        # self.db.set(self._vip_key, '172.16.124.1')

    @property
    def is_master(self):
        data = self.db.get(self._is_master_key)
        if data is None:
            return False
        if data == 'true':
            return True
        return False

    @classmethod
    def get_run_status(cls):
        run = False
        work = False
        try:
            with open('/tmp/NIDS_STATUS', 'rb') as f:
                if b"master" in f.read():
                    master = True
                else:
                    master = False
        except IOError:
            master = False

        for p in psutil.process_iter():
            if b'vrrpd' in p.name():
                run = True
            if b'suricata' in p.name():
                work = True
        return run, work, master

    @property
    def is_vrrpd_running(self):
        run = self.db.get(self._is_vrrpd_runnig_key)
        if run is None:
            return False
        if run == 'true':
            return True
        return False

    @property
    def is_running(self):
        run = self.db.get(self._is_runnig_key)
        if run is None:
            return False
        if run == 'true':
            return True
        return False

    def fetch(self):
        run, work, master = self.get_run_status()
        print("is vrrpd runing: {}".format(run))
        print("is suricata work: {}".format(work))
        print("is master: {}".format(master))
        self.db.set(self._is_vrrpd_runnig_key, run, timeout=10)
        self.db.set(self._is_runnig_key, work, timeout=10)
        self.db.set(self._is_master_key, master, timeout=10)
        return run

    def save(self, data=None):
        pass


def init_yaml_conf():
    import yaml
    config_path = b'/opt/ids/etc/suricata/users.yaml'
    with open(config_path, 'rb') as f:
        conf = yaml.load(f)['configserver']
        setattr(settings, 'SYS_REDIS_HOST', conf['server'])
        setattr(settings, 'SYS_REDIS_PORT', conf['port'])
        setattr(settings, 'SYS_REDIS_DB', conf['db'])
        setattr(settings, 'SYS_REDIS_PASSWORD', conf['authkey'])
        return conf['hostname']


if __name__ == "__main__":
    from sys import argv
    hostname = 'sit'
    if 'yaml' in argv:
        hostname = init_yaml_conf()

    for m in [CpuMonitor, MenMonitor, DiskMonitor, NetMonitor]:
        instance = m(key="scan_monitor_{}".format(hostname), hostname=hostname)
        print("check {}".format(instance.__class__.__name__.lower()))
        d = instance.fetch()
        instance.save(d)
        print(instance.last())


