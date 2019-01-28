# coding=utf8
import cProfile
import json
import marshal
import pstats
import re
import time
from cStringIO import StringIO
from datetime import datetime
from hashlib import md5
from django.conf import settings
from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from django.core.exceptions import MiddlewareNotUsed
from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone
from rest_framework.views import APIView
from soc_user.models import SecretKey


class DisableCsrf(object):
    def process_request(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)

class timeOutMiddleware(object):
    """
    超时中间件
    """

    def process_request(self, request):
        if request.user.is_authenticated():
            if 'lastRequest' in request.session:
                elapsed_time = time.time() - request.session['lastRequest']
                if elapsed_time > request.user.userinfo.agent.login_timeout:
                    del request.session['lastRequest']
                    logout(request)
            if request.path in ('/api/ticket/service', '/api/message', '/api/purchase/shopping_cart'):
                # 自动刷新接口不更新请求时间
                return None
            request.session['lastRequest'] = time.time()
        else:
            if 'lastRequest' in request.session:
                del request.session['lastRequest']

        return None
