# coding: utf-8
from __future__ import division

import logging
import json
import math

from datetime import datetime, timedelta

from rest_framework.response import Response
from rest_framework.views import APIView
from kafka import KafkaConsumer, TopicPartition

from common import soc_cache
from soc_assets.models import Assets, TermGroup
from soc.settings import KAFKA_HOSTS, KAFKA_TOPICS

from utils.es_select import exec_es_sql

logger = logging.getLogger('soc_ssa')


class OverallScore(APIView):
    """
    安全评分
    """

    @soc_cache(timeout=60 * 30, key="_home_overall_score", level="user")
    def post(self, request):
        """
        安全评分
        """

        day = datetime.now().strftime('%Y-%m-%d')
        index = 'all-event-{}-*'.format(day)
        sql = 'SELECT event_source,event_level,sum(event_total) count_ FROM {} where event_level>0 ' \
              'group by event_source,event_level order by event_source'.format(index)
        result = exec_es_sql(sql=sql)
        score, event_name, event_score = get_score(result)

        total_sql = 'SELECT sum(event_total) count_ FROM all-event-* where event_level>0 '
        total_result = exec_es_sql(sql=total_sql)
        total_count = 0
        if total_result:
            total_count = total_result[0]['count_']

        today_sql = 'SELECT sum(event_total) count_ FROM all-event-{}-* where event_level>0 '.format(day)
        today_result = exec_es_sql(sql=today_sql)
        today_count = 0
        if today_result:
            today_count = today_result[0]['count_']
        up = 0.0
        if total_count:
            up = today_count * 100 / total_count
        data = {
            "score": int(math.floor(score)),
            "total": int(math.floor(total_count)),
            "up": '{}%'.format(str(round(up, 2)))
        }
        return Response({"status": 200, "data": data})


class EventTypeScore(APIView):
    """
    设备风险指数比例
    """

    @soc_cache(timeout=60 * 30, key="_event_type_score", level="user")
    def post(self, request):
        """
        设备风险指数比例
        """
        day = datetime.now().strftime('%Y-%m-%d')
        index = 'all-event-{}-*'.format(day)
        sql = 'SELECT event_source,event_level,sum(event_total) count_ FROM {} where event_level>0 ' \
              'group by event_source,event_level order by event_source'.format(index)
        result = exec_es_sql(sql=sql)
        score, event_name, event_score = get_score(result)
        data = []
        for index, name in enumerate(event_name):
            data.append({
                'name': name,
                'value': int(math.floor(event_score[index]))
            })
        return Response({"status": 200, "data": data})


class AssetRiskTop5(APIView):
    """
    风险资产TOP5
    """

    @soc_cache(timeout=60 * 30, key="_asset_risk_top5", level="user")
    def post(self, request):
        """
        风险资产TOP10
        """

        day = datetime.now().strftime('%Y-%m-%d')
        index = 'all-event-{}-*'.format(day)
        sql = 'SELECT event_host,sum(event_total) count_ FROM {} ' \
              'where event_level>0 and event_host<>"" ' \
              'group by event_host order by count_ desc limit 5'.format(index)
        result = exec_es_sql(sql=sql)
        data = []
        for item in result:
            data.append({
                "name": item['event_host'],
                "value": item['count_']
            })
        return Response({"status": 200, "data": data})


