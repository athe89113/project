# -*- coding:utf-8 -*-
from __future__ import division
import logging

from rest_framework.views import APIView
from rest_framework.response import Response

from soc_scan.tools import mongo

logger = logging.getLogger('soc_scan')


class PluginList(APIView):
    """插件列表"""

    def post(self, request):
        length = request.data.get("number", 10)
        start = request.data.get("start", 0)
        conn = mongo.MongoConn()
        cursor = conn.db['Plugin'].find().sort('add_time', -1).limit(length).skip(start)
        count = cursor.count()
        result = []
        for item in cursor:
            item['_id'] = str(item['_id'])
            result.append(item)
        context = {
            'draw': 0,
            'recordsTotal': count,
            'recordsFiltered': count,
            'data': result,
            'result': 'ok'
        }
        return Response(context)


class PluginTypeList(APIView):
    """插件类型列表"""

    def post(self, request):
        """
        插件类型列表
        """
        conn = mongo.MongoConn()
        cursor = conn.db['Plugin'].find().distinct('type')
        result = []
        for item in cursor:
            result.append(item)
        context = {
            "status": 200,
            "msg": u'查询成功',
            "data": result
        }
        return Response(context)


class PluginView(APIView):
    """ 插件 """

    def get(self, request):
        '''
        根据类型和危害等级查询插件
        '''
        type = request.query_params.get('type', '')
        risk = request.query_params.get('risk', '')
        query = {}
        if type:
            query['type'] = type
        if risk:
            query['level'] = risk
        conn = mongo.MongoConn()

        cursor = conn.db['Plugin'].find(query)
        result = []
        for item in cursor:
            result.append({'name': item['name'], 'info': item['info']})
        context = {
            "status": 200,
            "msg": u'查询成功',
            "data": result
        }
        return Response(context)

    def delete(self, request):
        pass


class PluginPull(APIView):
    """插件更新"""

    def post(self, request):
        pass
