# coding: utf-8
"""
专家分析系统
"""
import logging
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from soc_ssa import models
from soc_ssa import serializers
from soc_ssa.ssa_common import prase_es_result, exec_elasticsearch_sql

logger = logging.getLogger("soc_ssa")

class RuleManageList(APIView):
    """
    专家分析系统 
    """
    def get(self, request):
        """获取规则目录树
        """
        agent = request.user.userinfo.agent
        company = request.user.userinfo.company
        data = models.SSARuleManage.tree(agent, company)
        return Response({"data": data, "status": 200, "msg": "获取成功"})
    
    def post(self, request):
        """
        添加规则
        """
        obj_serializer = serializers.RuleManageSerializers(
            data=request.data,
            context={'request': request})
        if obj_serializer.is_valid():
            instance = obj_serializer.save()
            return Response({"status": 200, "msg": "添加成功", "data": obj_serializer.data})
        else:
            errors = obj_serializer.errors
            return Response({"status": 500, "msg": errors.items()[0][1][0], "error": errors})


class RuleManageDetail(APIView):
    """
    专家分析系统 
    """

    def get_instance(self, request, pk):
        agent = request.user.userinfo.agent
        company = request.user.userinfo.company
        try:
            instance = models.SSARuleManage.objects.get(
                agent=agent, company=company, id=pk)
        except models.SSARuleManage.DoesNotExist:
            return None
        return instance

    def put(self, request, pk):
        """
        编辑规则
        """
        instance = self.get_instance(request, pk)
        if not instance:
            return Response({"status": 500, "msg": "获取对象错误"})
        obj_serializer = serializers.RuleManageSerializers(
            instance=instance,
            data=request.data,
            context={'request': request},
            partial=True)

        if obj_serializer.is_valid():
            instance = obj_serializer.save()
            return Response({"status": 200, "msg": "修改成功", "data": obj_serializer.data})
        else:
            errors = obj_serializer.errors
            return Response({"status": 500, "msg": errors.items()[0][1][0], "error": errors})

    def delete(self, request, pk):
        """
        删除规则
        """
        instance = self.get_instance(request, pk)
        if not instance:
            return Response({"status": 500, "msg": "获取对象错误"})
        if models.SSARuleManage.objects.filter(parent=instance.id).count() > 0:
             return Response({"status": 500, "msg": "目录下存在文件, 不能删除"})
        instance.delete()
        return Response({"status": 200, "msg": "删除成功"})


class ExecuteRuleDts(APIView):
    """专家分析
    """
    def post(self, request):
        """
        执行规则
        """
        agent = request.user.userinfo.agent
        company = request.user.userinfo.company
        start = request.data.get("start", 0)
        length = request.data.get("length", 10)
        sql = request.data.get('sql')
        if not sql:
            return Response({"status": 500, "data": [], "msg": "SQL 不能为空"})
        if "limit" not in sql.lower():
            sql = "{} limit {}, {}".format(sql, start, length)
        try:
            es_host = models.SelfServiceConf.objects.get(agent=agent, company=company, service="es")
        except models.SelfServiceConf.DoesNotExist:
            return Response({"status": 500, "msg": "ES服务未配置"})
        is_ok, data = exec_elasticsearch_sql(es_host.host, sql)
        if not is_ok:
            return Response({"status": 500, "msg": "查询失败"})
        all_count = data['hits']['total']        
        data = prase_es_result(data)
        data = {"recordsTotal": all_count, "data": data, "msg": "查询成功"}
        data['recordsFiltered'] = data['recordsTotal']
        return Response(data)
