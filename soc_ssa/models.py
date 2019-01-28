# coding: utf-8
import os
import json
import logging
import django.utils.timezone as timezone
import uuid
from django.db import models
from django.forms.models import model_to_dict
from celery.task.control import revoke
from soc_user.models import UserInfo
from soc.models import Agent, Company, User

logger = logging.getLogger("soc_ssa")

DEFAULT_MAX_ALARM_COUNT = 3
DEFAULT_TOGGLE_CONDITION = 1

# 预警类型
ALARM_CONF_TYPES = {
    1: "漏洞预警配置",
    2: "攻击预警配置",
    3: "业务预警配置",
    4: "安全预警配置",
}

# 处理类型
WORK_TYPE = {
    1: "批处理",
    2: "流处理",
}
THE_TIME_ZONE = ["-12:00", "-11:00", "-10:00", "-09:00", "-08:00", "-07:00", "-06:00", "-05:00", "-04:00", "-03:00",
                 "-02:00", "-01:00", "00:00",
                 "+01:00", "+02:00", "+03:00", "+04:00", "+05:00", "+06:00", "+07:00", "+08:00", "+09:00", "+10:00",
                 "+11:00", "+12:00"]


class SSADataTag(models.Model):
    """
    数据标签
    """
    # 名称
    name = models.CharField(max_length=256)
    # 存储路径或ES index
    path = models.CharField(max_length=256)
    # 时间格式 默认 年-月-日-时
    time_format = models.CharField(max_length=256, default="yyyy-MM-dd-HH")

    # 对应用户 为空时为系统自带TAG
    agent = models.ForeignKey(Agent, null=True, blank=True)
    company = models.ForeignKey(Company, null=True, blank=True)

    class Meta:
        db_table = "ssa_data_tag"
        verbose_name = '数据标签'


class SECDataTag(models.Model):
    """
    事件数据标签
    """
    # 名称
    name = models.CharField(max_length=256)
    # 存储路径或ES index
    path = models.CharField(max_length=256)
    # 时间格式 默认 年-月-日-时
    time_format = models.CharField(max_length=256, default="yyyy-MM-dd-HH")

    # 对应用户 为空时为系统自带TAG
    agent = models.ForeignKey(Agent, null=True, blank=True)
    company = models.ForeignKey(Company, null=True, blank=True)
    # 同表不同字段区分
    diff_field = models.CharField(max_length=256, null=True, blank=True)
    diff_value = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        db_table = "sec_data_tag"
        verbose_name = '数据标签'


class SelfServiceConf(models.Model):
    """
    自带大数据服务配置 包括HDFS ES Kafka hive 连接配置
    """
    # 服务名称 hdfs es kafka hive
    service = models.CharField(max_length=256)
    # 地址
    host = models.CharField(max_length=256)
    # username 
    username = models.CharField(max_length=256, null=True, blank=True)
    # password
    password = models.CharField(max_length=256, null=True, blank=True)
    # 对应用户
    agent = models.ForeignKey(Agent, null=True, blank=True)
    company = models.ForeignKey(Company, null=True, blank=True)

    @classmethod
    def get_service(cls, service, agent=None, company=None):
        """
        获取服务配置
        """
        server = cls.objects.filter(service=service, agent=agent, company=company).first()
        if not server:
            server = cls.objects.filter(service=service, agent=None, company=None).first()
        return server

    class Meta:
        db_table = "ssa_self_service_conf"
        verbose_name = '大数据服务配置'


