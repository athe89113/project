# coding=utf-8
import requests
import json

from datetime import datetime

from django.db.models import Q

from soc_ssa import models

from kafka import KafkaConsumer
from kafka import TopicPartition
from kafka.errors import KafkaError
from elasticsearch import Elasticsearch

from django.db.models import F
from django.db import transaction
from django.conf import settings
from django.utils import timezone

AGG_MAP = {
    "SUM": "求和",
    "AVG": "平均值",
    "MAX": "最大值",
    "MIN": "最小值",
    "COUNT": "计数",
    "DISTINCT": "去重计数",
}


def exec_elasticsearch_sql(es_host, sql):
    if "http" not in es_host:
        es_host = "http://{}/_sql".format(es_host)
    result = requests.post(es_host, data=str(sql).encode('utf-8'), timeout=30,
                           headers={"Connection": "close", "Content-Type": "application/json"})
    try:
        result = result.json()
    except (ValueError, TypeError) as e:
        return False, e
    if result.get('status') == 500:
        return False, result.get('error')
    return True, result


def select_from_kafka(topic):
    """
    从kafak读取数据，作为预览
    """
    c = KafkaConsumer(group_id="python", bootstrap_servers='127.0.0.1:9092')
    # 指定偏移位读取数据
    c.assign([TopicPartition(topic, 0)])
    c.seek_to_beginning()
    try:
        for message in c:
            if message.offset > 10:
                break
            print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                                 message.offset, message.key,
                                                 message.value))
    except KeyboardInterrupt as e:
        print(e)


def _parse_es_buckets(buckets, base_dict, base_key, data):
    """
    递归去解析bucket
    """
    othter_key = ['doc_count_error_upper_bound', 'sum_other_doc_count', 'key', 'doc_count']
    for item in buckets:
        new_base_key = filter(lambda x: x not in othter_key, item.keys())[0]
        item[base_key] = item['key']
        item.update(base_dict)
        if "buckets" in item[new_base_key]:
            new_item = item[new_base_key]
            del item[new_base_key]
            data = _parse_es_buckets(new_item['buckets'], item, new_base_key, data)
        else:
            for k, v in item.items():
                if isinstance(v, dict):
                    item[k] = v['value']
            del item['key']
            del item['doc_count']
            data.append(item)
    return data


def parse_es_buckets(aggregations):
    data = []
    for k, v in aggregations.items():
        if v.get("buckets"):
            data = _parse_es_buckets(v.get("buckets"), base_dict={}, base_key=k, data=data)
        # 支持 SUM AVG MIN MAX 等操作
        else:
            _data = {}
            for _k, _v in v.items():
                if _k == "value":
                    _k = ""
                else:
                    _k = ".{}".format(_k)
                _data["{}{}".format(k, _k)] = _v
            data.append(_data)
    return data


