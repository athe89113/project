# coding: utf-8
import uuid
import json
from django.utils import timezone
from django.db import models
from soc.models import Agent
from django.forms.models import model_to_dict


class DefaultMenu(models.Model):
    """
    系统默认菜单
    """
    # 索引，以此来确定所有菜单的顺序, 不依靠 ID
    index = models.PositiveIntegerField()
    # 默认排序
    sort = models.PositiveSmallIntegerField(default=50)
    # TODO 层级表示，三级，每级两位
    level = models.CharField(max_length=6)
    # 名称， 最大为六个中文字符
    name = models.CharField(max_length=32)
    # 前端话题
    topic = models.CharField(max_length=32)
    # 是否着陆页，1是0否
    is_landing = models.PositiveSmallIntegerField(default=0)
    # 是否启用
    enable = models.PositiveSmallIntegerField(default=1)
    # 父级菜单
    parent = models.ForeignKey("self", null=True)
    # 公司用户是否显示 为0不显示 1 显示
    company_show = models.IntegerField(default=1)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'default_menu'
        verbose_name = "默认菜单"

    # def get_dict(self):
    #     data = {
    #         "id": self.id,
    #         "name": self.name,
    #         "sort": self.sort,
    #         "is_landing": self.is_landing,
    #         "enable": self.enable,
    #         "index": self.index,
    #         "topic": self.topic
    #     }
    #     return data


class AdvancedMenu(models.Model):
    """
    代理商自定义菜单
    """

    agent = models.ForeignKey(Agent)
    default_menu = models.ForeignKey(DefaultMenu, null=True)
    # 默认菜单或者自定义菜单 default-默认, custom-自定义
    type = models.CharField(max_length=10, default='default')
    # 名称
    name = models.CharField(max_length=24)
    # 排序
    sort = models.PositiveSmallIntegerField(default=50)
    # 是否着陆页，1是0否
    is_landing = models.PositiveSmallIntegerField(default=0)
    # 是否启用
    enable = models.PositiveSmallIntegerField(default=1)

    def get_dict(self):
        data = {
            "id": self.id,
            "index": self.default_menu.index if self.default_menu else 50,
            "name": self.name,
            "sort": self.sort,
            "is_landing": self.is_landing,
            "enable": self.enable,
            "topic": self.default_menu.topic if self.default_menu else ""
        }
        return data

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'advanced_menu'
        verbose_name = "自定义菜单"


