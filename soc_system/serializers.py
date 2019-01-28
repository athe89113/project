# coding=utf-8
from __future__ import unicode_literals
import re
import json
import logging
import random
import os
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from soc.models import Agent
from rest_framework import serializers
from django.db import transaction
from django.contrib.auth.models import User as ModelUser
from soc_system import models
from soc_system.system_common import get_node_detail
from soc_user import models as user_models
from common import generate_google_url
from utils import version
from utils.api import NodeApi
from soc_knowledge import models as knowledge_model

logger = logging.getLogger("soc_system")


def is_email(email):
    if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email):
        return True
    return False


def get_error_messages(key):
    error_messages = {
        "max_value": "{} 错误".format(key),
        "min_value": "{} 错误".format(key),
        "invalid": "{} 错误".format(key),
        "null": "{} 错误".format(key),
    }
    return error_messages


class AuthSerializers(serializers.Serializer):
    """
    认证
    """

    auth_key = serializers.CharField(max_length=8192, allow_null=False, allow_blank=False, required=True,
                                     error_messages={'invalid': '认证key错误', 'blank': "认证key不能为空",
                                                     "null": "认证key不能为空", 'max_length': "认证key长度超出限制",
                                                     "required": "认证key参数必需",
                                                     }
                                     )
    # 格式 v2.24.6
    version = serializers.CharField(max_length=10, allow_null=False, allow_blank=False, required=True,
                                    error_messages={'invalid': '版本错误', 'blank': "版本不能为空",
                                                    "null": "版本不能为空", 'max_length': "版本长度超出限制",
                                                    "required": "版本号参数必需",
                                                    }
                                    )

    type = serializers.CharField(required=True, max_length=15,
                                 error_messages={"required": "中心类型错误", 'invalid': '中心类型错误',
                                                 'blank': "中心类型不能为空",
                                                 "null": "中心类型不能为空", 'max_length': "中心类型长度超出限制"}
                                 )

    name = serializers.CharField(allow_null=True, allow_blank=True, default='上级中心')
    ip = serializers.CharField(allow_null=True, allow_blank=True, default='127.0.0.1')
    # 中心标识
    uuid = serializers.UUIDField(required=True,
                                 error_messages={"required": "中心标识错误", 'invalid': '中心标识错误',
                                                 'blank': "中心标识不能为空",
                                                 "null": "中心标识不能为空", }
                                 )

    def validate_type(self, data):
        if data not in ["center", "sub_center", "child_center"]:
            raise serializers.ValidationError("中心类型配置错误")
        return data

    def validate_version(self, data):
        """
        :param data:
        :return:
        """
        if not data.startswith('v'):
            raise serializers.ValidationError("版本格式错误")
        try:
            self_version = version.get_int_version()
            parent_version = version.get_version(data, type='int')
        except Exception as e:
            logger.error(data)
            logger.error(e)
            raise serializers.ValidationError("版本格式错误")
        else:
            if parent_version < self_version:
                raise serializers.ValidationError("版本过低，不能级联，请升级至 {0} 及以上版本".format(version.get_version()))

        return data

    def create(self, validated_data):
        return None

    def update(self, instance, validated_data):
        return None


class ParentStatusSerializers(serializers.Serializer):
    """
    认证
    """

    auth_key = serializers.CharField(max_length=8192, allow_null=False, allow_blank=False, required=True,
                                     error_messages={'invalid': '认证key错误', 'blank': "认证key不能为空",
                                                     "null": "认证key不能为空", 'max_length': "认证key长度超出限制",
                                                     "required": "认证key参数必需",
                                                     }
                                     )

    def create(self, validated_data):
        return None

    def update(self, instance, validated_data):
        return None