def prase_es_result(result, data_tag="", data_type=""):
    # 处理普通查询与聚合查询)
    hits = result.get("hits", {}).get("hits")
    aggregations = result.get('aggregations')
    data = []
    if aggregations:
        data = parse_es_buckets(aggregations)
    if hits:
        for hit in hits:
            hit = hit['_source']
            _data = {}
            for k, v in hit.items():
                if isinstance(v, dict):
                    for _k, _v in v.items():
                        if _k == "value":
                            _k = ""
                        else:
                            _k = ".{}".format(_k)
                        _data["{}{}".format(k, _k)] = _v
                else:
                    _data[k] = v
            data.append(_data)
    # data_tag = ""
    if data_tag != "":
        key_list = []
        if data_type == 1:
            data_tag = models.SSADataTag.objects.filter(path=data_tag).first()
            new_field_map_list = models.SSAFieldMap.objects.filter(data_tag_id=data_tag.id).values("items", "key")
            new_key_list = []
            for field_map in new_field_map_list:
                new_key_list.append(field_map['key'])
            field_map_list = models.SSAFieldMap.objects.filter(~Q(items=''), ~Q(items='[]'),
                                                               data_tag_id=data_tag.id).values("items", "key")
            for field_map in field_map_list:
                key_list.append(field_map['key'])
        elif data_type == 2:
            data_tag = models.SECDataTag.objects.filter(path=data_tag).first()
            new_field_map_list = models.SECFieldMap.objects.filter(data_tag_id=data_tag.id).values("items", "key")
            new_key_list = []
            for field_map in new_field_map_list:
                new_key_list.append(field_map['key'])
            field_map_list = models.SECFieldMap.objects.filter(~Q(items=''), ~Q(items='[]'),
                                                               data_tag_id=data_tag.id).values("items", "key")
            for field_map in field_map_list:
                key_list.append(field_map['key'])

        for item in data:
            if '@timestamp' in item and item['@timestamp']:
                item['@timestamp'] = item['@timestamp'].replace('T', ' ').replace("Z", '')
            if 'act_time' in item and item['act_time']:
                item['act_time'] = datetime.strptime(str(item['act_time']), '%Y%m%d%H%M%S').strftime(
                    '%Y-%m-%d %H:%M:%S')
            if 'request_time' in item and item['request_time']:
                item['request_time'] = datetime.strptime(item['request_time'], '%Y%m%d%H%M%S').strftime(
                    '%Y-%m-%d %H:%M:%S')
            if 'time' in item and item['time']:
                item['time'] = datetime.strptime(item['time'], '%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M:%S')
            if 'approve_time' in item and item['approve_time']:
                item['approve_time'] = datetime.strptime(item['approve_time'], '%Y%m%d%H%M%S').strftime(
                    '%Y-%m-%d %H:%M:%S')
            if 'create_time' in item and item['create_time']:
                item['approve_time'] = datetime.strptime(item['create_time'], '%Y%m%d%H%M%S').strftime(
                    '%Y-%m-%d %H:%M:%S')
            if 'start_time' in item and item['start_time']:
                item['start_time'] = datetime.strptime(item['start_time'], '%Y%m%d%H%M%S').strftime(
                    '%Y-%m-%d %H:%M:%S')
            if 'end_time' in item and item['end_time']:
                item['end_time'] = datetime.strptime(item['end_time'], '%Y%m%d%H%M%S').strftime(
                    '%Y-%m-%d %H:%M:%S')
            if 'starttime' in item and item['starttime']:
                item['starttime'] = datetime.strptime(item['starttime'], '%Y%m%d%H%M%S').strftime(
                    '%Y-%m-%d %H:%M:%S')
            if 'endtime' in item and item['endtime']:
                item['endtime'] = datetime.strptime(item['endtime'], '%Y%m%d%H%M%S').strftime(
                    '%Y-%m-%d %H:%M:%S')
            if 'gen_time' in item and item['gen_time']:
                item['gen_time'] = datetime.strptime(item['gen_time'], '%Y%m%d%H%M%S').strftime(
                    '%Y-%m-%d %H:%M:%S')
            if 'utcms' in item and item['utcms']:
                item['utcms'] = datetime.strptime(item['utcms'], '%Y%m%d%H%M%S').strftime(
                    '%Y-%m-%d %H:%M:%S')
            for i in range(len(key_list)):
                desc_dict = json.loads(field_map_list[i]['items'])
                if key_list[i] in item:
                    if isinstance(desc_dict, list):
                        for desc in desc_dict:
                            if isinstance(desc['id'], int) and isinstance(item[key_list[i]], int) and desc['id'] == \
                                    item[key_list[i]]:
                                item[key_list[i]] = desc['name']
                                break
                            elif desc['id'] == item[key_list[i]]:
                                item[key_list[i]] = desc['name']
                                break
                                # for key in item.keys():
                                #     if key not in new_key_list:
                                #         item.pop(key)

    return data


