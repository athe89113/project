# coding=utf-8
from __future__ import unicode_literals
import json
import logging
from elasticsearch import Elasticsearch
from django.utils import timezone
from django.conf import settings

ELASTICSEARCH_HOSTS = settings.ELASTICSEARCH_HOSTS
logger = logging.getLogger("soc_ssa")


class BaseData(object):
    """
    数据基类
    """

    ES_KEY = None

    # 总数
    SUM_KYE = None
    # top 数据
    ORDER_KYE = None
    VALUE_KYE = None
    TOP_COUNT = 5
    # 分类数据
    TYPE_LIST = ['严重', '高', '中', '低', 'info']
    TYPE_FIELD = "data.security_level"

    DISPALY_MAP = {
    }

    def __init__(self, name, key, cycle):
        self.name = name
        self.key = key
        self.cycle = cycle

    def parse_time_cycle(self):
        """
        生成时间区间
        """
        now = timezone.now()
        now = timezone.datetime(now.year, now.month, now.day, 0, 0, 0, tzinfo=now.tzinfo)
        cycle = self.cycle
        time_list = []
        if cycle >= 360:
            range_len = 12
            hours = 24 * 30
        elif cycle >= 90:
            range_len = 10
            hours = 24
        elif cycle >= 30:
            range_len = 10
            hours = 24 * 3
        elif cycle >= 7:
            range_len = 7
            hours = 24
        else:
            range_len = 12
            hours = 2
        for i in range(range_len):
            i += 1
            time_list.append(now - timezone.timedelta(hours=hours * i))
        return time_list

    def generate_time_range(self):
        """
        生成 开始时间 结束时间 yield 返回
        """
        lte_time = None
        time_ranges = self.parse_time_cycle()
        for time_range in time_ranges:
            if not lte_time:
                lte_time = timezone.now()
            _lte_time = lte_time
            lte_time = time_range
            yield time_range, _lte_time

    def time_format_cycle(self, labels):
        """
        根据时间周期去格式化时间显示
        """
        if self.cycle == 1:
            labels = [i.strftime("%H:%M") for i in labels]
        else:
            labels = [i.strftime("%m-%d") for i in labels]
        return labels

    def query_orm_cycle(self, qs, time_field, is_range=True):
        """
        按时间周期取ORM 数据
        """
        data = []
        time_ranges = self.parse_time_cycle()
        for gte_time, lte_time in self.generate_time_range():
            if is_range:
                query_dict = {
                    "{}__gte".format(time_field): gte_time,
                    "{}__lte".format(time_field): lte_time,
                }
            else:
                query_dict = {
                    "{}__lte".format(time_field): lte_time,
                }
            data.append(qs.filter(**query_dict).count())

        labels = self.time_format_cycle(time_ranges)
        data.reverse()
        labels.reverse()
        return labels, data

    def generate_es_index(self):
        """
        生成 es index
        """
        index = []
        now = timezone.now()
        for _d in range(self.cycle):
            _t = now - timezone.timedelta(days=_d)
            index.append("ssa-result-{}".format(_t.strftime("%Y%m%d")))
        return list(set(index))

    def parse_top_data(self, hits):
        """
        解析top 数据
        """

        def get_dict_data_from_dot_key(_dict, dot_key):
            """
            {"data": {"key1": "value1"}}, "data.key" => value1
            """

            dot_key = dot_key.split(".")
            if len(dot_key) == 2:
                value = _dict[dot_key[0]][dot_key[1]]
            elif len(dot_key) == 1:
                value = _dict[dot_key[0]]
            else:
                value = ""
            return value

        for _dict in hits:
            value = get_dict_data_from_dot_key(_dict['_source'], self.VALUE_KYE)
            count = get_dict_data_from_dot_key(_dict['_source'], self.ORDER_KYE)

            yield count, value

    def fetch_es_top_data(self):
        """
        取top数据
        """
        labels = []
        data = []
        time_ranges = self.parse_time_cycle()
        gte_time = time_ranges[-1]
        lte_time = time_ranges[0]
        result = self._fetch_es_top_data(gte_time, lte_time)

        for count, value in self.parse_top_data(result):
            labels.append(value)
            data.append(count)

        data = {
            "labels": labels,
            "data": [
                {"name": self.DISPALY_MAP[self.VALUE_KYE], "data": data}
            ]
        }
        return data

    def _fetch_es_top_data(self, start_time, end_time):
        """
        拼接TOP 查询参数
        """
        body = {
            "sort": {self.ORDER_KYE: {"order": "desc"}},
            "size": self.TOP_COUNT
        }
        result = self.fetch_es_data(start_time, end_time, body)
        return result['hits']['hits']

    def fetch_es_data(self, start_time, end_time, body, must_list=None):
        """
        基础查询参数及ES查询交互
        """
        indexes = self.generate_es_index()
        start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
        end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")
        logger.info("search es {} start: {} end: {} index: {}" \
                    .format(str(ELASTICSEARCH_HOSTS), start_time, end_time, len(indexes)))
        base_body = {
            "query": {
                "bool": {
                    "must": [
                        {"match": {"key": self.ES_KEY}},
                        {"range": {"time": {"gte": start_time}}},
                        {"range": {"time": {"lt": end_time}}}
                    ]
                }
            }
        }
        if must_list:
            base_body['query']['bool']['must'] += must_list
        base_body.update(body)

        es = Elasticsearch(hosts=ELASTICSEARCH_HOSTS)
        try:
            result = es.search(request_timeout=15, doc_type='result', body=base_body,
                               index=indexes,
                               ignore_unavailable=True)
        except Exception:
            print(json.dumps(base_body))
            print(ELASTICSEARCH_HOSTS)
            raise
        return result

    def _fetch_es_sum_data(self, start_time, end_time, must_list=None, sum_key=None):
        """
        进行es SUM 操作
        """
        body = {
            "size": 0,
            "aggs": {
                "data": {
                    "sum": {
                        "field": sum_key or self.SUM_KYE
                    }
                }
            }
        }
        result = self.fetch_es_data(start_time, end_time, body, must_list=must_list)
        all_count = result['aggregations']['data']['value']
        return all_count

    def _fetch_es_max_data(self, start_time, end_time, must_list=None, max_key=None):
        """
        进行es MAX 操作
        """
        body = {
            "size": 0,
            "aggs": {
                "data": {
                    "max": {
                        "field": max_key
                    }
                }
            }
        }
        result = self.fetch_es_data(start_time, end_time, body, must_list=must_list)
        all_count = result['aggregations']['data']['value'] or 0
        return all_count

    def fetch_es_types_data(self):
        """
        获取es 各个类型的数据
        """
        types = self.TYPE_LIST
        type_field = self.TYPE_FIELD

        labels = []
        data = []
        time_ranges = self.parse_time_cycle()
        gte_time = time_ranges[-1]
        lte_time = time_ranges[0]
        # result = self._fetch_es_top_data(gte_time, lte_time)

        for t in types:
            must_list = [{
                "match": {
                    type_field: t
                }
            }]
            value = self._fetch_es_sum_data(gte_time, lte_time, must_list=must_list)
            labels.append(t)
            data.append(value)

        data = {
            "labels": labels,
            "data": [
                {"name": "", "data": data}
            ]
        }
        return data

    def fetch_es_sum_data(self, must_list=None):
        data = []
        labels = []
        for gte_time, lte_time in self.generate_time_range():
            value = self._fetch_es_sum_data(gte_time, lte_time, must_list=must_list)
            labels.append(gte_time)
            data.append(value)
        labels = self.time_format_cycle(labels)
        labels.reverse()
        data.reverse()
        data = {
            "labels": labels,
            "data": [
                {
                    "name": self.DISPALY_MAP[self.SUM_KYE],
                    "data": data
                }
            ]
        }
        return data

    def data(self):
        """
        实体数据
        """
        data = {
            "labels": ['2018-04-10', '2018-04-11', '2018-04-12', '2018-04-13', '2018-04-14'],
            "data": [
                {"name": "张三", "data": [11, 55, 99, 13, 13]},
                {"name": "李四", "data": [11, 55, 99, 13, 13]},
                {"name": "王五", "data": [11, 55, 99, 13, 13]},
            ]

        }
        return data

    @classmethod
    def demo_data(cls):
        """
        实体数据
        """
        data = {
            "labels": ['01-01', '01-02', '01-03', '01-04', '01-05', '01-06', '01-07'],
            "data": [
                {"name": "数据一", "data": [19, 33, 88, 22, 66, 44, 11]},
                {"name": "数据二", "data": [4, 22, 55, 99, 77, 22, 77]},
                {"name": "数据三", "data": [12, 1, 88, 33, 99, 221, 88]}
            ]
        }
        return data