class NodeSerializers(serializers.Serializer):
    """
    中心序列化
    """
    # 名称
    name = serializers.CharField(max_length=128, required=False, default='127.0.0.1',
                                 error_messages={'invalid': '名称错误', 'blank': "名称不能为空", "null": "名称不能为空",
                                                 'max_length': "名称长度超出限制"})
    # 备注
    info = serializers.CharField(max_length=256, required=False, default='', allow_blank=True, allow_null=True,
                                 error_messages={"invalid": "备注错误", "max_length": "超出最大长度"})
    # IP地址
    ip = serializers.CharField(required=True, max_length=200, min_length=None, allow_blank=False,
                               error_messages={"required": "中心地址不能为空", 'invalid': '中心地址错误',
                                               'blank': "中心地址不能为空", "null": "中心地址不能为空"}
                               )

    port = serializers.IntegerField(default=80, min_value=1, max_value=65535,
                                    error_messages={"required": "IP地址不能为空", 'invalid': 'IP地址错误',
                                                    'blank': "IP地址不能为空", "null": "IP地址不能为空",
                                                    "max_value": "端口范围1~65535", "min_value": "端口范围1~65535"})
    # 角色
    role = serializers.CharField(required=True, max_length=10,
                                 error_messages={'required': '中心类型错误', 'invalid': '中心类型错误',
                                                 'blank': "中心类型不能为空",
                                                 "null": "中心类型不能为空", 'max_length': "中心类型长度超出限制"}
                                 )
    # 类型
    type = serializers.CharField(required=False, max_length=15, allow_blank=True, allow_null=True,
                                 error_messages={"required": "中心类型错误", 'invalid': '中心类型错误',
                                                 'blank': "中心类型不能为空",
                                                 "null": "中心类型不能为空", 'max_length': "中心类型长度超出限制"}
                                 )

    auth_key = serializers.CharField(max_length=8192, allow_null=True, allow_blank=True, required=False,
                                     error_messages={'invalid': '认证错误', 'blank': "认证不能为空",
                                                     "null": "认证不能为空", 'max_length': "认证长度超出限制"}
                                     )

    # 配置本中心设置
    # 允许上级级联
    accept_parent_connection = serializers.IntegerField(
        default=0, max_value=1, min_value=0, allow_null=False,
        error_messages=get_error_messages('允许上级级联')
    )
    # 接收并应用上级控制中心下发的策略
    accept_apply_policy = serializers.IntegerField(
        default=0, max_value=1, min_value=0, allow_null=False,
        error_messages=get_error_messages('接收并应用上级控制中心下发的策略')
    )
    # 接收并应用上级控制中心下发的事件库升级包
    accept_apply_event_db = serializers.IntegerField(
        default=0, max_value=1, min_value=0, allow_null=False,
        error_messages=get_error_messages('接收并应用上级控制中心下发的事件库升级包')
    )
    # 接收并应用上级控制中心下发的引擎升级包
    accept_apply_engine = serializers.IntegerField(
        default=0, max_value=1, min_value=0, allow_null=False,
        error_messages=get_error_messages('接收并应用上级控制中心下发的引擎升级包')
    )
    # 接收并应用上级控制中心下发的控制中心升级包
    accept_apply_center = serializers.IntegerField(
        default=0, max_value=1, min_value=0, allow_null=False,
        error_messages=get_error_messages('接收并应用上级控制中心下发的控制中心升级包')
    )

    accept_apply_message = serializers.IntegerField(
        default=0, max_value=1, min_value=0, allow_null=False,
        error_messages=get_error_messages('接收上级控制中心下发的事件通知')
    )
    accept_apply_loophole = serializers.IntegerField(
        default=0, max_value=1, min_value=0, allow_null=False,
        error_messages=get_error_messages('接收并应用上级控制中心下发的漏洞库升级包')
    )
    next_message = serializers.IntegerField(
        default=0, max_value=1, min_value=0, allow_null=False,
        error_messages=get_error_messages('接收下级控制中心上报的事件通知')
    )
    next_source = serializers.IntegerField(
        default=0, max_value=1, min_value=0, allow_null=False,
        error_messages=get_error_messages('接收下级控制中心上报的资源数据')
    )
    next_monitor = serializers.IntegerField(
        default=0, max_value=1, min_value=0, allow_null=False,
        error_messages=get_error_messages('接收下级控制中心上报的监控数据')
    )
    next_loophole = serializers.IntegerField(
        default=0, max_value=1, min_value=0, allow_null=False,
        error_messages=get_error_messages('接收下级控制中心上报的漏洞信息')
    )
    next_attack = serializers.IntegerField(
        default=0, max_value=1, min_value=0, allow_null=False,
        error_messages=get_error_messages('接收下级控制中心上报的攻击信息')
    )

    # 当下级中心失联时发出告警
    notify_when_lose_children = serializers.IntegerField(
        default=0, max_value=1, min_value=0, allow_null=False,
        error_messages=get_error_messages('当下级中心失联时发出告警')
    )

    def validate_name(self, data):
        agent = self.context.get("agent")
        if self.instance:
            if models.Node.objects.filter(name=data, agent=agent).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError("中心名称重复")
        else:
            if models.Node.objects.filter(name=data, agent=agent).exists():
                raise serializers.ValidationError("中心名称重复")
        return data

    def validate_role(self, data):
        if data not in ["parent", "child", "self"]:
            raise serializers.ValidationError("中心角色错误")
        return data

    def validate_type(self, data):
        if self.instance:
            # TODO 有父子链接的时候不能修改
            if data != self.instance.type:
                request = self.context['request']
                parent = models.Node.objects.filter(agent=request.user.userinfo.agent, role='parent').first()
                children = models.Node.objects.filter(agent=request.user.userinfo.agent, role='child')
                if parent or children:
                    raise serializers.ValidationError("有上下级中心，禁止修改角色")
            if data and data not in ["center", "sub_center", "child_center"]:
                raise serializers.ValidationError("中心类型配置错误")
        return data

    def validate_auth_key(self, attr):
        "auth_key 密码"
        return attr

    def validate_ip(self, data):
        """
        下级地址
        :param data:
        :return:
        """
        val = URLValidator()
        try:
            val('http://{}'.format(data))
        except ValidationError:
            raise serializers.ValidationError("中心地址错误")

        return data

    def validate(self, attrs):
        agent = self.context.get("agent")
        if self.instance:
            # update
            # TODO 有父子链接的时候不能修改
            if attrs['auth_key'] != self.instance.auth_key and attrs.get('role') == 'self':
                request = self.context['request']
                parent = models.Node.objects.filter(agent=request.user.userinfo.agent, role='parent').first()
                if parent:
                    raise serializers.ValidationError('有上级中心，禁止修改密码')
        else:
            role = attrs.get("role")
            node_type = attrs.get("type")
            if node_type:
                if (role, node_type) in [('parent', 'child_center'), ("child", "center")]:
                    raise serializers.ValidationError("中心类型配置错误")

            if role == 'parent':
                # 只有一个上级中心
                if models.Node.objects.filter(role=role, agent=agent).exists():
                    raise serializers.ValidationError("只能添加一个上级中心")
                # 若当前中心为 center，则不能添加 center 中心
                self_node = models.Node.objects.filter(role='self').first()
                if not self_node:
                    raise serializers.ValidationError("请先配置本级角色")
                if self_node.type == 'center':
                    raise serializers.ValidationError("总中心不需要配置上级中心")
                # if self_node.type == 'sub_center' and node_type in ['child_center', 'sub_center']:
                #     raise serializers.ValidationError("分中心不能配置上级子中心或分中心")
                # if self_node.type == 'child_center' and node_type == "child_center":
                #     raise serializers.ValidationError("子中心不能配置上级子中心")
            elif role == 'self':
                attrs["ip"] = "127.0.0.1"
                attrs["status"] = 1
                # 自己只能配置一个
                if models.Node.objects.filter(role=role, agent=agent).exists():
                    raise serializers.ValidationError("中心配置配置重复")
            elif role == "child":
                # 添加子中心
                # 若当前中心为 child_center，则不能添加 child_center 中心
                self_node = models.Node.objects.filter(role='self', agent=agent).first()
                if not self_node:
                    raise serializers.ValidationError("请先配置本级角色")
                if self_node.type == 'child_center':
                    raise serializers.ValidationError("子中心不能配置下级中心")

                # 下级中心认证
                node_auth_key = attrs.get("auth_key")
                node_ip = attrs.get("ip")
                # 获取认证
                node_api = NodeApi(base_url='http://' + node_ip, auth_key=node_auth_key)
                result = node_api.fetch_auth(self_node_info=self_node.get_dict())
                if result["status"] == 200:
                    status = 1
                    secret_id = result.get("data", {}).get("secret_id")
                    secret_key = result.get("data", {}).get("secret_key")
                    # 检查下级中心的类型
                    get_node_type = result.get("data", {}).get("type")
                    child_version = result.get("data", {}).get("version")
                    if not get_node_type or not secret_id or not secret_key:
                        raise serializers.ValidationError("没有获取到下级中心的角色，请先配置下级中心")

                    if self_node.type == 'center' and get_node_type == 'center':
                        raise serializers.ValidationError("总中心不能配置下级总中心")
                    if self_node.type == 'sub_center' and get_node_type in ['center', 'sub_center']:
                        raise serializers.ValidationError("分中心不能配置下级总中心或分中心")
                else:
                    msg = result.get('msg', "下级中心认证错误")
                    raise serializers.ValidationError(msg)

                attrs["secret_id"] = secret_id
                attrs["secret_key"] = secret_key
                attrs["status"] = status
                attrs["type"] = get_node_type
                attrs["version"] = child_version

            else:
                raise serializers.ValidationError("中心类型错误")

        attrs["agent_id"] = agent.id
        return attrs

    def get_or_create_ghost_user(self, ):
        """
        创建 ghost 用户
        :return:
        """

        ghost_user = user_models.UserInfo.objects.filter(agent=self.context.get("agent"), is_ghost=1,
                                                         user__username__startswith='ghost_user_').first()
        if not ghost_user:
            password = ''.join([random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789!@#') for i in range(50)])
            username = 'ghost_user_{0}'.format(password[:5])
            email = username + '@ghost.com'
            ghost_user = ModelUser.objects.create_user(username=username, password=password, email=email)
            user_info = user_models.UserInfo()
            user_info.user = ghost_user
            user_info.agent = self.context.get("agent")
            user_info.role_type = 2
            user_info.is_admin = 1
            user_info.is_ghost = 1
            gs_key, b32secret, url, _ = generate_google_url(username)
            user_info.google_secret = gs_key
            user_info.gs_status = 1
            user_info.save()

        return ghost_user

    def create(self, validated_data):
        """
        添加
        :param validated_data:
        :return:
        """
        accept_next_settings = {
            "next_message": validated_data['next_message'],
            "next_source": validated_data['next_source'],
            "next_monitor": validated_data['next_monitor'],
            "next_loophole": validated_data['next_loophole'],
            "next_attack": validated_data['next_attack']
        }
        accept_next_settings = json.dumps(accept_next_settings)
        data = {
            "version": version.get_version(),
            "accept_next_settings": accept_next_settings
        }
        data.update(validated_data)
        for sett in ['next_message', 'next_source', 'next_monitor', 'next_loophole', 'next_attack']:
            data.pop(sett)
        new_node = models.Node.objects.create(**data)
        self.get_or_create_ghost_user()
        return new_node

    def update(self, instance, validated_data):
        """
        更新
        :param instance:
        :param validated_data:
        :return:
        """
        instance.version = version.get_version()
        instance.name = validated_data.get('name', instance.name)
        instance.info = validated_data.get('info', instance.info)
        instance.ip = validated_data.get('ip', instance.ip)
        instance.port = validated_data.get('port', instance.port)
        # self settings
        old_accept = json.loads(instance.accept_next_settings)
        accept_next_settings = {
            "next_message": validated_data.get('next_message', old_accept.get('next_message')),
            "next_source": validated_data.get('next_source', old_accept.get('next_source')),
            "next_monitor": validated_data.get('next_monitor', old_accept.get('next_monitor')),
            "next_loophole": validated_data.get('next_loophole', old_accept.get('next_loophole')),
            "next_attack": validated_data.get('next_attack', old_accept.get('next_attack'))
        }
        accept_next_settings = json.dumps(accept_next_settings)
        instance.accept_next_settings = accept_next_settings
        instance.accept_parent_connection = validated_data.get("accept_parent_connection", instance.accept_parent_connection)
        instance.accept_apply_policy = validated_data.get("accept_apply_policy", instance.accept_apply_policy)
        instance.accept_apply_event_db = validated_data.get("accept_apply_event_db", instance.accept_apply_event_db)
        instance.accept_apply_engine = validated_data.get("accept_apply_engine", instance.accept_apply_engine)
        instance.accept_apply_center = validated_data.get("accept_apply_center", instance.accept_apply_center)
        instance.notify_when_lose_children = validated_data.get("notify_when_lose_children", instance.notify_when_lose_children)
        # 修改了通信地址需要重新检测链接状态
        if validated_data.get('ip') or validated_data.get('port') or validated_data.get("auth_key"):
            instance.status = 0
        # 更新类型，处理变化
        with transaction.atomic():
            if instance.role == 'self':
                auth_key_changed = validated_data.get('auth_key') and validated_data.get('auth_key') != instance.auth_key

                ghost_user = self.get_or_create_ghost_user()
                # 密钥变换
                # 更换 token 秘钥，
                if auth_key_changed:
                    instance.auth_key = validated_data.get('auth_key', instance.auth_key)

                    token = ''.join([random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789') for i in range(20)])
                    user_models.SecretKey.objects.update_or_create(user=ghost_user, defaults={"key": token})
                    # 更改上级状态
                    models.Node.objects.filter(agent=instance.agent, role='parent').update(status=2)

                # 角色变换
                new_type = validated_data.get("type")
                i_type = instance.type
                if new_type and new_type != i_type:
                    # 类型变化
                    # 1. 总中心->分中心，如连接的下级是分中心则清除下级关系，如连接的是子中心则保留下级关系
                    # 2. 总中心->子中心，清除下级关系
                    # 3. 分中心->子中心，清除下级关系
                    # 4. 分中心->总中心，清除上级关系
                    # 5. 子中心->分中心，如连接的是总中心则保留上级关系，如连接的是分中心则清除关系
                    # 6. 子中心->总中心，清除上级关系
                    if (i_type, new_type) in [
                        ('sub_center', 'center'),  # 4
                        ('child_center', 'center')  # 6
                    ]:
                        self.clear_parent(instance)
                    elif (i_type, new_type) in [
                        ('center', 'child_center'),   # 2
                        ('sub_center', 'child_center')  # 3
                    ]:
                        self.clear_children(instance, type='child_center')
                        self.clear_children(instance, type='sub_center')
                    elif (i_type, new_type) in [
                        ('center', 'sub_center')  # 1
                    ]:
                        self.clear_children(instance, type='sub_center')
                    elif (i_type, new_type) in [
                        ('child_center', 'sub_center')  # 5
                    ]:
                        parent = models.Node.objects.filter(agent=instance.agent, role='parent').first()
                        if parent.type == 'sub_center':
                            parent.delete()
            instance.type = validated_data.get('type', instance.type)
            instance.save()
        return instance

    def clear_parent(self, node):
        """
        清除上级中心
        :param node:
        :return:
        """
        models.Node.objects.filter(agent=node.agent, role='parent').delete()

    def clear_children(self, node, type):
        """
        清除下级中心
        :param node:
        :param type:
        :return:
        """
        models.Node.objects.filter(agent=node.agent, role='child', type=type).delete()


class MenuSerializers(serializers.Serializer):
    """
    菜单序列化
    """

    name = serializers.CharField(allow_null=False, allow_blank=False,
                                 error_messages={"null": "名称不能为空", "blank": "名称不能为空", "invalid": "名称输入错误"})
    sort = serializers.IntegerField(allow_null=False, default=50, min_value=1, max_value=99,
                                    error_messages={"null": "排序不能为空", "max_value": "排序最大值为99",
                                                    "min_value": "排序最小值为1", "invalid": "排序输入错误"})
    enable = serializers.IntegerField(allow_null=False, max_value=1, min_value=0,
                                      error_messages={"null": "启用参数错误", "min_value": "启用参数错误",
                                                      "max_value": "启用参数错误", "invalid": "启用输入错误"})
    is_landing = serializers.IntegerField(allow_null=False, max_value=1, min_value=0,
                                          error_messages={"null": "着陆页参数错误", "min_value": "着陆页参数错误",
                                                          "max_value": "着陆页参数错误", "invalid": "着陆页输入错误"})

    def validate_name(self, data):
        if self.instance:
            if not self.instance.default_menu.parent:
                max_name_length = 6
                level = '一'
            else:
                max_name_length = 7
                level = '二三'
            if len(data) > max_name_length:
                raise serializers.ValidationError("{0}级菜单名称最长为{1}个字符".format(level, max_name_length))
        return data

    def validate(self, attrs):
        if self.instance:
            # 着陆页必须启用
            is_landing = attrs.get("is_landing", self.instance.is_landing)
            enable = attrs.get("enable", self.instance.enable)
            if enable == 0 and is_landing == 1:
                raise serializers.ValidationError("着陆页必须启用")
            # 着陆页必须是最低级别的默认页面
            if is_landing == 1:
                # 必须是默认页面
                # 默认页面必须是最低级别页面
                if not self.instance.default_menu \
                        or not self.instance.default_menu.level \
                        or self.instance.default_menu.level.endswith("00"):
                    raise serializers.ValidationError("该页面不能设置为着陆页")
        return attrs

    def create(self, validated_data):
        return None

    def update(self, instance, validated_data):
        """
        更新
        :param instance:
        :param validated_data:
        :return:
        """

        instance.name = validated_data.get("name", instance.name)
        instance.enable = validated_data.get("enable", instance.enable)
        instance.sort = validated_data.get("sort", instance.sort)
        # 着陆页
        is_landing = validated_data.get("is_landing", instance.is_landing)
        instance.is_landing = is_landing
        with transaction.atomic():
            instance.save()

            # 处理菜单的启用和禁用状态
            # 1. 父级别菜单禁用会使得所有子菜单禁用
            # 2. 最后一个子菜单禁用会使得父级别菜单禁用
            # 3. 父级别菜单启用会启用所有禁用的菜单？
            default_menu = instance.default_menu
            level = default_menu.level
            if level.endswith('00'):
                # 不是最后一级子菜单时
                while level.endswith('00'):
                    level = level[:len(level)-2]
                # 当前菜单的子菜单
                child_menus = models.DefaultMenu.objects.filter(level__startswith=level).exclude(id=default_menu.id).all()
                for child in child_menus:
                    child_advance = child.advancedmenu_set.filter(agent=instance.agent).first()
                    child_advance.enable = instance.enable
                    child_advance.save()

            # 与当前菜单平行的菜单
            if default_menu.parent:
                same_level_menus = default_menu.parent.defaultmenu_set.exclude(id=default_menu.id)
                ass_list = []
                if same_level_menus:
                    for cs in same_level_menus:
                        ass = cs.advancedmenu_set.filter(agent=instance.agent).first()
                        ass_list.append(ass.enable)
                ass_list = list(set(ass_list))
                if len(ass_list) == 0 or len(ass_list) == 1 and (ass_list[0], instance.enable) in [(0, 1), (0, 0), (1, 1)]:
                    child_advance = default_menu.parent.advancedmenu_set.filter(agent=instance.agent).first()
                    child_advance.enable = instance.enable
                    child_advance.save()

            if is_landing == 1:
                # 设置其他登录页为0
                models.AdvancedMenu.objects.filter(agent=instance.agent).exclude(id=instance.id).update(is_landing=0)

        return instance


# class MsgSerializers(serializers.Serializer, UserInfos):
class MsgSerializers(serializers.Serializer):
    """

    """
    # agent_id = serializers.IntegerField(allow_null=False, allow_blank=False, error_messages={"invalid": "代理商错误"})
    api = serializers.CharField(allow_null=True, allow_blank=True, max_length=256,
                                error_messages={'max_length': "api长度超出限制", "invalid": "API错误"})
    user = serializers.CharField(allow_null=True, allow_blank=True, max_length=64,
                                 error_messages={'max_length': "用户名长度超出限制", "invalid": "API用户名错误"})
    password = serializers.CharField(allow_null=True, allow_blank=True, max_length=64,
                                     error_messages={'max_length': "密码长度超出限制", "invalid": "API密码错误"})

    def create(self, validated_data):
        return None

    def update(self, instance, validated_data):
        # instance.agent_id = self.agent.id
        instance.api = validated_data.get("api", instance.api)
        instance.user = validated_data.get("user", instance.user)
        if validated_data.get("password", None):
            instance.password = validated_data.get("password", instance.password)
        instance.save()
        return instance


class SMTPSerializers(serializers.Serializer):
    """
    """
    smtp_server = serializers.CharField(allow_null=True, allow_blank=True,
                                        error_messages={"invalid": "smtp服务器错误"})
    send_sender = serializers.CharField(allow_null=True, allow_blank=True,
                                        error_messages={"invalid": "smtp发信地址"})
    user = serializers.CharField(allow_null=True, allow_blank=True,
                                 error_messages={"invalid": "smtp用户名"})
    password = serializers.CharField(allow_null=True, allow_blank=True,
                                     error_messages={"invalid": "smtp密码"})
    tls_or_ssl = serializers.BooleanField(default=False)

    def create(self, validated_data):
        return None

    def update(self, instance, validated_data):
        instance.smtp_server = validated_data.get('smtp_server', instance.smtp_server)
        instance.send_sender = validated_data.get('send_sender', instance.send_sender)
        instance.user = validated_data.get('user', instance.user)
        if validated_data.get('password', None):
            instance.password = validated_data.get('password', instance.password)
        instance.tls_or_ssl = validated_data.get('tls_or_ssl', instance.tls_or_ssl)
        instance.save()
        return instance


class CloudEmailSerializers(serializers.Serializer):
    user = serializers.CharField(allow_null=True, allow_blank=True,
                                 error_messages={"invalid": "api接口错误"})
    password = serializers.CharField(allow_null=True, allow_blank=True,
                                     error_messages={"invalid": "api接口密码错误"})

    def create(self, validated_data):
        return None

    def update(self, instance, validated_data):
        instance.user = validated_data.get("user", instance.user)
        if validated_data.get("password", None):
            instance.password = validated_data.get("password", instance.password)
        instance.save()
        return instance


class FinanceSerializers(serializers.Serializer):
    bank = serializers.CharField(allow_null=True, allow_blank=True, max_length=32,
                                 error_messages={'max_length': "开户银行长度超出限制", "invalid": "银行名称错误"})
    username = serializers.CharField(allow_null=True, allow_blank=True, max_length=32,
                                     error_messages={'max_length': "账户名长度超出限制", "invalid": "账户名称"})
    bank_user = serializers.CharField(allow_null=True, allow_blank=True, max_length=64,
                                      error_messages={'max_length': "账号长度超出限制", "invalid": "银行账号名称"})
    email = serializers.CharField(allow_null=True, allow_blank=True, max_length=32,
                                  error_messages={'max_length': "邮箱长度超出限制", "invalid": "邮箱"})
    pay_pid = serializers.CharField(allow_null=True, allow_blank=True,
                                    error_messages={"null": "身份ID不能为空", "invalid": "身份ID错误"})
    pay_private_key = serializers.CharField(allow_null=True, allow_blank=True,
                                            error_messages={"null": "密钥不能为空", "invalid": "密钥错误"})
    pay_online = serializers.BooleanField(default=True)
    pay_outline = serializers.BooleanField(default=False)
    invoice = serializers.BooleanField(default=False)

    def validate_email(self, email):
        if self.instance:
            if email and not is_email(email):
                raise serializers.ValidationError("邮箱格式不匹配")
        return email

    def create(self, validated_data):
        return None

    def update(self, instance, validated_data):
        instance.bank = validated_data.get("bank", instance.bank)
        instance.username = validated_data.get("username", instance.username)
        instance.bank_user = validated_data.get("bank_user", instance.bank_user)
        instance.pay_outline = validated_data.get("pay_outline", instance.pay_outline)
        instance.pay_online = validated_data.get("pay_online", instance.pay_online)
        instance.invoice = validated_data.get("invoice", instance.invoice)
        instance.save()
        return instance


class SetAPISerializers(serializers.Serializer):
    qs_token = serializers.CharField(allow_null=True, allow_blank=True, max_length=128,
                                     error_messages={'max_length': "token长度超出限制", "invalid": "接口token错误"})
    qs_token_secret = serializers.CharField(allow_null=True, allow_blank=True, max_length=128,
                                            error_messages={'max_length': "token密码长度超出限制", "invalid": "token密码错误"})
    qs_api_timeout = serializers.IntegerField(allow_null=True, default=60, min_value=1, max_value=120,
                                              error_messages={"max_value": "最大值为120",
                                                              "min_value": "排序最小值为1", "invalid": "溢出时间输入错误"})

    def create(self, validated_data):
        return None

    def update(self, instance, validated_data):
        instance.qs_token = validated_data.get("qs_token", instance.qs_token)
        instance.qs_token_secret = validated_data.get("qs_token_secret", instance.qs_token_secret)
        instance.qs_api_timeout = validated_data.get("qs_api_timeout", instance.qs_api_timeout)
        instance.save()
        return instance


class BaseInfoSerializers(serializers.Serializer):
    title = serializers.CharField(allow_null=False, allow_blank=False, max_length=120,
                                  error_messages={"null": "系统名称不能为空", "blank": "系统名称不能为空", 'max_length': "系统名称长度超出限制",
                                                  "invalid": "系统名称错误"})
    web_domain = serializers.CharField(allow_null=False, allow_blank=False, max_length=256,
                                       error_messages={"null": "域名不能为空", "blank": "域名不能为空", 'max_length': "系统域名长度超出限制",
                                                       "invalid": "系统域名错误"})
    record_number = serializers.CharField(allow_null=False, allow_blank=False, max_length=128,
                                          error_messages={"null": "备案编号不能为空", "blank": "备案编号不能为空",
                                                          'max_length': "备案编号超出限制",
                                                          "invalid": "备案编号错误"})
    server_phone = serializers.CharField(allow_null=False, allow_blank=False, max_length=64,
                                         error_messages={"null": "服务电话不能为空", "blank": "服务电话不能为空",
                                                         'max_length': "服务电话超出限制",
                                                         "invalid": "服务电话错误"})
    email = serializers.CharField(allow_null=False, allow_blank=False, max_length=128,
                                  error_messages={"null": "邮箱不能为空", "blank": "邮箱不能为空", 'max_length': "邮箱长度超出限制",
                                                  "invalid": "邮箱错误"})

    def validate_title(self, data):
        if self.instance:
            obj = Agent.objects.filter(web_title=data).exclude(id=self.instance.id)
            if obj:
                raise serializers.ValidationError("系统名称和已有的重复")
        return data

    def validate_email(self, data):
        if not is_email(data):
            raise serializers.ValidationError("邮箱格式错误")
        return data

    def update(self, instance, validate_data):
        instance.web_title = validate_data.get("title", instance.title)
        instance.web_domain = validate_data.get("web_domain", instance.web_domain)
        instance.record_number = validate_data.get("record_number", instance.record_number)
        instance.server_phone = validate_data.get("server_phone", instance.server_phone)
        instance.email = validate_data.get("email", instance.email)
        instance.save()
        return instance


class SystemUpgradeSerializers(serializers.Serializer):
    """
    系统升级
    """

    u_type = serializers.CharField(max_length=15,
                                   error_messages={'invalid': '升级类型错误', 'blank': "升级类型不能为空",
                                                   "null": "升级类型不能为空", "required": "升级类型必需",
                                                   },
                                   )

    upgrade_type = serializers.CharField(max_length=15, required=False)

    file_id = serializers.IntegerField(required=True,
                                       error_messages={'invalid': '升级文件错误', 'blank': "升级文件不能为空",
                                                       "null": "升级文件不能为空", "required": "升级文件必需",
                                                       },
                                       )

    targets = serializers.ListField(
        error_messages={'invalid': '升级目标错误', 'blank': "升级目标不能为空",
                        "null": "升级目标不能为空", "required": "升级目标必需",
                        },
    )

    cannot_upgrade = ''
    targets_detail_list = []
    targets_list = []

    def validate_upgrade_type(self, data):
        if data not in ['system', 'event', 'engine']:
            raise serializers.ValidationError("升级类型错误")
        return data

    def validate_file_id(self, data):
        agent_now = self.context["request"].user.userinfo.agent
        upgrade_file = models.SystemUpgradeFile.objects.filter(agent=agent_now, id=data).first()
        if not upgrade_file:
            raise serializers.ValidationError("文件不存在，请重新上传")
        if not os.path.exists(upgrade_file.path):
            raise serializers.ValidationError("文件不存在, 请重新上传")
        return data

    def validate_targets(self, targets):
        # 包含 uudi 和 ID
        for target in targets:
            if 'uuid' not in target or 'id' not in target:
                raise serializers.ValidationError("目标参数错误")
        return targets

    def get_info(self, data):

        info = {
            "uuid": data.get('uuid'),
            "name": data.get("name"),
            "version": data.get("version"),
        }

        return info

    def filter_list_by_key(self, targets, key, value):
        """
        根据 key 和 value 过滤
        :param targets:
        :param key:
        :param value:
        :return:
        """
        return [target for target in targets if key in target and target[key] == value]

    def get_u_type_name(self, u_type):

        data = {
            "center": "中心",
            "nids": "网络主机",
            "vul": "漏洞库"
        }
        return data.get(u_type, ' ')

    def travel_tree(self, trees, u_type, parent=None):
        """
        递归遍历
        :param trees:
        :param u_type:
        :param parent:
        :return:
        """
        if not trees:
            return
        for node in trees:
            # 检查中心或者组件
            if node.get('u_type') == u_type:
                tree_uuid = node.get('uuid')
                device_id = node.get('id')
                if {"uuid": tree_uuid, 'id': device_id} in self.targets_list:
                    # 不可升级
                    if node.get("status", 0) != 1:
                        raise serializers.ValidationError(self.cannot_upgrade.format(node.get("name", '')))

                    info = self.get_info(node)
                    info.update({"parent_id": parent['id'] if parent else None, 'device_id': node['id']})
                    self.targets_detail_list.append(info)

            if node.get('u_type') == 'center':
                self.travel_tree(node.get('children', []), u_type, parent=node)

            if u_type == 'vul':
                # 上传漏洞库
                tree_uuid = node.get('uuid')
                device_id = node.get('id')
                if {"uuid": tree_uuid, 'id': device_id} in self.targets_list:
                    # 不可升级
                    if node.get("status", 0) != 1:
                        raise serializers.ValidationError(self.cannot_upgrade.format(node.get("name", '')))
                    vul_version = knowledge_model.VulStoreVersion.objects.first()
                    version = vul_version.version if vul_version else '--'
                    info = {
                        "uuid": node.get('uuid'),
                        "name": node.get("name"),
                        "version": version,
                    }
                    info.update({"parent_id": parent['id'] if parent else None, 'device_id': node['id']})
                    self.targets_detail_list.append(info)

    def validate(self, attrs):
        """
        检查是否可以升级
        :param attrs:
        :return:
        """
        # 获取当前代理商的所有中心状态
        agent_now = self.context["request"].user.userinfo.agent
        u_type = attrs['u_type']
        upgrade_file = models.SystemUpgradeFile.objects.filter(agent=agent_now, id=attrs['file_id']).first()
        if upgrade_file.u_type != u_type:
            raise serializers.ValidationError("升级类型和文件类型不匹配")

        file_info = {"version": upgrade_file.version, 'u_type': u_type}

        # 中心和可升级组件
        tree = get_node_detail(agent_now, file_info)

        # 检查是否所有的 target 都满足可以升级
        if not tree:
            raise serializers.ValidationError("中心错误")

        u_type_name = self.get_u_type_name(u_type)
        self.cannot_upgrade = "{0} {1} 不可升级或已经是最新版本".format(u_type_name, '{0}')
        self.targets_detail_list = []
        self.targets_list = attrs['targets']

        # 递归中心和组件
        trees = [tree]
        self.travel_tree(trees, u_type, parent=None)

        if not self.targets_detail_list:
            raise serializers.ValidationError("没有获取到可升级的{0}".format(u_type_name))

        # todo 处理多余目标
        # if targets:
        #     raise serializers.ValidationError("存在不可识别的{0}".format(u_type_name))

        attrs['targets_detail_list'] = self.targets_detail_list

        return attrs

    def create(self, validated_data):
        """
        :param validated_data:
        :return:
        """
        # 创建升级任务
        targets = validated_data.get("targets_detail_list")
        u_type = validated_data.get('u_type')
        file_id = validated_data.get("file_id")
        agent_now = self.context["agent"]
        upgrade_file = models.SystemUpgradeFile.objects.filter(agent=agent_now, id=file_id).first()
        # TODO 处理正在升级
        with transaction.atomic():
            for target in targets:
                data = {
                    "agent": agent_now,
                    "u_type": u_type,
                    "target_id": target["device_id"],
                    "target_name": target["name"],
                    "target_uuid": target["uuid"],
                    "target_version": target['version'],
                    "target_parent_id": target["parent_id"],
                    "file_uuid": upgrade_file.id,
                    "file_version": upgrade_file.version,
                }
                new_task = models.SystemUpgradeTask.objects.create(**data)
                target.update({"task_id": new_task.id})

        """
        返回可更新的任务
        {
            "file_name": "55aed099-47b4-4e50-ae63-8232dfaff492",
            "file_version": 'v2.25.2',
            "u_type": "center",
            "targets": [
                {
                    "parent_id": 2,
                    "task_id": 1,
                    "uuid": "soc-uuid-1",
                    "device_id": 1,
                }
            ]
        }
        """
        upgrade_detail = {
            "file_name": upgrade_file.name,
            "file_version": upgrade_file.version,
            "u_type": upgrade_file.u_type,
            "targets": targets
        }

        return upgrade_detail

    def update(self, instance, validated_data):
        return None


class UpgradeNodeSerializers(serializers.Serializer):

    u_type = serializers.CharField(max_length=15)

    file_id = serializers.IntegerField()

    def validate_u_type(self, data):
        if data not in ["center", "monitor", "scan", "defense", "cloud_defense", "hids", "nids", "vul"]:
            raise serializers.ValidationError("升级文件类型错误")
        return data

    def validate_file_id(self, data):
        # todo verify file
        agent_now = self.context.get("request").user.userinfo.agent
        upgrade_file = models.SystemUpgradeFile.objects.filter(agent=agent_now, id=data).first()
        if not upgrade_file:
            raise serializers.ValidationError("上传文件不存在")
        return data

    def validate(self, attrs):
        agent_now = self.context.get("request").user.userinfo.agent
        attrs["file"] = models.SystemUpgradeFile.objects.filter(agent=agent_now, id=attrs["file_id"]).first()
        if attrs["file"].u_type != attrs['u_type']:
            raise serializers.ValidationError("升级类型错误")
        return attrs

    def create(self, validated_data):
        return None

    def update(self, instance, validated_data):
        return None


class SystemUpgradeRetrySerializers(serializers.Serializer):
    """
    升级重试
    """

    task_id = serializers.CharField(allow_null=False,
                                    error_messages={'invalid': '任务ID错误', 'blank': "任务ID不能为空",
                                                    "null": "任务ID不能为空", "required": "任务ID必需",
                                                    },
                                    )

    def validate_task_id(self, data):
        request = self.context.get("request")
        agent_now = request.user.userinfo.agent
        upgrade_task = models.SystemUpgradeTask.objects.filter(agent=agent_now, id=data).first()
        if not upgrade_task:
            raise serializers.ValidationError("任务不存在")
        if upgrade_task.status != 2:
            # 非错误任务不能重试
            raise serializers.ValidationError("任务不能重试")
        return data

    def create(self, validated_data):
        return None

    def update(self, instance, validated_data):
        return None


class VisitSerializers(serializers.Serializer):
    fail_range_time = serializers.IntegerField(min_value=1, allow_null=False,
                                               error_messages={"min_value": "时间或次数最小值为1", "invalid": "限制时间错误"})
    register_time = serializers.IntegerField(min_value=1, allow_null=False,
                                             error_messages={"min_value": "时间或次数最小值为1", "invalid": "限制时间错误"})
    fail_ban_time = serializers.IntegerField(min_value=1, allow_null=False,
                                             error_messages={"min_value": "时间或次数最小值为1", "invalid": "限制时间错误"})
    register_count = serializers.IntegerField(min_value=1, allow_null=False,
                                              error_messages={"min_value": "时间或次数最小值为1", "invalid": "限制次数错误"})
    fail_count = serializers.IntegerField(min_value=1, allow_null=False,
                                          error_messages={"min_value": "时间或次数最小值为1", "invalid": "限制次数错误"})
    user_fail_count = serializers.IntegerField(min_value=1, allow_null=False,
                                               error_messages={"min_value": "时间或次数最小值为1", "invalid": "限制次数错误"})
    user_fail_range_time = serializers.IntegerField(min_value=1, allow_null=False,
                                                    error_messages={"min_value": "时间或次数最小值为1", "invalid": "限制时间错误"})
    user_fail_ban_time = serializers.IntegerField(min_value=1, allow_null=False,
                                                  error_messages={"min_value": "时间或次数最小值为1", "invalid": "限制时间错误"})
    login_timeout = serializers.IntegerField(min_value=1, max_value=1440, allow_null=False,
                                             error_messages={"min_value": "会话结束时间最小为1分钟", "invalid": "会话结束时间错误",
                                                             "max_value": "会话结束时间最大为1440分钟(24小时)",
                                                             "null": "会话结束时间不能为空"})

    username = serializers.BooleanField()
    email = serializers.BooleanField()
    phone = serializers.BooleanField()
    wechat = serializers.BooleanField()

    is_find_password = serializers.BooleanField()

    register_allow = serializers.BooleanField()
    login_allow = serializers.BooleanField()

    def update(self, instance, validate_data):
        """update
        """
        instance.fail_range_time = validate_data.get('fail_range_time') * 60
        instance.register_time = validate_data.get('register_time') * 60
        instance.fail_ban_time = validate_data.get('fail_ban_time') * 60
        instance.register_count = validate_data.get('register_count')
        instance.fail_count = validate_data.get('fail_count')
        instance.login_allow = validate_data.get('login_allow')
        instance.register_allow = validate_data.get('register_allow')
        instance.is_find_password = validate_data.get('is_find_password')
        instance.login_timeout = validate_data.get('login_timeout') * 60
        login_types = []
        if validate_data.get("username") is True:
            login_types.append("username")
        if validate_data.get("email") is True:
            login_types.append("email")
        if validate_data.get("phone") is True:
            login_types.append("phone")
        if validate_data.get("wechat") is True:
            login_types.append("wechat")
        login_type = ','.join(login_types)
        instance.login_type = login_type
        instance.save()

        # user
        fail_count = validate_data.get("user_fail_count")
        fail_range_time = validate_data.get("user_fail_range_time") * 60
        fail_ban_time = validate_data.get("user_fail_ban_time") * 60
        user_models.UserInfo.objects.filter(agent=instance).update(
            fail_count=fail_count, fail_range_time=fail_range_time, fail_ban_time=fail_ban_time)

        return instance