def prase_event_result(result):
    # 处理事件普通查询与聚合查询)
    hits = result.get("hits", {}).get("hits")
    aggregations = result.get('aggregations')
    data = []
    if aggregations:
        data = parse_es_buckets(aggregations)
    if hits:
        for hit in hits:
            hit = hit['_source']
            _data = {}
            for k, v in hit.items():
                if isinstance(v, dict):
                    for _k, _v in v.items():
                        if _k == "value":
                            _k = ""
                        else:
                            _k = ".{}".format(_k)
                        _data["{}{}".format(k, _k)] = _v
                else:
                    _data[k] = v
            data.append(_data)
    # 处理字段翻译
    field_map_list = models.SECFieldMap.objects.filter(~Q(items=''), ~Q(items='[]'), ).values("items", "key")
    key_list = []
    for field_map in field_map_list:
        key_list.append(field_map['key'])

    # 处理字段别名
    field_priority_list = models.SECFieldMap.objects.filter(~Q(field_priority__isnull=True),
                                                            ~Q(field_priority='')).values("field_priority", "key")
    priority_list = dict()
    for priority in field_priority_list:
        priority_list[priority['key']] = priority['field_priority'].split(",")[0]

    for item in data:
        # 处理字段翻译
        if '@timestamp' in item and item['@timestamp']:
            item['@timestamp'] = item['@timestamp'].replace('T', ' ').replace("Z", '')
        if 'act_time' in item and item['act_time']:
            item['act_time'] = datetime.strptime(item['act_time'], '%Y%m%d%H%M%S').strftime(
                '%Y-%m-%d %H:%M:%S')
        if 'request_time' in item and item['request_time']:
            item['request_time'] = datetime.strptime(item['request_time'], '%Y%m%d%H%M%S').strftime(
                '%Y-%m-%d %H:%M:%S')
        if 'time' in item and item['time']:
            item['time'] = datetime.strptime(item['time'], '%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M:%S')
        if 'approve_time' in item and item['approve_time']:
            item['approve_time'] = datetime.strptime(item['approve_time'], '%Y%m%d%H%M%S').strftime(
                '%Y-%m-%d %H:%M:%S')
        if 'create_time' in item and item['create_time']:
            item['approve_time'] = datetime.strptime(item['create_time'], '%Y%m%d%H%M%S').strftime(
                '%Y-%m-%d %H:%M:%S')
        if 'start_time' in item and item['start_time']:
            item['start_time'] = datetime.strptime(item['start_time'], '%Y%m%d%H%M%S').strftime(
                '%Y-%m-%d %H:%M:%S')
        if 'end_time' in item and item['end_time']:
            item['end_time'] = datetime.strptime(item['end_time'], '%Y%m%d%H%M%S').strftime(
                '%Y-%m-%d %H:%M:%S')
        if 'starttime' in item and item['starttime']:
            item['starttime'] = datetime.strptime(item['starttime'], '%Y%m%d%H%M%S').strftime(
                '%Y-%m-%d %H:%M:%S')
        if 'endtime' in item and item['endtime']:
            item['endtime'] = datetime.strptime(item['endtime'], '%Y%m%d%H%M%S').strftime(
                '%Y-%m-%d %H:%M:%S')
        if 'gen_time' in item and item['gen_time']:
            item['gen_time'] = datetime.strptime(item['gen_time'], '%Y%m%d%H%M%S').strftime(
                '%Y-%m-%d %H:%M:%S')
        for i in range(len(key_list)):
            desc_dict = json.loads(field_map_list[i]['items'])
            if key_list[i] in item:
                if isinstance(desc_dict, list):
                    for desc in desc_dict:
                        if isinstance(desc['id'], int) and isinstance(item[key_list[i]], int) and desc['id'] == \
                                item[key_list[i]]:
                            item[key_list[i]] = desc['name']
                            break
                        elif desc['id'] == item[key_list[i]]:
                            item[key_list[i]] = desc['name']
                            break
        # 处理别名翻译
        for name in priority_list.keys():
            if name in item:
                if name != priority_list[name]:
                    item[priority_list[name]] = item[name]
                    item.pop(name)
                    continue
    return data