class SSAScoreSystem(models.Model):
    """态势感知评分系统"""
    agent = models.ForeignKey(Agent)
    # 态势感知综合评分
    # 态势感知综合评分＝15*漏洞资产指数＋25*漏洞严重指数＋20*攻击指数＋20*僵木蠕指数＋10*业务流康指数＋10*业务访问指数
    security_mark = models.IntegerField(default=0)
    # 漏洞资产占比
    hole_assets = models.IntegerField(default=0)
    # 漏洞严重指数
    hole_serious = models.IntegerField(default=0)
    # 攻击指数
    attack = models.IntegerField(default=0)
    # 僵木蠕感染指数
    trojan = models.IntegerField(default=0)
    # 业务流康指数
    business_health = models.IntegerField(default=0)
    # 业务访问指数
    business_visit = models.IntegerField(default=0)
    # 时间
    score_date = models.DateField(null=False)

    class Meta:
        db_table = "ssa_score_system"
        verbose_name = '态势感知评分系统'


class SSARuleManage(models.Model):
    """
    专家分析系统-保存SQL
    """
    # 名称
    name = models.CharField(max_length=256)
    # 类型 1 文件夹 2 文件
    type = models.IntegerField(default=1)
    # sql 存储sql语句
    sql = models.CharField(max_length=1024)
    # 父目录
    parent = models.ForeignKey('self', related_name='parent_folder', verbose_name=u'父目录', null=True)
    # 对应用户
    agent = models.ForeignKey(Agent, null=True, blank=True)
    company = models.ForeignKey(Company, null=True, blank=True)

    @classmethod
    def tree(cls, agent, company):
        """生成目录树
        """
        data = []
        all_rule = list(cls.objects.filter(agent=agent, company=company) \
                        .values("id", "name", "type", "sql", "parent_id"))
        return cls._tree(all_rule, data)

    @classmethod
    def _tree(cls, per_list, per_tree=None, parent_list=None, max_level=5, level=0):
        """
        递归 构建目录树
        :param per_list: 原始列表
        :param per_tree: 目录树
        :param parent_list: 当前递归所需的父级权限列表
        :param max_level: 最大递归层数
        :param level: 当前递归层数
        :return:
        """
        if not per_list:
            per_list = []
        if not parent_list:
            parent_list = []

        level += 1
        if level > max_level:
            return per_tree
        need_remove = []
        if not per_list:
            return per_tree
        if not per_tree:
            for _, per in enumerate(per_list):
                if per.get('parent_id') is None:
                    per['level'] = level
                    per['data'] = []
                    per['show'] = 0
                    per['edit'] = 0
                    per_tree.append(per)
                    need_remove.append(per)
                    parent_list.append(per)
            for i in need_remove:
                per_list.remove(i)

        else:
            new_parent_list = []
            for parent in parent_list:
                need_remove = []
                for role in filter(lambda x: x.get("parent_id") == parent.get("id"), per_list):
                    role['level'] = level
                    role['data'] = []
                    role['show'] = 0
                    role['edit'] = 0
                    parent.get("data").append(role)
                    need_remove.append(role)
                    new_parent_list.append(role)
                for i in need_remove:
                    per_list.remove(i)
            parent_list = new_parent_list

        return cls._tree(per_list, per_tree, parent_list=parent_list, max_level=max_level, level=level)

    class Meta:
        db_table = "ssa_rule_manage"
        verbose_name = '专家分析系统'


class SSAReportTemplate(models.Model):
    """
    报表模板
    """
    name = models.CharField(max_length=256)
    # 1 immediately,2 runonce, 3 daily, 4 weekly,5 monthly, 6 quarterly， 7 yearly
    schedule_type = models.PositiveSmallIntegerField()
    # 开始时间
    schedule_start_date = models.DateField(null=True)
    # 每X天 / 星期X / 第X天
    schedule_days = models.PositiveSmallIntegerField()
    # 第X月
    schedule_months = models.PositiveSmallIntegerField(default=1)
    # 某天的具体执行时间
    schedule_time = models.TimeField(null=True)
    # 下次扫描时间
    next_scan_time = models.DateTimeField(null=True)
    # 模版内容
    content = models.TextField(null=True)
    # 模版类型 1 定制模版 2 固定模版
    template_type = models.IntegerField(default=1)

    # 对应用户
    agent = models.ForeignKey(Agent, null=True, blank=True)
    company = models.ForeignKey(Company, null=True, blank=True)

    class Meta:
        db_table = "ssa_report_template"
        verbose_name = '报表模板'


