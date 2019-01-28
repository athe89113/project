# coding: utf-8
from __future__ import unicode_literals
from hashlib import md5
import logging
import random
import datetime
import base64
import itsdangerous
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import transaction
from django.contrib import auth
from django.core.cache import cache
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import logout
from soc.models import (
    Agent as ModelAgent,
    AgentPerms as ModelAgentPerms,
)
from soc_user.models import UserInfo
from soc_system.models import BlackIPList
from oath import accept_totp
from soc_user.user_common import (
    verify_phone_captcha,
    get_random_string, send_phone_captcha,
    verify_email_link_code,
    send_forgot_password_mail,
    rsa_decrypt,
    verify_sign,
    str2dict,
    set_login_ip,
    PhoneCaptchaTools
)
from soc_user.serializers import UserSerializer, CompanySerializer, PhoneCaptchaSerializer, EmailVerificationSerializer
from utils import auth as utils_auth
from soc.models import SocLog as MoldelSocLog
import functools
DEFAULT_AGENT_PERMS = range(1, 9)
logger = logging.getLogger("soc")


def get_user_from_username(username, agent=None):
    """获取登陆方式 可以多种方式登陆"""
    user_model = auth.get_user_model()
    if agent:
        login_types = agent.login_type.split(',')
    else:
        login_types = ["username", "email"]
    if "username" in login_types:
        try:
            user = user_model.objects.get(username=username)
            return user
        except:
            pass
    if "email" in login_types:
        try:
            user = user_model.objects.get(email=username)
            return user
        except:
            pass
    if "phone" in login_types:
        try:
            userinfo = UserInfo.objects.get(phone=username)
            return userinfo.user
        except:
            pass
    else:
        return None


# def fail_ip(ip):
#     key = "login_fail_ip_{0}".format(ip)
#     fail_count = cache.get(key)
#         if not fail_count:
#             cache.add(key, 1, self.fail_range_time)
#
#         else:
#             fail_count = cache.incr(key)
#             if fail_count >= self.fail_count:
#                 self.ban()
#
# def ban_ip(ip):
#     key = "login_fail_ip_{0}".format(ip)
#
#     pass
#
#
# def is_ban_ip(ip):
#     key = "login_fail_ip_{0}".format(ip)
#
#     pass

def soclog_login(func):
    """记录登陆信息装饰器"""

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        request = args[0]
        if request.META.has_key('HTTP_X_FORWARDED_FOR'):
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        username = request.DATA.get('username', 0)
        user = None
        if username:
            try:
                user = get_user_from_username(username=username)
                # user = User.objects.get(username=username)
            except:
                user = None
        res = func(self, *args, **kwargs)
        if res.data.has_key('status'):
            if user:
                role = {1: "青松", 2: "管理员", 3: '企业用户'}.get(user.userinfo.role_type)
                agent = user.userinfo.agent
                company = user.userinfo.company
                if res.data['status'] == 200:
                    MoldelSocLog.objects.create(category='登陆', role=role, level='info', info='登陆成功', user=user,
                                                ip=ip, logtype=2, login_status=1, agent=agent, company=company)
                else:
                    MoldelSocLog.objects.create(category='登陆', role=role, level='info', info='登陆失败', user=user,
                                                ip=ip, logtype=2, login_status=2, agent=agent, company=company)

            else:
                MoldelSocLog.objects.create(category='登陆', level='info', info='登陆失败',
                                            ip=ip, logtype=2, login_status=2)
        return res

    return wrapper


