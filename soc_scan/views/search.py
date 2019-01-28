# -*- coding:utf-8 -*-
from __future__ import division
from datetime import datetime
import logging

from rest_framework.response import Response
from rest_framework.views import APIView

from soc_scan.tools import mongo
from soc_scan.views.task import querylogic

logger = logging.getLogger('soc_scan')


class SecrchView(APIView):
    """ 搜索 """

    def post(self, request):
        """
        搜索
        """
        length = request.data.get("number", 10)
        start = request.data.get("start", 0)
        search = request.data.get("search[value]", '')
        result = []
        conn = mongo.MongoConn()
        query = querylogic(search.strip().split(';'))
        cursor = conn.db['Info'].find(query).sort('time', -1).limit(length).skip(start)
        count = cursor.count()
        for item in cursor:
            item['_id'] = str(item['_id'])
            item['time'] = datetime.strftime(item['time'], '%Y-%m-%d %H:%M:%S')
            result.append(item)
        context = {
            'draw': 0,
            'recordsTotal': count,
            'recordsFiltered': count,
            'data': result,
            'result': 'ok'
        }
        return Response(context)
