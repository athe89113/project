# coding=utf-8
from __future__ import unicode_literals
import os
import psutil
import requests
import commands

from django.conf import settings

if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'soc.settings')
    import django
    django.setup()

from django.utils import timezone
from django.core.cache import cache
from utils.crm_api import Crm
from soc_user.models import User, Agent
from elasticsearch import Elasticsearch


class SysCheck(object):
    """
    * 云松中心配置(必要配置)
    * 系统秘钥，Django SECRET_KEY是否配置(不为空)
    * 运行权限，云松项目使用qsadmin运行
    * 目录配置，MEDIA_ROOT，REPORT_DIR，SCREENSHOT_DIR配置不为空
    * 目录权限，系统目录和日志目录具有qsadmin可写权限

    * 数据连接，本地Mysql，数据中心Mysql，数据中心ZMQ，Redis，Celery队列，ES，Zookeeper已配置且均可连接正常
    * 关联服务，CRM，青松网站，qs_api，备案查询地址配置且可连接正常
    * Soc Agent配置，配置AGENT_SECRET_KEY，添加至少一个soc_agent且可连接正常
    * 通知发送，邮件服务，短信
    * 合作相关，代理商支付宝信息
    * 运行环境，ENV变量不为空且不为local
    * 定时任务，除必须开启外，其他模块需要根据功能开启状况(菜单管理-一级菜单)判断crontab的启用情况，其中
        * soc_agent心跳，heartbeat，必需开启
        * 监控，sync_monitor，sync_item_history
        * 扫描，execute_tasks，execute_run_tasks，xml2db
        * 资产，count_assets，check_domain_icp，必须开启
        * 高防服务(Hades)，sync_hades，syncdata，hw_analyse_data，sync_hw_data
        * 终端安全，sync_hids_log，sync_hids
        * 订单，sync_orders，sync_services，必须开启
    """

    def __init__(self, agent_id=None, user_id=None):
        self.user_id = user_id
        self.agent_id = agent_id

        self.cloud_status = False
        self.qssec_status, self.qssec_ms = False, 0
        self.crm_status, self.crm_ms = False, 0
        self.qs_api_status, self.qs_api_ms = False, 0

    def vaild(self, func, key, args, kwargs):
        if func and kwargs:
            result = func(*args, **kwargs)
        elif args:
            result = func(*args)
        else:
            result = func()
        key = "soc_system_agent_{}_{}".format(self.agent_id, key)
        cache.set(key, result, timeout=60 * 60 * 60)

    def get_values(self):
        db_result = cache.keys("soc_system_agent_{}*".format(self.agent_id))
        result = {}
        for i in db_result:
            key = i.split("soc_system_agent_{}".format(self.agent_id))[1]
            result[key] = cache.get(i)

        print(result)

    @classmethod
    def _get_config(cls, key):
        try:
            conf = getattr(settings, key)
        except Exception:
            return False
        return conf

    @classmethod
    def v_write(cls, path):
        return os.access(path, os.W_OK)

    @classmethod
    def v_run_user(cls):
        p = psutil.Process()
        user = p.username()
        if user == "qsadmin":
            return True
        return False

    def v_path(self):
        paths = [self._get_config("MEDIA_ROOT"), self._get_config("REPORT_DIR"), self._get_config("SCREENSHOT_DIR")]
        return all(paths)

    def v_path_assess(self):
        if not self.v_path():
            return False
        paths = [self._get_config("MEDIA_ROOT"), self._get_config("REPORT_DIR"),
                 self._get_config("BASE_DIR"),
                 '/var/log/soc',
                 self._get_config("SCREENSHOT_DIR")]
        for path in paths:
            if not self.v_write(path):
                return False
        return True

    def v_config(self):
        p = psutil.Process()
        user = p.username()
        data = {
            "secret_key": bool(self._get_config("SECRET_KEY")),
            "media_root": self._get_config("MEDIA_ROOT") and self.v_write(self._get_config("MEDIA_ROOT")),
            "report_dir": self._get_config("REPORT_DIR") and self.v_write(self._get_config("REPORT_DIR")),
            "screenshot_dir": self._get_config("SCREENSHOT_DIR") and self.v_write(self._get_config("SCREENSHOT_DIR")),
            "sys_path": self._get_config("BASE_DIR"),
            "log_path": self.v_write('/var/log/soc'),
            "user": user
        }
        return data

    @classmethod
    def _v_redis(cls, *args):
        import redis
        try:
            r = redis.Redis(*args[0], socket_timeout=3)
            r.info()
        except Exception as e:
            return {"status": False, "msg": e.message}
        return {"status": True, "msg": "连接正常"}

    def v_sys_redis(self):
        configs = ["SYS_REDIS_HOST", "SYS_REDIS_PORT", "SYS_REDIS_DB", "SYS_REDIS_PASSWORD"]
        configs = map(self._get_config, configs)
        return self._v_redis(configs),

    def v_nidps_redis(self):
        configs = ["NIDPS_REDIS_HOST", "NIDPS_REDIS_PORT", "NIDPS_REDIS_DB", "NIDPS_REDIS_PASSWORD"]
        configs = map(self._get_config, configs)
        return self._v_redis(configs),

    def v_dc(self):
        return True

    def v_es(self):
        hosts = self._get_config("ELASTICSEARCH_HOSTS")
        try:
            es = Elasticsearch(hosts=hosts)
            es.info()
        except Exception:
            return False
        return True

    def v_qssec(self):
        user_obj = User.objects.get(id=self.user_id)
        headers = {}
        cloud_url = settings.IFRAME_CLOUD_URL
        url = cloud_url + '/ysapi/home/domain_list/'
        start_time = timezone.now()
        try:
            r = requests.post(url, headers=headers, timeout=5)
            result = r.json()
        except Exception as e:
            return False, '连接失败'
        if result.get("status", 200) != 200:
            return False, result.get("msg")
        used_time = timezone.now() - start_time
        return True, used_time.microseconds / 1000

    def v_qs_api(self):
        agent = Agent.objects.get(id=self.agent_id)
        if not all([agent.qs_token_secret, agent.qs_token]):
            return False, 'TOKEN 未配置'
        user_obj = User.objects.get(id=self.user_id)
        start_time = timezone.now()
        result = {}
        if result.get("status") != 200:
            return False, result.get("msg")
        used_time = timezone.now() - start_time
        return True, used_time.microseconds / 1000

    def v_crm(self):
        user_obj = User.objects.get(id=self.user_id)
        start_time = timezone.now()
        crm = Crm(user=user_obj, timeout=5)
        result = crm.get_custom_service_info("ddos")
        used_time = timezone.now() - start_time
        if result.get("status") != 200:
            return False, result.get("msg")
        return True, used_time.microseconds / 1000

    @staticmethod
    def v_icp():
        start_time = timezone.now()
        result = False
        used_time = timezone.now() - start_time
        return bool(result), used_time.microseconds / 1000

    def v_crontab(self):
        crontabs = []
        all_status = True
        service_crontabs = {
            "cron_soc_agent": ['heartbeat.sh'],
            "cron_asset": ['count_assets.sh', 'check_domain_icp.sh'],
            "cron_monitor": ['sync_monitor.sh', 'sync_item_history.sh'],
            "cron_hw": ['sync_hades.sh', 'hw_analyse_data.sh', 'sync_hw_data.sh'],
            "cron_hids": ['sync_hids_log.sh', 'sync_hids.sh'],
            "cron_purchase": ['sync_orders.sh', 'sync_services.sh'],
            "cron_system": ['sync_system_monitor.sh']
        }
        with open("/etc/crontab", 'rb') as f:
            for line in f.readlines():
                if '#' not in line:
                    crontabs.append(line.split('/')[-1].replace('\n', '').replace(' ', ''))
        services = {}
        for service in service_crontabs:
            if set(service_crontabs[service]).issubset(set(crontabs)):
                services[service] = True
            else:
                services[service] = False
                all_status = False
        return all_status, services

    def v_soc_agent(self):
        from soc.management.commands.check_soc_agent_heartbeat import Command
        from soc.models import SocAgent
        soc_agent = SocAgent.objects.filter(agent_id=self.agent_id)
        c = Command()
        return c.send_breakbeat(soc_agent, notify=False)

    def v_db_service(self):
        msg = []
        if not self.v_sys_redis():
            msg.append("系统资源Redis")
        if not self.v_nidps_redis():
            msg.append("网络安全Redis")
        if not msg:
            status = True
        else:
            status = False
        return status, "和".join(msg)

    def v_message(self):
        from soc_system.models import Message
        if Message.objects.filter(agent_id=self.agent_id, type__in=[1, 4]).count() == 0:
            return False
        if Message.objects.filter(agent_id=self.agent_id, type__in=[2]).count() == 0:
            return False
        return True

    def v_pay(self):
        user = User.objects.get(id=self.user_id)
        crm = Crm(user=user, timeout=5)
        try:
            data = crm.get_agent_info()
        except Exception:
            return False
        if data.get("status") == 200:
            if data.get("data", {}).get("pay_private_key") and \
                    data.get("data", {}).get("pay_pid"):
                return True
        return False

    def v_env(self, v_all=False):
        """

        :param v_all: 是否检查全部
        :return:
        """
        if self._get_config('ENV') in ["", "Yunsong"]:
            return False
        if v_all:
            return True
        if self._get_config("EMAIL_SUBJECT_PREFIX") in ['[Yunsong]']:
            return False
        if self._get_config('DEBUG'):
            return False

        return True

    def v_sso(self):
        try:
            agent = Agent.objects.get(id=self.agent_id)
        except Agent.DoesNotExist:
            return False
        if not agent.ssl_pub_key:
            return False
        if not self._get_config("SSO_PRIVATE_KEY"):
            return False
        return True

    def v_agent_info(self):
        try:
            agent = Agent.objects.get(id=self.agent_id)
        except Agent.DoesNotExist:
            return False
        if not all([agent.web_domain, agent.web_logo, agent.web_title]):
            return False
        return True

    def v_monitor(self):
        return False

    def v_hades(self):
        if not self._get_config("DATACENTER_IP"):
            return False
        if not self._get_config("DATACENTER_PORT"):
            return False
        if not self._get_config("HADES_SECURITY_KEY"):
            return False
        return True

    def v_cloud(self):
        return self.v_qs_api()

    def v_cloud_services(self):
        """qssec, qssec_api, crm"""
        self.cloud_status = True
        self.qssec_status, self.qssec_ms = self.v_qssec()
        self.crm_status, self.crm_ms = self.v_crm()
        self.qs_api_status, self.qs_api_ms = self.v_qs_api()
        return True

    def v_waf(self):
        return self.v_qssec()

    def v_scan_tool(self):
        return False

    def v_scan_conf(self):
        return False

    def v_hids(self):
        return False

    def v_nids(self):
        return False

    @classmethod
    def check_date(cls):

        try:
            result = commands.getoutput('ntpdate -q time1.aliyun.com')
            diff = (result.split('\n')[0].split()[-1])
            diff = float(diff)
        except Exception:
            return False, 0
        if diff > 30:
            return False, round(diff * 1000.0, 2)
        return True, round(diff * 1000.0, 2)

    def c_sys(self):
        sys_data = dict()
        sys_data['secret_key'] = bool(self._get_config("SECRET_KEY"))
        sys_data['run_user'] = self.v_run_user()
        sys_data['path_conf'] = self.v_path()
        sys_data['path_access'] = self.v_path_assess()
        sys_data['db'], sys_data['db_msg'] = self.v_db_service()
        cache.set(str(self.agent_id) + '_system_check_progress', 10)

        self.qssec_status, self.qssec_ms = self.v_qssec()
        cache.set(str(self.agent_id) + '_system_check_progress', 20)
        self.crm_status, self.crm_ms = self.v_crm()
        cache.set(str(self.agent_id) + '_system_check_progress', 30)
        self.qs_api_status, self.qs_api_ms = self.v_qs_api()
        cache.set(str(self.agent_id) + '_system_check_progress', 40)
        self.cloud_status = True
        sys_data['date'], sys_data['date_ms'] = self.check_date()
        cache.set(str(self.agent_id) + '_system_check_progress', 45)
        sys_data['services'] = all([self.qssec_status, self.crm_status, self.qs_api_status])
        sys_data['qssec'] = self.qssec_status
        sys_data['qssec_ms'] = self.qssec_ms

        sys_data['crm'] = self.crm_status
        sys_data['crm_ms'] = self.crm_ms

        sys_data['qs_api'] = self.qs_api_status
        sys_data['qs_api_ms'] = self.qs_api_ms
        sys_data['icp'], sys_data['icp_ms'] = self.v_icp()
        sys_data['soc_agent'] = self.v_soc_agent()[0]
        sys_data['message'] = self.v_message()
        sys_data['pay'] = self.v_pay()
        sys_data['env'] = self.v_env(v_all=True)
        crontab_status, crontabs = self.v_crontab()
        sys_data['crontabs'] = crontab_status
        sys_data.update(crontabs)

        cache.set(str(self.agent_id) + '_system_monitor_sys', sys_data, timeout=None)

        cache.set(str(self.agent_id) + '_system_monitor_lastitme',
                  timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S"))

        cache.set(str(self.agent_id) + '_system_check_progress', 50)
        return all(sys_data.values())

    @staticmethod
    def v_true():
        return True

    def c_sys_b2(self):
        all_conf = {
            "env": {"func": self.v_env},
            "sso": {"func": self.v_sso},
            "agent_info": {"func": self.v_agent_info},
            "menu": {"func": self.v_true},

        }
        for i in all_conf:
            func = all_conf[i].get('func')
            args = all_conf[i].get('args')
            kwargs = all_conf[i].get('kwargs')
            self.vaild(func, key=i, args=args, kwargs=kwargs)

    def c_sys_b(self):
        sys_b_data = dict()
        sys_b_data['env'] = self.v_env()
        sys_b_data['sso'] = self.v_sso()
        sys_b_data['menu'] = True
        cache.set(str(self.agent_id) + '_system_check_progress', 60)
        sys_b_data['agent_info'] = self.v_agent_info()
        cache.set(str(self.agent_id) + '_system_check_progress', 70)

        cache.set(str(self.agent_id) + '_system_monitor_sys_b', sys_b_data, timeout=None)

    def c_component(self):
        soc_c_data = dict()
        soc_c_data['monitor'] = self.v_monitor()

        soc_c_data['hw_key'] = self.v_hades()
        soc_c_data['hw_dc'] = self.v_dc()
        soc_c_data['hw'] = all([soc_c_data['hw_key'], soc_c_data['hw_dc']])
        if not self.cloud_status:
            self.v_cloud_services()
        soc_c_data['cloud_crm'] = self.crm_status
        soc_c_data['cloud_qssec'] = self.qssec_status
        soc_c_data['cloud_qs_api'] = self.qs_api_status
        soc_c_data['cloud'] = all([soc_c_data['cloud_crm'], soc_c_data['cloud_qssec'], soc_c_data['cloud_qs_api']])
        soc_c_data['cloud_waf'] = self.qssec_status
        cache.set(str(self.agent_id) + '_system_check_progress', 75)
        soc_c_data['scan_conf'] = soc_c_data['scan_tools'] = self.v_scan_tool()
        soc_c_data['scan_dir'] = self._get_config("REPORT_DIR") and self.v_write(self._get_config("REPORT_DIR"))
        soc_c_data['scan'] = soc_c_data['scan_dir'] and soc_c_data['scan_conf']
        soc_c_data['hids'] = soc_c_data['hids_conf'] = soc_c_data['hids_tools'] = self.v_hids()
        soc_c_data['nids'] = self.v_nidps_redis()
        cache.set(str(self.agent_id) + '_system_monitor_soc_component', soc_c_data, timeout=None)

    def v_all(self):
        print("start check")
        if cache.get(str(self.agent_id)+'_system_check_start'):
            print("pass check")
            return True
        cache.set(str(self.agent_id)+'_system_check_start', True, timeout=60)
        cache.set(str(self.agent_id)+'_system_status', 'loading')
        cache.set(str(self.agent_id)+'_system_check_p', 5)
        cache.set(str(self.agent_id)+'_system_monitor_sys', {})
        cache.set(str(self.agent_id)+'_system_monitor_sys_b', {})
        cache.set(str(self.agent_id)+'_system_monitor_soc_component', {})
        result = self.c_sys()
        self.c_sys_b()
        self.c_component()
        cache.set(str(self.agent_id) + '_system_status', result)
        cache.set(str(self.agent_id)+'_system_check_progress', 100)
        cache.delete('system_check_start')

        """
        sys_b: {
          env: true,
          sso: true,
          menu: false,
          agent_info: false
        },
        soc_component: {
          monitor: false,
          hw: false,
          hw_key: false,
          hw_dc: false,
          cloud: false,
          cloud_crm: false,
          cloud_qssec: false,
          cloud_qs_api: false,
          waf: false,
          scan: false,
          scan_conf: false,
          scan_tools: false,
          scan_dir: false,
          hids: false,
          hids_conf: false,
          hids_tools: false,
          nids: false,
        }
         sys: {
          secret_key: true,
          run_user: false,
          path_conf: 'loading',
          path_access: false,
          db: false,
          services: 'loading',
          crm: false,
          qs_api: true,
          qssec: true,
          icp: true,
          soc_agent: true,
          message: false,
          pay: true,
          env: true,
          crontabs: true,
          cron_soc_agent: false,
          cron_monitor: false,
          cron_asset: true,
          cron_hw: true,
          cron_hids: true,
          cron_purchase: false,
        },
        :return:
        """


if __name__ == "__main__":
    s = SysCheck(user_id=5, agent_id=2)
    # c = s.v_config()
    # print(c)
    # ser = s.v_service()
    # print(ser)
    # qs_ap = s.v_qssec()
    # print(qs_ap)
    print(s.check_date())
    # print(s.v_qs_api()[1])
    # print(s.v_sso())
    # print(s.v_crm())