class Node(models.Model):
    """
    级联节点
    """

    # 所属代理商
    agent = models.ForeignKey(Agent)
    # 名称, 默认以IP为名称
    name = models.CharField(max_length=128, null=False)
    # 全局唯一标识
    uuid = models.CharField(max_length=200, default=uuid.uuid4, null=True, blank=True)
    # 中心地址，并不一定是 IP
    ip = models.CharField(max_length=200, null=False, default='127.0.0.1')
    port = models.IntegerField(default=80)
    # 中心角色 self - 当前, parent - 上级, child - 下级
    role = models.CharField(max_length=10, null=False)
    # 类型， center - 总中心, sub_center - 分中心, child_center - 子中心
    type = models.CharField(max_length=15, null=False)
    # 认证 key
    auth_key = models.TextField(null=True)
    # 链接状态, 0-未连接/连接中，1-已连接, 2-连接错误
    status = models.PositiveSmallIntegerField(default=0)
    # 请求接口地址及认证
    api_url = models.CharField(max_length=256, null=True, blank=True)
    secret_id = models.CharField(max_length=64, null=True)
    secret_key = models.CharField(max_length=128, null=True)
    # 允许上级级联
    accept_parent_connection = models.PositiveSmallIntegerField(default=0)
    # 接收下级控制中心设置 {"next_message":0,"next_source":0,"next_monitor":0,"next_loophole":0,"next_attack":0}
    accept_next_settings = models.TextField(default='{}')
    """
    接收下级控制中心上报的事件通知  next_message
    接收下级控制中心上报的资源数据  next_source
    接收下级控制中心上报的监控数据  next_monitor
    接收下级控制中心上报的漏洞信息  next_loophole
    接收下级控制中心上报的攻击信息  next_attack
    """
    # 接收上级控制中心下发的事件通知
    accept_apply_message = models.PositiveSmallIntegerField(default=0)
    # 接收并应用上级控制中心下发的漏洞库升级包
    accept_apply_loophole = models.PositiveSmallIntegerField(default=0)
    # 接收并应用上级控制中心下发的策略
    accept_apply_policy = models.PositiveSmallIntegerField(default=0)
    # 接收并应用上级控制中心下发的事件库升级包
    accept_apply_event_db = models.PositiveSmallIntegerField(default=0)
    # 接收并应用上级控制中心下发的引擎升级包
    accept_apply_engine = models.PositiveSmallIntegerField(default=0)
    # 接收并应用上级控制中心下发的控制中心升级包
    accept_apply_center = models.PositiveSmallIntegerField(default=0)

    # 当下级失联时告警，针对 self 设置，默认开启
    notify_when_lose_children = models.PositiveSmallIntegerField(default=1)

    # 最后心跳
    last_heartbeat = models.DateTimeField(auto_now_add=True, null=True)
    # 下次检测时间，用来收敛检测
    next_check = models.DateTimeField(auto_now_add=True, null=True)
    # 版本
    version = models.CharField(max_length=10, null=True, default='')
    # 备注说明
    info = models.CharField(max_length=256, null=True, blank=True, default='')

    class Meta:
        db_table = "system_node"
        verbose_name = "级联节点"

    def __unicode__(self):
        return self.name

    def get_dict(self):
        """
        获取对象信息
        :return:
        """
        data = {
            'id': self.id,
            # 本机中心去代理商的web_domain
            'ip': self.agent.web_domain if self.role == 'self' and self.agent.web_domain else self.ip,
            'port': self.port,
            # 本机中心根据代理商的 title 显示
            # 'name': self.agent.title if self.role == 'self' and self.agent.title else self.name,
            'name': self.name,
            "role": self.role,
            "type": self.type,
            "status": 1 if self.role == 'self' else self.status,
            "last_heartbeat": timezone.localtime(self.last_heartbeat).strftime('%Y-%m-%d %H:%M:%S') if self.last_heartbeat else "",
            "version": self.version,
            "uuid": self.uuid,
            "api_url": self.api_url or '',
            "auth_key": self.auth_key,
            "info": self.info,
            "children": []
        }
        if self.role == 'self':
            accept_next_settings = json.loads(self.accept_next_settings)
            if not accept_next_settings:
                accept_next_settings = {
                    "next_message": 0,
                    "next_source": 0,
                    "next_monitor": 0,
                    "next_loophole": 0,
                    "next_attack": 0
                }
            configs = {
                "accept_parent_connection": self.accept_parent_connection,
                "accept_apply_policy": self.accept_apply_policy,
                "accept_apply_event_db": self.accept_apply_event_db,
                "accept_apply_engine": self.accept_apply_engine,
                "accept_apply_center": self.accept_apply_center,
                "notify_when_lose_children": self.notify_when_lose_children,
                "accept_apply_message": self.accept_apply_message,
                "accept_apply_loophole": self.accept_apply_loophole
            }
            configs.update(accept_next_settings)
            data.update(configs)
        return data


