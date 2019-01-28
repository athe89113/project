# coding=utf-8
"""
报告管理
"""
import os
import logging
import time
import json
from django.db.models import Q
from datetime import datetime

from common import get_next_scan_time
from soc_ssa.tools.make_docx.docx_plugin import MakeDocx
from soc_ssa.tools.make_pdf.pdf_plugin import MakePdf
from soc.settings import REPORT_DIR
from django.utils import timezone
from django.http import StreamingHttpResponse, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response

from soc_ssa import models
from soc_ssa import serializers
from soc_ssa.tools.make_docx import fetch_data, fetch_new_data
from soc_ssa.tools.make_docx.docx_common import underline_to_camel
from soc_ssa.tools.report.report_data import ReportData
from soc_ssa.ssa_common import ESSQL

from utils.datatable import DatatableView
from utils.select2 import select2_filter

logger = logging.getLogger('soc_ssa')

DATA_TYPE_MAP = {
    1: "资产信息分析",
    2: "事件信息分析",
    3: "终端数据分析",
    4: "网络数据分析",
    5: "攻击数据分析",
    6: "违规数据分析",
    7: "病毒数据分析",
    99: "自定义分析"
}


# def underline_to_camel(underline_format):
#     '''
#          下划线命名格式驼峰命名格式
#     '''
#     camel_format = ''
#     for _s_ in underline_format.split('_'):
#         camel_format += _s_.capitalize()
#     return camel_format

class ReportCellTypeList(APIView):
    """
    报告元素
    """

    def post(self, request):
        """
        报告元素
        """
        datas = []
        for data_type, name in DATA_TYPE_MAP.items():
            datas.append({
                "data_type": data_type,
                "data_type_name": name,
                "data": []
            })
        return Response({"status": 200, "data": datas})


class ReportCellList(APIView):
    """
    报告元素
    """

    def get_custom_data(self, userinfo, data):
        '''
        封装自定义图表数据
        '''
        wheres = ""
        if data.data_type == 1:
            index_path = models.SSADataTag.objects.get(id=data.data_tag)
        elif data.data_type == 2:
            index_path = models.SECDataTag.objects.get(id=data.data_tag)
            wheres = "where {} = {}".format("event_source", data.data_tag)
        else:
            return {}
        if not index_path:
            return {}
        es_sql = ESSQL(userinfo=userinfo,
                       limit=data.limit,
                       x=json.loads(data.x),
                       y=json.loads(data.y),
                       ssa_data_tag=index_path.path,
                       query_time=data.query_time)
        try:
            is_ok, result = es_sql.exec_serach(wheres=wheres, data_type=data.data_type, data_tag=index_path.path)
            if is_ok:
                y_data = []
                for key in result['y']:
                    y_data.append({"name": key, "data": result['y'][key]})
                if len(list(result['x'].items())) > 0:
                    char_data = {
                        'labels': list(result['x'].items())[0][1],
                        'data': y_data
                    }
                else:
                    char_data = {
                        'labels': [],
                        'data': []
                    }
                return char_data
            else:
                return {}
        except ValueError as e:
            logger.error(e)
            return {}

    def post(self, request):
        """
        报告元素
        """
        data_type = request.data.get("data_type")

        char_data = []
        if data_type:
            # 非自定义图表
            if data_type != 99:
                data_list = models.SSAReportCell.objects.filter(data_type=data_type)
                for item in data_list:
                    try:
                        data_class_name = underline_to_camel(item.data_key)
                        data_class = getattr(fetch_new_data, data_class_name)
                        data_class_obj = data_class(top=5, term='', cycle=1)
                        data = data_class_obj.data()
                    except Exception as e:
                        data = fetch_new_data.demo_data()
                    char_data.append({
                        "id": item.id,
                        "name": item.name,
                        "report_type": "report",
                        "chart_type": item.default_chart,
                        "data": data
                    })
            else:
                # 自定义图表
                data_list = models.SSAChart.objects.all().order_by('-id')
                for item in data_list:
                    custom_data = self.get_custom_data(request.user.userinfo, item)
                    char_data.append({
                        "id": item.id,
                        "name": item.name,
                        "report_type": "custom",
                        "chart_type": item.chart_type,
                        "data": custom_data
                    })
        return Response({"status": 200, "data": char_data})


