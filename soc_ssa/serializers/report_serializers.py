# coding=utf-8
"""
报告管理序列化
"""
from __future__ import unicode_literals
import json
from django.utils import timezone
from rest_framework import serializers
from soc.serializers import UserInfos
from utils.serializers import generate_error_msg
from soc_ssa import models
from common import get_next_scan_time


class ReportTemplateCellSerializers(serializers.Serializer):
    """
    报告模板元素
    """
    cell_id = serializers.IntegerField(error_messages=generate_error_msg("报告元素ID"))
    cycle = serializers.IntegerField(error_messages=generate_error_msg("统计周期"))
    chart_type = serializers.CharField(error_messages=generate_error_msg("图表类型"))
    has_table = serializers.IntegerField(error_messages=generate_error_msg("表格选项"))
    remark = serializers.CharField(required=False, allow_blank=True, error_messages=generate_error_msg("备注"))
    order = serializers.IntegerField(required=True, error_messages=generate_error_msg("排序字段"))


class ReportTemplateSerializers(serializers.Serializer, UserInfos):
    """
    报告模板
    """
    name = serializers.CharField(
        required=False, allow_null=True,
        error_messages=generate_error_msg("模板名称"))
    cells = serializers.ListField(
        child=serializers.DictField(),
        required=False, allow_null=True,
        error_messages=generate_error_msg("报告元素"))
    # 生成时间
    schedule_type = serializers.IntegerField(
        error_messages=generate_error_msg("周期类型"), max_value=7, min_value=0)
    schedule_time = serializers.TimeField(
        required=False, allow_null=True,
        error_messages=generate_error_msg("执行时间"))
    schedule_days = serializers.IntegerField(
        error_messages=generate_error_msg("执行日期"),
        required=False, allow_null=True, default=1, max_value=32, min_value=1)
    schedule_months = serializers.IntegerField(
        error_messages=generate_error_msg("执行月份"),
        required=False, allow_null=True, default=1, max_value=12, min_value=1)
    schedule_start_date = serializers.CharField(
        required=False, allow_null=True, allow_blank=True,
        default=timezone.localtime(timezone.now()).date(),
        error_messages=generate_error_msg("开始时间"))
    content = serializers.ListField(required=False, error_messages=generate_error_msg("模版内容"))

    def validate_schedule_start_date(self, data):
        if not data:
            return timezone.localtime(timezone.now()).date()
        return timezone.datetime.strptime(data, "%Y-%m-%d")

    def validate_name(self, data):
        if not data:
            if not self.instance:
                raise serializers.ValidationError("模板名称不能为空")
        qs = models.SSAReportTemplate.objects.filter(
            agent=self.agent, company=self.company, name=data)
        if self.instance:
            print(self.instance.id)
            qs = qs.exclude(id=self.instance.id)
        if qs.count() > 0:
            raise serializers.ValidationError("模板名称不能重复")
        return data

    def validate(self, attrs):
        # 按季度执行月份不能超过3
        if attrs['schedule_type'] == 6:
            if attrs['schedule_months'] > 3:
                raise serializers.ValidationError("按季度执行月份不能超过3")
        return attrs

    def validate_cells(self, value):
        data = []
        for index, cell in enumerate(value):
            cell['order'] = cell.get('order', index + 1)
            v = ReportTemplateCellSerializers(data=cell)
            if not v.is_valid():
                raise serializers.ValidationError(v.errors.items()[0][1][0])
            data.append(cell)
        return data

    def create(self, validated_data):
        # cells = validated_data.get("cells") or []
        # del validated_data['cells']
        if validated_data['content']:
            validated_data['content'] = json.dumps(validated_data['content'])
        else:
            del validated_data['content']
        instance = models.SSAReportTemplate.objects.create(
            agent=self.agent, company=self.company, **validated_data
        )

        instance.next_scan_time = get_next_scan_time(
            start_date=instance.schedule_start_date,
            time_s=instance.schedule_time,
            period_type=instance.schedule_type,
            days=instance.schedule_days,
            months=instance.schedule_months
        )
        instance.save()
        '''
        for cell in cells:
            models.SSAReportTemplateCell.objects.create(
                agent=self.agent, company=self.company,
                template=instance,
                **cell)
        '''
        return instance

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.schedule_type = validated_data.get('schedule_type', instance.schedule_type)
        instance.schedule_time = validated_data.get('schedule_time', instance.schedule_time)
        instance.schedule_days = validated_data.get('schedule_days', instance.schedule_days)
        instance.schedule_months = validated_data.get('schedule_months', instance.schedule_months)
        instance.schedule_start_date = validated_data.get('schedule_start_date', instance.schedule_start_date)
        if 'content' in validated_data and validated_data['content']:
            instance.content = json.dumps(validated_data.get('content'))

        '''
        cells = validated_data.get("cells") or []
        if cells:
            instance.ssareporttemplatecell_set.all().delete()
            for cell in cells:
                models.SSAReportTemplateCell.objects.create(
                    agent=self.agent, company=self.company,
                    template=instance,
                    **cell)
        '''
        instance.next_scan_time = get_next_scan_time(
            start_date=instance.schedule_start_date,
            time_s=instance.schedule_time,
            period_type=instance.schedule_type,
            days=instance.schedule_days,
            months=instance.schedule_months
        )
        instance.save()
        return instance
