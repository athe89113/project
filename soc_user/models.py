# coding: utf-8
import os
import logging
import uuid
from PIL import Image
from hashlib import md5
from django.contrib.auth.models import User
from django.db import models, DatabaseError
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.core.cache import cache

from soc.models import Agent, Company
logger = logging.getLogger('soc')


class WorkGroup(models.Model):
    """
    工作组，部门
    """

    name = models.CharField(max_length=128, null=False)
    agent = models.ForeignKey(Agent)

    class Meta:
        db_table = 'work_group'
        unique_together = ('name', 'agent')

    def __unicode__(self):
        return self.name


def _user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/avatar/user_<id>/<filename>
    if instance.user.userinfo.avatar == 'images/default_avatar.jpg' or instance.user.userinfo.avatar == '':
        name = 'avatar_HEIL_QINGSONG_' + str(instance.user.id)
        name = md5(name).hexdigest()
        name = name[0] + "/" + name[1] + "/" + name
        new_file_name = 'avatar/{}.jpg'.format(name)
    else:
        new_file_name = instance.user.userinfo.avatar.name
        instance.user.userinfo.avatar.delete()
    return new_file_name


def _resize_image(avatar, size=(200,200)):
    image = Image.open(avatar.path)
    image.resize(size, Image.ANTIALIAS).save(avatar.path, 'JPEG', quality=75)


class UserInfo(models.Model):
    user = models.OneToOneField(User)
    phone = models.CharField(max_length=11, null=True)
    agent = models.ForeignKey(Agent)
    # google Two-factor authentication 0 关 1 开
    gs_status = models.IntegerField(default=0)
    google_secret = models.CharField(max_length=30)
    # 0 正常 2 锁定(由于某些原因临时禁用，如登陆错误超限，可自解禁) 1 禁用(不允许登陆，管理员可解禁)，
    is_locked = models.IntegerField(default=0)
    # 用户角色 1是青松, 2为代理商, 3为企业用户
    role_type = models.IntegerField()
    company = models.ForeignKey(Company, null=True)
    # 用户头像
    avatar = models.ImageField(upload_to=_user_directory_path, null=True, default='images/default_avatar.jpg', blank=True)
    work_group = models.ForeignKey(WorkGroup, null=True)
    last_login_ip = models.GenericIPAddressField(null=True)
    # 是否为管理员,1是,0否
    is_admin = models.PositiveSmallIntegerField(default=0)
    # 用户唯一标识，用来区分用户，不仅仅是 ID
    key = models.CharField(max_length=64, default=uuid.uuid4)
    roles = models.ManyToManyField("Roles")
    # 登录失败限制次数
    fail_count = models.IntegerField(default=10)
    # 登录失败限制时间 单位秒
    fail_range_time = models.IntegerField(default=180)
    # 登录失败锁定时间 单位秒
    fail_ban_time = models.IntegerField(default=3600)
    # 登录失败自解锁 0 禁用 1 启用
    fail_self_uban = models.IntegerField(default=0)
    # 是否是隐藏的管理员，作为中心通信接口通信用户
    is_ghost = models.IntegerField(default=0)
    # 注册IP
    ip = models.CharField(max_length=64, null=True, default='')
    # 工号
    employee_id = models.CharField(max_length=64, null=True, blank=True)

    def __unicode__(self):
        return self.user.username + "'s user_info"

    def save(self, *args, **kwargs):
        super(UserInfo, self).save(*args, **kwargs)
        if self.avatar:
            _resize_image(self.avatar)

    @property
    def ban_key(self):
        return "ban_user_{0}".format(self.id)

    def ban(self, ban_time=None):
        if not ban_time:
            ban_time = self.fail_ban_time
        logger.error("用户: {}-{} 超出最大登录失败次数，禁止登录{}秒".format(self.user_id, self.user.username, ban_time))
        cache.add(self.ban_key, 'ban', ban_time)

    def uban(self):
        cache.delete(self.ban_key)

    def is_ban(self):
        return bool(cache.get(self.ban_key, False))

    def login_fail(self):
        key = "login_fail_user_{0}".format(self.id)
        fail_count = cache.get(key)
        if not fail_count:
            cache.add(key, 1, self.fail_range_time)
            if 1 >= self.fail_count:
                self.ban()

        else:
            fail_count = cache.incr(key)
            if fail_count >= self.fail_count:
                self.ban()

    @property
    def is_agent_admin(self):
        """判断是否为代理商管理员"""
        if self.role_type == 3:
            return False
        return bool(self.is_admin)

    @property
    def is_not_agent_admin(self):
        return not self.is_agent_admin


class SecretKey(models.Model):
    # 对应到公司用户, 即role_type为3的User
    user = models.ForeignKey(UserInfo)
    # key 唯一
    key = models.CharField(max_length=128, unique=True)
    # 是否启用 0: 启用 1: 禁用
    enable = models.IntegerField(default=0)
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True)
    # 最后使用时间
    last_used = models.DateTimeField(blank=True, null=True)


class VerifyTmp(models.Model):
    """
    验证邮箱和电话临时存储
    """
    # 验证方式 1电话2邮箱
    type = models.PositiveSmallIntegerField(default=1)
    email = models.EmailField(max_length=128)
    phone = models.CharField(max_length=11, default='')
    # 邮箱激活链接中的认证字串
    link_code = models.CharField(max_length=256, blank=True, null=True, default='')
    # 电话验证码 md5值, 同时需要邮箱
    captcha = models.CharField(max_length=64, blank=True, null=True, default='')
    # 过期时间，短信30分钟，邮箱验证为2小时
    expire_time = models.DateTimeField()
    # 是否验证过
    validated = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = "verify_tmp"

    def __unicode__(self):
        if self.type == 1:
            return self.email + " : " + self.phone
        else:
            return self.email


class Roles(models.Model):
    name = models.CharField(max_length=256)
    agent = models.ForeignKey(Agent)
    # 是否启用 0: 禁用, 1: 启用
    enable = models.IntegerField(default=1)
    is_admin = models.IntegerField(default=0)
    # is_default = models.IntegerField(default=0)
    # 二次验证 0 关 1 开
    two_factor = models.IntegerField(default=0)

    class Meta:
        db_table = 'roles'


class Permissions(models.Model):
    name = models.CharField(max_length=256)
    # url = models.CharField(max_length=256)
    # method = models.CharField(max_length=125, default="GET")
    # 是否启用 0: 禁用, 1: 启用
    default_enable = models.IntegerField(default=1)
    parent = models.ForeignKey("self", null=True, blank=True)

    class Meta:
        db_table = 'permissions'


class RolePermissions(models.Model):
    role = models.ForeignKey(Roles)
    agent = models.ForeignKey(Agent)
    permissions = models.ForeignKey(Permissions)
    # 是否启用 0: 禁用, 1: 启用
    enable = models.IntegerField(default=1)

    class Meta:
        db_table = 'role_permissions'


class PermissionUrls(models.Model):
    url = models.CharField(max_length=256)
    method = models.CharField(max_length=125, default="GET")
    permissions = models.ForeignKey(Permissions)

    class Meta:
        db_table = 'permission_urls'


class WorkTime(models.Model):
    """
    工作时间
    """
    morning_start_time = models.DateTimeField(null=True, blank=True)
    morning_end_time = models.DateTimeField(null=True, blank=True)
    afternoon_start_time = models.DateTimeField(null=True, blank=True)
    afternoon_end_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'work_time'
