# coding=utf-8
# 自定义报表
import json
import logging
import requests
from datetime import datetime
from elasticsearch import Elasticsearch

from django.conf import settings
from django.utils import timezone
from django.db.models import Q

from soc_ssa import models
from soc_ssa import serializers
from utils.datatable import DatatableView
from utils.select2 import select2_filter
from rest_framework.views import APIView
from rest_framework.response import Response
from common import localtime_to_timestamp
from soc_ssa.ssa_common import prase_es_result, AGG_MAP, ESSQL


class SSAChartPerview(APIView):
    """
    报表元素-预览
    """

    def post(self, request):
        """报表元素-预览"""
        obj_serializer = serializers.SSAChartPerViewSerializer(
            data=request.data,
            context={'request': request})
        if not obj_serializer.is_valid():
            errors = obj_serializer.errors
            return Response({"status": 500, "msg": errors.items()[0][1][0], "error": errors})
        data = obj_serializer.data
        data_tag_id = request.data.get('data_tag')
        query_time = request.data.get('query_time', 30)
        data_type = request.data.get('data_type')
        wheres = ""
        if data_type == 1:
            data_tag = models.SSADataTag.objects.get(id=data_tag_id).path
        elif data_type == 2:
            data_tag = models.SECDataTag.objects.get(id=1).path
            wheres = "where {} = {}".format("event_source", data_tag_id)
        else:
            return Response({"status": 500, "msg": "查询失败", "error": {}})
        es_sql = ESSQL(userinfo=request.user.userinfo,
                       limit=data['limit'],
                       x=data['x'], y=data['y'], ssa_data_tag=data_tag, query_time=query_time)
        try:
            is_ok, result = es_sql.exec_serach(wheres=wheres, data_tag=data_tag, data_type=data_type)
        except ValueError as e:
            return Response({"status": 500, "msg": e.message})
        if not is_ok:
            return Response({"status": 500, "msg": "查询失败", "error": result})
        return Response({"status": 200, "msg": "查询成功", "data": result})


class SSAChartList(APIView):
    """
    报表元素
    """

    def post(self, request):
        """报表元素"""
        obj_serializer = serializers.SSAChartSerializer(
            data=request.data,
            context={'request': request})
        if obj_serializer.is_valid():
            instance = obj_serializer.save()
            data = obj_serializer.data
            data['data_tag'] = instance.data_tag
            data['x'] = json.loads(instance.x)
            data['y'] = json.loads(instance.y)
            data['styles'] = json.loads(instance.styles)
            req = Response({"status": 200, "msg": "添加成功", "data": data})
        else:
            errors = obj_serializer.errors
            req = Response({"status": 500, "msg": errors.items()[
                0][1][0], "error": errors})
        return req


class SSAChartDetail(APIView):
    """
    图表
    """

    def get_obj(self, pk):
        agent_now = self.request.user.userinfo.agent
        company_now = self.request.user.userinfo.company

        try:
            obj = models.SSAChart.objects.get(
                id=pk, agent=agent_now, company=company_now)
        except models.SSAChart.DoesNotExist:
            return False
        return obj

    def get(self, request, pk):
        """
        获取图表信息
        """
        obj = self.get_obj(pk)
        if not obj:
            return Response({"status": 500, "msg": "该图表不存在或不允许修复"})
        if obj.type:
            obj_type = int(obj.type)
        else:
            obj_type = 0
        data = {
            "id": obj.id,
            "name": obj.name,
            "type": obj_type,
            "limit": obj.limit,
            "map_type": obj.map_type,
            "data_tag": obj.data_tag,
            "chart_type": obj.chart_type,
            "query_time": obj.query_time,
            "x": json.loads(obj.x),
            "y": json.loads(obj.y),
            "styles": json.loads(obj.styles),
            "data_type": obj.data_type
        }
        return Response({"status": 200, "msg": "获取图表成功", "data": data})

    def put(self, request, pk):
        """
        修改图表
        """
        obj = self.get_obj(pk)
        if not obj:
            return Response({"status": 500, "msg": "该图表不存在或此图表不允许修改"})

        obj_serializer = serializers.SSAChartSerializer(
            data=request.data,
            instance=obj,
            context={'request': request})

        if obj_serializer.is_valid():
            obj_serializer.save()
            req = Response({"status": 200, "msg": "修改成功"})
        else:
            errors = obj_serializer.errors
            req = Response({"status": 500, "msg": errors.items()[
                0][1][0], "error": errors})
        return req

    def delete(self, request, pk):
        obj = self.get_obj(pk)
        if not obj:
            return Response({"status": 500, "msg": "该图表不存在或此图表不允许修改"})
        obj.delete()
        return Response({"status": 200, "msg": "删除成功"})