class NewEvent(APIView):
    """
    最新事件
    """

    # @soc_cache(timeout=60 * 30, key="_new_event", level="user")
    def post(self, request):
        """
        最新事件
        """
        '''
        day = datetime.now().strftime('%Y-%m-%d')

        num_ = random.randint(6, 20)
        sql = 'select event_three_type,event_source,event_host,start_time ' \
              'from all-event-{0}-* order by start_time desc limit {1} '.format(day, num_)
        result = exec_es_sql(sql=sql)
        data = []
        source_name = [u'防火墙', u'数据库审计', u'IDS', u'隔离设备', u'摆渡设备', u'终端', u'杀毒软件']
        source_type = [1, 3, 2, 5, 4, 7, 6]
        for item in result:
            data.append({
                "name": source_name[source_type.index(item['event_source'])],
                "app": item['event_three_type'],
                "ip": item['event_host'],
                "time": item['start_time']
            })
        return Response({"status": 200, "data": data})
        '''
        result = self.get_kafka_data()
        return Response({"status": 200, "data": result})

    def get_kafka_data(self):
        result = []
        try:
            consumer = KafkaConsumer(KAFKA_TOPICS,
                                     bootstrap_servers=KAFKA_HOSTS,
                                     consumer_timeout_ms=1000)
            topics = consumer.topics()  # 获取主题列表
            assignment = consumer.assignment()  # 获取当前消费者topic、分区信息
            # 获取当前消费者可消费的偏移量
            end_offsets = consumer.end_offsets(assignment)
            offset = end_offsets[end_offsets.keys()[0]]
            offset = offset - 5 if offset >= 5 else offset
            consumer.seek(TopicPartition(topic=KAFKA_TOPICS, partition=0), offset)  # 重置偏移量，从第5个偏移量消费

            for message in consumer:
                content = json.loads(message.value)
                for item in content:
                    result.append({
                        "name": item['event_top_type'],
                        "app": item['event_type'],
                        "ip": item['dev_ip'],
                        "time": datetime.strptime(item['event_time'], "%Y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
                    })
                if message.offset == offset - 1:
                    break
            consumer.close()
        except Exception as e:
            logger.error(e)

        return result


class EventTypeCount(APIView):
    """
    事件总数
    """

    @soc_cache(timeout=60 * 30, key="_event_type_count", level="user")
    def post(self, request):
        """
        事件总数
        """

        day = datetime.now().strftime('%Y-%m-%d')
        index = 'all-event-{}-*'.format(day)
        sql = 'SELECT event_source,sum(event_total) count_ FROM {} where event_level>0 group by source'.format(index)
        result = exec_es_sql(sql=sql)
        data = []
        total_count = 0
        for item in result:
            total_count = total_count + item['count_']

        event_name = ['防火墙', 'IDS', '数据库审计', '摆渡设备', '隔离设备', '杀毒软件', '终端']
        event_type = [1, 2, 3, 4, 5, 6, 7]

        for item in result:
            count = item['count_']
            percent = 0.0
            if total_count:
                percent = round(count * 100 / total_count, 2)
            index = event_type.index(item['event_source'])
            data.append({
                "name": event_name[index],
                "value": count,
                "percent": '{}%'.format(str(percent))
            })

        return Response({"status": 200, "data": data})


class EventTrend(APIView):
    """
    事件趋势
    """

    @soc_cache(timeout=60 * 30, key="_event_trend", level="user")
    def post(self, request):
        """
        事件趋势
        """

        day = datetime.now().strftime('%Y-%m-%d')
        index = 'all-event-{}-*'.format(day)
        sql = 'select sum(event_total) count_ from {} where event_level>0 ' \
              'group by date_histogram(field=\'start_time\',\'interval\'=\'1h\')'.format(index)
        result = exec_es_sql(sql=sql)
        x_data = []
        y_data = []
        for item in result:
            x_data.append(item['date_histogram(field=start_time,interval=1h)'][11:13])
            y_data.append(item['count_'])
        data = {"x": x_data, "y": y_data}
        return Response({"status": 200, "data": data})


class AssetStatus(APIView):
    """
    设备状态
    """

    @soc_cache(timeout=60 * 30, key="_asset_status", level="user")
    def post(self, request):
        """
        设备状态
        """
        day = datetime.strftime(datetime.now(), "%Y-%m-%d")
        index = get_day7_index('statistics-*')
        sql = 'select log_source,count(distinct terminal) count_ from {0}  ' \
              'group by log_source'.format(index)
        result = exec_es_sql(sql=sql)
        labes = [u'数据库审计', u'IDS', u'隔离设备', u'摆渡设备', u'360', u'终端']
        event_source_type = [3, 2, 5, 4, 6, 7]
        for item in result:
            log_source = item['log_source']
            if u'防火墙' in log_source and log_source not in labes:
                labes.append(log_source)
                event_source_type.append(1)

        data = []
        for index, lab in enumerate(labes):
            assets_num, normal, off, abnormal = 0, 0, 0, 0
            for item in result:
                if item['log_source'] == lab:
                    assets_num = item['count_']
                    continue
            # 防火墙
            where = ''
            if event_source_type[index] == 1:
                where = ' and event_host=\'\' '.format(lab.replace(u'防火墙', ''))
            assets_sql = 'SELECT event_source,count(distinct event_host) count_,sum(event_total) sum_ ' \
                         'FROM all-event-{}-* where event_source={} {} ' \
                         'group by event_source'.format(day, event_source_type[index], where)
            assets_count = exec_es_sql(sql=assets_sql)
            if assets_count:
                normal = assets_count[0]['count_']
                abnormal = assets_count[0]['sum_']

            if normal > assets_num:
                assets_num = normal
                off = 0
            else:
                off = assets_num - normal
            if lab == '360':
                data.append({"type": u'杀毒软件', "num": assets_num, "normal": normal, "off": off, "abnormal": abnormal})
            else:
                data.append({"type": lab, "num": assets_num, "normal": normal, "off": off, "abnormal": abnormal})
        return Response({"status": 200, "data": data})


class EventRiskTop5(APIView):
    """
    风险事件TOP5
    """

    @soc_cache(timeout=60 * 30, key="_event_risk_top5", level="user")
    def post(self, request):
        """
        风险事件TOP5
        """

        day = datetime.now().strftime('%Y-%m-%d')
        index = 'all-event-{}-*'.format(day)
        sql = 'SELECT event_three_type,sum(event_total) count_ FROM {} ' \
              'where event_level>0 and event_three_type<>"" ' \
              'group by event_three_type order by count_ desc limit 5'.format(index)
        result = exec_es_sql(sql=sql)
        data = []
        for item in result[0:5]:
            data.append({
                "name": item['event_three_type'],
                "count": item['count_']
            })

        return Response({"status": 200, "data": data})


class RiskState(APIView):
    '''
    风险状态
    '''

    @soc_cache(timeout=60 * 30, key="_risk_state", level="user")
    def post(self, request):
        '''
        风险状态
        '''
        index = get_day7_index('all-event')
        sql = 'select event_three_type,sum(event_total) count_  from {0} ' \
              'where event_level>0 and event_three_type<>"" ' \
              'group by event_three_type order by count_ desc'.format(index)
        result = exec_es_sql(sql=sql)
        data = []
        for item in result:
            data.append({
                "name": item['event_three_type'],
                "value": item['count_']
            })
        return Response({"status": 200, "data": data})


class EventCount(APIView):
    '''
    事件统计
    '''

    @soc_cache(timeout=60 * 30, key="_event_count", level="user")
    def post(self, request):
        '''
        事件统计
        '''
        index = get_day7_index('all-event')
        event_type_sql = 'select event_one_type,count(*) count_ from {0} ' \
                         'where event_level>0 group by event_one_type order by count_ desc'.format(index)
        event_type_result = exec_es_sql(sql=event_type_sql)
        data, norule, attack, viruses = dict(), 0, 0, 0
        for item in event_type_result:
            if item['event_one_type'] == u'攻击':
                attack = item['count_']
            elif item['event_one_type'] == u'违规':
                norule = item['count_']
            elif item['event_one_type'] == u'病毒':
                viruses = item['count_']
            else:
                pass
        event_source_sql = 'select event_source,sum(event_total) count_ from {0}  ' \
                           'where event_level>0 group by event_source order by count_ desc'.format(index)
        event_source_result = exec_es_sql(sql=event_source_sql)

        event_source_data = []
        source_name = [u'数据库审计', u'IDS', u'隔离设备', u'摆渡设备', u'终端', u'杀毒软件']
        source_type = [3, 2, 5, 4, 7, 6]
        source_data = [0, 0, 0, 0, 0, 0]
        for item in event_source_result:
            if item['event_source'] in source_type:
                i = source_type.index(item['event_source'])
                source_data[i] += item['count_']
                continue
        for i in range(len(source_name)):
            event_source_data.append({
                'name': source_name[i],
                'value': source_data[i]
            })
        # 防火墙
        event_source_fw_sql = 'select event_host,sum(event_total) count_ from {0}  ' \
                              'where event_level>0 and event_source=1 ' \
                              'group by event_host order by count_ desc'.format(index)
        event_source_fw_result = exec_es_sql(sql=event_source_fw_sql)
        for fw in event_source_fw_result:
            event_source_data.append({
                'name': '防火墙{}'.format(fw['event_host']),
                'value': fw['count_']
            })
        data = {
            'event_type': {'norule': norule, 'attack': attack, 'viruses': viruses},
            'event_source': event_source_data
        }
        return Response({"status": 200, "data": data})


class AssetsEventTrend(APIView):
    '''
    设备事件情况
    '''

    @soc_cache(timeout=60 * 30, key="_asset_event_trend", level="user")
    def post(self, request):
        '''
        设备事件情况
        '''
        start_time = datetime.strftime(datetime.now() - timedelta(days=6), "%Y%m%d%H%M%S")
        end_time = datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")
        index = get_day7_index('all-event')
        sql = 'select event_source,event_host,sum(event_total) count_ from {0} ' \
              'where start_time>=\'{1}\' and start_time<\'{2}\' and event_level>0 ' \
              'group by date_histogram(field=\'start_time\',\'interval\'=\'1d\') ' \
              ',event_source,event_host order by  start_time'.format(index, start_time, end_time)
        result = exec_es_sql(sql=sql)
        days, data_list = [], []

        source_name = [u'数据库审计', u'IDS', u'隔离设备', u'摆渡设备', u'终端', u'杀毒软件']
        source_type = [3, 2, 5, 4, 7, 6]
        for item in result:
            day = item['date_histogram(field=start_time,interval=1d)'][0:10]
            if day not in days:
                days.append(day)
            if item['event_source'] == 1:
                event_source = u'防火墙{}'.format(item['event_host'])
                if event_source not in source_name:
                    source_name.append(event_source)

        for index, source in enumerate(source_name):
            data_dict = {
                'name': source,
                'data': []
            }
            for d in range(len(days)):
                event_count = 0
                for item in result:
                    if item['event_source'] == 1:
                        event_source = u'防火墙{}'.format(item['event_host'])
                    else:
                        event_source = source_name[source_type.index(item['event_source'])]

                    day = item['date_histogram(field=start_time,interval=1d)'][0:10]
                    if day == days[d] and source == event_source:
                        event_count += item['count_']
                data_dict['data'].append(event_count)
            data_list.append(data_dict)
        data = {'days': days, 'labes': source_name, 'data': data_list}
        return Response({"status": 200, "data": data})


class NetworkFlow(APIView):
    '''
    网络流量
    '''

    @soc_cache(timeout=60 * 30, key="_network_flow", level="user")
    def post(self, request):
        '''
        网络流量
        '''
        start_time = datetime.strftime(datetime.now() - timedelta(days=6), "%Y%m%d%H%M%S")
        end_time = datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")
        index = get_day7_index('all-event')
        sql = 'select event_source,event_host,sum(flow) count_ from {0} ' \
              'where start_time>=\'{1}\' and start_time<\'{2}\' and event_level>0 and event_source in (1,5) ' \
              'group by date_histogram(field=\'start_time\',\'interval\'=\'1d\') ' \
              ',event_source,event_host order by  start_time'.format(index, start_time, end_time)
        result = exec_es_sql(sql=sql)
        days, data_list = [], []

        source_name = [u'隔离设备']
        source_type = [5]
        for item in result:
            day = item['date_histogram(field=start_time,interval=1d)'][0:10]
            if day not in days:
                days.append(day)
            if item['event_source'] == 1:
                event_source = u'防火墙{}'.format(item['event_host'])
                if event_source not in source_name:
                    source_name.append(event_source)

        for index, source in enumerate(source_name):
            data_dict = {
                'name': source,
                'data': []
            }
            for d in range(len(days)):
                event_count = 0
                for item in result:
                    if item['event_source'] == 1:
                        event_source = u'防火墙{}'.format(item['event_host'])
                    else:
                        event_source = source_name[source_type.index(item['event_source'])]

                    day = item['date_histogram(field=start_time,interval=1d)'][0:10]
                    if day == days[d] and source == event_source:
                        event_count += item['count_']
                data_dict['data'].append(event_count)
            data_list.append(data_dict)
        data = {'days': days, 'labes': source_name, 'data': data_list}
        return Response({"status": 200, "data": data})


class TerminalLevel(APIView):
    '''
    检查结果风险统计
    '''

    @soc_cache(timeout=60 * 30, key="_terminal_level", level="user")
    def post(self, request):
        '''
        检查结果风险统计
        '''
        index = get_day7_index('ssa-event-terminal')
        sql = 'SELECT event_level,count(*) count_ FROM {0}  ' \
              'group by event_level order by event_level'.format(index)
        result = exec_es_sql(sql=sql)
        labels = ['low', 'mid', 'high', 'super']
        series = [0, 0, 0, 0]
        data = dict()
        for item in result:
            if item['event_level'] == 1 or item['event_level'] == '1':
                series[0] = item['count_']
            elif item['event_level'] == 2 or item['event_level'] == '2':
                series[1] = item['count_']
            elif item['event_level'] == 3 or item['event_level'] == '3':
                series[2] = item['count_']
            elif item['event_level'] == 4 or item['event_level'] == '4':
                series[3] = item['count_']
            else:
                pass
        for i in range(len(labels)):
            data[labels[i]] = series[i]
        return Response({"status": 200, "data": data})


class FoulTypeCount(APIView):
    '''
    违规类型统计
    '''

    @soc_cache(timeout=60 * 30, key="_foul_type_count", level="user")
    def post(self, request):
        '''
        违规类型统计
        '''

        index = get_day7_index('all-event')
        sql = 'SELECT event_two_type,count(*) count_  FROM {} where event_one_type=\'违规\' ' \
              'group by event_two_type order by count_ desc'.format(index)
        result = exec_es_sql(sql=sql)
        data = []
        for item in result:
            data.append({
                "name": item['event_two_type'],
                "value": item['count_']
            })
        return Response({"status": 200, "data": data})


class VirusTypeCount(APIView):
    '''
    病毒类型统计
    '''

    @soc_cache(timeout=60 * 30, key="_virus_type_count", level="user")
    def post(self, request):
        '''
        病毒类型统计
        '''

        index = get_day7_index('all-event')
        sql = 'SELECT event_three_type,count(*) count_  FROM {} where event_one_type=\'病毒\' ' \
              'group by event_three_type order by count_ desc'.format(index)
        result = exec_es_sql(sql=sql)
        data = []
        for item in result:
            data.append({
                "name": item['event_three_type'],
                "value": item['count_']
            })
        return Response({"status": 200, "data": data})


class AttackTypeCount(APIView):
    '''
    攻击类型统计
    '''

    @soc_cache(timeout=60 * 30, key="_attack_type_count", level="user")
    def post(self, request):
        '''
        攻击类型统计
        '''

        index = get_day7_index('all-event')
        sql = 'SELECT event_two_type,count(*) count_  FROM {} where event_one_type=\'攻击\' ' \
              'group by event_two_type order by count_ desc'.format(index)
        result = exec_es_sql(sql=sql)
        data = []
        for item in result:
            data.append({
                "name": item['event_two_type'],
                "value": item['count_']
            })
        return Response({"status": 200, "data": data})


class FoulOrgCount(APIView):
    '''
    违规单位统计
    '''

    @soc_cache(timeout=60 * 30, key="_foul_org_count", level="user")
    def post(self, request):
        '''
        违规单位统计
        '''
        index = get_day7_index('all-event')
        sql = 'SELECT organization,count(*) count_ FROM {0} ' \
              'where organization<>\'\' and event_one_type=\'违规\' ' \
              'group by organization order by count_ desc limit 5'.format(index)
        result = exec_es_sql(sql=sql)
        lables, series = [], []
        for item in result:
            lables.append(item['organization'])
            series.append(item['count_'])
        data = {'lables': lables, 'series': series}
        return Response({"status": 200, "data": data})


class VirusCount(APIView):
    '''
    病毒单位统计
    '''

    @soc_cache(timeout=60 * 30, key="_virus_count", level="user")
    def post(self, request):
        '''
        病毒单位统计
        '''
        index = get_day7_index('ssa-ag-360')
        sql = 'select virusname,count(*) count_ from {} ' \
              'group by virusname order by count_ desc limit 5'.format(index)
        result = exec_es_sql(sql=sql)
        lables, series = [], []
        for item in result:
            lables.append(item['virusname'])
            series.append(item['count_'])
        data = {'lables': lables, 'series': series}
        return Response({"status": 200, "data": data})


class TerminalFoulOperate(APIView):
    '''
    终端操作违规
    '''

    @soc_cache(timeout=60 * 30, key="_terminal_foul_operate", level="user")
    def post(self, request):
        '''
        终端操作违规
        '''
        index = get_day7_index('ssa-event-terminal')
        sql = 'SELECT terminal,count(*) count_ FROM {0}  ' \
              'group by terminal order by count_ desc limit 5'.format(index)
        result = exec_es_sql(sql=sql)
        lables, series = [], []
        for item in result:
            lables.append(item['terminal'])
            series.append(item['count_'])
        data = {'lables': lables, 'series': series}
        return Response({"status": 200, "data": data})


class OrgRiskCount(APIView):
    '''
    部门风险统计
    '''

    @soc_cache(timeout=60 * 30, key="_org_risk_count", level="user")
    def post(self, request):
        '''
        部门风险统计
        '''
        index = get_day7_index('ssa-event-terminal')
        sql = 'select organization,event_level,count(*) count_ from {0} ' \
              'group by organization,event_level'.format(index)
        result = exec_es_sql(sql=sql)
        data, org = [], dict()

        for item in result:
            if item['organization'] not in org:
                org[item['organization']] = 0
            if item['event_level'] == 1:
                org[item['organization']] += item['count_'] * 0.2
            elif item['event_level'] == 2:
                org[item['organization']] += item['count_'] * 0.3
            elif item['event_level'] == 3:
                org[item['organization']] += item['count_'] * 0.5
            else:
                pass

        for key in org:
            data.append({
                "name": key,
                "value": int(org[key])
            })
        data = sorted(data, key=lambda s: s['value'], reverse=True)
        if len(data) >= 5:
            data = data[0:5]
        lables, series = [], []
        for item in data:
            lables.append(item['name'])
            series.append(item['value'])
        ret_data = {'lables': lables, 'series': series}

        return Response({"status": 200, "data": ret_data})


class AttackSrcipCount(APIView):
    '''
    攻击源统计
    '''

    @soc_cache(timeout=60 * 30, key="_attack_src_ip_count", level="user")
    def post(self, request):
        '''
        攻击源统计
        '''

        index = get_day7_index('all-event')
        sql = 'select src_ip,sum(event_total) count_ from {0} ' \
              'where src_ip <> "" and event_level>0 ' \
              'group by src_ip order by count_ desc limit 5'.format(index)
        result = exec_es_sql(sql=sql)
        lables, series = [], []
        for item in result:
            lables.append(item['src_ip'])
            series.append(item['count_'])
        data = {'lables': lables, 'series': series}
        return Response({"status": 200, "data": data})


class AttackDstipCount(APIView):
    '''
    被攻击终端统计
    '''

    @soc_cache(timeout=60 * 30, key="_attack_dst_ip_count", level="user")
    def post(self, request):
        '''
        被攻击终端统计
        '''

        index = get_day7_index('all-event')
        sql = 'select dst_ip,sum(event_total) count_ from {0} ' \
              'where dst_ip <> "" and event_level>0 ' \
              'group by dst_ip order by count_ desc limit 5'.format(index)
        result = exec_es_sql(sql=sql)
        data = []
        lables, series = [], []
        for item in result:
            lables.append(item['dst_ip'])
            series.append(item['count_'])
        data = {'lables': lables, 'series': series}
        return Response({"status": 200, "data": data})


class RiskIpOrgCount(APIView):
    '''
    风险IP和风险部门数量统计
    '''

    @soc_cache(timeout=60 * 30, key="_risk_ip_org_count", level="user")
    def post(self, request):
        '''
        风险IP和风险部门数量统计
        '''

        index = get_day7_index('all-event')
        org_sql = 'SELECT organization,count(*) FROM {} where event_level>0 ' \
                  'group by organization'.format(index)
        org_list = exec_es_sql(sql=org_sql)

        ip_sql = 'SELECT event_host,count(*) FROM {} where event_level>0 ' \
                 'group by event_host'.format(index)
        ip_list = exec_es_sql(sql=ip_sql)

        result = {
            'org_size': len(org_list),
            'ip_size': len(ip_list)
        }
        return Response({"status": 200, "data": result})


class AllEventCount(APIView):
    '''
    全局事件统计
    '''

    # @soc_cache(timeout=60 * 30, key="_all_event_count", level="user")
    def post(self, request):
        '''
        全局事件统计
        '''
        type = request.data.get('type')
        index = get_day7_index('all-event')
        # 默认
        if not type:
            type = u'攻击'
        if type == '全部':
            return get_all_event_count(index)
        # 攻击类事件数、日志量
        total, num = 0, 0
        count_sql = 'select count(*) count_,sum(event_total) sum_ from {} ' \
                    'where event_one_type=\'{}\' and event_level>0'.format(index, type)
        count_list = exec_es_sql(sql=count_sql)
        if len(count_list) > 0:
            total = count_list[0]['count_']
            num = count_list[0]['sum_']

        # 事件类型数量
        count_type_sql = 'select event_three_type,count(*) count_ from {} ' \
                         'where event_one_type=\'{}\' and event_level>0 ' \
                         'group by event_three_type'.format(index, type)
        count_type_list = exec_es_sql(sql=count_type_sql)

        # 攻击源ip数量
        src_ip_sql = 'select src_ip,count(*) count_ from {} ' \
                     'where event_one_type=\'{}\' and event_level>0 ' \
                     'group by src_ip'.format(index, type)
        src_ip_list = exec_es_sql(sql=src_ip_sql)
        # 被攻击ip数量
        dst_ip_sql = 'select dst_ip,count(*) count_ from {} ' \
                     'where event_one_type=\'{}\' and event_level>0 ' \
                     'group by dst_ip'.format(index, type)
        dst_ip_list = exec_es_sql(sql=dst_ip_sql)

        event_type_list = []  # 事件类型
        attack_ip_list = []  # 攻击源ip
        attacked_ip_list = []  # 被攻击ip
        attacked_org_list = []  # 被攻击单位
        for item in count_type_list:
            event_type = item['event_three_type']
            event_type_list.append({
                'name': event_type,
                'value': item['count_']
            })
            # 攻击源ip
            event_src_ip_sql = 'select src_ip,count(*) count_ from {} ' \
                               'where event_level>0 and event_one_type=\'{}\' and  event_three_type=\'{}\' ' \
                               'group by src_ip order by count_ desc limit 5'.format(index, type, event_type)
            event_src_ip_list = exec_es_sql(sql=event_src_ip_sql)
            attack_ip_list.append([event['src_ip'] for event in event_src_ip_list])

            # 被攻击ip
            event_dst_ip_sql = 'select dst_ip,count(*) count_ from {} ' \
                               'where event_level>0 and event_one_type=\'{}\' and  event_three_type=\'{}\' ' \
                               'group by dst_ip order by count_ desc limit 5'.format(index, type, event_type)
            event_dst_ip_list = exec_es_sql(sql=event_dst_ip_sql)
            attacked_ip_list.append([event['dst_ip'] for event in event_dst_ip_list])
            org_name_list = []
            for dst in event_dst_ip_list:
                org_name = ''
                assets_list = Assets.objects.filter(ip=dst['dst_ip'])
                if assets_list:
                    org_list = TermGroup.objects.filter(term_group_id=assets_list.first().term_group_id)
                    if org_list:
                        org_name = org_list.first().term_group_name
                org_name_list.append(org_name)
            attacked_org_list.append(org_name_list)

        result = {
            'total': total,
            'num': num,
            'type': len(count_type_list),
            'src_ip': len(src_ip_list),
            'dst_ip': len(dst_ip_list),
            'name': '{}类事件数'.format(type),
            'event': event_type_list,
            'attackIp': attack_ip_list,
            'attackedIp': attacked_ip_list,
            'attackedOrg': attacked_org_list,
        }
        return Response({"status": 200, "data": result})


def get_all_event_count(index):
    '''
    全部事件统计
    '''
    total, num = 0, 0
    count_sql = 'select count(*) count_,sum(event_total) sum_ from {} ' \
                'where event_level>0'.format(index)
    count_list = exec_es_sql(sql=count_sql)
    if len(count_list) > 0:
        total = count_list[0]['count_']
        num = count_list[0]['sum_']
    attack, viruse, outline = 0, 0, 0
    # 攻击
    attack_sql = 'select event_one_type,count(DISTINCT dst_ip) count_ from {} ' \
                 'where event_level>0 and event_one_type=\'攻击\' ' \
                 'group by event_one_type,dst_ip'.format(index)
    attack_list = exec_es_sql(sql=attack_sql)
    if len(attack_list) > 0:
        attack = attack_list[0]['count_']
    # 病毒
    viruses_sql = 'select event_one_type,count(DISTINCT src_ip) count_ from {} ' \
                  'where event_level>0 and event_one_type=\'病毒\' ' \
                  'group by event_one_type,src_ip'.format(index)
    viruses_list = exec_es_sql(sql=viruses_sql)
    if len(viruses_list) > 0:
        viruse = viruses_list[0]['count_']
    # 违规
    outline_sql = 'select event_one_type,count(DISTINCT dst_ip) count_ from {} ' \
                  'where event_level>0 and event_one_type=\'违规\' ' \
                  'group by event_one_type,dst_ip'.format(index)
    outline_list = exec_es_sql(sql=outline_sql)
    if len(outline_list) > 0:
        outline = outline_list[0]['count_']
    result = {
        'total': total,
        'num': num,
        'type': attack,  # 攻击
        'src_ip': viruse,  # 病毒
        'dst_ip': outline,  # 违规
        'name': '事件总数',
        'event': [],
        'attackIp': [],
        'attackedIp': [],
        'attackedOrg': [],
    }
    return Response({"status": 200, "data": result})


def get_day7_index(index):
    '''最近7天索引 '''
    indexs = []
    for i in range(6):
        day = datetime.strftime(datetime.now() - timedelta(days=i), "%Y-%m-%d")
        indexs.append('{0}-{1}-*'.format(index, day))
    return ','.join(indexs)


def get_score(data):
    '''
    计算全网风险指数
    '''
    score = 0
    event_name = ['防火墙', 'IDS', '数据库审计', '摆渡设备', '隔离设备', '杀毒软件', '终端']
    event_type = [1, 2, 3, 4, 5, 6, 7]
    event_score = [0, 0, 0, 0, 0, 0, 0]
    event_type_power = [5, 4, 2, 3, 3, 6, 5]
    event_level_power = [[0.2, 0.3, 0.5], [0.1, 0.3, 0.6], [0.2, 0.3, 0.5], [0.2, 0.4, 0.4], [0.2, 0.4, 0.4],
                         [0.1, 0.3, 0.6], [0.2, 0.3, 0.5]]
    event_level_total = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for item in data:
        type = item['event_source']
        level = item['event_level']
        index = event_type.index(type)
        event_level_total[index][level - 1] = item['count_']

    for index, total in enumerate(event_level_total):
        power = event_level_power[index]
        total_ = total[0] + total[1] + total[2]
        if total_ > 0:
            event_score[index] = 100 * (total[0] * power[0] + total[1] * power[1] + total[2] * power[2]) / (
                total_)
        else:
            event_score[index] = 0

    event_power = event_type_power[0] + event_type_power[1] + event_type_power[2] + event_type_power[3] + \
                  event_type_power[4] + event_type_power[5] + event_type_power[6]
    if event_power > 0:
        score = (event_score[0] * event_type_power[0] + \
                 event_score[1] * event_type_power[1] + \
                 event_score[2] * event_type_power[2] + \
                 event_score[3] * event_type_power[3] + \
                 event_score[4] * event_type_power[4] + \
                 event_score[5] * event_type_power[5] + \
                 event_score[6] * event_type_power[6]) / (event_power)
    else:
        score = 0
    return score, event_name, event_score
