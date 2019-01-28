# coding: utf-8
from django.conf import settings
from elasticsearch import Elasticsearch


def get_by_any(**kwargs):
    """
    获取告警和故障信息
    """
    es_hosts = getattr(settings, "ELASTICSEARCH_HOSTS",
                       ["http://127.0.0.1:9200/"])
    esarch = Elasticsearch(
        hosts=es_hosts
    )
    # match_field_list = ['agent_id', 'company_id', 'config_id', 'device_type', 'device_id', 'query_str']
    must_list = []

    timestamp_range = {}

    sort_list = []
    sort_field = kwargs.pop('sort_field', '')
    sort_model = kwargs.pop('sort_model', 'desc')
    if sort_field:
        sort_list.append(
            {
                sort_field: sort_model
            }
        )

    index = kwargs.pop("index", [])
    doc_type = kwargs.pop("doc_type", [])

    start_time = kwargs.pop("start_time", '')
    if start_time:
        timestamp_range.setdefault('range', {}).setdefault(
            'datetime', {}).setdefault('format', 'yyyy-MM-dd HH:mm:SS')
        timestamp_range.setdefault('range', {}).setdefault(
            'datetime', {}).setdefault('gt', str(start_time))

    end_time = kwargs.pop("end_time", '')
    if end_time:
        timestamp_range.setdefault('range', {}).setdefault(
            'datetime', {}).setdefault('format', 'yyyy-MM-dd HH:mm:SS')
        timestamp_range.setdefault('range', {}).setdefault(
            'datetime', {}).setdefault('lt', str(end_time))

    page = kwargs.pop('page', 1)
    per_page_count = kwargs.pop('per_page_count', 10)
    if page == 1:
        f = 0
    else:
        f = (page - 1) * per_page_count

    for arg, value in kwargs.items():
        if arg == "query_str":
            must_list.append(
                {
                    "query_string": {
                        "fields": ["item_name", "config_name", "device_name", "rack_sn", "idc_name", "message", "person"],
                        "query": "*" + str(value) + "*",
                    }
                }
            )
        else:
            must_list.append({"match": {arg: value}})

    body = {}
    if must_list:
        body["query"] = {
            "bool": {
                "must": must_list
            }
        }

    if timestamp_range:
        body.setdefault('query', {}).setdefault(
            'bool', {}).setdefault('must', []).append(timestamp_range)

    if sort_list:
        body['sort'] = sort_list

    # print body
    res = esarch.search(from_=f, size=per_page_count,
                        doc_type=doc_type, body=body)
    return res