class SSAChartDts(DatatableView):
    """图表库管理"""
    render_columns = [
        ("id", "id", 0),
        ("name", "name"),
        ("type", "type"),
        ("chart_type", "chart_type"),
        ("map_type", "map_type"),
        ("query_time", "query_time"),
        ("data_type", "data_type", 0),
        ("data_tag", "data_tag", 0),
        ("limit", "limit"),
    ]

    model = models.SSAChart

    def get_initial_queryset(self):
        """获取可查询的数据"""
        agent_now = self.request.user.userinfo.agent
        company_now = self.request.user.userinfo.company
        type_id = self.request.data.get("type")
        order_field = self.request.data.get("order_field")
        order_type = self.request.data.get("order_type")
        qs = self.model.objects.filter(
            Q(agent=agent_now, company=company_now) | Q(agent=None, company=None))
        if type_id:
            qs = qs.filter(type=type_id)
        order = '-id'
        if order_field:
            if order_field in [i[0] for i in self.render_columns]:
                if order_type == "desc":
                    order = "-{}".format(order_field)
                else:
                    order = order_field
        qs = qs.order_by(order)
        return qs

    def prepare_one_result(self, item, data_dict):
        """
        格式化输出形式，不处理则默认按原来对应字段输出
        :param item: 操作对象
        :param data_dict: 操作对象对应结果
        """
        data_dict['x'] = json.loads(item.x)
        data_dict['y'] = json.loads(item.y)
        data_dict['styles'] = json.loads(item.styles)
        if item.type:
            data_dict['type'] = int(item.type)
        else:
            data_dict['type'] = 0
        return data_dict


class SSADashBoradChart(APIView):
    """态势感知DashBorad"""

    def get_dashborad(self, request):
        agent = request.user.userinfo.agent
        company = request.user.userinfo.company
        dashborad_type = request.DATA.get('dashborad_type')
        dashborad = models.SSADashBorad.objects.filter(type=dashborad_type, agent=agent, company=company).last()
        # 取最后一个
        if not dashborad:
            return '此dashborad不允许修改', None
        return 'ok', dashborad

    def post(self, request):
        """添加dashborad图表"""
        agent = request.user.userinfo.agent
        company = request.user.userinfo.company
        dashborad_msg, dashborad = self.get_dashborad(request)
        order = request.DATA.get('order', 0)
        if not order:
            return Response({'status': 500, "msg": "order错误"})
        if dashborad_msg != 'ok':
            return Response({'status': 500, 'msg': dashborad_msg})
        chart_id = request.DATA.get('chart_id')
        try:
            # 要不自定义的表 要不系统自带的表
            chart = models.SSAChart.objects.get(Q(id=chart_id, agent=agent, company=company) |
                                                Q(id=chart_id, agent=None, company=None))
        except models.SSAChart.DoesNotExist:
            return Response({"status": 500, "msg": "表ID错误"})
        cells_number = models.SSADashBoradCell.objects.filter(dashboard=dashborad, order=order).count()
        if cells_number >= 2:
            return Response({'status': 500, "msg": "添加失败,同一个位置最多添加两个表"})
        # cell_order = 1
        # # 图表顺序 第一个为1 后续+1
        # if cells:
        #     cell_order = cells.last().order + 1
        cell_order = int(order)
        cell = models.SSADashBoradCell()
        cell.chart = chart
        cell.dashboard = dashborad
        cell.agent = chart.agent
        cell.order = cell_order
        cell.company = chart.company
        cell.save()
        return Response({'status': 200, "msg": "添加成功"})

    def put(self, request):
        """修改DashBorad表"""
        agent = request.user.userinfo.agent
        company = request.user.userinfo.company
        dashborad_msg, dashborad = self.get_dashborad(request)
        if dashborad_msg != 'ok':
            return Response({'status': 500, 'msg': dashborad_msg})
        cell_id = request.DATA.get('cell_id')
        chart_id = request.DATA.get('chart_id')
        try:
            # 要不自定义的表 要不系统自带的表
            chart = models.SSAChart.objects.get(Q(id=chart_id, agent=agent, company=company) |
                                                Q(id=chart_id, agent=None, company=None))
        except models.SSAChart.DoesNotExist:
            return Response({"status": 500, "msg": "表ID错误"})
        try:
            cell = models.SSADashBoradCell.objects.get(id=int(cell_id), dashboard=dashborad)
        except models.SSADashBoradCell.DoesNotExist:
            return Response({"status": 500, 'msg': "cell_order错误"})
        cell.chart = chart
        cell.dashboard = dashborad
        cell.agent = chart.agent
        # cell.order = cell_order
        cell.company = chart.company
        cell.save()
        return Response({'status': 200, "msg": "修改成功"})

    def delete(self, request):
        """删除dashborad表"""
        dashborad_msg, dashborad = self.get_dashborad(request)
        if dashborad_msg != 'ok':
            return Response({'status': 500, 'msg': dashborad_msg})
        cell_id = request.DATA.get('cell_id')
        try:
            cell = models.SSADashBoradCell.objects.get(id=int(cell_id), dashboard=dashborad)
        except models.SSADashBoradCell.DoesNotExist:
            return Response({'status': 500, "msg": "删除错误"})
        cell.delete()
        return Response({'status': 200, "msg": "删除成功"})


