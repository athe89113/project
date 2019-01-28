# coding=utf-8
from __future__ import unicode_literals
import logging
import time
from django.core.management.base import BaseCommand
from django.core.cache import cache
from django.db.models import Count, Q
from django.utils import timezone
from soc import models as soc_models
from soc_message_center.tasks import send_message
from soc_ssa import models as ssa_models
from soc_ssa.views.ssa_views import es_common
logger = logging.getLogger('console')


def logger_it(msg, data):
    # logger.info(msg)
    # logger.info(data)
    pass


class Command(BaseCommand):

    def handle(self, *args, **options):
        """SSA预警告警
        需要在数据计算完成时执行本脚本
        """
        time_now = timezone.localtime(timezone.now())
        # 统计上一个小时的开始和结束
        self.start_time = (time_now - timezone.timedelta(hours=1)
                           ).strftime("%Y-%m-%d 00:00:00")
        self.end_time = (time_now - timezone.timedelta(hours=1)
                         ).strftime("%Y-%m-%d 23:59:59")
        self.start_timestamp = time.mktime(time_now.replace(
            hour=0, minute=0, second=0, microsecond=0).timetuple())
        print(self.start_timestamp)

        agents = soc_models.Agent.objects.all()
        for agent in agents:
            # TODO 检查当前小时的数据是否计算完成

            locations = {"未知": 0}
            locations_ip = {"未知": []}

            idcs = soc_models.Idc.objects.filter(
                agent=agent).annotate(mynum=Count("netdevice"))
            self.get_location(locations, locations_ip, 'netdevice', idcs)

            idcs = soc_models.Idc.objects.filter(
                agent=agent).annotate(mynum=Count("server"))
            self.get_location(locations, locations_ip, 'server', idcs)

            groups = soc_models.AssetGroup.objects.filter(
                agent=agent).annotate(mynum=Count("terminal"))
            self.get_location(locations, locations_ip, 'terminal', groups)

            self.locations = locations
            self.locations_ip = locations_ip

            # print(self.locations_ip)

            # 阈值判断
            alarm_confs = ssa_models.SSAAlarmConf.objects.filter(agent=agent)

            for ac in alarm_confs:
                max_alarm_count = ac.max_alarm_count
                alarm_cells = ssa_models.SSAAlarmConfCell.objects.filter(
                    agent=agent, enable=1, cell__conf_type=ac.conf_type)

                # 判断条件
                results = []
                for alarm_cell in alarm_cells:
                    func = getattr(self, alarm_cell.cell.key, None)
                    if func:
                        # logger.info(alarm_cell.cell.key)
                        result = func(
                            cell=alarm_cell.cell,
                            threshold=[alarm_cell.warning, alarm_cell.alarm]
                        )
                        results.append(result+(alarm_cell.cell,))
                    else:
                        logger.info("不支持: {}".format(alarm_cell.cell.key))

                # 判断条件 1 满足其中任意一项 2 满足所有条件
                notifys = ssa_models.SSAAlarmNotifyConf.objects.filter(
                    agent=agent, conf_type=ac.conf_type).filter(Q(email=1) | Q(sms=1))
                if ac.toggle_condition == 1:
                    for result in results:
                        if result[0]:
                            if self.verify(agent, result[2].key, max_alarm_count):
                                msg = self.modify_msg(result[1])
                                self.send_warning_and_alarm(
                                    result[2].name, notifys, msg)
                elif ac.toggle_condition == 2:
                    if all([r[0] for r in results]):
                        if self.verify(agent, "conf_type_{}_all".format(ac.conf_type), max_alarm_count):
                            msgs = []
                            for result in results:
                                if isinstance(result[1], list):
                                    msgs += result[1]
                                else:
                                    msgs.append(result[1])
                            # 聚合消息
                            mss = []
                            for m in msgs:
                                ms = m.split("，")
                                if len(ms) == 3 and ms[2]:
                                    ms = "，".join([ms[0], ms[2]])
                                else:
                                    ms = ms[0]
                                mss.append(ms)
                            msgs = self.modify_msg("；".join(mss))
                            self.send_warning_and_alarm(
                                "多项触发", notifys, msgs)

    def modify_msg(self, msgs):
        is_list = True
        if not isinstance(msgs, list):
            is_list = False
            msgs = [msgs]
        rets = []
        for msg in msgs:
            ret = "您好，当前系统中 {}，请尽快登录系统查看具体信息。".format(msg)
            rets.append(ret)

        return rets if is_list else rets[0]

    def check_single_value(self, value, cell, threshold, display_all=False):
        """检查单个值是否超过阈值
        """

        single_msg_template = "{name}{real_value}已{expression}{threshold_value}{threshold}值，{dangerous_level}"

        # 反过来比较
        for idx, v in reversed(list(enumerate(threshold))):

            expre = "{} {} {}".format(value, cell.expression, threshold[idx])
            if eval(expre):

                value = round(value, 2)
                real_value = "{}{}".format(
                    value, cell.unit) if cell.unit else value
                msg = single_msg_template.format(**{
                    "name": cell.name,
                    "real_value": real_value if display_all else "",
                    "expression": {">=": "超过", "<=": "低于"}.get(cell.expression),
                    "threshold": ["预警", "告警"][idx],
                    "dangerous_level": ["存在安全风险", "处于安全紧急状态"][idx],
                    "threshold_value": "{}{}".format(threshold[idx], cell.unit) if cell.unit else threshold[idx],
                })
                return True, msg

        # 检查是否超过阈值
        return False, ""

    def check_multi_values(self, items, cell, threshold, display_all=False):
        """检查多个值是否超过阈值
        :return: 返回超过阈值的实际值
        """

        multi_msg_template = "{item_num}个{target}的{name}已{expression}{threshold_value}{threshold}值，{dangerous_level}，{real_value}"

        targets = {
            "vul_single_ip_count": "IP地址",
            "vul_localtion_count": "单位",
            "attack_single_ip_count": "IP地址",
            "web_status_4xx": "网站",
            "web_status_5xx": "网站",
            "virus_single_ip_count": "IP地址",
        }
        target = targets[cell.key] if cell.key in targets else "目标"

        rets = {}
        # 区分预警和告警
        for item in items:
            name = item["name"]
            value = item["value"]
            for idx, v in reversed(list(enumerate(threshold))):
                expre = "{} {} {}".format(
                    value, cell.expression, threshold[idx])
                if eval(expre):
                    if idx not in rets:
                        rets[idx] = [item]
                    else:
                        rets[idx].append(item)
                    # 触发一个
                    break

        # 整合消息
        if rets:
            # 0, 1
            msgs = []
            for idx, items in rets.items():
                items_str = []
                for item in items:
                    value = round(item["value"], 2)
                    items_str.append(
                        "{}({})".format(item["name"],
                                        "{}{}".format(value, cell.unit) if cell.unit else value))
                msg = multi_msg_template.format(**{
                    "item_num": len(items),
                    "name": cell.name,
                    "target": target,
                    "real_value": "[{}]".format(",".join(items_str)) if display_all else "",
                    "expression": {">=": "超过", "<=": "低于"}.get(cell.expression),
                    "threshold": ["预警", "告警"][idx],
                    "dangerous_level": ["存在安全风险", "处于安全紧急状态"][idx],
                    "threshold_value": "{}{}".format(threshold[idx], cell.unit) if cell.unit else threshold[idx],
                })
                msgs.append(msg)

            return True, msgs

        return False, []

    def verify(self, agent, key, max_alarm_count):
        """判断是否需要发送
        """
        timeout = 3*60*60  # 3小时
        cache_key = "ssa_alarm:{}_{}".format(key, agent.id)
        last = cache.get(cache_key)
        if last:
            logger.info(cache_key)
            logger.info(last)
            # 计算时间和次数
            if last[0] - self.start_timestamp < (60+5)*60:
                # 一小时前触发过
                if last[1] < max_alarm_count:
                    # 未到阈值
                    cache.set(
                        cache_key, [self.start_timestamp, last[1]+1], timeout)
                    return True
                else:
                    cache.set(
                        cache_key, [self.start_timestamp, last[1]+1], timeout)
                    return False
            else:
                # 一小时前未触发，首次触发
                cache.set(cache_key, [self.start_timestamp, 1], timeout)
                return True
        else:
            cache.set(cache_key, [self.start_timestamp, 1], timeout)
            return True

    def send_warning_and_alarm(self, key_name, notifys, msgs):
        """发送预警和告警
        """

        if not isinstance(msgs, list):
            msgs = [msgs]
        for msg in msgs:
            title = '告警' if "告警" in msg else "预警"
            title = "{}:{}".format(title, key_name)
            for notify in notifys:
                if notify.email == 1:
                    send_message.delay(msg_type=1, content=msg,
                                       title=title,
                                       to=notify.user.email,
                                       agent=notify.agent.id)
                    logger.info("==> {}:{} 邮件 {}".format(
                        notify.user.id, notify.user.email, msg))
                if notify.sms == 1:
                    send_message.delay(msg_type=2, content=msg,
                                       title=title,
                                       to=notify.user.userinfo.phone,
                                       agent=notify.agent.id)
                    logger.info("==> {}:{} 短信 {}".format(
                        notify.user_id, notify.user.userinfo.phone, msg))

    def virus_btw_count(self, cell, threshold):
        """僵木蠕感染数
        """
        virus_total = es_common.get_aggs_sum_data(key='virus-btw_count',
                                                  field='data.virus_btw_count',
                                                  start_time=self.start_time,
                                                  end_time=self.end_time)
        logger_it("僵木蠕感染数", virus_total)

        yes, msg = self.check_single_value(virus_total, cell, threshold)
        return yes, msg

    def virus_asset_count(self, cell, threshold):
        """感染资产数
        """
        virus_asset = es_common.get_business_es(key='vul-asset_top',
                                                field='data.virus_host_ip',
                                                start_time=self.start_time,
                                                end_time=self.end_time,
                                                count_field="data.virus_btw_count")
        virus_asset_count = 0
        for ip_count in virus_asset:
            for location, ips in self.locations_ip.items():
                if ip_count["name"] in ips:
                    virus_asset_count += 1
                    break
        logger_it("感染资产数", virus_asset_count)

        yes, msg = self.check_single_value(virus_asset_count, cell, threshold)
        return yes, msg

    def virus_single_ip_count(self, cell, threshold):
        """单IP感染数
        """
        virus_asset = es_common.get_business_es(key='virus-asset_top',
                                                field='data.virus_host_ip',
                                                start_time=self.start_time,
                                                end_time=self.end_time,
                                                count_field="data.virus_btw_count")

        logger_it("单IP感染数", virus_asset)
        # print(virus_asset)
        yes, msgs = self.check_multi_values(virus_asset, cell, threshold)
        return yes, msgs

    def virus_btw_cleared_rate(self, cell, threshold):
        """查杀率
        """
        btw_cleared_1 = es_common.get_aggs_sum_data(key='virus-btw_cleared',
                                                    field='data.virus_btw_cleared_1',
                                                    start_time=self.start_time,
                                                    end_time=self.end_time)
        btw_cleared_0 = es_common.get_aggs_sum_data(key='virus-btw_cleared',
                                                    field='data.virus_btw_cleared_0',
                                                    start_time=self.start_time,
                                                    end_time=self.end_time)
        btw_total = btw_cleared_1 + btw_cleared_0
        btw_cleared_rate = 0 if btw_total == 0 else btw_cleared_1 / \
            float(btw_total) * 100

        logger_it("查杀", btw_cleared_1)
        logger_it("未查杀", btw_cleared_0)
        logger_it("查杀率", btw_cleared_rate)

        yes, msg = self.check_single_value(btw_cleared_rate, cell, threshold)

        return yes, msg

    def virus_location_count(self):
        """单位感染数
        """
        virus_asset = es_common.get_business_es(key='vul-asset_top',
                                                field='data.virus_host_ip',
                                                start_time=self.start_time,
                                                end_time=self.end_time,
                                                count_field="data.virus_btw_count")
        # 单位感染数
        virus_loc = {"未知": 0}  # 一直保持未知是0
        for ip_count in virus_asset:
            for location, ips in self.locations_ip.items():
                # 从 locations_ip里查询ip位置 如果没查到,归为未知IP
                if location not in virus_loc:
                    virus_loc[location] = 0

                if ip_count["name"] in ips:
                    virus_loc[location] += ip_count["count"]
                    break
            # else:
            #     virus_loc["未知"] += 1
        logger_it("单位感染数", virus_loc)

    # web_status_4xx
    # web_status_5xx
    # web_throughput_peak

    def web_status_4xx(self, cell, threshold):
        """响应吗4xx
        """
        domain_status = self.get_host_http_status(start_time=self.start_time,
                                                  end_time=self.end_time)
        items = []
        for domain, status_list in domain_status.items():
            data = 0
            for status_count in status_list:
                status = status_count["web_log_http_status"]
                count = status_count["count"]
                if str(status)[0] == "4":
                    data += count

            items.append({"name": domain, "value": data})
            logger_it("响应码4xx {}".format(domain), data)

        yes, msgs = self.check_multi_values(items, cell, threshold)
        return yes, msgs

    def web_status_5xx(self, cell, threshold):
        """响应吗5xx
        """
        domain_status = self.get_host_http_status(start_time=self.start_time,
                                                  end_time=self.end_time)
        items = []
        for domain, status_list in domain_status.items():
            data = 0
            for status_count in status_list:
                status = status_count["web_log_http_status"]
                count = status_count["count"]
                if str(status)[0] == 5:
                    data += count

            items.append({"name": domain, "value": data})
            logger_it("响应码4xx {}".format(domain), data)

        yes, msgs = self.check_multi_values(items, cell, threshold)
        return yes, msgs

    def web_throughput_peak(self, cell, threshold):
        """访问流量峰值
        """
        # 访问流量峰值
        throughput_peak = 0
        x, y, _ = es_common.global_es_data(key="network-throughput",
                                           field="data.network_out_bytes",
                                           start_time=self.start_time,
                                           end_time=self.end_time)
        if self.start_time in x:
            throughput_peak = y[x.index(self.start_time)]

        throughput_peak /= float(1024*1024)
        logger_it("访问流量峰值", throughput_peak)

        yes, msg = self.check_single_value(throughput_peak, cell, threshold)

        return yes, msg

    # vul_count
    # vul_level_high_rate
    # vul_asset_rate
    # vul_single_ip_count
    # vul_localtion_count

    def vul_count(self, cell, threshold):
        """
        """
        # 漏洞总数
        vul_total = es_common.get_aggs_sum_data(key='vul-vul_total_count',
                                                field='data.vul_total_count',
                                                start_time=self.start_time,
                                                end_time=self.end_time)

        logger_it("漏洞总数", vul_total)

        yes, msg = self.check_single_value(vul_total, cell, threshold)
        return yes, msg

    def vul_level_high_rate(self, cell, threshold):
        """
        """
        # 高危漏洞占比
        vul_level = es_common.get_business_es(key='vul-vul_level_count',
                                              field='data.vul_level',
                                              start_time=self.start_time,
                                              end_time=self.end_time)
        vul_level_high = 0
        vul_level_total = 0
        for level in vul_level:
            vul_level_total += level["value"]
            if level["name"] in ['严重', "高"]:
                vul_level_high += level["value"]
        vul_high_rate = 0 if vul_level_total == 0 else vul_level_high / \
            float(vul_level_total) * 100

        logger_it("高危漏洞", vul_level_high)
        logger_it("总漏洞", vul_level_total)
        logger_it("高危漏洞占比", vul_high_rate)

        yes, msg = self.check_single_value(vul_high_rate, cell, threshold)
        return yes, msg

    def vul_asset_rate(self, cell, threshold):
        """漏洞资产占比
        """
        vul_ips = es_common.get_business_es(key='vul-vul_ip_count',
                                            field='data.vul_ip',
                                            start_time=self.start_time,
                                            end_time=self.end_time)
        vul_asset_rate = 0
        vul_asset = {"未知": 0}
        vul_ips_distinct = set([vul_ip["name"] for vul_ip in vul_ips])
        for vul_ip in vul_ips_distinct:
            for location, ips in self.locations_ip.items():
                # 从 locations_ip里查询ip位置 如果没查到,归为未知IP
                if location not in vul_asset:
                    vul_asset[location] = 0

                if vul_ip in ips:
                    vul_asset[location] += 1
                    break
            # else:
            #     vul_asset["未知"] += 1
        total_asset = sum(self.locations.values())
        vul_asset_rate = sum(vul_asset.values()) / \
            float(total_asset) * 100 if total_asset else 0

        logger_it("总资产", total_asset)
        logger_it("漏洞资产占比", vul_asset_rate)

        yes, msg = self.check_single_value(vul_asset_rate, cell, threshold)
        return yes, msg

    def vul_single_ip_count(self, cell, threshold):
        """单IP漏洞数
        """
        vul_ips = es_common.get_business_es(key='vul-vul_ip_count',
                                            field='data.vul_ip',
                                            start_time=self.start_time,
                                            end_time=self.end_time)
        logger_it("单IP漏洞数", vul_ips)
        yes, msgs = self.check_multi_values(vul_ips, cell, threshold)
        return yes, msgs

    def vul_localtion_count(self, cell, threshold):
        """
        """
        # 单位漏洞数
        vul_ips = es_common.get_business_es(key='vul-vul_ip_count',
                                            field='data.vul_ip',
                                            start_time=self.start_time,
                                            end_time=self.end_time)
        vul_loc = {"未知": 0}  # 一直保持未知是0
        for vul_ip in vul_ips:
            for location, ips in self.locations_ip.items():
                # 从 locations_ip里查询ip位置 如果没查到,归为未知IP
                if location not in vul_loc:
                    vul_loc[location] = 0

                if vul_ip["name"] in ips:
                    vul_loc[location] += vul_ip["count"]
                    break
            # else:
            #     vul_loc["未知"] += 1

        logger_it("单位漏洞数", vul_loc)
        items = []
        for n, v in vul_loc.items():
            if n != "未知":
                items.append({"name": n, "value": v})
        yes, msgs = self.check_multi_values(items, cell, threshold)
        return yes, msgs

    # attack_count
    # attack_level_high_count
    # attack_level_high_rate
    # attack_single_ip_count
    #- attack_location_count
    # attack_abnormal_throughput_peak

    def attack_count(self, cell, threshold):
        """
        """
        # 漏洞总数
        sec_total = es_common.get_aggs_sum_data(key='security-total_count',
                                                field='data.security_total_count',
                                                start_time=self.start_time,
                                                end_time=self.end_time)
        logger_it("漏洞总数", sec_total)
        yes, msg = self.check_single_value(sec_total, cell, threshold)
        return yes, msg

    def attack_level_high_count(self, cell, threshold):
        """
        """
        # 严重事件数, 严重事件占比
        sec_level = es_common.get_business_es(key='security-level_count',
                                              field='data.security_level',
                                              start_time=self.start_time,
                                              end_time=self.end_time)
        level_high = 0
        level_total = 0
        for level in sec_level:
            level_total += level["value"]
            if level["name"] in ['严重']:
                level_high += level["value"]

        sec_high_rate = 0 if level_total == 0 else level_high / \
            float(level_total)
        logger_it("严重事件数", level_high)
        # logger_it("严重事件占比", sec_high_rate)
        yes, msg = self.check_single_value(level_high, cell, threshold)
        return yes, msg

    def attack_level_high_rate(self, cell, threshold):
        """严重事件占比
        """
        sec_level = es_common.get_business_es(key='security-level_count',
                                              field='data.security_level',
                                              start_time=self.start_time,
                                              end_time=self.end_time)
        level_high = 0
        level_total = 0
        for level in sec_level:
            level_total += level["value"]
            if level["name"] in ['严重']:
                level_high += level["value"]

        sec_high_rate = 0 if level_total == 0 else level_high / \
            float(level_total) * 100
        # logger_it("严重事件数", level_high)
        logger_it("严重事件占比", sec_high_rate)
        yes, msg = self.check_single_value(sec_high_rate, cell, threshold)
        return yes, msg

    def attack_single_ip_count(self, cell, threshold):
        """
        """
        # 单IP攻击事件数
        sec_ips = es_common.get_business_es(key='security-dst_ip_count',
                                            field='data.security_dst_ip',
                                            start_time=self.start_time,
                                            end_time=self.end_time)
        logger_it("单IP攻击事件数", sec_ips)
        yes, msgs = self.check_multi_values(sec_ips, cell, threshold)
        return yes, msgs

    def attack_abnormal_throughput_peak(self, cell, threshold):
        """
        """
        # 异常流量峰值
        abnormal_throughput_peak = self.get_abnormal_throughput_peak(
            start_time=self.start_time,
            end_time=self.end_time
        )
        abnormal_throughput_peak /= float(1024*1024)
        logger_it("异常流量峰值", abnormal_throughput_peak)

        yes, msg = self.check_single_value(
            abnormal_throughput_peak, cell, threshold)
        return yes, msg
        return False, ""

    def get_location(self, locations, locations_ip, models, idcs):
        """位置对应的资产IP以及资产总数
        """
        for idc in idcs:
            if models == 'server':
                host_list = idc.server_set.all()
            elif models == 'netdevice':
                host_list = idc.netdevice_set.all()
            else:
                host_list = idc.terminal_set.all()

            if not idc.location:
                locations['未知'] = locations['未知'] + idc.mynum
                locations_ip['未知'] = locations_ip['未知'] + \
                    [x.ip for x in host_list]
            else:
                if idc.location.name not in locations:
                    locations[idc.location.name] = 0
                    locations_ip[idc.location.name] = []

                locations[idc.location.name] = locations[idc.location.name] + idc.mynum
                locations_ip[idc.location.name] = locations_ip[idc.location.name] + \
                    [x.ip for x in host_list]

    def get_host_http_status(self, start_time, end_time):
        """网站http状态统计
        """

        body = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {"key": "web-log-http_status_count"}
                        }, {
                            "range": {"time": {"gte": start_time}}
                        },
                        {
                            "range": {"time": {"lt": end_time}}
                        }
                    ]
                }
            },
            "aggs": {
                "top_host": {
                    "top_hits": {
                        "sort": [
                            {
                                "data.web_log_http_status_total_count": {
                                    "order": "desc"
                                }
                            }
                        ],
                        "_source": {},
                        "size": 100
                    }
                }
            }
        }
        result = es_common.get_es_data(body, size=0)
        domains = {}
        if result:
            hits = result.get('aggregations', {}).get(
                'top_host', {}).get("hits", {}).get("hits", [])
            for da in hits:
                data = da.get("_source", {}).get("data", {})
                # [{
                #     "count": 17,
                #     "web_log_http_status": 502
                # },]
                status_list = data.get("web_log_http_status_count", [])
                domain = data.get("web_log_host", "")
                if domain:
                    domains[domain] = status_list
        return domains

    def get_abnormal_throughput_peak(self, start_time, end_time):
        """异常流量峰值，一小时
        """
        body = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {"key": "network-abnormal_throughput_peak"}
                        },
                        {
                            "range": {"time": {"gte": start_time}}
                        },
                        {
                            "range": {"time": {"lt": end_time}}
                        }
                    ]
                }
            },
            "aggs": {
                "mydata": {
                    "max": {"field": "data.network_max_in_bytes"}
                }
            }
        }
        result = es_common.get_es_data(body, size=0, days=2)
        if result:
            data = result.get("aggregations", {}).get(
                "mydata", {}).get("value")
            if not data:
                data = 0
        return data
