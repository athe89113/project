# coding=utf-8
from rest_framework import serializers
from utils.serializers import generate_error_msg as error_msg


class EventTimeLineSerializer(serializers.Serializer):
    tag = serializers.IntegerField(default=1, error_messages=error_msg("事件来源"))
    ip = serializers.CharField(error_messages=error_msg("IP格式"))
    start = serializers.IntegerField(default=0, error_messages=error_msg("开始数目"))
    length = serializers.IntegerField(default=10, error_messages=error_msg("查询条数"))
    min_level = serializers.IntegerField(default=0, min_value=0, max_value=5, error_messages=error_msg("最低威胁级别"))
    max_level = serializers.IntegerField(default=5, min_value=0, max_value=5, error_messages=error_msg("最高威胁级别"))
    event_type = serializers.CharField(required=False, allow_blank=True, error_messages=error_msg("事件类型"))

    def validate(self, data):
        min_level = data.get("min_level")
        max_level = data.get("max_level")
        if min_level > max_level:
            raise serializers.ValidationError("最低威胁级别不能大于最高威胁级别")
        return data


class IpEventSerializer(serializers.Serializer):
    event_name = serializers.CharField(error_messages=error_msg("事件名称"))
    level = serializers.IntegerField(min_value=0, max_value=5, error_messages=error_msg("事件等级"))
    event_time = serializers.CharField(max_length=20, error_messages=error_msg("事件时间"))
    source_ip = serializers.CharField(max_length=16, error_messages=error_msg("来源IP"))
    source_port = serializers.IntegerField(min_value=1, max_value=65535, error_messages=error_msg("来源PORT"))
    source_addr = serializers.CharField(error_messages=error_msg("事件来源地址"))
    target_ip = serializers.CharField(max_length=16, error_messages=error_msg("目标IP"))
    target_port = serializers.IntegerField(min_value=1, max_value=65535, error_messages=error_msg("目标PORT"))
    target_addr = serializers.CharField(error_messages=error_msg("事件目标地址"))
    comment = serializers.CharField(error_messages=error_msg("事件备注"))


class EventSerializer(serializers.Serializer):
    ip = serializers.CharField(error_messages=error_msg("事件源地址"))
    tag = serializers.IntegerField(min_value=1, error_messages=error_msg("事件数据标签"))
    event_time = serializers.CharField(error_messages=error_msg("事件时间"))
    start = serializers.IntegerField(default=0, error_messages=error_msg("开始数目"))
    length = serializers.IntegerField(default=10, error_messages=error_msg("查询条数"))


class EventLineSerializer(serializers.Serializer):
    ip = serializers.CharField(error_messages=error_msg("事件源地址"))
    tag = serializers.IntegerField(min_value=1, error_messages=error_msg("事件数据标签"))
    event_time = serializers.CharField(error_messages=error_msg("事件时间"))

