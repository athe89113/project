# coding=utf-8
import json
from rest_framework import serializers
from utils.serializers import generate_error_msg
from models import (KnowledgeStore, KnowledgeTag, KnowledgeType,
                    PlanStore, PlanTag, PlanContacts, SmWord, GroupRule, AlarmRule, AlarmLog)
from utils.message import PHONE_PREFIX
from common import get_ip_list


class KnowledgeSerializer(serializers.Serializer):
    """转换序列化"""

    title = serializers.CharField(required=True, max_length=256, min_length=1,
                                  error_messages=generate_error_msg('标题'))
    user = serializers.CharField(required=False, max_length=128, allow_blank=True,
                                 error_messages=generate_error_msg('添加人'))
    type = serializers.CharField(required=True, max_length=128,
                                 error_messages=generate_error_msg('分类'))
    content = serializers.CharField(required=True, min_length=1,
                                    error_messages=generate_error_msg('内容'))
    relate = serializers.CharField(required=False, allow_blank=True,
                                   error_messages=generate_error_msg('关联内容'))
    scene = serializers.CharField(required=False, max_length=128, allow_blank=True,
                                  error_messages=generate_error_msg('应用场景'))
    description = serializers.CharField(required=False, max_length=2048, allow_blank=True,
                                        error_messages=generate_error_msg('现象描述'))
    operate = serializers.CharField(required=False, max_length=2048, allow_blank=True,
                                    error_messages=generate_error_msg('运维操作'))
    decide = serializers.CharField(required=False, max_length=2048, allow_blank=True,
                                   error_messages=generate_error_msg('信息研判'))
    feedback = serializers.CharField(required=False, max_length=2048, allow_blank=True,
                                     error_messages=generate_error_msg('结果反馈'))

    # 验证
    def validate_type(self, attr):
        type = KnowledgeType.objects.filter(name=attr).first()
        if not type:
            raise serializers.ValidationError("分类错误")
        return type

    # 创建
    def get_tags(self):
        tag_list = self.context.get('tag', '').split(',')
        tag_data = []
        for tag in tag_list:
            if not tag:
                continue
            tag_obj, _ = KnowledgeTag.objects.get_or_create(name=tag)
            tag_data.append(tag_obj)
        return tag_data

    def create(self, validated_data):
        KnowledgeType.objects.filter()
        store = KnowledgeStore.objects.create(**validated_data)
        tag_data = self.get_tags()
        if tag_data:
            store.tag.add(*tag_data)
        return store

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title')
        instance.user = validated_data.get('user')
        instance.type = validated_data.get('type')
        instance.content = validated_data.get('content')
        instance.relate = validated_data.get('relate')
        instance.scene = validated_data.get('scene')
        instance.description = validated_data.get('description')
        instance.operate = validated_data.get('operate')
        instance.decide = validated_data.get('decide')
        instance.feedback = validated_data.get('feedback')
        instance.save()
        tag_data = self.get_tags()
        if tag_data:
            instance.tag.clear()
            instance.tag.add(*tag_data)
        return instance


