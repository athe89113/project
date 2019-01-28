# coding=utf-8
import logging
import json
from django.contrib import auth
from django.core.cache import cache
from django.http import JsonResponse
from utils.throttles import rate_limit
logger = logging.getLogger("console")


class AdminPassword(object):
    """
    处理密码
    """
    def process_request(self, request):
        """处理 system 下的密码请求
        /api/system
        """
        # 不需要验证密码的几个特殊路由
        not_verify_path = ['/api/system/paytest', '/api/system/message/send', '/api/system/cloud_email/send',
                           '/api/system/smtp_info/test', '/api/system/qs_api/test', '/api/system/baseinfo']
        if request.path in not_verify_path:
            pass

        # 对系统操作部分的请求操作需要输入管理员密码
        elif "/api/system/" in request.path and request.method.lower() in ['post', 'put', 'delete']:
            # 代理商，系统管理员
            if request.user.userinfo.role_type == 2 and request.user.userinfo.is_admin == 1:
                try:
                    admin_password = json.loads(request.body).get("admin_password", '')
                except Exception as e:
                    context = {"msg": "请输入管理员密码", "error": "请输入管理员密码", "status": 403}
                    return JsonResponse(context, status=200)
                else:
                    if not admin_password:
                        context = {"msg": "请输入管理员密码", "error": "请输入管理员密码", "status": 403}
                        return JsonResponse(context, status=200)
                    else:
                        user = auth.authenticate(username=request.user.username, password=admin_password)
                        if user and user.is_active:
                            pass
                            # 验证通过
                        else:
                            # 限制错误请求速度
                            left = rate_limit(cache, request.user.username)
                            if left == -1:
                                context = {"msg": "尝试次数过多，请稍后再请求", "error": "尝试次数过多，请稍后再请求", "status": 429}
                                return JsonResponse(context, status=200)
                            context = {"msg": "密码错误，请重新输入", "error": "密码错误，请重新输入", "status": 403}
                            return JsonResponse(context, status=200)
            else:
                context = {"msg": "您无权操作该接口", "error": "您无权操作该接口", "status": 403}
                return JsonResponse(context, status=200)

        return None