class SSAReportCell(models.Model):
    """
    报表元素
    """
    # 名称
    name = models.CharField(max_length=256)
    # 数据
    data_key = models.CharField(max_length=256)
    # 数据类型 1 资产信息分析 2 攻击数据分析 3 僵木蠕数据分析 4 漏洞数据分析 5 报警数据分析 6 业务数据分析
    data_type = models.IntegerField(default=1)
    # 默认图表类型
    default_chart = models.CharField(max_length=256, default="pie")
    # 描述    
    description = models.CharField(max_length=256)

    class Meta:
        db_table = "ssa_report_cell"
        verbose_name = '报表模板元素'


class SSAReportTemplateCell(models.Model):
    """
    报表模板元素
    """
    # 对应元素
    cell = models.ForeignKey(SSAReportCell, null=True, blank=True)
    # 周期 单位 天
    cycle = models.IntegerField()
    # 是否有表格
    has_table = models.IntegerField(default=0)
    # 图表类型 柱形，条形，折线，表格
    chart_type = models.CharField(max_length=256)
    # 描述
    description = models.CharField(max_length=256)
    # 备注
    remark = models.CharField(max_length=256)
    # 对应模板
    template = models.ForeignKey(SSAReportTemplate, null=True)
    # 排序字段
    order = models.IntegerField()
    # 对应用户
    agent = models.ForeignKey(Agent, null=True, blank=True)
    company = models.ForeignKey(Company, null=True, blank=True)

    class Meta:
        db_table = "ssa_report_template_cell"
        verbose_name = '报表模板元素'


class SSAReportResult(models.Model):
    """
    报表
    """
    # 名称
    name = models.CharField(max_length=256)
    # 对应模板
    template = models.ForeignKey(SSAReportTemplate, null=True)
    # 生成时间
    create_time = models.DateTimeField(auto_now_add=True)
    # word存储路径
    docx_path = models.CharField(max_length=256, null=True)
    # word文件大小
    docx_size = models.IntegerField(default=0)
    # pdf存储路径
    pdf_path = models.CharField(max_length=256, null=True)
    # pdf文件大小
    pdf_size = models.IntegerField(default=0)
    # 对应用户
    agent = models.ForeignKey(Agent, null=True, blank=True)
    company = models.ForeignKey(Company, null=True, blank=True)
    # 模版类型 1 定制模版 2 固定模版
    template_type = models.IntegerField(default=1)
    class Meta:
        db_table = "ssa_report_result"
        verbose_name = '报表'


class SSAAlarmConf(models.Model):
    """
    态势感知-预警/告警配置
    """
    # 最大告警次数
    max_alarm_count = models.IntegerField(default=DEFAULT_MAX_ALARM_COUNT)
    # 判断条件 1 满足其中任意一项 2 满足所有条件
    toggle_condition = models.IntegerField(default=DEFAULT_TOGGLE_CONDITION)
    # 配置类型 1 漏洞 2 攻击 3 业务 4 安全
    conf_type = models.IntegerField()
    # 对应用户
    agent = models.ForeignKey(Agent)
    company = models.ForeignKey(Company, null=True, blank=True)

    class Meta:
        db_table = "ssa_alarm_conf"
        verbose_name = '态势感知-预警/告警配置'


class SSAAlarmCell(models.Model):
    """
    态势感知-预警/告警项
    """
    # 名称
    name = models.CharField(max_length=125)
    key = models.CharField(max_length=256)

    # 配置类型 1 漏洞 2 攻击 3 业务 4 安全
    conf_type = models.IntegerField()
    # 默认预警阈值
    warning = models.IntegerField()
    # 默认告警阈值
    alarm = models.IntegerField()
    # 单位 % Mbps 等
    unit = models.CharField(max_length=125, null=True, blank=True)
    # 表达式 <= >=
    expression = models.CharField(max_length=125, default=">=")
    # 发送消息内容模板
    message = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        db_table = "ssa_alarm_cell"
        verbose_name = '态势感知-预警/告警项'