class Login(APIView):
    """ 登陆API """

    permission_classes = (AllowAny,)

    def ip_is_ban(self, agent, ip):
        """判断IP是否应该被禁"""
        objs = BlackIPList.objects.filter(agent=agent, is_black=1, ip=ip, type=0)
        if objs:
            obj = objs[0]
            fail_ban_time = agent.fail_ban_time
            start_time = obj.start_time
            # ip被禁的时间 + 应该被禁止的时间 如果大于当前时间 说明此IP应该被禁
            if start_time + timedelta(seconds=fail_ban_time) > timezone.now():
                return True
            return False
        else:
            return False

    def fail_ip_login(self, agent, ip):
        """检查IP在登录日志表里是否应该禁止"""
        objs = BlackIPList.objects.filter(agent=agent, is_black=2, ip=ip)
        # 如果一个 IP在白名单里, 不检查其是否因为登陆次数过多而被禁止
        if objs:
            return None
        # 登录次数
        fail_count = agent.fail_count
        # 登录限制时间
        fail_range_time = agent.fail_range_time
        # 登录失败锁定时间
        fail_ban_time = agent.fail_ban_time
        ban_time = timezone.now() - timedelta(seconds=fail_range_time)
        objs = MoldelSocLog.objects.filter(create_time__gte=ban_time, ip=ip, logtype=2)
        ips = []
        for obj in objs:
            if obj.login_status == 2:
                ips.append(ip)
            else:
                ips = []
        # 本次操作也算失败，但是执行当前函数的时候，还未写入失败日志。所以len(ips)要比实际的少1，故-1
        if len(ips) >= fail_count-1:
            BlackIPList.objects.update_or_create(agent=agent, is_black=1, ip=ip, type=0, defaults={"start_time" : timezone.now()})
            # cache.add("ban_ip_{0}".format(ip), timezone.now(), fail_ban_time)

    def user_is_ban(self, user):
        """判断用户是否应该被禁"""
        if user.userinfo.is_locked == 1:
            # 禁用
            return True, '此账号已被禁用，请联系管理员'
        if user.userinfo.is_locked == 0:
            # 自由身 放开
            return False, ''
        key = "ban_user_{0}".format(user.id)
        start_time = cache.get(key)
        fail_ban_time = user.userinfo.fail_ban_time
        if start_time:
            # 开始时间 + 应该被禁的时间 大于 当前时间 被禁
            if start_time + timedelta(seconds=fail_ban_time) > timezone.now():
                return True, '超出登录失败限制次数，已被锁定'
        user.userinfo.is_locked = 0
        user.userinfo.save()
        return False, ''

    def fail_user_login(self, user):
        """检查user在登录日志表里是否该禁止"""
        fail_count = user.userinfo.fail_count
        fail_range_time = user.userinfo.fail_range_time
        fail_ban_time = user.userinfo.fail_ban_time
        ban_time = timezone.now() - timedelta(seconds=fail_range_time)
        objs = MoldelSocLog.objects.filter(create_time__gte=ban_time, user=user, logtype=2)
        mylist = []
        for obj in objs:
            if obj.login_status == 2:
                mylist.append(user.username)
            else:
                mylist = []
        # 本次操作也算失败，但是执行当前函数的时候，还未写入失败日志。所以len(imylist)要比实际的少1，故-1
        if len(mylist) >= fail_count-1:
            user.userinfo.is_locked = 2
            user.userinfo.save()
            cache.set("ban_user_{0}".format(user.id), timezone.now(), None)

    def get_agent(self):
        host = self.request.META['HTTP_HOST']
        try:
            agent = ModelAgent.objects.get(web_domain=host)
        except ModelAgent.DoesNotExist:
            return None
        return agent

    @soclog_login  # 记录登陆信息装饰器
    def post(self, request):
        """
        登陆信息
        ---
        parameters:
            - name: username
              description: 用户名
              type: string
              paramType: form
              required: true
            - name: password
              description: 密码
              type: string
              paramType: form
              required: true
            - name: gcode
              description: google二次验证码
              type: string
              paramType: form
              required: true
        """
        step = request.DATA.get('step')
        if step not in ['auth', 'token']:
            context = {
                "status": 500,
                "msg": "登录信息错误",
                "error": "登录步骤错误"
            }
            return Response(context)
        secret_key = getattr(settings, "SECRET_KEY")
        login_salt = getattr(settings, "LOGIN_SALT")
        s = itsdangerous.URLSafeTimedSerializer(secret_key, salt=login_salt)
        agent = self.get_agent()
        try:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                real_ip = x_forwarded_for.split(',')[0]
            else:
                real_ip = request.META.get('REMOTE_ADDR')
        except Exception as e:
            real_ip = ""
        if agent and self.ip_is_ban(agent, real_ip):
            context = {
                "status": 400,
                "msg": u"IP超出登录失败限制次数，已被锁定",
                "error": u"IP超出登录失败限制次数，已被锁定",
            }
            self.fail_ip_login(agent, real_ip)
            return Response(context)

        verified = False
        if step == "auth":
            # 用户名和密码验证
            username = str(request.DATA.get('username'))
            password = str(request.DATA.get('password'))
            noauth_user = get_user_from_username(username=username, agent=agent)
            if not noauth_user:
                if agent:
                    # agent.login_fail_ip(real_ip)
                    self.fail_ip_login(agent, real_ip)
                context = {
                    "status": 400,
                    "msg": u"用户名或密码错误",
                    "error": u"用户名或密码错误"
                }
                return Response(context)
            the_login_status, login_msg = self.user_is_ban(noauth_user)
            if the_login_status:
                context = {
                    "status": 400,
                    "msg": login_msg,
                    "error": login_msg,
                }
                self.fail_user_login(noauth_user)
                if agent:
                    self.fail_ip_login(agent, real_ip)
                return Response(context)

            user = auth.authenticate(username=noauth_user.username, password=password)

            if user and user.is_active:

                if user.userinfo.is_locked:
                    context = {
                        "status": 400,
                        "msg": u"用户名被锁定，不能登录",
                        "error": u"用户名被锁定，不能登录"
                    }
                    self.fail_user_login(user)
                    if agent:
                        self.fail_ip_login(agent, real_ip)
                    return Response(context)

                if not user.userinfo.agent.login_allow:
                    # 不允许登陆 除了代理商管理员以外都不能登陆
                    role = user.userinfo.role_type
                    if role == 2 and user.userinfo.is_admin:
                        pass
                    elif role == 1:
                        pass
                    else:
                        self.fail_user_login(user)
                        if agent:
                            self.fail_ip_login(agent, real_ip)
                        return Response({
                            "status": 500,
                            "msg": "不允许登陆，请联系机房管理员",
                            "error": "不允许登陆，请联系机房管理员"
                        })

                # 当前账号的角色是否要二次验证，多对多关系，查出所有，若所有角色身份其中任意一个身份要验证，则验证
                roles = user.userinfo.roles.all()
                two_factor = [obj.two_factor for obj in roles]
                if user.userinfo.gs_status == 1 or sum(two_factor):
                    # 开启了二次验证
                    token = s.dumps(user.username)
                    context = {
                        "status": 200,
                        "msg": "请输入二次验证",
                        "data": {
                            "token": token,
                            "step": "token"
                        }
                    }
                    return Response(context)

                else:
                    verified = True
            else:
                # noauth_user.userinfo.login_fail()
                self.fail_user_login(noauth_user)
                if agent:
                    self.fail_ip_login(agent, real_ip)
                    # agent.login_fail_ip(real_ip)
                context = {
                    "status": 400,
                    "msg": u"用户名或密码错误",
                    "error": u"用户名或密码错误"
                }
                return Response(context)
        else:
            # "token"
            g_code = request.DATA.get('g_code')
            token = request.DATA.get('token')
            # 验证 token正确性和有效性，并获得用户
            try:
                username = s.loads(token, max_age=600)
            except itsdangerous.SignatureExpired as e:
                context = {
                    "status": 500,
                    "msg": "登录超时，请重新登录",
                    "error": "timeout",
                    "data": {
                        "error": "timeout",
                        "action": "re_login"
                    }
                }
                if agent:
                    self.fail_ip_login(agent, real_ip)
                return Response(context)
            except Exception as e:
                context = {
                    "status": 500,
                    "msg": "验证错误，请重新登录",
                    "error": "sign_error#1",
                    "data": {
                        "error": "sign_error",
                        "action": "re_login"
                    }
                }
                if agent:
                    self.fail_ip_login(agent, real_ip)
                return Response(context)

            user = User.objects.get(username=username)
            if not user:
                context = {
                    "status": 400,
                    "msg": u"验证错误，请重新登录",
                    "error": u"sign_error#2"
                }
                if agent:
                    self.fail_ip_login(agent, real_ip)
                return Response(context)
            google_secret = user.userinfo.google_secret
            try:
                result = accept_totp(google_secret, g_code, "dec6")
                if not result[0]:
                    context = {
                        "status": 400,
                        "msg": u"验证码错误",
                        "error": u"验证码错误"
                    }
                    self.fail_user_login(user)
                    if agent:
                        self.fail_ip_login(agent, real_ip)
                    return Response(context)
                verified = True
            except TypeError as e:
                context = {
                    "status": 400,
                    "msg": u"验证码错误",
                    "error": u"验证码错误"
                }
                self.fail_user_login(user)
                if agent:
                    self.fail_ip_login(agent, real_ip)
                return Response(context)

        if verified:
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            auth.login(request, user)

            agent_perms = ModelAgentPerms.objects.filter(agent=user.userinfo.agent).values('perms')
            agent_perms = [ap['perms'] for ap in agent_perms]
            if not agent_perms:
                # default perms
                agent_perms = DEFAULT_AGENT_PERMS
            data = {
                "username": user.username,
                "role_type": user.userinfo.role_type,
                "is_admin": user.userinfo.is_admin,
                "enable_iframe": user.userinfo.agent.enable_iframe
            }
            user.userinfo.last_login_ip = real_ip
            user.userinfo.save()
            context = {
                "status": 200,
                "msg": u"登陆成功",
                "data": data
            }
            return Response(context)
        else:
            # user.userinfo.login_fail()
            # if agent:
            #    agent.login_fail_ip(real_ip)
            self.fail_user_login(user)
            if agent:
                self.fail_ip_login(agent, real_ip)
            context = {
                "status": 400,
                "msg": u"用户名或密码错误",
                "error": u"用户名或密码错误"
            }
            return Response(context)


