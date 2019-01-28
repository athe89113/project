# coding=utf-8
"""
专家分析系统experts_analysis
"""
from __future__ import unicode_literals
from rest_framework import serializers
from soc.serializers import  UserInfos
from utils.serializers import generate_error_msg
from soc_ssa import models

class RuleManageSerializers(serializers.Serializer, UserInfos):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, error_messages=generate_error_msg("规则名称"))
    # 1 文件夹 2 文件
    type = serializers.IntegerField(
        min_value=1, max_value=2, error_messages=generate_error_msg("类型"))
    sql = serializers.CharField(
        required=False, allow_null=True, allow_blank=True, error_messages=generate_error_msg("SQL"))
    parent_id = serializers.IntegerField(required=False, allow_null=True)

    def validate_name(self, name):
        qs = models.SSARuleManage.objects.filter(
            agent=self.agent, company=self.company, name=name)
        if self.instance:
            qs = qs.exclude(id=self.instance.id)
        if qs.count() > 0:
            raise serializers.ValidationError("名称不能重复")
        return name

    def create(self, validated_data):
        if not validated_data['parent_id']:
            del validated_data['parent_id']
        return models.SSARuleManage.objects.create(agent=self.agent, company=self.company, **validated_data)

    def update(self, instance, validated_data):
        if not validated_data['parent_id']:
            del validated_data['parent_id']
        instance.name = validated_data.get("name", instance.name)
        instance.sql = validated_data.get("sql", instance.sql)
        instance.save()
        return instance
