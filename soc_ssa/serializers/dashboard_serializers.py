# coding: utf-8
from __future__ import unicode_literals
import json
from soc_ssa import models
from soc_ssa import ssa_common
from rest_framework import serializers
from utils.serializers import generate_error_msg
from soc.serializers import UserInfos


class SSAdashborad(serializers.Serializer):
    "dashborad"
    name = serializers.CharField(
        required=True, max_length=256, error_messages=generate_error_msg("名称"))

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.save()
        return instance


class SSAChartSerializer(serializers.Serializer, UserInfos):
    """图表"""

    name = serializers.CharField(
        required=True, max_length=256, error_messages=generate_error_msg("名称"))
    chart_type = serializers.CharField(
        required=False, max_length=256, error_messages=generate_error_msg("图表类型"))
    map_type = serializers.CharField(
        required=False, max_length=256, error_messages=generate_error_msg("地图类型"))
    type = serializers.IntegerField(
        required=False, error_messages=generate_error_msg("图表标签"))
    data_tag = serializers.IntegerField(
        required=True, error_messages=generate_error_msg("数据标签"))
    limit = serializers.IntegerField(default=0, error_messages=generate_error_msg("显示条数"))
    styles = serializers.DictField(
        write_only=True,
        required=False, default='{}', error_messages=generate_error_msg("样式配置"))
    x = serializers.ListField(
        # type=serializers.CharField(max_length=256),
        # value=serializers.CharField(max_length=256),
        # order=serializers.CharField(max_length=256),
    )
    y = serializers.ListField(
        # aggregator=serializers.CharField(max_length=256),
        # value=serializers.CharField(max_length=256),
        # order=serializers.CharField(max_length=256),
    )
    query_time = serializers.IntegerField(
        required=False,
        error_messages=generate_error_msg("时间周期"))

    data_type = serializers.IntegerField(required=False, error_messages=generate_error_msg("数据源类型"))

    def validate_name(self, data):
        """
        v name
        """
        if not data:
            raise serializers.ValidationError("图表名称不能为空")
        qs = models.SSAChart.objects.filter(
            agent=self.agent, company=self.company, name=data)
        if self.instance:
            qs = qs.exclude(id=self.instance.id)
        if qs.count() > 0:
            raise serializers.ValidationError("图表名称不能重复")
        return data

    def validate_x(self, data):
        """
        验证维度
        """
        uniq_list = []
        for i in data:
            if not isinstance(i, dict):
                raise serializers.ValidationError("维度条件错误")
            uniq_str = str(i)
            if uniq_str in uniq_list:
                raise serializers.ValidationError("维度条件重复")
            else:
                uniq_list.append(uniq_str)
            i_type = i.get('type')
            i_value = i.get('value')
            i_order = i.get('order')

            if i_type not in ['date', 'key']:
                raise serializers.ValidationError("维度类型错误")
            if not i_value:
                raise serializers.ValidationError("维度值不能为空")
            if i_order:
                if i_order not in ['desc', 'asc']:
                    raise serializers.ValidationError("排序方式错误")
        return data

    def validate_y(self, data):
        """
        验证数值字段
        """
        uniq_list = []
        for i in data:
            if not isinstance(i, dict):
                raise serializers.ValidationError("查询条件错误")
            uniq_str = str(i)
            if uniq_str in uniq_list:
                raise serializers.ValidationError("查询条件重复")
            else:
                uniq_list.append(uniq_str)
            i_type = i.get('aggregator')
            i_value = i.get('value')
            i_order = i.get('order')
            if i_type not in ssa_common.AGG_MAP.keys():
                raise serializers.ValidationError("聚合方式错误")
            if not i_value:
                raise serializers.ValidationError("数值字段不能为空")
            if i_order:
                if i_order not in ['desc', 'asc']:
                    raise serializers.ValidationError("排序方式错误")
        return data

    '''
    def validate_data_tag(self, data):
        """
        v name
        """
        try:
            models.SSADataTag.objects.get(id=data)
        except models.SSADataTag.DoesNotExist:
            raise serializers.ValidationError("数据标签错误")
        return data
    '''

    def create(self, validated_data):
        # validated_data['data_tag_id'] = validated_data['data_tag']
        validated_data['x'] = json.dumps(validated_data['x'])
        validated_data['y'] = json.dumps(validated_data['y'])
        validated_data['styles'] = json.dumps(validated_data['styles'])
        # del validated_data['data_tag']
        instance = models.SSAChart.objects.create(
            agent=self.agent, company=self.company, **validated_data)
        return instance

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.type = validated_data.get("type", instance.type)
        instance.limit = validated_data.get("limit", instance.limit)
        instance.chart_type = validated_data.get("chart_type", instance.chart_type)
        instance.map_type = validated_data.get("map_type", instance.map_type)
        instance.data_tag = validated_data.get("data_tag", instance.data_tag)
        instance.query_time = validated_data.get("query_time", instance.query_time)
        x = validated_data.get('x')
        y = validated_data.get('y')
        styles = validated_data.get('styles')
        if x:
            instance.x = json.dumps(x)
        if y:
            instance.y = json.dumps(y)
        if styles:
            instance.styles = json.dumps(styles)
        instance.data_type = validated_data.get("data_type", instance.data_type)
        instance.save()
        return instance


class SSAChartPerViewSerializer(SSAChartSerializer):
    """
    预览接口验证
    """
    name = serializers.CharField(
        required=False, max_length=256, error_messages=generate_error_msg("名称"))

    def validate_name(self, data):
        """
        预览不验证名称
        """
        return data