class PlanSerializer(serializers.Serializer):
    """转换序列化"""

    title = serializers.CharField(required=True, max_length=256, min_length=1,
                                  error_messages=generate_error_msg('标题'))
    user = serializers.CharField(required=False, max_length=128, min_length=1,
                                 error_messages=generate_error_msg('添加人'))
    level = serializers.IntegerField(required=True, min_value=1,
                                     error_messages=generate_error_msg('等级'))
    scene = serializers.CharField(required=True, max_length=128, min_length=1,
                                  error_messages=generate_error_msg('应用场景'))
    description = serializers.CharField(required=True, min_length=1,
                                        error_messages=generate_error_msg('内容'))
    brief = serializers.CharField(required=False, max_length=2048, min_length=1,
                                  error_messages=generate_error_msg('简介'))

    # 验证
    # 创建
    def get_tags(self):
        tag_list = self.context.get('tag', '').split(',')
        tag_data = []
        for tag in tag_list:
            if not tag:
                continue
            tag_obj, _ = PlanTag.objects.get_or_create(name=tag)
            tag_data.append(tag_obj)
        return tag_data

    def get_contact(self):
        contact = self.context.get('contact', '')
        all_contact = []
        if contact:
            contact_list = contact.split(',')
            for c in contact_list:
                info = c.split('&')
                c_dict = dict()
                c_dict['name'] = info[0]
                c_dict['phone'] = info[1]
                c_dict['email'] = info[2]
                all_contact.append(c_dict)
        return all_contact

    def create(self, validated_data):
        store = PlanStore.objects.create(**validated_data)
        tag_data = self.get_tags()
        if tag_data:
            store.tag.add(*tag_data)
        contact_data = self.get_contact()
        contact_list = []
        for c in contact_data:
            c['plan_id'] = store.id
            contact_list.append(PlanContacts(**c))
        PlanContacts.objects.bulk_create(contact_list)
        return store

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title')
        instance.user = validated_data.get('user')
        instance.level = validated_data.get('level')
        instance.scene = validated_data.get('scene')
        instance.description = validated_data.get('description')
        instance.brief = validated_data.get('brief')
        instance.save()
        tag_data = self.get_tags()
        if tag_data:
            instance.tag.clear()
            instance.tag.add(*tag_data)
        contact_data = self.get_contact()
        contact_list = []
        for c in contact_data:
            c['plan_id'] = instance.id
            contact_list.append(PlanContacts(**c))
        # 删掉旧的管理人
        PlanContacts.objects.filter(plan=instance).delete()
        PlanContacts.objects.bulk_create(contact_list)
        return instance


class PlanContactsSerializer(serializers.Serializer):
    """预案库联系人"""
    name = serializers.CharField(required=True, max_length=256, min_length=1,
                                 error_messages=generate_error_msg('联系人'))
    phone = serializers.CharField(required=True, max_length=11, min_length=11,
                                  error_messages=generate_error_msg('手机号'))
    email = serializers.EmailField(required=True, error_messages=generate_error_msg('邮箱'))

    def validate_phone(self, phone):
        supported = False
        for pre in PHONE_PREFIX:
            if phone.startswith(pre):
                supported = True
                break
        if not supported:
            raise serializers.ValidationError('手机号码不支持')
        return phone

    def create(self, validated_data):
        contact = PlanContacts.objects.create(**validated_data)
        return contact

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name')
        instance.phone = validated_data.get('phone')
        instance.email = validated_data.get('email')
        instance.save()
        return instance


class SmWordSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True, error_messages={'required': 'id必填', })
    """SM词库"""
    word = serializers.CharField(required=True, max_length=50, min_length=1,
                                 error_messages=generate_error_msg('SM词'))


class WorkDaySerializer(serializers.Serializer):
    """转换序列化"""
    id = serializers.IntegerField(required=True, error_messages={'required': 'id必填', })
    week = serializers.CharField(required=True, max_length=100, min_length=1,
                                 error_messages=generate_error_msg('工作日'))
    state = serializers.CharField(required=True, max_length=100, min_length=1,
                                  error_messages=generate_error_msg('上班状态 1-上班 2-休息'))
    am_start_time = serializers.CharField(required=False, max_length=100,
                                          error_messages=generate_error_msg('上午开始时间'))
    am_end_time = serializers.CharField(required=False, max_length=100,
                                        error_messages=generate_error_msg('上午结束时间'))
    pm_start_time = serializers.CharField(required=False, max_length=100,
                                          error_messages=generate_error_msg('下午开始时间'))
    pm_end_time = serializers.CharField(required=False, max_length=100,
                                        error_messages=generate_error_msg('下午结束时间'))


class GroupRuleSerializer(serializers.Serializer):
    """转换序列化"""
    id = serializers.IntegerField(read_only=True)
    group_name = serializers.CharField(required=True, error_messages=generate_error_msg("规则组名称"))
    description = serializers.CharField(required=False, allow_blank=True, error_messages=generate_error_msg('描述'))

    def create(self, validated_data):
        return GroupRule.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.group_name = validated_data.get('group_name')
        instance.description = validated_data.get('description')
        instance.save()
        return instance