def prase_log_result(result, data_tag="", data_type=""):
    # 处理普通查询与聚合查询)
    hits = result.get("hits", {}).get("hits")
    aggregations = result.get('aggregations')
    data = []
    if aggregations:
        data = parse_es_buckets(aggregations)
    if hits:
        for hit in hits:
            hit = hit['_source']
            _data = {}
            for k, v in hit.items():
                if isinstance(v, dict):
                    for _k, _v in v.items():
                        if _k == "value":
                            _k = ""
                        else:
                            _k = ".{}".format(_k)
                        _data["{}{}".format(k, _k)] = _v
                else:
                    _data[k] = v
            data.append(_data)
    # data_tag = ""
    if data_tag != "":
        key_list = []
        if data_type == 1:
            data_tag = models.SSADataTag.objects.filter(path=data_tag).first()
            new_field_map_list = models.SSAFieldMap.objects.filter(data_tag_id=data_tag.id).values("items", "key")
            new_key_list = []
            for field_map in new_field_map_list:
                new_key_list.append(field_map['key'])
            field_map_list = models.SSAFieldMap.objects.filter(~Q(items=''), ~Q(items='[]'),
                                                               data_tag_id=data_tag.id).values("items", "key")
            for field_map in field_map_list:
                key_list.append(field_map['key'])
        elif data_type == 2:
            data_tag = models.SECDataTag.objects.filter(path=data_tag).first()
            new_field_map_list = models.SECFieldMap.objects.filter(data_tag_id=data_tag.id).values("items", "key")
            new_key_list = []
            for field_map in new_field_map_list:
                new_key_list.append(field_map['key'])
            field_map_list = models.SECFieldMap.objects.filter(~Q(items=''), ~Q(items='[]'),
                                                               data_tag_id=data_tag.id).values("items", "key")
            for field_map in field_map_list:
                key_list.append(field_map['key'])

        for item in data:
            if '@timestamp' in item and item['@timestamp']:
                item['@timestamp'] = item['@timestamp'].replace('T', ' ').replace("Z", '')
            if 'act_time' in item and item['act_time']:
                item['act_time'] = datetime.strptime(item['act_time'], '%Y%m%d%H%M%S').strftime(
                    '%Y-%m-%d %H:%M:%S')
            if 'request_time' in item and item['request_time']:
                item['request_time'] = datetime.strptime(item['request_time'], '%Y%m%d%H%M%S').strftime(
                    '%Y-%m-%d %H:%M:%S')
            if 'time' in item and item['time']:
                item['time'] = datetime.strptime(item['time'], '%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M:%S')
            if 'approve_time' in item and item['approve_time']:
                item['approve_time'] = datetime.strptime(item['approve_time'], '%Y%m%d%H%M%S').strftime(
                    '%Y-%m-%d %H:%M:%S')
            if 'create_time' in item and item['create_time']:
                item['approve_time'] = datetime.strptime(item['create_time'], '%Y%m%d%H%M%S').strftime(
                    '%Y-%m-%d %H:%M:%S')
            if 'start_time' in item and item['start_time']:
                item['start_time'] = datetime.strptime(item['start_time'], '%Y%m%d%H%M%S').strftime(
                    '%Y-%m-%d %H:%M:%S')
            if 'end_time' in item and item['end_time']:
                item['end_time'] = datetime.strptime(item['end_time'], '%Y%m%d%H%M%S').strftime(
                    '%Y-%m-%d %H:%M:%S')
            if 'starttime' in item and item['starttime']:
                item['starttime'] = datetime.strptime(item['starttime'], '%Y%m%d%H%M%S').strftime(
                    '%Y-%m-%d %H:%M:%S')
            if 'endtime' in item and item['endtime']:
                item['endtime'] = datetime.strptime(item['endtime'], '%Y%m%d%H%M%S').strftime(
                    '%Y-%m-%d %H:%M:%S')
            if 'gen_time' in item and item['gen_time']:
                item['gen_time'] = datetime.strptime(item['gen_time'], '%Y%m%d%H%M%S').strftime(
                    '%Y-%m-%d %H:%M:%S')
            if 'utcms' in item and item['utcms']:
                item['utcms'] = datetime.strptime(item['utcms'], '%Y%m%d%H%M%S').strftime(
                    '%Y-%m-%d %H:%M:%S')
            if data_tag.path == 'ssa-ag-all-terminal':
                file_url_list = [item['file_name'], item['ie_name'], item['print_doc'], item['file_path'], item['act_info']]
                item['file_name'] = ''.join(file_url_list)
            for i in range(len(key_list)):
                desc_dict = json.loads(field_map_list[i]['items'])
                if key_list[i] in item:
                    if isinstance(desc_dict, list):
                        for desc in desc_dict:
                            if isinstance(desc['id'], int) and isinstance(item[key_list[i]], int) and desc['id'] == \
                                    item[key_list[i]]:
                                item[key_list[i]] = desc['name']
                                break
                            elif desc['id'] == item[key_list[i]]:
                                item[key_list[i]] = desc['name']
                                break
            for key in item.keys():
                if key not in new_key_list:
                    item.pop(key)

    return data


