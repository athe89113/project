# coding: utf-8
import logging
import time
from hashlib import md5
from itsdangerous import URLSafeTimedSerializer
from django.conf import settings
from django.core.cache import cache
from rest_framework.permissions import IsAuthenticated
from utils.exceptions import AdminPasswordException, AdminPasswordThrottled
from utils.throttles import rate_limit
logger = logging.getLogger("soc")
# 认证相关
secret_key = getattr(settings, "SECRET_KEY")
email_salt = getattr(settings, "EMAIL_SALT")


class AllowAdminWithPassword(IsAuthenticated):
    """
    Allow Admin access.
    Check Admin Password
    """
    def has_permission(self, request, view):
        is_authenticated = super(AllowAdminWithPassword, self).has_permission(request, view)
        if not is_authenticated:
            return False

        if request.method in ("GET", "DELETE"):
            return True
        try:
            user = request.user
            if not user.userinfo.is_admin == 1:
                raise AdminPasswordException
        except Exception as e:
            logger.debug(e.message)
            raise AdminPasswordException

        password = request.data.get("admin_password")
        if not user.check_password(password):
            left = rate_limit(cache, request.user.username)
            if left == -1:
                # 尝试次数过多
                raise AdminPasswordThrottled
            raise AdminPasswordException
        return True


class AllowAdmin(IsAuthenticated):
    """
    Allow Admin access.
    Check Admin Password
    """
    def has_permission(self, request, view):
        is_authenticated = super(AllowAdmin, self).has_permission(request, view)
        if not is_authenticated:
            return False

        try:
            user = request.user
        except Exception as e:
            logger.debug(e.message)
            return False
        if not user.userinfo.is_admin == 1:
            return False
        return True


def get_qs_user_name():
    """
    通过青松ys_user_id, 获取所属用户
    :param ys_user_id:
    :return:
    """
    from soc.models import Agent, Company
    user_data = dict()
    # 所有公司
    companies = Company.objects.all()
    for cp in companies:
        user_info = {cp.key: cp.name}
        user_data.update(user_info)
    # 所有代理商
    agents = Agent.objects.all()
    for ag in agents:
        user_info = {ag.key: ag.name}
        user_data.update(user_info)
    return user_data