class Message(models.Model):
    """
    代理商消息的设置，包括邮件、短信等
    """
    TYPE = (
        (1, "SMTP邮件"),
        (2, "短信"),
        (4, "cloud邮件"),
    )
    agent = models.ForeignKey(Agent)
    # 消息类型
    type = models.IntegerField(choices=TYPE)
    # smtp邮件服务器
    smtp_server = models.CharField(max_length=128, null=False, blank=True)
    # smtp发信地址
    send_sender = models.CharField(max_length=64, null=False, blank=True)
    # 用户名
    user = models.CharField(max_length=64, null=False, blank=True)
    # 密码
    password = models.CharField(max_length=64, null=False, blank=True)
    # tls or ssl False为tls  True为ssl
    tls_or_ssl = models.BooleanField(default=False)
    # API 接口地址
    api = models.CharField(max_length=256, null=False, blank=True)

    class Meta:
        db_table = "system_message"
        verbose_name = "消息中心设置"

    @classmethod
    def get_cloud_info(cls, agent_id):
        """
        获取cloud 发邮件的需要数据
        :return: 
        """
        try:
            obj = cls.objects.get(type=4, agent_id=agent_id)
            return model_to_dict(obj, fields=['api', 'user', 'password'])
        except:
            return dict()

    @classmethod
    def get_smtp_info(cls, agent_id):
        """
        获取smtp服务信息
        :param msg: 
        :return: 
        """
        try:
            obj = cls.objects.get(type=1, agent_id=agent_id)
            return model_to_dict(obj)
        except:
            return dict()

    @classmethod
    def get_msg_info(cls, agent_id):
        """
        获取发短信信息
        :param agent_id: 
        :return: 
        """
        try:
            obj = cls.objects.get(type=2, agent_id=agent_id)
            return model_to_dict(obj, fields=['api', 'user', 'password'])
        except:
            return dict()


class SetPay(models.Model):
    """
    代理商关于财务的设置
    """
    agent = models.ForeignKey(Agent)
    # 开户银行
    bank = models.CharField(max_length=32, null=False, blank=True)
    # 账户名称
    username = models.CharField(max_length=32, null=False, blank=True)
    # 银行账号
    bank_user = models.CharField(max_length=64, null=False, blank=True)
    # 合作伙伴邮箱
    email = models.CharField(max_length=32, null=False, blank=True)

    # 是否启用支付宝进行在线支付
    pay_online = models.BooleanField(default=True)
    # 是否启用支付宝进行离线支付
    pay_outline = models.BooleanField(default=True)
    # 是否开启发票
    invoice = models.BooleanField(default=True)

    class Meta:
        db_table = "system_setpay"
        verbose_name = "财务设置"


class SystemUpgradeTask(models.Model):
    """
    升级管理
    """
    # 代理商
    agent = models.ForeignKey(Agent)

    # 升级类型
    u_type = models.CharField(max_length=15)
    # 目标 ID
    target_id = models.IntegerField(null=True)
    # 目标名称
    target_name = models.CharField(max_length=256)
    # 目标uuid
    target_uuid = models.CharField(max_length=256)
    # 目标版本
    target_version = models.CharField(max_length=15)
    # 升级对象的父节点
    target_parent_id = models.IntegerField(null=True)

    # 文件
    file_uuid = models.CharField(max_length=256)
    # 升级版本
    file_version = models.CharField(max_length=15)

    # 任务状态，
    status = models.PositiveSmallIntegerField(default=0)
    # 完成百分比
    percent = models.PositiveSmallIntegerField(default=0)

    def __unicode__(self):
        return self.target_name

    class Meta:
        db_table = 'system_upgrade_task'
        verbose_name = "升级任务"


class SystemUpgradeFile(models.Model):
    """
    升级文件管理
    """

    # 代理商
    agent = models.ForeignKey(Agent)
    # 文件名称
    name = models.CharField(max_length=256)
    # 文件类型
    u_type = models.CharField(max_length=15)
    # 升级类型, 系统，事件，引擎
    upgrade_type = models.CharField(max_length=15)
    # 文件版本
    version = models.CharField(max_length=15)
    # 文件存储路径
    path = models.FilePathField(null=True)
    # 构建日期
    build_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'system_upgrade_file'
        verbose_name = "升级文件"


class BlackIPList(models.Model):
    """IP黑白名单"""
    FLAG = ((1, '黑名单'), (2, '白名单'))
    agent = models.ForeignKey(Agent)
    # 黑名单or白名单
    is_black = models.IntegerField(choices=FLAG, default=1)
    # 黑名单开始时间
    start_time = models.DateTimeField(null=True, blank=True)
    # ip
    ip = models.CharField(max_length=64)
    # 类型 手动添加还是自动添加 0是自动添加 1是手动添加 自动添加黑名单要计算结束时间
    type = models.IntegerField(default=0)

    class Meta:
        db_table = 'black_ip_list'