class Logout(APIView):
    """ 退出API """

    def get(self, request):
        """退出"""
        logout(request)
        context = {
            "status": 200,
            "msg": "退出成功"}
        return Response(context)


def soclog_register(func):
    """记录注册信息装饰器"""

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        request = args[0]
        if request.META.has_key('HTTP_X_FORWARDED_FOR'):
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        username = request.DATA.get('email', 0)
        res = func(self, *args, **kwargs)
        if res.data.has_key('status'):
            if res.data['status'] == 200:
                try:
                    user = User.objects.get(username=username)
                except:
                    user = None
                if user:
                    role = {1: "青松", 2: "管理员", 3: '企业用户'}.get(user.userinfo.role_type)
                    agent = user.userinfo.agent
                    company = user.userinfo.company
                    MoldelSocLog.objects.create(category='注册', role=role, level='info', info='注册成功', user=user,
                                                ip=ip, logtype=3, login_status=1, agent=agent, company=company)

            else:
                MoldelSocLog.objects.create(category='注册', level='info', info='注册失败',
                                            ip=ip, logtype=3, login_status=2)

        return res

    return wrapper


class RegisterStatus(APIView):
    """注册状态"""
    permission_classes = (AllowAny,)

    def get_agent(self):
        host = self.request.META['HTTP_HOST']
        try:
            agent = ModelAgent.objects.get(web_domain=host)
        except ModelAgent.DoesNotExist:
            return None
        return agent

    def get(self, request):
        """获取是否允许注册"""
        agent = self.get_agent()
        if agent:
            return Response({
                "status": 200,
                "msg": "获取数据成功",
                "data": {"status": agent.register_allow}
            })
        else:
            return Response({
                "status": 500,
                "msg": "获取代理商错误",
                "data": {}
            })