class AlarmRuleSerializer(serializers.Serializer):
    """转换序列化"""
    id = serializers.IntegerField(read_only=True)
    group_id = serializers.IntegerField(required=True, error_messages=generate_error_msg("规则组ID"))
    rule_name = serializers.CharField(required=True, error_messages=generate_error_msg("规则名称"))
    description = serializers.CharField(required=False, allow_blank=True, error_messages=generate_error_msg('描述'))
    level = serializers.IntegerField(required=False, default=0)
    status = serializers.IntegerField(required=False, default=-1)
    content = serializers.ListField()
    sql = serializers.CharField(required=False, allow_blank=True, error_messages=generate_error_msg('拼装sql'))
    time_type = serializers.IntegerField(required=False, default=0)
    time_start = serializers.CharField(required=False, allow_blank=True, error_messages=generate_error_msg('开始时间'))
    time_end = serializers.CharField(required=False, allow_blank=True, error_messages=generate_error_msg('结束时间'))
    interval = serializers.IntegerField(required=False, default=0)

    def parase_sql(self, content):
        sql_list = []

        for item in json.loads(content):
            sql = 'select * from all-event-* '
            where_list = []
            time_type = self.validated_data.get('time_type')
            if time_type == 2 or time_type == "2":
                time_start = str(self.validated_data.get('time_start')).replace(":", "")
                time_end = str(self.validated_data.get('time_end')).replace(":", "")
                where = 'stastic_time > ${} AND stastic_time < ${}'.format(time_start, time_end)
                where_list.append(where)
            if 'event_type' in item and item['event_type']:
                where = 'event_three_type=\'{}\' '.format(item['event_type']['name'])
                where_list.append(where)
            if 'sourceIp' in item and item['sourceIp']:
                source_ip_list = item['sourceIp'].split(';')
                ips = []
                for item_ip in source_ip_list:
                    if '-' in item_ip:
                        ip_list = get_ip_list(item_ip)
                        ips.extend(ip_list)
                    else:
                        ips.append(item_ip)
                ips = ['\'{}\''.format(i) for i in ips]
                where = 'src_ip in ({}) '.format(','.join(ips))
                where_list.append(where)
            if 'sourcePort' in item and item['sourcePort']:
                source_port_list = item['sourcePort'].split(';')
                where = 'src_port in ({}) '.format(','.join(source_port_list))
                where_list.append(where)
            if 'targetIp' in item and item['targetIp']:
                target_ip_list = item['targetIp'].split(';')
                ips = []
                for item_ip in target_ip_list:
                    if '-' in item_ip:
                        ip_list = get_ip_list(item_ip)
                        ips.extend(ip_list)
                    else:
                        ips.append(item_ip)
                ips = ['\'{}\''.format(i) for i in ips]
                where = 'dst_ip in ({}) '.format(','.join(ips))
                where_list.append(where)
            if 'targetPort' in item and item['targetPort']:
                target_port_list = item['targetPort'].split(';')
                where = 'dst_port in ({}) '.format(','.join(target_port_list))
                where_list.append(where)

            if where_list:
                sql = sql + 'WHERE ' + ' AND '.join(where_list)
                if 'count' in item and item['count']:
                    sql += '|{}'.format(item['count'])
                sql_list.append(sql)
        return '@'.join(sql_list)

    def create(self, validated_data):
        group_id = validated_data.get('group_id')
        group_rule = GroupRule.objects.get(id=group_id)
        content = json.dumps(validated_data['content']).decode("unicode_escape")
        validated_data['status'] = validated_data['status'] if validated_data['status'] else -1
        validated_data['content'] = content
        validated_data['sql'] = self.parase_sql(content=content)
        instance = AlarmRule.objects.create(**validated_data)
        instance.group = group_rule
        return instance

    def update(self, instance, validated_data):
        instance.rule_name = validated_data.get('rule_name')
        instance.description = validated_data.get('description')
        instance.level = validated_data.get('level')
        instance.status = validated_data.get('status') if validated_data.get('status') else -1
        content = json.dumps(validated_data['content']).decode("unicode_escape")
        instance.content = content
        instance.sql = self.parase_sql(content=content)
        instance.time_type = validated_data.get('time_type')
        instance.time_start = validated_data.get('time_start')
        instance.time_end = validated_data.get('time_end')
        instance.interval = validated_data.get('interval')
        instance.save()
        group_id = validated_data.get('group_id')
        group_rule = GroupRule.objects.get(id=group_id)
        if group_rule:
            instance.group = group_rule
        return instance