class ESSQL(object):
    """
    根据条件生成ES SQL 执行
    """

    def __init__(self, x, y, indices=None, userinfo=None, es_host=None, ssa_data_tag=None, query_time=1, limit=0):
        """
        x: 查询维度
        [
            {"type": "key", "value": "src_ip"},
            {"type": "date", "value": "year"}
        ]
        y: 查询内容
        [
            {"aggregator": "AVG", "value": "level"},
            {"aggregator": "MAX", "value": "level"},
            {"aggregator": "COUNT", "value": "all"},
        ]
        es_host: es 地址
        127.0.0.1:9200
        indices: es index 列表
        ['es-index1']
        limit: 展示条数
        10
        """
        self.es_host = es_host
        self.indices = indices
        self.userinfo = userinfo
        self.x = x
        self.y = y
        self.limit = limit
        if not indices:
            self.indices = self.generate_index(ssa_data_tag, query_time)

    def get_es_host(self):
        """
        获取ES地址
        """
        host = None
        if self.es_host:
            host = self.es_host
        if self.userinfo:
            host = self.get_es_host_from_user(self.userinfo)
        if not host:
            raise ValueError("缺少 es_host 参数")
        return host

    def generate_index(self, data_tag, query_time):
        """
        生成需要搜索的indexs
        """
        end_time = datetime.now()
        start_time = end_time - timezone.timedelta(days=query_time)
        es = Elasticsearch(hosts=[self.get_es_host()])
        all_indexs = es.indices.get_alias("*").keys()
        indexs = []
        while True:
            index = "{}-{}".format(data_tag, start_time.strftime("%Y-%m-%d-%H"))
            if index in all_indexs:
                indexs.append(index)
            start_time = start_time + timezone.timedelta(hours=1)
            if start_time > end_time:
                break
        return indexs

    def get_es_host_from_user(self, userinfo):
        agent = userinfo.agent
        company = userinfo.company
        try:
            es_host = models.SelfServiceConf.objects.get(
                agent=agent, company=company, service="es").host
        except models.SelfServiceConf.DoesNotExist:
            es_host = getattr(settings, "ELASTICSEARCH_HOSTS")[0]
        if not es_host:
            raise ValueError("ES 服务未配置")
        return es_host

    def order(self, order_dict, data):
        """
        自定义排序
        """
        for order_key, order_type in order_dict:
            if order_type == "asc":
                reverse = False
            else:
                reverse = True
            data = sorted(data, key=lambda elem: elem[order_key], reverse=reverse)
        return data

    def fetch_diy_data(self, es_host, wheres, data_tag="", data_type=""):
        """
        自定义查询
        """
        if data_type == 1:
            field_map = models.SSAFieldMap.get_field_map()
        else:
            field_map = models.SECFieldMap.get_field_map()
        dimensions = self.x
        values = self.y
        # 分组条件列表
        dimension_list = []
        # 查询参数列表
        value_list = []
        # 排序参数字典
        order_dict = {}
        order_list = []
        # 查询参数翻译字典
        value_map = {}
        interval_map = {
            "year": {"interval": "year", "format": "yyyy-MM-dd", "name": "年"},
            "quarter": {"interval": "quarter", "format": "yyyy-MM-dd", "name": "季度"},
            "month": {"interval": "month", "format": "yyyy-MM-dd", "name": "月"},
            "week": {"interval": "week", "format": "yyyy-MM-dd", "name": "星期"},
            "day": {"interval": "day", "format": "yyyy-MM-dd", "name": "日"},
            "hour": {"interval": "hour", "format": "MM-dd HH:mm", "name": "时"},
            "minute": {"interval": "minute", "format": "MM-dd HH:mm", "name": "分"},
            "second": {"interval": "second", "format": "HH:mm:ss", "name": "秒"},
        }
        # 是否有时间分区（有时间分区时无法进行order 操作）
        has_date_histogram = False
        for dimension in dimensions:
            if dimension['type'] == "date":
                if dimension['value'] not in interval_map:
                    return False, "时间周期错误"
                has_date_histogram = True
                dimension_list.append(
                    "date_histogram(field='@timestamp', 'interval'='{interval}', 'format'='{format}')".format(
                        **interval_map.get(dimension['value'])))
            else:
                order = dimension.get("order")
                if order:
                    if order not in ['desc', 'asc']:
                        return False, "排序方式错误"
                    order_list.append(
                        (dimension['value'], order)
                    )
                    # order_dict[dimension['value']] = order
                dimension_list.append("`{}`".format(dimension['value']))
        for value in values:
            aggregator = value['aggregator']
            agg_value = value['value']
            order = value.get('order')
            nick_agg_value = field_map.get(agg_value, {"name": agg_value})['name']
            alias_key = "{}_{}".format(aggregator.lower(), agg_value)
            # 是否有时间分区（有时间分区时无法进行order 操作）
            if order:
                if order not in ['desc', 'asc']:
                    return False, "排序方式错误"
                # order_dict[alias_key] = order
                order_list.append(
                    (alias_key, order)
                )
            if aggregator not in AGG_MAP:
                return False, "不支持的操作：{}".format(aggregator)
            if aggregator == "DISTINCT":
                value_map[alias_key] = "{}(去重计数)".format(nick_agg_value)
                _select_value = "COUNT(DISTINCT {}) as {}".format(agg_value, alias_key)
            else:
                value_map[alias_key] = "{}({})".format(nick_agg_value, AGG_MAP.get(aggregator, aggregator))
                _select_value = "{}({}) as {}".format(aggregator, agg_value, alias_key)
            value_list.append(_select_value)
        # 拼接ES SQL
        if dimension_list:
            group_by_sql = "GROUP BY ({})".format(", ".join(["{}".format(i) for i in dimension_list]))
        else:
            group_by_sql = ""
        _sql = "select {} from {} {} {}".format(
            ", ".join(value_list),
            ", ".join(self.indices),
            wheres,
            group_by_sql)
        # 无时间参数事采用es 排序
        if order_list and (not has_date_histogram):
            _sql = "{} ORDER BY {}".format(_sql, ", ".join(
                ["`{}` {}".format(k, v) for k, v in order_list]))
        is_ok, result = self.fetch_es(es_host, _sql)
        if not is_ok:
            return is_ok, result
        result = prase_es_result(result, data_tag=data_tag, data_type=data_type)
        result = self.order(order_list, result)
        new_result_x = {}
        new_result_y = {}
        if self.limit:
            result = result[:self.limit]
        for i in result:
            y_key, y_value = None, 0
            x_key, x_value = None, 0

            for k, v in i.items():
                if k in value_map.keys():
                    y_key = value_map[k]
                    y_value = v
                    new_result_y[y_key] = new_result_y.get(y_key, [])
                    new_result_y[y_key].append(y_value)
                if str(k).startswith("date_histogram"):
                    for i_k, i_v in interval_map.items():
                        if i_k in k:
                            key = "日期({})".format(i_v['name'])
                            x_key = key
                            x_value = i['key_as_string']
                            new_result_x[x_key] = new_result_x.get(x_key, [])
                            new_result_x[x_key].append(x_value)

                elif "`{}`".format(k) in dimension_list:
                    key = field_map.get(k, {"name": k})['name']
                    x_key, x_value = key, v
                    new_result_x[x_key] = new_result_x.get(x_key, [])
                    new_result_x[x_key].append(x_value)
                else:
                    pass

        return True, {"x": new_result_x, "y": new_result_y, "result": result}

    def fetch_es(self, host, sql):
        """
        查询ES
        """
        return exec_elasticsearch_sql(host, sql)

    def exec_serach(self, wheres="", data_tag="", data_type=""):
        """
        执行搜索
        """
        if not self.indices:
            raise ValueError("该时间段无数据")
        is_ok, result = self.fetch_diy_data(self.get_es_host(), wheres=wheres, data_tag=data_tag, data_type=data_type)
        return is_ok, result


if __name__ == "__main__":
    select_from_kafka("test")
