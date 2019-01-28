# -*- coding:utf-8 -*-
from __future__ import division
import logging
import re

from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response

from bson.objectid import ObjectId
from bson.json_util import dumps

from urllib import unquote

from soc_scan.tools import mongo

logger = logging.getLogger('soc_scan')


class TaskList(APIView):
    """任务列表"""

    def post(self, request):
        '''
        任务列表
        '''
        length = request.data.get("number", 10)
        start = request.data.get("start", 0)
        conn = mongo.MongoConn()
        cursor = conn.db['Task'].find().sort('time', -1).limit(length).skip(start)
        count = cursor.count()
        result = []
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


class TaskCheck(APIView):
    """任务复测"""

    def post(self, request):
        """
        重新执行任务
        """

        tid = request.data.get('taskid', '')
        conn = mongo.MongoConn()
        task = conn.db['Task'].find_one({'_id': ObjectId(tid)})

        # 一次性任务，并且已经扫描完成
        if task and task['plan'] == 0 and task['status'] == 2:
            # 修改扫描状态
            result = conn.db['Task'].update({'_id': ObjectId(tid)}, {'$set': {'status': 0}})
            if result:
                return Response({"status": 200, "msg": u'执行成功', "data": {}})
            else:
                return Response({"status": 500, "msg": u"执行失败!", "error": u"执行失败!"})
        else:
            return Response({"status": 500, "msg": u"执行失败!", "error": u"执行失败!"})


class TaskView(APIView):
    """ 任务 """

    def post(self, request):
        '''
        添加任务
        '''
        title = request.data.get('title', '')
        plugin = request.data.get('plugin', '')
        condition = unquote(request.data.get('condition', ''))
        plan = request.data.get('plan', 0)
        ids = request.data.get('ids', '')
        isupdate = request.data.get('isupdate', '0')

        conn = mongo.MongoConn()
        if plugin:
            targets = []
            # 当前页结果选择
            for i in ids.split(','):
                tar = [i.split(':')[0], int(i.split(':')[1])]
                targets.append(tar)
            temp_result = True
            for p in plugin.split(','):
                query = querylogic(condition.strip().split(';'))
                item = {'status': 0, 'title': title, 'plugin': p, 'condition': condition, 'time': datetime.now(),
                        'target': targets, 'plan': int(plan), 'isupdate': int(isupdate), 'query': dumps(query)}
                insert_reuslt = conn.db['Task'].insert(item)
                if not insert_reuslt:
                    temp_result = False
            if temp_result:
                return Response({"status": 200, "msg": u'添加成功', "data": {}})
            else:
                return Response({"status": 500, "msg": u"执行失败!", "error": u"执行失败!"})
        else:
            return Response({"status": 500, "msg": u"执行失败!", "error": u"执行失败!"})

    def delete(self, request, id=None):
        '''
        删除任务
        '''
        conn = mongo.MongoConn()
        if id:
            result = conn.db['Task'].delete_one({'_id': ObjectId(id)})
            if result.deleted_count > 0:
                result = conn.db['Result'].delete_many({'task_id': ObjectId(id)})
                return Response({"status": 200, "msg": u'删除成功', "data": {}})
        return Response({"status": 500, "msg": u"执行失败!", "error": u"执行失败!"})


