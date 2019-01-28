# coding=utf-8
from django.db import models
from pypinyin import lazy_pinyin


class VulStore(models.Model):
    """ 漏洞参考库
    """
    # 漏洞名称
    vul_name = models.CharField(max_length=128, null=True, blank=True)
    # cve 编号
    cve_id = models.CharField(max_length=128, null=True, blank=True)
    # 各漏洞库的编号
    vul_id = models.CharField(max_length=128, null=True, blank=True, unique=True)
    # 危害等级 高 中 低
    vul_level = models.CharField(max_length=10, null=True, blank=True)
    # 漏洞类型
    vul_type = models.CharField(max_length=128, null=True, blank=True)
    # 攻击类型
    attack_type = models.CharField(max_length=128, null=True, blank=True)
    # 受影响实体/产品
    impact = models.CharField(max_length=2048, null=True, blank=True)
    # 漏洞描述
    description = models.CharField(max_length=2048, null=True, blank=True)
    # 漏洞来源
    vul_source = models.CharField(max_length=128, null=True, blank=True)
    # 漏洞公告/解决方案
    advice = models.CharField(max_length=2048, null=True, blank=True)
    # 补丁
    patch = models.CharField(max_length=1024, null=True, blank=True)
    # 参考链接
    reference = models.CharField(max_length=2048, null=True, blank=True)
    # 发布时间
    publish_date = models.DateField(null=True, blank=True)
    # 更新时间
    update_date = models.DateField(null=True, blank=True)
    # 数据采集来源 CNNVD CNVD CVE
    data_source = models.CharField(max_length=10, null=True, blank=True)
    # 标签
    tag = models.CharField(max_length=128, null=True, blank=True)
    # 厂商
    firm = models.CharField(max_length=128, null=True, blank=True)
    # 评分
    score = models.CharField(max_length=10, null=True, blank=True)
    # cvss
    cvss = models.CharField(max_length=128, null=True, blank=True)

    def __unicode__(self):
        return self.vul_id

    class Meta:
        db_table = 'vul_store'
        verbose_name = u"漏洞库"


class SearchKnowledgeLog(models.Model):
    """ 漏洞库/知识库查询记录
    """
    # 查询类型 0 漏洞库 1 知识库 2 预案库
    search_type = models.CharField(max_length=20, blank=True, null=True)
    # 查询对应库ID
    result_id = models.IntegerField()
    # 查询时间
    search_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return str(self.result_id)

    class Meta:
        db_table = 'search_knowledge_log'
        verbose_name = u"查询库记录"


class KnowledgeType(models.Model):
    """ 知识库分类
    """
    name = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'knowledge_type'
        verbose_name = u"知识点类型"


class KnowledgeTag(models.Model):
    """ 知识库分类
    """
    name = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'knowledge_tag'
        verbose_name = u"知识点标签"