class Register(APIView):
    """
    注册
    """
    permission_classes = (AllowAny,)

    def is_ban(self, agent, ip):
        """从注册表里查询IP登陆信息，判断IP是否允许登录"""
        # 注册次数
        register_count = agent.register_count
        # 注册限制时间
        register_time = agent.register_time
        ban_time = timezone.now() - timedelta(seconds=register_time)
        objs = MoldelSocLog.objects.filter(create_time__gte=ban_time, ip=ip, logtype=3)
        # 本次操作也算失败，但是执行当前函数的时候，还未写入失败日志。所以len(ips)要比实际的少1，故-1
        if len(objs) >= register_count:
            return True
        return False

    @soclog_register
    def post(self, request):
        """
        注册
            * email             邮箱
            * password          密码
            * confirm_password  确认密码
            * phone             电话
            * captcha           验证码
            * hostname          当前用户的登录地址，用来确定不同代理商

        用户公司用用户信息暂时确定
        :param request:
        :return:
        """
        # 获取代理商
        hostname = request.data.get('hostname', None)
        agent = ModelAgent.objects.filter(web_domain=hostname).first()
        if not agent:
            agent = ModelAgent.objects.get(id=1)
        # 获取IP
        try:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                real_ip = x_forwarded_for.split(',')[0]
            else:
                real_ip = request.META.get('REMOTE_ADDR')
        except Exception as e:
            real_ip = ""
        if self.is_ban(agent, real_ip):
            return Response({
                "status": 500,
                "msg": '{0}分钟之内只允许注册{1}个账号'.format(agent.register_time / 60, agent.register_count),
                "error": '{0}分钟之内只允许注册{1}个账号'.format(agent.register_time / 60, agent.register_count)
            })
        # 验证验证码
        captcha = request.DATA.get("captcha", '')
        email = request.DATA.get("email", '')
        phone = request.DATA.get("phone", '')
        verified, msg = verify_phone_captcha(email, phone, captcha)
        if not verified:
            context = {
                "status": 500,
                "msg": msg,
                "error": msg
            }
            return Response(context)

        # 添加用户及所属个人公司
        context = {
            "agent": agent,
        }
        new_user_data = {
            "is_admin": 1,
            "agent_id": agent.id,
            "role_type": 3,
            "username": request.data.get('email')
        }
        new_user_data.update(request.data)
        new_user = UserSerializer(data=new_user_data, context=context)

        if new_user.is_valid():
            # 生成公司并和生成的用户绑定
            company_name = '_user_company_' + str(random.randint(1, 10)) + "_" + new_user.validated_data.get('username')
            new_company = CompanySerializer(data={"name": company_name}, context=context)
            if new_company.is_valid():
                # 创建公司并绑定用户
                with transaction.atomic():
                    new_company = new_company.save()
                    new_user = new_user.save()
                    new_user.userinfo.company = new_company
                    new_user.userinfo.ip = real_ip
                    new_user.userinfo.save()

            else:
                logger.error(new_company.errors)
                # for error in new_company.errors:
                #     context = {
                #         "status": 500,
                #         "msg": new_company.errors[error][0],
                #         "error": new_company.errors[error][0],
                #     }
                #     return Response(context)
                context = {
                    "status": 500,
                    "msg": "请求错误，请重试",
                    "error": "请求错误，请重试"
                }
                return Response(context)

            return Response({'status': 200, 'msg': '注册成功'})
        else:
            for error in new_user.errors:
                context = {
                    "status": 500,
                    "msg": new_user.errors[error][0],
                    "error": new_user.errors[error][0],
                }
                return Response(context)

        # return Response({'status': 500, 'msg': new_user.errors.items()[0][1][0], 'error': new_user.errors})


