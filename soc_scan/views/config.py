# -*- coding:utf-8 -*-
from __future__ import division
import logging

from rest_framework.views import APIView

from rest_framework.response import Response

from soc_scan.tools import mongo

logger = logging.getLogger('soc_scan')


class ConfigInfoView(APIView):
    """ 配置 """

    def post(self, request):
        '''
        扫描配置
        '''
        conn = mongo.MongoConn()
        result = []
        dict_list = conn.db['Config'].find()
        for item in dict_list:
            if item and 'config' in item:
                dict = item['config']
                for conf in dict:
                    if conf.find('_') > 0:
                        item_type = "list"
                    else:
                        item_type = "word"
                    result.append({"show": item_type,
                                   "conftype": item['type'],
                                   "type": conf,
                                   "info": dict[conf]["info"],
                                   "help": dict[conf]["help"],
                                   "value": dict[conf]["value"]})
        if result:
            result = sorted(result, key=lambda x: x["show"], reverse=True)
        return Response({"status": 200, "msg": u'成功', "data": result})


class ConfigUpdateView(APIView):
    """ 修改配置 """

    def post(self, request):
        '''
        修改配置
        '''
        conftype = request.data.get("conftype", '')
        type = request.data.get('type', '')
        value = request.data.get('value', '')

        if type and value and conftype:
            conn = mongo.MongoConn()
            if type == 'Masscan' or type == 'Port_list':
                origin_value = conn.db['Config'].find_one({'type': 'nascan'})["config"][type]["value"]
                value = str(origin_value.split('|')[0]) + '|' + str(value)
            elif type == 'Port_list':
                origin_value = conn.db['Config'].find_one({'type': 'nascan'})["config"]['Port_list']["value"]
                value = value + '|' + origin_value.split('|')[1]
            elif type == 'Masscan':
                path = conn.db['Config'].find_one({'type': 'nascan'})["config"]["Masscan"]["value"]
                if len(path.split('|')) == 3:
                    path = path.split('|')[1] + "|" + path.split('|')[2]
                else:
                    path = path.split('|')[1]
                if value == '1':
                    value = '1|' + path
                else:
                    value = '0|' + path
            result = conn.db['Config'].update({"type": conftype}, {'$set': {'config.' + type + '.value': value}})
            return Response({"status": 200, "msg": u'成功', "data": {}})
        else:
            return Response({"status": 500, "msg": u"修改失败!", "error": u"修改失败!"})