class KnowledgeStore(models.Model):
    """ 知识库
    """
    # 知识点标题/名称
    title = models.CharField(max_length=256)
    # 添加人
    user = models.CharField(max_length=128, blank=True, null=True)
    # 分类
    type = models.ForeignKey(KnowledgeType)
    # 标签
    tag = models.ManyToManyField(KnowledgeTag, db_table='knowledge_store_tag')
    # 内容
    content = models.TextField()
    # 关联实体
    relate = models.TextField(blank=True, null=True)
    # 应用场景
    scene = models.CharField(max_length=128, default='')
    # 现象描述
    description = models.CharField(max_length=2048, blank=True, null=True)
    # 操作
    operate = models.CharField(max_length=2048, blank=True, null=True)
    # 判断
    decide = models.CharField(max_length=2048, blank=True, null=True)
    # 结果反馈
    feedback = models.CharField(max_length=2048, blank=True, null=True)
    # 更新编辑时间
    update_time = models.DateTimeField(auto_now=True)
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True)
    # 查询字母
    search_letter = models.CharField(max_length=10, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.search_letter = lazy_pinyin(self.title)[0][0].upper()
        super(KnowledgeStore, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

    class Meta:
        db_table = 'knowledge_store'
        verbose_name = u"知识库"


class PlanTag(models.Model):
    """ 预案库标签
    """
    name = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'plan_tag'
        verbose_name = u"预案标签"


class PlanType(models.Model):
    """ 预案类型
    """
    name = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'plan_type'
        verbose_name = u"预案类型"


class PlanStore(models.Model):
    """ 预案库
    """
    # 标题/名称
    title = models.CharField(max_length=256)
    # 添加人
    user = models.CharField(max_length=128, blank=True, null=True)
    # 等级
    level = models.SmallIntegerField()
    # 类别
    type = models.ForeignKey(PlanType, blank=True, null=True)
    # 标签
    tag = models.ManyToManyField(PlanTag, db_table='plan_store_tag')
    # 应用场景
    scene = models.CharField(max_length=128, default='')
    # 简介
    brief = models.CharField(max_length=2048, blank=True, null=True)
    # 详细
    description = models.TextField()
    # 编辑时间
    update_time = models.DateTimeField(auto_now=True)
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title

    class Meta:
        db_table = 'plan_store'
        verbose_name = u"预案库"


class PlanContacts(models.Model):
    """ 预案联系人
    """
    # 联系人
    name = models.CharField(max_length=128)
    # 手机号
    phone = models.CharField(max_length=20)
    # 邮箱
    email = models.CharField(max_length=128)
    # 预案
    plan = models.ForeignKey(PlanStore, blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'plan_contacts'
        verbose_name = u'预案联系人'


# class OpImgStore(models.Model):
#     """ 安全管理上传图片库
#     """
#     # 图片名称
#     img_name = models.CharField(max_length=128)
#     # 图片目录
#     img_dir = models.CharField(max_length=128)
#     # 对应的库类型 （知识库: 0 /预案库: 1）
#     store_type = models.SmallIntegerField(default=0)
#     # 对应的文章ID
#     store_id = models.IntegerField()
#
#     def __unicode__(self):
#         return self.img_name
#
#     class Meta:
#         db_table = 'op_img_store'
#         verbose_name = u'安全管理文章图片信息'


class SceneType(models.Model):
    """ 应用场景类别
    """
    # 名称
    name = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'scene_type'
        verbose_name = u'应用场景'


class VulStoreVersion(models.Model):
    """ 漏洞库版本
    """
    # 当前的漏洞时间
    current_date = models.CharField(max_length=30, default='')
    # 上一次版本
    last_version = models.CharField(max_length=30, default='')
    # 当前版本
    version = models.CharField(max_length=30, default='')
    # 更新时间
    update_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.version

    class Meta:
        db_table = 'vul_store_version'
        verbose_name = u'漏洞库版本'


class SmWord(models.Model):
    """
    SM词
    """
    word = models.CharField(u'名称', max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'sm_word'


class SmWordLogMessage(models.Model):
    """
    SM词日志信息
    """
    ip = models.CharField(max_length=64)
    word = models.CharField(u'名称', max_length=100, null=True, blank=True)
    sm_content = models.CharField(u'名称', max_length=100, null=True, blank=True)
    add_date = models.DateTimeField(null=True, blank=True)
    level = models.IntegerField()

    class Meta:
        db_table = 'sm_word_log_message'


class WorkDay(models.Model):
    """
    工作日设置
    """
    week = models.CharField(u'工作日', max_length=100, null=True, blank=True)
    state = models.CharField(u'上班状态 1-上班 2-休息', max_length=100, null=True, blank=True)
    am_start_time = models.CharField(u'上午开始时间', max_length=100, null=False, blank=False)
    am_end_time = models.CharField(u'上午结束时间', max_length=100, null=False, blank=False)
    pm_start_time = models.CharField(u'下午开始时间', max_length=100, null=False, blank=False)
    pm_end_time = models.CharField(u'下午结束时间', max_length=100, null=False, blank=False)

    class Meta:
        db_table = 'work_day'


class GroupRule(models.Model):
    """
    规则组
    """
    group_name = models.CharField(u'组名称', max_length=100, null=True, blank=True)
    description = models.CharField(u'描述', max_length=200, null=True, blank=True)
    # 编辑时间
    update_time = models.DateTimeField(auto_now=True)
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'group_rule'


class AlarmRule(models.Model):
    """
    告警规则
    """
    group = models.ForeignKey(GroupRule, null=True, blank=True)
    rule_name = models.CharField(u'规则名称', max_length=100, null=True, blank=True)
    description = models.CharField(u'描述', max_length=200, null=True, blank=True)
    # 级别 1,2,3,4
    level = models.IntegerField(u'等级', default=0)
    # -1-关闭 0-暂停 1-启用
    status = models.IntegerField(u'状态', default=-1)
    # 查询条件
    content = models.TextField(u'查询条件', null=True, blank=True)
    sql = models.TextField(u'拼装sql', null=True, blank=True)
    #  1-时间间隔 2- 时间段
    time_type = models.IntegerField(u'时间间隔类型', default=0)
    # 开始时间
    time_start = models.CharField(u'开始时间', max_length=20, null=True, blank=True)
    # 结束时间
    time_end = models.CharField(u'结束时间', max_length=20, null=True, blank=True)
    interval = models.IntegerField(u'时间间隔', default=0)
    # 编辑时间
    update_time = models.DateTimeField(auto_now=True)
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'alarm_rule'


class AlarmLog(models.Model):
    """
    告警日志
    """
    rule = models.ForeignKey(AlarmRule, null=True, blank=True)
    group_name = models.CharField(u'规则组名称', max_length=100, null=True, blank=True)
    rule_name = models.CharField(u'规则名称', max_length=100, null=True, blank=True)
    src_ip = models.CharField(u'源ip', max_length=50, null=True, blank=True)
    src_port = models.CharField(u'源端口', max_length=10, null=True, blank=True)
    tran_protocol = models.CharField(u'传输层协议', max_length=50, null=True, blank=True)
    app_protocol = models.CharField(u'应用层协议', max_length=50, null=True, blank=True)
    dst_ip = models.CharField(u'目的ip', max_length=50, null=True, blank=True)
    dst_port = models.CharField(u'目的端口', max_length=10, null=True, blank=True)
    event_host = models.CharField(u'发现攻击行为设备ip', max_length=50, null=True, blank=True)
    event_time = models.DateTimeField(u'事件发生时间', null=True, blank=True)
    alarm_time = models.DateTimeField(u'告警时间', null=True, blank=True)
    alarm_level = models.IntegerField(u'事件级别', default=0)
    old_log_list = models.TextField(u'原始日志id集合', null=True, blank=True)
    event_source = models.CharField(u'设备类型', max_length=10, null=True, blank=True)
    status = models.IntegerField(u'状态', default=1)

    class Meta:
        db_table = 'alarm_log'
