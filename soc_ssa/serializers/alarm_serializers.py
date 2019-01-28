#coding=utf-8
"""
预警告警序列化
"""
from __future__ import unicode_literals
from django.utils import timezone
from rest_framework import serializers
from soc.serializers import  UserInfos
from utils.serializers import generate_error_msg
from soc_ssa import models


class SSAAlarmCellSerializers(serializers.Serializer):
    id = serializers.IntegerField()
    enable = serializers.IntegerField(min_value=0, max_value=1, error_messages=generate_error_msg("是否启用"))
    alarm = serializers.IntegerField(error_messages=generate_error_msg("告警阈值"))
    warning = serializers.IntegerField(error_messages=generate_error_msg("预警阈值"))

    def update(self, instance, validated_data):
        instance.enable = validated_data.get('enable', instance.enable)
        instance.alarm = validated_data.get('alarm', instance.alarm)
        instance.warning = validated_data.get('warning', instance.warning)
        instance.save()
        return instance


class SSAAlarmNotifySerializers(serializers.Serializer):
    id = serializers.IntegerField()
    sms = serializers.IntegerField(
        min_value=0, max_value=1, error_messages=generate_error_msg("是否启用短信"))
    email = serializers.IntegerField(
        min_value=0, max_value=1, error_messages=generate_error_msg("是否启用邮件"))

    def update(self, instance, validated_data):
        instance.sms = validated_data.get('sms', instance.sms)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance

class SSAAlarmConfSerializers(serializers.Serializer):
    max_alarm_count = serializers.IntegerField(min_value=1, max_value=24, error_messages=generate_error_msg("最大告警次数"))
    toggle_condition = serializers.IntegerField(min_value=1, max_value=2, error_messages=generate_error_msg("触发条件"))
    cells = serializers.ListField(child=serializers.DictField())
    notifys = serializers.ListField(child=serializers.DictField())

    def validate_cells(self, value):
        data = []
        for  cell in value:
            v = SSAAlarmCellSerializers(data=cell)
            if not v.is_valid():
                raise serializers.ValidationError(v.errors.items()[0][1][0])
            data.append(cell)
        return data

    def validate_notifys(self, value):
        data = []
        for  cell in value:
            v = SSAAlarmNotifySerializers(data=cell)
            if not v.is_valid():
                raise serializers.ValidationError(v.errors.items()[0][1][0])
            data.append(cell)
        return data

    def update(self, instance, validated_data):
        instance.max_alarm_count = validated_data.get('max_alarm_count', instance.max_alarm_count)
        instance.toggle_condition = validated_data.get('toggle_condition', instance.toggle_condition)
        
        for cell in validated_data.get('cells'):
            cell_instance = models.SSAAlarmConfCell.objects.get(id=cell['id'])
            v = SSAAlarmCellSerializers(data=cell, instance=cell_instance)
            if v.is_valid():
                v.save()

        for cell in validated_data.get('notifys'):
            cell_instance = models.SSAAlarmNotifyConf.objects.get(id=cell['id'])
            v = SSAAlarmNotifySerializers(data=cell, instance=cell_instance)
            if v.is_valid():
                v.save()

        instance.save()
        return instance