class PhoneCaptcha(APIView):
    """
    验证码
    """
    permission_classes = (AllowAny,)
    throttle_scope = 'phone_captcha'

    def get(self, request):
        """发送验证码"""
        phone = request.user.phone
        if not phone:
            return Response({"status": 500, "msg": "请先绑定手机"})
        pct = PhoneCaptchaTools()
        captcha = pct.create(phone, user_key=request.user.id)
        # captcha = get_random_string(6)
        site = get_current_site(request)
        send_phone_captcha(phone, captcha, 'http://' + site.domain)
        context = {
            "status": 200,
            "msg": "发送验证码成功，请注意查收短信"
        }
        return Response(context)

    def post(self, request):
        """
        发送手机验证码
        :param request:
        :return:
        """
        captcha = get_random_string(6)
        context = {
            "captcha": captcha
        }
        new_captcha = PhoneCaptchaSerializer(data=request.data, context=context)
        if new_captcha.is_valid():
            new_captcha.save()
            phone = new_captcha.validated_data.get('phone')
            # 发送短信
            site = get_current_site(request)
            send_phone_captcha(phone, captcha, 'http://' + site.domain)
        else:
            logger.error(new_captcha.errors)
            for error in new_captcha.errors:
                context = {
                    "status": 500,
                    "msg": new_captcha.errors[error][0],
                    "error": new_captcha.errors[error][0],
                }
                return Response(context)

        context = {
            "status": 200,
            "msg": "发送验证码成功，请注意查收短信"
        }
        return Response(context)