class TaskResultList(APIView):
    """任务结果列表"""

    def post(self, request):
        '''
        任务结果列表
        '''
        taskid = request.data.get("search[value]", 0)
        taskdate = request.data.get('taskdate', "")

        length = request.data.get("number", 10)
        start = request.data.get("start", 0)
        conn = mongo.MongoConn()

        result_list = []
        vulcount = 0
        lastscan = []
        if taskid:
            lastscan = conn.db["Result"].distinct('task_date', {'task_id': ObjectId(taskid)})
        if len(lastscan) > 0:
            lastscan.sort(reverse=True)
            if taskdate:  # 根据扫描批次查看结果
                cursor = conn.db['Result'].find(
                    {'task_id': ObjectId(id), 'task_date': datetime.strptime(taskdate, "%Y-%m-%d %H:%M:%S.%f")}
                ).sort('time', -1).limit(length).skip(start)
            else:  # 查看最新批次结果
                cursor = conn.db['Result'].find({'task_id': ObjectId(taskid),
                                                 'task_date': lastscan[0]
                                                 }).sort('time', -1).limit(length).skip(start)
            vulcount = cursor.count()
            for item in cursor:
                result_list.append({'ip': item['ip'],
                                    'port': item['port'],
                                    'info': item['info'],
                                    'vul_level': item['vul_info']['vul_level'],
                                    'time': datetime.strftime(item['time'], '%Y-%m-%d %H:%M:%S')
                                    })

            # 速度优化，数据量多采取不同的方式查询
            if len(result_list) > 100:
                ip_hostname = {}
                hostname = conn.db['Info'].aggregate(
                    [{'$match': {'hostname': {'$ne': None}}}, {'$project': {'_id': 0, 'ip': 1, 'hostname': 1}}])
                for _ in hostname:
                    if 'hostname' in hostname:
                        ip_hostname[_["ip"]] = _["hostname"]
                for _ in result_list:
                    if 'ip' in ip_hostname:
                        _['hostname'] = ip_hostname[_["ip"]]
                    else:
                        _['hostname'] = ''
            else:
                for _ in result_list:
                    hostname = conn.db['Info'].find_one({'ip': _['ip']})
                    if hostname and 'hostname' in hostname:
                        _['hostname'] = hostname['hostname']
                    else:
                        _['hostname'] = ''

        context = {
            'draw': 0,
            'recordsTotal': vulcount,
            'recordsFiltered': vulcount,
            'data': result_list,
            'result': 'ok'
        }
        return Response(context)


# 搜索逻辑
def querylogic(list):
    query = {}
    if len(list) > 1 or len(list[0].split(':')) > 1:
        for _ in list:
            if _.find(':') > -1:
                q_key, q_value = _.split(':', 1)
                if q_key == 'port':
                    query['port'] = int(q_value)
                elif q_key == 'banner':
                    zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
                    contents = q_value
                    match = zhPattern.search(contents)
                    # 如果没有中文用全文索引
                    if match:
                        query['banner'] = {"$regex": q_value, '$options': 'i'}
                    else:
                        text_query = mgo_text_split(q_value)
                        query['$text'] = {'$search': text_query, '$caseSensitive': True}
                elif q_key == 'ip':
                    query['ip'] = {"$regex": q_value}
                elif q_key == 'server':
                    query['server'] = q_value.lower()
                elif q_key == 'title':
                    query['webinfo.title'] = {"$regex": q_value, '$options': 'i'}
                elif q_key == 'tag':
                    query['webinfo.tag'] = q_value.lower()
                elif q_key == 'hostname':
                    query['hostname'] = {"$regex": q_value, '$options': 'i'}
                elif q_key == 'all':
                    filter_lst = []
                    for i in ('ip', 'banner', 'port', 'time', 'webinfo.tag', 'webinfo.title', 'server', 'hostname'):
                        filter_lst.append({i: {"$regex": q_value, '$options': 'i'}})
                    query['$or'] = filter_lst
                else:
                    query[q_key] = q_value
    else:
        filter_lst = []
        for i in ('ip', 'banner', 'port', 'time', 'webinfo.tag', 'webinfo.title', 'server', 'hostname'):
            filter_lst.append({i: {"$regex": list[0], '$options': 'i'}})
        query['$or'] = filter_lst
    return query


def mgo_text_split(query_text):
    ''' split text to support mongodb $text match on a phrase '''
    sep = r'[`\-=~!@#$%^&*()_+\[\]{};\'\\:"|<,./<>?]'
    word_lst = re.split(sep, query_text)
    text_query = ' '.join('\"{}\"'.format(w) for w in word_lst)
    return text_query