class ReportCellSelect2List(APIView):
    """
    报告元素 Select2
    """

    def post(self, request):
        """
        报告元素
        """
        agent_now = request.user.userinfo.agent
        company_now = request.user.userinfo.company
        q = request.DATA.get("q", '')
        data_list = models.SSAReportCell.objects.filter(
            name__contains=q).values("id", "name")
        result = select2_filter(request, data_list)
        return Response(result)


class ReportTemplateList(APIView):
    """
    报告模板
    """

    def post(self, request):
        """添加模板"""
        obj_serializer = serializers.ReportTemplateSerializers(
            data=request.data,
            context={'request': request})
        if obj_serializer.is_valid():
            obj_serializer.save()
            req = Response({"status": 200, "msg": "添加成功",
                            })
        else:
            errors = obj_serializer.errors
            req = Response({"status": 500, "msg": errors.items()[
                0][1][0], "error": errors})
        return req


class ReportTemplateDetail(APIView):
    """
    报告模板
    """

    def get_obj(self, pk):
        agent_now = self.request.user.userinfo.agent
        company_now = self.request.user.userinfo.company

        try:
            obj = models.SSAReportTemplate.objects.get(id=pk, agent=agent_now, company=company_now)
        except models.SSAReportTemplate.DoesNotExist:
            return False
        return obj

    def get(self, request, pk):
        """
        获取模板信息
        """
        obj = self.get_obj(pk)
        if not obj:
            return Response({"status": 500, "msg": "该模板不存在"})
        data = {
            "id": obj.id,
            "name": obj.name,
            "schedule_type": obj.schedule_type,
            "schedule_time": obj.schedule_time,
            "schedule_days": obj.schedule_days,
            "schedule_months": obj.schedule_months,
            "schedule_start_date": obj.schedule_start_date,
            "cells": obj.ssareporttemplatecell_set.values(),
            "content": obj.content,
        }
        return Response({"status": 200, "msg": "获取模板成功", "data": data})

    def put(self, request, pk):
        """
        修改模板
        """
        obj = self.get_obj(pk)
        if not obj:
            return Response({"status": 500, "msg": "该模板不存在或此模板不允许修改"})

        obj_serializer = serializers.ReportTemplateSerializers(
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
        """
        删除模板
        """
        obj = self.get_obj(pk)
        if not obj:
            return Response({"status": 500, "msg": "该模板不存在或此模板不允许删除"})

        models.SSAReportResult.objects.filter(template=obj).update(template=None)
        obj.delete()
        return Response({"status": 200, "msg": "删除成功"})


class ReportTemplateDts(DatatableView):
    """报告模板"""
    render_columns = [
        ("id", "id", 0),
        ("name", "name", 1),
        ("count", "id", 0),
        ("company_id", "company_id", 0),
        ("next_scan_time", "next_scan_time", 0),
        ("agent_id", "agent_id", 0)
    ]

    model = models.SSAReportTemplate

    def time2hourmin(self, time_obj):
        """ 将datetime.time对象转换成字符串
        """
        str_obj = time_obj.strftime("%H:%M")
        return str_obj

    def get_initial_queryset(self):
        """获取可查询的数据"""
        agent_now = self.request.user.userinfo.agent
        company_now = self.request.user.userinfo.company

        template_type = self.request.data.get('template_type')

        qs = self.model.objects.filter(Q(agent=agent_now, company=company_now)
                                       | Q(agent=None, company=None))
        if template_type:
            if template_type == 2:  # 终端安全检查模版
                qs = qs.filter(id__in=[1, 2, 3, 4, 5, 11])
            elif template_type == 3:  # 安全审计模版
                qs = qs.filter(id__in=[6, 7, 8, 9, 10, 12])
            else:
                qs = qs.filter(template_type=template_type)

        return qs.order_by('-id')

    def prepare_one_result(self, item, data_dict):
        """
        格式化输出形式，不处理则默认按原来对应字段输出
        :param item: 操作对象
        :param data_dict: 操作对象对应结果
        """
        char_count = 0
        content = item.content
        if content:
            content = json.loads(content)
            for line in content:
                if line['type'] == 'echart':
                    char_count = char_count + 1
        data_dict['count'] = char_count
        type_list = ["立即执行",
                     "一次性任务",
                     "每{0}天{1}执行",
                     "每周{0}{1}执行",
                     "每月{0}日{1}执行",
                     "每季度第{0}个月{1}日{2}执行",
                     "每年{0}月{1}日{2}执行",
                     ]
        weekdays = ["一", "二", "三", "四", "五", "六", "日"]
        time_type = item.schedule_type
        if time_type == 1 or time_type == 2:
            data_dict["schedule_time"] = type_list[time_type - 1]
        elif time_type == 3 or time_type == 5:
            data_dict["schedule_time"] = type_list[time_type - 1].format(item.schedule_days,
                                                                         self.time2hourmin(item.schedule_time))
        elif time_type == 4:
            data_dict["schedule_time"] = type_list[time_type - 1].format(
                weekdays[item.schedule_days - 1], self.time2hourmin(item.schedule_time))
        elif time_type in [6, 7]:
            data_dict["schedule_time"] = type_list[time_type - 1].format(
                item.schedule_months, item.schedule_days, self.time2hourmin(item.schedule_time))

        data_dict['default'] = 0
        if not data_dict['agent_id'] and not data_dict['company_id']:
            data_dict['default'] = 1
        data_dict.pop('agent_id')
        data_dict.pop('company_id')
        data_dict['next_scan_time'] = data_dict['next_scan_time']
        return data_dict


class ReportResultDts(DatatableView):
    """报告"""
    render_columns = [
        ("id", "id", 0),
        ("name", "name", 1),
        ("create_time", "create_time", 0),
        ("docx_size", "docx_size", 0),
        ("pdf_size", "pdf_size", 0),
        ("template_type", "template__template_type", 0),
    ]

    model = models.SSAReportResult

    def time2hourmin(self, time_obj):
        """ 将datetime.time对象转换成字符串
        """
        str_obj = time_obj.strftime("%H:%M")
        return str_obj

    def get_initial_queryset(self):
        """获取可查询的数据"""
        agent_now = self.request.user.userinfo.agent
        company_now = self.request.user.userinfo.company
        template_type = self.request.data.get('template_type')
        qs = self.model.objects.filter(
            agent=agent_now, company=company_now).order_by('-id')
        template_id = self.request.data.get("template_id")
        if template_id:
            qs = qs.filter(template_id=template_id)
        if template_type:
            if template_type == 2:  # 终端安全检查模版
                qs = qs.filter(template_id__in=[1, 2, 3, 4, 5, 11])
            elif template_type == 3:  # 安全审计模版
                qs = qs.filter(template_id__in=[6, 7, 8, 9, 10, 12])
            else:
                qs = qs.filter(template_type=template_type)
        return qs

    def prepare_one_result(self, item, data_dict):
        """
        格式化输出形式，不处理则默认按原来对应字段输出
        :param item: 操作对象
        :param data_dict: 操作对象对应结果
        """
        data_dict['create_time'] = timezone.localtime(item.create_time).strftime("%Y-%m-%d %H:%M:%S")
        return data_dict


class ReportResultDetail(APIView):
    """
    报告详情
    """

    def delete(self, request, pk):
        """
        删除
        """
        agent = request.user.userinfo.agent
        company = request.user.userinfo.company
        try:
            task = models.SSAReportResult.objects.get(
                agent=agent,
                company=company,
                id=pk
            )
        except models.SSAReportTemplate.DoesNotExist:
            return Response({"status": 500, "msg": "改报告不存在或不允许删除"})
        task.delete()
        return Response({"status": 200, "msg": "删除成功"})


class TaskStart(APIView):
    """数据报表"""

    def post(self, request, pk):
        """启动报告任务"""
        agent = request.user.userinfo.agent
        company = request.user.userinfo.company
        start_day = request.data.get("start_day")
        end_day = request.data.get("end_day")
        docx_path = os.path.join(REPORT_DIR, 'ssa_report_docx')
        if not os.path.exists(docx_path):
            os.makedirs(docx_path)
        pdf_path = os.path.join(REPORT_DIR, 'ssa_report_pdf')
        if not os.path.exists(pdf_path):
            os.makedirs(pdf_path)
        time_now = timezone.localtime(timezone.now())
        version = timezone.datetime.strftime(time_now, '%Y%m%d%H%M%S')
        try:
            task = models.SSAReportTemplate.objects.get(
                # schedule_type__in=[2], 不限制
                agent=agent,
                company=company,
                id=pk
            )
        except models.SSAReportTemplate.DoesNotExist:
            return Response({"status": 500, "msg": "获取任务错误"})

        docx_path = os.path.join(docx_path, str(task.id) + '_' + version) + '.doc'
        pdf_path = os.path.join(pdf_path, str(task.id) + '_' + version) + '.pdf'
        try:
            logger.info('开始统计报表数据{}'.format(datetime.now()))
            report_data = ReportData(template_id=task.id)
            data = report_data.data(start_day, end_day)
            logger.info('开始生成wor文档{}'.format(datetime.now()))
            m = MakeDocx(template_id=task.id)
            m.generate_docx(path=docx_path, data=data)
            logger.info('开始生成pdf文档{}'.format(datetime.now()))
            p = MakePdf(template_id=task.id)
            p.generate_pdf(path=pdf_path, data=data)
            logger.info('生成pdf文档结束{}'.format(datetime.now()))
            for item in data:
                if 'chart_path' in item and item['chart_path']:
                    os.remove(item['chart_path'])

        except Exception as e:
            logger.error('task id = {0} run error!!'.format(task.id), exc_info=True)
            logger.error(str(e))
            return Response({"status": 500, "msg": "执行错误{0}".format(str(e))})
            # 执行错误
            # task.status = 2
            # task.save()
            # todo 重试
        else:
            logger.info('task id = {0} run success!'.format(task.id))
            result = models.SSAReportResult()
            result.name = task.name + '_' + version
            result.template = task
            result.docx_path = docx_path
            result.docx_size = os.path.getsize(docx_path) if os.path.exists(docx_path) else 0
            result.pdf_path = pdf_path
            result.pdf_size = os.path.getsize(pdf_path) if os.path.exists(pdf_path) else 0
            result.agent = task.agent
            result.company = task.company
            result.template_type = task.template_type
            result.save()
            return Response({"status": 200, "msg": "执行成功"})


def report_download(request, type, pk):
    """下载view"""

    def file_iterator(file_name, chunk_size=512):
        """文件流"""
        with open(file_name, 'rb') as f:
            while True:
                line = f.read(chunk_size)
                if line:
                    yield line
                else:
                    break

    agent = request.user.userinfo.agent
    company = request.user.userinfo.company
    try:
        report = models.SSAReportResult.objects.get(id=pk, agent=agent, company=company)
    except models.SSAReportResult.DoesNotExist:
        return HttpResponse(status=500, content="获取数据错误")
    file_name = report.name
    if type == "pdf":
        file_path = report.pdf_path
    else:
        file_path = report.docx_path
    if not os.path.isfile(file_path):
        return HttpResponse(status=500, charset="报告不存在")
    response = StreamingHttpResponse(file_iterator(file_path))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(
        file_name + ('.pdf' if type == "pdf" else ".doc"))
    return response