class EmailVerification(APIView):
    """
    验证码
    """

    def post(self, request):
        """
        发送手机验证码
        :param request:
        :return:
        """
        pass


class ForgotPassword(APIView):
    """
    忘记密码
    """
    permission_classes = (AllowAny,)
    throttle_scope = 'email_verification'

    def post(self, request):
        """
        通过邮箱找回密码，发送链接
        :param request:
        :return:
        """
        email_verify = EmailVerificationSerializer(data=request.data, context={"link_code": "link_code"})
        if email_verify.is_valid():
            # 生成找回密码链接
            email = email_verify.validated_data.get('email')
            link_code = utils_auth.generate_confirmation_token(email)
            # 保存
            verify_tmp = email_verify.save()
            verify_tmp[0].link_code = md5(link_code).hexdigest()
            verify_tmp[0].save()

            # 发送
            site = get_current_site(request)
            link = 'http://' + site.domain + '/confirm/' + link_code
            # todo 发送确认邮件
            send_forgot_password_mail(email, link=link)
            context = {
                "status": 200,
                "msg": "验证链接已发送，请注意查收邮件",
                "error": "验证链接已发送，请注意查收邮件",
            }
            return Response(context)
        else:
            for error in email_verify.errors:
                context = {
                    "status": 500,
                    "msg": email_verify.errors[error][0],
                    "error": email_verify.errors[error][0],
                }
                return Response(context)

    def put(self, request):
        """
        修改忘记的密码
            password
            confirm_password
            link_code
        :param request:
        :return:
        """
        # 验证 link_code
        link_code = request.DATA.get("link_code")
        email = utils_auth.confirm_token(link_code, expiration=1800)
        if not email:
            context = {
                "status": 500,
                "msg": "验证错误",
                "error": "验证错误",
            }
            return Response(context)

        # 验证邮件链接
        ok, msg = verify_email_link_code(email, link_code=link_code)
        if not ok:
            context = {
                "status": 500,
                "msg": msg,
                "error": msg,
            }
            return Response(context)

        # 验证密码
        password = request.DATA.get('password')
        confirm_password = request.DATA.get('confirm_password')
        if not password:
            context = {
                "status": 500,
                "msg": "请输入密码",
                "error": "请输入密码",
            }
            return Response(context)
        if password != confirm_password:
            context = {
                "status": 500,
                "msg": "密码和确认密码必须一致",
                "error": "密码和确认密码必须一致",
            }
            return Response(context)

        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()
        context = {
            "status": 200,
            "msg": "修改密码成功",
            "error": "修改密码成功",
        }
        return Response(context)


