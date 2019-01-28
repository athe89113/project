# coding:utf-8
from __future__ import unicode_literals, print_function
import datetime
import json
import logging
import random
import time
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.cache import cache
from django.utils import timezone
from optparse import make_option
from utils import ip as geoip
from kafka import KafkaProducer
from soc.models import Agent
from soc_ssa.models import SelfServiceConf
from utils import ip as geoip

# 请使用域名brokers
kafka_brokers = getattr(settings, "KAFKA_BROKERS", ["http://127.0.0.1:9092"])
logger = logging.getLogger('console')


class Command(BaseCommand):
    help = "生成态势感知实时数据数据"
    option_list = BaseCommand.option_list + (
        make_option('--agent', dest='agent_id', default='',
                    help='AGENT_ID, agent ID'),
        make_option('--dst_ip', dest='dst_ip', default='139.217.22.49',
                    help='DST_IP, dst ip'),
        make_option('--frequency', dest='frequency', default=15, type=int,
                    help='frequency'),
        make_option('--timeout', dest='timeout', default=60, type=int,
                    help='timeout'),
    )

    def handle(self, *args, **options):
        """实时数据
        """
        timeout = options.get("timeout")
        try:
            agent_id = Agent.objects.get(id=options.get("agent_id"))
            kafka_broker = SelfServiceConf.objects.get(
                agent_id=agent_id, service='kafka')
        except Agent.DoesNotExist:
            logger.info("no agent")
            return
        except SelfServiceConf.DoesNotExist:
            logger.info("no kafka")
            return
        # 实例化一个KafkaProducer示例，用于向Kafka投递消息
        producer = KafkaProducer(
            bootstrap_servers=kafka_broker.host,
            # bootstrap_servers="hd-datanode2:9092",
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            api_version=(0, 8, 0)
        )
        # metrics = producer.metrics()
        # print(metrics)
        dst_ip = options.get("dst_ip")
        try:
            dst_ip_location = geoip.find_ip_location(dst_ip)[1]
        except Exception:
            dst_ip_location = "北京"

        while True:
            time_now = timezone.localtime(timezone.now())
            logger.info(time_now.strftime("%Y-%m-%d %H:%M:%S"))
            timestamp = int(time.mktime(time_now.timetuple()))
            # producer.send('web-log', '{"status":"301","body_bytes_sent":"178","bytes_sent":"500","prospector":{"type":"log"},"upstream_status":"\"301\"","http_referer":"\"http://[139.219.97.13]\"","upstream_response_time":"\"0.160\"","time_iso8601":"2018-03-21T15:41:43+08:00","tags":["beats_input_codec_plain_applied"],"request_length":"146","server_protocol":"HTTP/1.1","type":"261263cd-3895-4ec8-88a1-7468cca63a4a","beat":{"name":"DED-Azure-North-QINGSONG-QSSEC-NODE01","version":"6.2.2","hostname":"DED-Azure-North-QINGSONG-QSSEC-NODE01"},"offset":297961,"method":"GET","http_x_forwarded_for":"\"-\"","@timestamp":"2018-03-21T07:41:47.065Z","request_time":"0.160","http_user_agent":"\"Go-http-client/1.1\"","@version":"1","request_uri":"/","upstream_addr":"\"139.219.226.91:443\"","host":["DED-Azure-North-QINGSONG-QSSEC-NODE01","www.qssec.com"],"remote_addr":"139.219.100.132","hostname":"ded-azure-north-qingsong-qssec-node01","real_ip":"139.219.100.132","source":"/usr/local/nginx/logs/access.www.qssec.com_ssl.log","message":"2018-03-21T15:41:43+08:00 ded-azure-north-qingsong-qssec-node01 139.219.100.132 139.219.100.132 www.qssec.com GET / HTTP/1.1 301 146 500 178 0.160 \"139.219.226.91:443\" \"301\" \"-\" \"0.160\" \"http://[139.219.97.13]\" \"Go-http-client/1.1\" \"-\"","upstream_cache_status":"\"-\""}')
            # UV

            realtime_uv = cache.get("ssa_realtime_uv")
            if not realtime_uv:
                realtime_uv = random.randint(20, 35)
                cache.set("ssa_realtime_uv", realtime_uv, timeout=timeout)

            producer.send('realtime_uv', [realtime_uv])
            logger.info("realtime_uv: {}".format(realtime_uv))

            # 实时访问
            web_log_ip_map = cache.get("ssa_web_log_ip_map")
            if not web_log_ip_map:
                ips = geoip.random_china_ip(realtime_uv)
                web_log_ip_map = [
                    {"ip": ip[0], "location": ip[1]} for ip in ips
                ]
                cache.set("ssa_web_log_ip_map",
                          web_log_ip_map, timeout=timeout)

            producer.send('web_log_ip_map', web_log_ip_map)
            logger.info("web_log_ip_map: {}".format(len(web_log_ip_map)))

            # 实时攻击
            attack_map = cache.get("ssa_attack_map")
            if not attack_map:
                ips = geoip.random_china_ip(random.randint(2, 50))
                attack_map = []
                for ip in ips:
                    level_random = random.randint(0, 100)
                    # pos = [98, 95, 90, 80, 0]
                    pos = [90, 75, 50, 0]
                    index = 3
                    for idx, p in enumerate(pos):
                        if level_random > p:
                            index = idx
                    level = ["严重", "高", "中", "低"][index]
                    attack_map.append(
                        {
                            "time": timezone.localtime(timezone.datetime.fromtimestamp(random.randint(timestamp-timeout, timestamp)).replace(tzinfo=timezone.get_current_timezone())).strftime("%Y-%m-%d %H:%M:%S"),
                            "dst_ip": dst_ip_location,
                            "dst_ip_location": dst_ip_location,
                            "level": level,
                            "src_ip": ip[0],
                            "src_ip_location": ip[1]
                        }
                    )
                attack_map = sorted(attack_map, key=lambda elem: elem["time"])

                cache.set("ssa_attack_map", attack_map, timeout=timeout)
            producer.send('attack_map', attack_map)
            logger.info("attack_map: {}".format(len(attack_map)))
            producer.flush()

            time.sleep(options.get("frequency"))