class SSAAlarmConfCell(models.Model):
    """
    态势感知-预警/告警项配置
    """
    # 对应项目
    cell = models.ForeignKey(SSAAlarmCell)
    # 是否启用 0 禁用 1 启用
    enable = models.IntegerField(default=0)
    # 预警阈值
    warning = models.IntegerField()
    # 告警阈值
    alarm = models.IntegerField()
    # 对应用户
    agent = models.ForeignKey(Agent)
    company = models.ForeignKey(Company, null=True, blank=True)

    class Meta:
        db_table = "ssa_alarm_conf_cell"
        verbose_name = '态势感知-预警/告警项配置'


class SSAAlarmNotifyConf(models.Model):
    """
    态势感知-预警/告警 通知配置
    """
    # 接收告警的人
    user = models.ForeignKey(User)
    # 配置类型 1 漏洞 2 攻击 3 业务 4 安全
    conf_type = models.IntegerField()
    # 邮件 0 关闭 1 开启
    email = models.IntegerField(default=0)
    # 短信 0 关闭 1 开启
    sms = models.IntegerField(default=0)
    # 对应用户
    agent = models.ForeignKey(Agent)
    company = models.ForeignKey(Company, null=True, blank=True)

    class Meta:
        db_table = "ssa_alarm_notify_conf"
        verbose_name = '态势感知-预警/告警项配置'


class SSAChart(models.Model):
    """
    态势感知-自定义图表(用于dashboard和报告)
    """
    # 名称
    name = models.CharField(max_length=256)
    # 类型 1:资源 2:业务 3:安全
    type = models.CharField(max_length=256)
    # 图表类型
    chart_type = models.CharField(max_length=256)
    # 地图类型 全国/北京/上海
    map_type = models.CharField(max_length=256, null=True, blank=True)
    # 时间周期
    query_time = models.IntegerField(default=1)
    # 样式
    styles = models.TextField(null=True)
    # x轴 查询条件
    x = models.TextField(null=True)
    # y轴 查询条件
    y = models.TextField(null=True)
    # 结果条数 0 不限制
    limit = models.IntegerField(default=0)
    # 执行结果缓存
    cache = models.TextField(null=True)
    # 描述
    description = models.CharField(max_length=256)
    # 备注
    remark = models.CharField(max_length=256)
    # 对应用户
    agent = models.ForeignKey(Agent, null=True, blank=True)
    company = models.ForeignKey(Company, null=True, blank=True)
    # 数据类型 1=日志 2=事件
    data_type = models.IntegerField(default=0)
    # 数据标签（数据来源）
    data_tag = models.IntegerField(default=0)

    class Meta:
        db_table = "ssa_chart"
        verbose_name = "态势感知-图表"


class SSADashBorad(models.Model):
    """
    态势感知-DashBorad
    """
    # 名称
    name = models.CharField(max_length=256)
    # 类型 1:资源 2:业务 3:安全
    type = models.CharField(max_length=256)
    # 时间周期
    query_time = models.IntegerField(default=1)
    # 对应用户
    agent = models.ForeignKey(Agent, null=True, blank=True)
    company = models.ForeignKey(Company, null=True, blank=True)

    class Meta:
        db_table = "ssa_dashboard"
        verbose_name = "态势感知-DashBorad"


class SSADashBoradCell(models.Model):
    """
    态势感知-DashBorad元素
    """
    # 图表
    chart = models.ForeignKey(SSAChart)
    # 报表
    dashboard = models.ForeignKey(SSADashBorad)
    # 排序
    order = models.IntegerField(default=0)
    # 对应用户
    agent = models.ForeignKey(Agent, null=True, blank=True)
    company = models.ForeignKey(Company, null=True, blank=True)

    class Meta:
        db_table = "ssa_dashboard_cell"
        verbose_name = "态势感知-DashBorad元素"