class ConfirmEmail(APIView):
    """登陆信息"""
    def post(self, request):
        """
        确认邮箱链接
        :param request:
        :return:
        """

        link_code = request.DATA.get("link_code")
        email = utils_auth.confirm_token(link_code, expiration=1800)
        if not email:
            context = {
                "status": 500,
                "msg": "验证错误",
                "error": "验证错误",
            }
            return Response(context)

        # 验证邮件链接
        ok, msg = verify_email_link_code(link_code=link_code)
        if not ok:
            context = {
                "status": 500,
                "msg": msg,
                "error": msg,
            }
            return Response(context)

        context = {
            "status": 200,
            "msg": "验证合法",
            "error": "验证合法",
        }
        return Response(context)


class SSOLogin(APIView):
    """登录信息"""
    permission_classes = ()

    """
    501: partner 不存在
    502 信息缺失
    503 解密失败
    504 时间错误
    505 用户不存在
    """

    def post(self, request, base_str):
        """登陆信息加密"""
        try:
            if '==' not in base_str:
                base_str += '=='
            base_str = base64.b64decode(base_str)
        except Exception as e:
            logger.error("sso error 503 {0}".format(e.message))
            return Response({"status": 503, "msg": "验证失败"})
        try:
            partner = base_str.split('partner=')[1].split('&sign=')[0]
            sign = base_str.split('&sign=')[1].split('&user=')[0]
            user = base_str.split('&user=')[1]

        except Exception as e:
            logger.error("sso error 503 {0}".format(e.message))
            return Response({"status": 503, "msg": "验证失败"})

        try:
            agent = ModelAgent.objects.get(key=partner)
        except ModelAgent.DoesNotExist:
            return Response({"status": 501, "msg": "验证失败"})

        # 代理商私钥 验证签名
        agent_pub_key = agent.ssl_pub_key
        try:
            is_verify = verify_sign(agent_pub_key, user, sign)
        except Exception as e:
            logger.error("sso error 503 {0}".format(e.message))
            return Response({"status": 503, "msg": "验证失败"})

        if not is_verify:
            return Response({"status": 503, "msg": "验证失败"})
        #
        # RAS解密
        try:
            data = rsa_decrypt(settings.SSO_PRIVATE_KEY, user)
            data = str2dict(data)
        except Exception as e:
            logger.error("sso error 503 {0}".format(e.message))
            return Response({"status": 503, "msg": "验证失败"})

        user_email = data.get('user_id')
        timestamp = data.get('timestamp')

        try:
            if len(timestamp) == 10:
                timestamp = datetime.datetime.fromtimestamp(int(timestamp))
            elif len(timestamp) == 13:
                timestamp = datetime.datetime.fromtimestamp(int(timestamp)/1000)
            else:
                logger.error("sso error 504 {0}".format(len(timestamp)))
                return Response({"status": 504, "msg": "验证失败"})
            diff_time = abs(timestamp - datetime.datetime.now()).seconds
        except Exception as e:
            logger.error("sso error 504 {0}".format(e.message))
            return Response({"status": 504, "msg": "验证失败"})

        if diff_time > 600:
            return Response({"status": 504, "msg": "验证失败"})

        try:
            user = User.objects.get(email=user_email)
        except Exception as e:
            logger.error("sso error 505 {0}".format(e.message))
            return Response({"status": 505, "msg": "验证失败"})

        user.backend = 'django.contrib.auth.backends.ModelBackend'
        auth.login(request, user)
        set_login_ip(request, user)
        data = {
            "username": user.username,
            "role_type": user.userinfo.role_type,
            "is_admin": user.userinfo.is_admin,
            "enable_iframe": user.userinfo.agent.enable_iframe
        }
        return Response({"status": 200, "data": data})


class CheckPassword(APIView):
    """锁定检查"""

    def post(self, request):
        """锁定检查"""
        
        user = request.user
        password = request.data.get('password')
        if user.check_password(password):
            return Response({"status": 200, "msg": "验证成功"})
        return Response({"status": 500, "msg": "验证失败"})
