# coding=utf-8
import logging
from django.core.management.base import BaseCommand
from elasticsearch import Elasticsearch


class Command(BaseCommand):

    def handle(self, *args, **options):
        # TODO 取到ES的地址
        es_hosts = [""]
        es =  Elasticsearch(hosts=es_hosts)
        indexs = es.indices.get_alias("*").keys()
        # 删除index
        #es.indices.delete(index='test-index', ignore=[400, 404])