class SSAFieldMap(models.Model):
    """
    字段中英对照表
    """
    key = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    # 优先级 9最高 0最低 默认最低
    precedence = models.IntegerField(default=0)
    # 值列表 例如 [{"id":0, "name": "紧急"}]
    items = models.TextField(default="[]")
    # 数据标签 默认应用到所有数据标签
    data_tag = models.ForeignKey(SSADataTag, null=True, blank=True)

    @classmethod
    def get_field_map(cls, data_tag_id=None):
        if data_tag_id:
            qs = cls.objects.filter(data_tag_id=data_tag_id)
        else:
            qs = cls.objects.all()
        all_dict = {}
        for i in qs.values("key", "name", "precedence", "items"):
            items = i['items']
            if items:
                items = json.loads(i['items'])
            else:
                items = []
            all_dict[i['key']] = {
                "name": i['name'],
                "precedence": i['precedence'],
                "items": items
            }
        return all_dict

    class Meta:
        db_table = "ssa_field_map"


class SECFieldMap(models.Model):
    """
    字段中英对照表
    """
    key = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    # 优先级 9最高 0最低 默认最低
    precedence = models.IntegerField(default=0)
    # 值列表 例如 [{"id":0, "name": "紧急"}]
    items = models.TextField(default="[]")
    # 数据标签 默认应用到所有数据标签
    data_tag = models.ForeignKey(SECDataTag, null=True, blank=True)
    # 字段优先级 （查询详情时使用）
    field_priority = models.CharField(max_length=256, null=True, blank=True)

    @classmethod
    def get_field_map(cls, data_tag_id=None):
        if data_tag_id:
            qs = cls.objects.filter(data_tag_id=data_tag_id)
        else:
            qs = cls.objects.all()
        all_dict = {}
        for i in qs.values("key", "name", "precedence", "items", "field_priority"):
            items = i['items']
            if items:
                items = json.loads(i['items'])
            else:
                items = []
            all_dict[i['key']] = {
                "name": i['name'],
                "field_priority": i['field_priority'],
                "precedence": i['precedence'],
                "items": items
            }
        return all_dict

    class Meta:
        db_table = "sec_field_map"


class SecEventType(models.Model):
    """
    事件类型对照表
    """
    # 编号
    tag = models.IntegerField(auto_created=True, primary_key=True)
    # 事件类型
    type_name = models.CharField(max_length=100)
    # 类型对应字段
    type_field = models.CharField(max_length=100, null=True, blank=True)
    # 类型匹配符
    type_items = models.TextField(default="[]")
    # 父级编号
    last_tag = models.IntegerField(default=0)
    # 关联事件数据标签
    type_tag = models.ForeignKey(SECDataTag, null=True, blank=True)
    # 事件描述
    type_desc = models.CharField(max_length=100, null=True, blank=True)

    @classmethod
    def get_field_map(cls, type_tag=None):
        if type_tag:
            qs = cls.objects.filter(type_tag=type_tag)
        else:
            qs = cls.objects.all()
        all_dict = {}
        for i in qs.values("type_name", "type_field", "type_items", "type_desc"):
            items = i['type_items']
            if items:
                items = json.loads(i['type_items'])
            else:
                items = []
            all_dict[i['type_field']] = {
                "type_name": i['type_name'],
                "type_desc": i['type_desc'],
                "items": items
            }
        return all_dict

    class Meta:
        db_table = "sec_event_type"
        verbose_name = "事件类型对照表"


class SSAEventType(models.Model):
    """
    事件类型
    """
    data_tag_id = models.IntegerField()
    # 事件类型
    event_two_type = models.CharField(max_length=500)
    event_three_types = models.CharField(max_length=500, null=True, blank=True)
    event_one_type = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        db_table = "ssa_event_type"
        verbose_name = "事件类型对照表"