class SSADashBorad(APIView):
    """态势感知DashBorad"""

    def put(self, request):
        """修改dashborad名称"""
        dashborad_type = int(request.DATA.get('dashborad_type', 1))
        agent = request.user.userinfo.agent
        try:
            dashborad = models.SSADashBorad.objects.get(type=dashborad_type, agent=agent)
        except models.SSADashBorad.DoesNotExist:
            return Response({"status": 500, "msg": "dashborad不存在"})
        obj_serializer = serializers.SSAdashborad(
            data=request.data,
            instance=dashborad)
        if obj_serializer.is_valid():
            obj_serializer.save()
            return Response({
                "msg": "修改成功",
                "status": 200
            })
        else:
            errors = obj_serializer.errors
            return Response({"status": 500, "msg": errors.items()[
                0][1][0], "error": errors})

    def get(self, request):
        """获取相应态势感知图表"""
        dashborad_type = int(request.GET.get('dashborad_type', 1))
        t = {1: "资源", 2: "业务", 3: "安全"}
        agent = request.user.userinfo.agent
        dashboard, create = models.SSADashBorad.objects.get_or_create(type=dashborad_type, agent=agent,
                                                                      defaults={"name": t[dashborad_type]})
        if dashboard:
            pass
            # dashboard = dashboards.last()
        else:
            return Response({'status': 500, 'msg': '获取dashborad错误'})
        return_data = {}
        cells = models.SSADashBoradCell.objects.filter(dashboard=dashboard).order_by('order')
        cells_number = []
        return_data1 = []
        for cell in cells:
            if cell.order not in return_data:
                return_data[cell.order] = []
            temp = {
                "cell_id": cell.id,
                "cells": 2 if cell.order in cells_number else 1,
                "cell_order": cell.order,
                "id": cell.chart_id,
                "name": cell.chart.name,
                "type": cell.chart.type,
                "limit": cell.chart.limit,
                "map_type": cell.chart.map_type,
                "chart_type": cell.chart.chart_type,
                "query_time": cell.chart.query_time,
                "data_tag": cell.chart.data_tag,
                "x": json.loads(cell.chart.x),
                "y": json.loads(cell.chart.y),
                "styles": json.loads(cell.chart.styles),
                "data_type": cell.chart.data_type,
            }
            cells_number.append(cell.order)
            return_data[cell.order].append(temp)
            return_data1.append(temp)
        data = {
            "name": dashboard.name,
            "data": return_data1
        }
        return Response({
            "msg": "获取数据成功",
            "status": 200,
            "data": data
        })
