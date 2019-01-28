# coding=utf-8
import re
import hashlib
import time
import logging
from copy import deepcopy
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.http import HttpResponse
from django.utils import timezone
from soc_user.models import UserInfo
from datetime import timedelta
from django.contrib.auth import authenticate
from django.forms.models import model_to_dict
from django.contrib.sites.shortcuts import get_current_site
from utils.alipay import Alipay
from django.core.cache import cache
from utils.datatable import DatatableView
from utils.auth import AllowAdminWithPassword
from soc_system import serializers
from soc_user.models import Roles
from utils.crm_api import Crm
# from soc_system.models import SetEmail, SetMsg,
from soc_system.models import SetPay, Message as ModelMessage, BlackIPList
from soc_system.form import PaymentReturnBaseForm
from soc_message_center.message_center.send_messages import SendMessage, SendEmailCloud, SendEmailSMTP

logger = logging.getLogger("soc")


def pw_valid(username, pw):
    # 检验密码
    user = authenticate(username=username, password=pw)
    if user is not None and user.is_active:
        return True
    return False


def is_phone(phone):
    p2 = re.compile('^0\d{2,3}\d{7,8}$|^1[3587]\d{9}$|^147\d{8}')
    phonematch = p2.match(phone)
    if phonematch:
        return True
    return False


def is_email(email):
    if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email):
        return True
    return False


class BaseInfo(APIView):
    """系统基本信息"""
    permission_classes = (AllowAdminWithPassword,)

    def utos(self, ag):
        if ag and type(ag) == unicode:
            return ag.encode("utf8")
        return ag

    def get(self, request):
        """获取系统基本信息"""
        agent = request.user.userinfo.agent
        if agent.web_logo:
            web_logo = agent.web_logo.name
        else:
            web_logo = ''
        data = {
            "title": self.utos(agent.web_title),
            "web_domain": self.utos(agent.web_domain),
            "web_logo": '',
            "record_number": self.utos(agent.record_number),
            "server_phone": self.utos(agent.server_phone),
            "email": self.utos(agent.email),
        }
        context = {
            "status": 200,
            "msg": "获取数据成功",
            "data": data
        }
        return Response(context)

    def put(self, request):
        """
        修改基本信息数据 
        先校验管理员密码
        为空即为不修改此项
        title不大于10个长度
        web_domain 以https:// 或者http://开头
        :param request: 
        :return: 
        """
        agent = request.user.userinfo.agent
        agent_serializers = serializers.BaseInfoSerializers(instance=agent, data=request.data)
        if agent_serializers.is_valid():
            agent_serializers.save()
            image = ''
            if "logo" in request.FILES:
                image = request.FILES["logo"]
                if not image.name.endswith('.png'):
                    return Response({
                        "status": 500,
                        "msg": "文件格式错误",
                        "data": {}
                    })
                m1 = hashlib.md5(image.name[:-4])
                image.name = m1.hexdigest() + '.png'
            if image and image.size > 200 * 1000:  # 不能大于200K
                return Response({
                    "status": 500,
                    "msg": "图片体积太大",
                    "data": {}
                })
            if image:
                agent.web_logo = image
                agent.save()
            return Response({
                "status": 200,
                "msg": "修改成功",
                "data": {}
            })
        else:
            msg = "数据错误"
            for error in agent_serializers.errors:
                msg = agent_serializers.errors[error][0]
                break
            context = {
                "status": 500,
                "msg": msg,
                "error": agent_serializers.errors
            }
            return Response(context)


class SMTPinfo(APIView):
    """邮件服务信息"""
    permission_classes = (AllowAdminWithPassword,)

    def get(self, request):
        """获取邮件配置信息"""
        agent = request.user.userinfo.agent
        data = ModelMessage.get_smtp_info(agent_id=agent.id)
        data["password"] = ''
        context = {
            "status": 200,
            "msg": "获取数据成功",
            "data": data
        }
        return Response(context)

    def put(self, request):
        """修改邮件配置信息"""
        agent = request.user.userinfo.agent
        email = ModelMessage.objects.get_or_create(agent=agent, type=1)[0]
        email_serializers = serializers.SMTPSerializers(instance=email, data=request.data)
        if email_serializers.is_valid():
            email_serializers.save()
            return Response({
                "status": 200,
                "msg": "修改成功",
                "data": {}
            })
        else:
            msg = "数据错误"
            for error in email_serializers.errors:
                msg = email_serializers.errors[error][0]
                break
            context = {
                "status": 500,
                "msg": msg,
                "error": email_serializers.errors
            }
            return Response(context)


class CloudEmail(APIView):
    """邮件配置信息"""
    permission_classes = (AllowAdminWithPassword,)

    def get(self, request):
        """获取邮件配置信息"""
        agent = request.user.userinfo.agent
        data = ModelMessage.get_cloud_info(agent_id=agent.id)
        data["password"] = ''
        context = {
            "status": 200,
            "msg": "获取数据成功",
            "data": data
        }
        return Response(context)

    def put(self, request):
        """修改邮件配置信息"""
        agent = request.user.userinfo.agent
        email = ModelMessage.objects.get_or_create(agent=agent, type=4)[0]
        cloud_email = serializers.CloudEmailSerializers(instance=email, data=request.data)
        if cloud_email.is_valid():
            cloud_email.save()
            return Response({
                "status": 200,
                "msg": "修改成功",
                "data": {}
            })
        else:
            msg = "数据错误"
            for error in cloud_email.errors:
                msg = cloud_email.errors[error][0]
                break
            context = {
                "status": 500,
                "msg": msg,
                "error": cloud_email.errors
            }
            return Response(context)


class SendTestSmtp(APIView):
    """
    smtp 发送测试邮件
    """
    def post(self, request):
        """发送邮件"""
        agent = request.user.userinfo.agent
        email = ModelMessage.objects.get_or_create(agent=agent, type=1)[0]
        email_serializers = serializers.SMTPSerializers(instance=email, data=request.data)
        password = request.data.get("password").strip()
        tls_or_ssl = int(request.data.get('tls_or_ssl'))
        if tls_or_ssl:
            SSL = True
            TLS = False
        else:
            SSL = False
            TLS = True
        send_test = request.data.get("send_test").strip()
        if not is_email(send_test):
            return Response({
                'status': 500,
                'msg': '邮箱格式错误',
                'data': {}
            })
        if not password:
            data = ModelMessage.get_smtp_info(agent_id=agent.id)
            password = data["password"]
        if email_serializers.is_valid():
            # 发送测试邮件
            obj = SendEmailSMTP(target_id=0, agent_id=0, content={"title": "测试邮件", "content": "这是一封测试邮件"},
                                tls=TLS, ssl=SSL, send_address=request.data.get("send_sender").strip(), to=send_test,
                                smtp_server=request.data.get('smtp_server').strip(),
                                smtp_user=request.data.get("user").strip(),
                                smtp_pwd=password
                                )
            status, msg = obj.send()
            if status:
                return Response({
                    "status": 200,
                    "msg": "发送成功",
                    "data": {}
                })
            else:
                logger.error(msg)
                return Response({
                    "status": 500,
                    "msg": msg,
                    "data": {}
                })
        else:
            msg = "数据错误"
            for error in email_serializers.errors:
                msg = email_serializers.errors[error][0]
                break
            logger.error(msg)
            context = {
                "status": 500,
                "msg": msg,
                "error": email_serializers.errors
            }
            return Response(context)


class SendTestCloud(APIView):
    """cloud 发送测试邮件"""
    def post(self, request):
        """发送邮件"""
        user = request.data.get("user", '').strip()
        password = request.data.get("password", '').strip()
        send_test = request.data.get("send_test", '').strip()
        if not is_email(send_test):
            return Response({
                "status": 500,
                "msg": '邮箱格式不正确',
                "data": {}
            })
        if not password:
            agent = request.user.userinfo.agent
            data = ModelMessage.get_cloud_info(agent_id=agent.id)
            password = data["password"]
        msg = SendEmailCloud(target_id=0, sender_type_id=0, agent_id=0,
                             content={"title": "测试邮件", "content": "这是一封测试邮件"}, to=send_test, api_user=user,
                             api_key=password)
        status = msg.send()
        if status["result"] == 'ok':

            return Response({
                "status": 200,
                "msg": "发送成功",
                "data": {}
            })
        else:
            return Response({
                "status": 500,
                "msg": '发送失败',
                "data": {}
            })


class Message(APIView):
    """
    短信设置
    """
    permission_classes = (AllowAdminWithPassword,)

    def get(self, request):
        """获取短信设置信息"""
        agent = request.user.userinfo.agent
        data = ModelMessage.get_msg_info(agent_id=agent.id)
        data["password"] = ''
        context = {
            "status": 200,
            "msg": "获取数据成功",
            "data": data
        }
        return Response(context)

    def put(self, request):
        """修改短信设置信息"""
        agent = request.user.userinfo.agent
        obj = ModelMessage.objects.get_or_create(agent=agent, type=2)[0]
        msg_serializers = serializers.MsgSerializers(instance=obj, data=request.data)
        if msg_serializers.is_valid():
            msg_serializers.save()
            return Response({
                "status": 200,
                "msg": "保存成功",
                "data": {}
            })

        else:
            msg = "数据错误"
            for error in msg_serializers.errors:
                msg = msg_serializers.errors[error][0]
                break
            context = {
                "status": 500,
                "msg": msg,
                "error": msg_serializers.errors
            }
            return Response(context)


class MessageTest(APIView):
    """测试短信"""
    def post(self, request):
        """发送测试短信"""
        api = request.data.get("api", '').strip()
        user = request.data.get("user", '').strip()
        password = request.data.get("password", '').strip()
        test_phone = request.data.get("send_test", '').strip()
        if not is_phone(test_phone):
            return Response({
                "status": 500,
                "msg": "手机号输入错误",
                "data": {}
            })
        if not api or not user:
            return Response({
                "status": 500,
                "msg": "信息输入错误",
                "data": {}
            })
        if not password:
            agent = request.user.userinfo.agent
            data = ModelMessage.get_msg_info(agent_id=agent.id)
            password = data["password"]
        content = "这是一条测试短信"
        msg = SendMessage(target_id=0, content={"content": content}, agent_id=0, to=test_phone, api=api,
                          api_user=user, api_pwd=password)
        status = msg.send()
        if status["result"] == 'ok':
            return Response({
                "status": 200,
                "msg": "发送成功",
                "data": {}
            })
        else:
            return Response({
                "status": 500,
                "msg": status["error"],
                "data": {}
            })


class Finance(APIView):
    """支付信息"""
    permission_classes = (AllowAdminWithPassword,)

    def get(self, request):
        """获取财务设置信息 包括在线支付离线支付"""
        agent = request.user.userinfo.agent
        obj = SetPay.objects.get_or_create(agent=agent)[0]
        mydata = model_to_dict(obj)
        user = request.user
        crm = Crm(user=user)
        data = crm.get_agent_info()
        if data["status"] == 200:  # CRM返回正确 添加自身的数据
            mydata["pay_online"] = int(mydata["pay_online"])
            mydata["pay_outline"] = int(mydata["pay_outline"])
            mydata["invoice"] = int(mydata["invoice"])
            data["data"].update(mydata)
            data["data"]["pay_private_key"] = ''
        return Response(data)

    def put(self, request):
        """修改财务信息"""
        agent = request.user.userinfo.agent
        obj = SetPay.objects.get_or_create(agent=agent)[0]
        finance_data = serializers.FinanceSerializers(instance=obj, data=request.data)
        if finance_data.is_valid():
            args = {
                "pay_pid": finance_data.validated_data.get('pay_pid'),
                "pay_private_key": finance_data.validated_data.get('pay_private_key')
            }
            user = request.user
            crm = Crm(user=user)
            data = crm.set_agent_info(args=args)
            if data["status"] == 200:
                data["msg"] = '保存成功'
                finance_data.save()
            return Response(data)
        else:
            msg = "数据错误"
            for error in finance_data.errors:
                msg = finance_data.errors[error][0]
                break
            context = {
                "status": 500,
                "msg": msg,
                "error": finance_data.errors
            }
            return Response(context)


class AliPayCallBack(APIView):
    """
    支付宝回调接口
    """
    permission_classes = (AllowAny,)

    def do_pay(self, request):
        """
        支付宝异步回调接口
        :param request:
        :return: 向支付宝返回成功接收并处理异步通知状态 success
        """
        request_data = getattr(request, request.method)
        request_data = deepcopy(request_data)
        form = PaymentReturnBaseForm(request_data)
        if not form.is_valid():
            logger.error('error alipay form {0}'.format(form.errors))
            return HttpResponse('出现未知错误')
        cld = form.cleaned_data
        # 获取订单号
        seller_id = cld["seller_id"]
        # 取缓存
        cache_data = cache.get('alipay')
        alipay = Alipay(
            partner=cache_data.get('partner'),
            private_key=cache_data.get('private_key'),
            seller_id=cache_data.get('seller_id'),
            seller_email=cache_data.get('seller_email'),
            alipay_public_key_string=''
        )

        if not alipay.partner == seller_id:
            logger.error("error seller_id: %s" % seller_id)
            return HttpResponse("支持出现错误")
        notify_id = cld['notify_id']
        # # 验证签名
        if not alipay.verify_sign(cld):
            logger.error("invalid sign")
            return HttpResponse('支持出现错误')
        # 验证是否是支付宝发来的通知
        if not alipay.verify_notify(notify_id):
            logger.error("invalid sign")
            return HttpResponse("支持出现错误")
        # 验证 total_fee
        if not float(cld['total_fee']) == 0.01:
            logger.error("error total_fee: %s" % str(cld['total_fee']))
            return HttpResponse("支持出现错误")
        logging.info('pay test successful')
        return HttpResponse("支付成功")

    def get(self, request):
        """同步回调"""
        return self.do_pay(request)

    def post(self, request):
        """异步回调"""
        return self.do_pay(request)


class PayTest(APIView):
    """测试支付"""
    def post(self, request):
        """
        :param request: 
        :return: 
        """
        money = request.data.get("money", 0)
        pay_pid = request.data.get("pay_pid", '').strip()  # alipay_partner
        pay_private_key = request.data.get("pay_private_key", '').strip()  # alipay_private_key
        email = request.data.get("email", '').strip()  # alipay_seller_email
        if not money:
            return Response({
                "status": 500,
                "msg": "支付金额错误",
                "data": {}
            })
        try:
            float(money)
        except Exception as e:
            return Response({
                "status": 500,
                "msg": "支付金额错误",
                "data": {}
            })
        if not email or not pay_pid:
            return Response({
                "status": 500,
                "msg": "支付信息不完整",
                "data": {}
            })
        if not pay_private_key:
            agent = request.user.userinfo.agent
            obj = SetPay.objects.get_or_create(agent=agent)[0]
            mydata = model_to_dict(obj)
            user = request.user
            crm = Crm(user=user)
            data = crm.get_agent_info()
            pay_private_key = data['data']['pay_private_key']
        alipay = Alipay(
            partner=pay_pid,
            private_key=pay_private_key,
            seller_id=pay_pid,
            seller_email=email
        )
        cache_data = {
            "partner": pay_pid,
            "private_key": pay_private_key,
            "seller_id": pay_pid,
            "seller_email": email
        }
        # 把数据存入缓存 有效期10分钟
        cache.set('alipay', cache_data, 10*60)
        site = get_current_site(request)
        protocol = 'http://' if request.is_secure() else 'https://'
        notify_url = protocol + site.domain + "/soc/system/order_callback"
        return_url = protocol + site.domain + '/soc/system/finance/alipay'
        alipay_dict = {
            'notify_url': notify_url,
            'return_url': "http" + return_url[5:],
            'sign_type': 'MD5',
            # 'out_trade_no': ''.join([random.SystemRandom().choice("asdfghjklqwertyuiopmnbvcxz") for i in range(20)]),
            'out_trade_no': str(int(time.time()*10000)),
            'subject': "测试订单",
            'total_fee': money,
            'body': "测试支付",
            'anti_phishing_key': 'AABBCDDEG',
        }
        pay_url = alipay.create_direct_pay_by_user_url(**alipay_dict)
        context = {
            "status": 200,
            "url": pay_url,
            "data": {}
        }
        return Response(context)


class TestApi(APIView):
    """
    api测试接口 和crm通信
    """
    qs_token = ''
    qs_token_secret = ''
    qs_api_timeout = ''
    user = None

    def post(self, request):
        """发送API测试数据"""
        agent = request.user.userinfo.agent
        self.user = request.user
        apiobj = serializers.SetAPISerializers(instance=agent, data=request.data)
        if apiobj.is_valid():
            self.qs_token = apiobj.validated_data.get("qs_token")
            self.qs_token_secret = apiobj.validated_data.get('qs_token_secret')
            self.qs_api_timeout = apiobj.validated_data.get("qs_api_timeout")
            crm = Crm(user=self.user, timeout=self.qs_api_timeout, ys_token=self.qs_token,
                      private_key=self.qs_token_secret)
            data = crm.get_agent_info()
            if data["status"] == 200:
                data["msg"] = '接口测试成功'
            return Response(data)
        else:
            msg = "数据错误"
            for error in apiobj.errors:
                msg = apiobj.errors[error][0]
                break
            context = {
                "status": 500,
                "msg": msg,
                "error": apiobj.errors
            }
            return Response(context)


class SetApi(APIView):
    """API接口信息设置"""
    permission_classes = (AllowAdminWithPassword,)

    def get(self, request):
        """获取API接口数据"""
        agent = request.user.userinfo.agent
        data = {
            "qs_token": agent.qs_token,
            "qs_token_secret": agent.qs_token_secret,
            "qs_api_timeout": agent.qs_api_timeout
        }
        return Response({
            "status": 200,
            "msg": "获取成功",
            "data": data
        })

    def put(self, request):
        """
        修改接口信息设置
        :param request: 
        :return: 
        """
        agent = request.user.userinfo.agent
        apiobj = serializers.SetAPISerializers(instance=agent, data=request.data)
        if apiobj.is_valid():
            apiobj.save()
            return Response({
                "status": 200,
                "msg": "保存成功",
                "data": {}
            })
        else:
            msg = "数据错误"
            for error in apiobj.errors:
                msg = apiobj.errors[error][0]
                break
            context = {
                "status": 500,
                "msg": msg,
                "error": apiobj.errors
            }
            return Response(context)


class Visit(APIView):
    """访问设置"""
    permission_classes = (AllowAdminWithPassword,)

    def get(self, request):
        """
        获取访问设置信息
        data = {
            'username': True, 
            'email': True
            'phone': True, 
            'wechat': True,  
            
            'fail_range_time': 180L,   IP限制时间
            'fail_ban_time': 60L,   IP限制禁止时间
            'fail_count': 10L,  IP限制次数   
            
            'user_fail_count': 10L,     账号限制次数
            'user_fail_range_time': 3L,     账号限制时间
            'user_fail_ban_time':           账号限制禁止时间
            
            'register_time': 180L,  注册限制时间
            'register_count': 5L,   注册限制次数
            
            'login_allow': 1L, 是否允许登陆
            'is_find_password': 1L,     是否找回密码
            'register_allow': 1L,   是否允许注册

            'login_timeout': 登录会话超时时间
        }
        """
        agent = request.user.userinfo.agent
        userinfo = request.user.userinfo
        login_types = agent.login_type.split(',')
        data = model_to_dict(agent,
                             fields=["register_time", "register_count", "register_allow", "login_allow", "fail_count",
                                     "fail_range_time", "fail_ban_time", 'is_find_password', 'login_timeout'])
        data["username"] = data["email"] = data["phone"] = data["wechat"] = False
        if "username" in login_types:
            data["username"] = True
        if "email" in login_types:
            data["email"] = True
        if "phone" in login_types:
            data["phone"] = True
        if "wechat" in login_types:
            data["wechat"] = True
        data["user_fail_count"] = userinfo.fail_count
        data["user_fail_range_time"] = userinfo.fail_range_time/60
        data["user_fail_ban_time"] = userinfo.fail_ban_time/60
        data["register_allow"] = bool(data["register_allow"])
        data["login_allow"] = bool(data["login_allow"])
        data["is_find_password"] = bool(data["is_find_password"])
        data["register_time"] /= 60
        data["fail_range_time"] /= 60
        data["fail_ban_time"] /= 60
        data["login_timeout"] /= 60
        return Response({
            "status": 200,
            "msg": "获取数据成功",
            "data": data
        })

    def put(self, request):
        """
        修改访问信息
        :param request: 
        :return: 
        data = {
            'username': True, 
            'email': True
            'phone': True, 
            'wechat': True,  
            
            'fail_range_time': 180L,   IP限制时间
            'fail_ban_time': 60L,   IP限制禁止时间
            'fail_count': 10L,  IP限制次数   
            
            'user_fail_count': 10L,     账号限制次数
            'user_fail_range_time': 3L,     账号限制时间
            'user_fail_ban_time':           账号限制禁止时间
            
            'register_time': 180L,  注册限制时间
            'register_count': 5L,   注册限制次数
            
            'login_allow': 1L, 是否允许登陆
            'is_find_password': 1L,     是否找回密码
            'register_allow': 1L,   是否允许注册

            'login_timeout': 登录会话超时时间
        }
        """
        agent = request.user.userinfo.agent
        visit_serializers = serializers.VisitSerializers(instance=agent, data=request.data)
        if visit_serializers.is_valid():
            visit_serializers.save()
            return Response({
                "status": 200,
                "msg": "保存设置成功",
            })
        else:
            msg = "数据错误"
            for error in visit_serializers.errors:
                msg = visit_serializers.errors[error][0]
                break
            context = {
                "status": 500,
                "msg": msg,
                "error": visit_serializers.errors
            }
            return Response(context)


class SystemSafe(APIView):
    """黑白名单添加和删除数据"""
    permission_classes = (AllowAdminWithPassword,)

    def is_ip(self, myip):
        if re.match(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$",
                    myip):
            return True
        else:
            return False

    def post(self, request):
        """添加黑白名单"""
        ip = request.data.get("ip", 0)
        is_black = request.data.get("is_black", 0)
        if not self.is_ip(ip):
            return Response({
                "status": 500,
                "msg": "IP输入错误",
                "data": {}
            })
        objs = BlackIPList.objects.filter(ip=ip)
        if objs:
            return Response({
                "status": 500,
                "msg": "此IP已经存在,请先删除",
                "data": {},
            })
        else:
            BlackIPList.objects.create(ip=ip, agent=request.user.userinfo.agent, is_black=int(is_black), start_time=timezone.now(), type=1)
            if int(is_black) == 1:
                # 黑名单，添加到缓存里
                cache.set("blackip_{0}".format(ip), True)
            if int(is_black) == 2:
                # 白名单 添加到缓存里
                cache.set("blackip_{0}".format(ip), False)
            return Response({
                "status": 200,
                "msg": "添加成功",
                "data": {}
            })

    def delete(self, request):
        """删除黑白名单"""
        id = int(request.data.get("id", 0))
        if not id:
            return Response({
                "status": 500,
                "msg": "数据传入错误",
                "data": {}
            })
        try:
            obj = BlackIPList.objects.get(id=id)
        except:
            return Response({
                "status": 500,
                "msg": "未获取到数据",
                "data": {}
            })
        else:
            # 删除缓存里的数据
            cache.delete("blackip_{0}".format(obj.ip))
            obj.delete()
            return Response({
                    "status": 200,
                    "msg": "删除成功",
                    "data": {}
            })


class SystemSafeDts(DatatableView):
    """黑白名单查询"""
    model = BlackIPList
    is_black = 0

    render_columns = [
        ("id", "id"),
        ("ip", "ip"),
    ]

    def get_initial_queryset(self):
        # 1为h黑名单 2为白名单
        self.is_black = int(self.request.data.get("is_black", 1))

        agent = self.request.user.userinfo.agent
        company = self.request.user.userinfo.company
        logoobj = BlackIPList.objects.filter(agent=agent, is_black=self.is_black)
        return logoobj

    def prepare_results(self, qs):
        """
        qs 为查询集合
        """
        data = []
        # 有 column 的话返回对应 column 值字典
        columns = self.get_columns()
        now = timezone.now()
        for item in qs:
            data_dict = {
                self.render_columns[columns.index(column)][0]: self.render_column(item, '.'.join(column.split('__')))
                for column in columns
            }
            # 白名单
            if self.is_black == 2:
                temp = {
                    "id": item.id,
                    "ip": item.ip,
                    "starttime": timezone.localtime(item.start_time).strftime("%Y-%m-%d %H:%M:%S"),
                    "endtime": '-'
                }
                data.append(temp)
            elif self.is_black == 1:
                # 黑名单
                if item.type == 1:
                    # 手动添加的黑名单，没有结束时间
                    temp = {
                        "id": item.id,
                        "ip": item.ip,
                        "starttime": timezone.localtime(item.start_time).strftime("%Y-%m-%d %H:%M:%S"),
                        "endtime": '-'
                    }
                    data.append(temp)
                elif item.type == 0:
                    # 自动添加的黑名单，有结束时间
                    fail_ban_time = self.request.user.userinfo.agent.fail_ban_time  # 禁止时间
                    now = timezone.now()
                    if item.start_time + timedelta(seconds=fail_ban_time) > now:
                        temp = {
                            "id": item.id,
                            "ip": item.ip,
                            "starttime": timezone.localtime(item.start_time).strftime("%Y-%m-%d %H:%M:%S"),
                            "endtime": timezone.localtime(item.start_time + timedelta(seconds=fail_ban_time)).strftime("%Y-%m-%d %H:%M:%S"),
                        }
                        data.append(temp)
        return data


class TwoValidation(APIView):
    """是否开启二次验证"""
    permission_classes = (AllowAdminWithPassword,)

    def get(self, request):
        """获取所有角色的二次验证信息"""
        objs = Roles.objects.filter(agent=request.user.userinfo.agent)
        role = []
        for obj in objs:
            role.append({"name": obj.name, "id": obj.id, "status": bool(obj.two_factor)})
        return Response({
            "status": 200,
            "msg": "获取数据成功",
            "data": role
        })

    def put(self, request):
        """修改角色的二次验证"""
        tablelist = request.data.get("tablelist")
        for obj in tablelist:
            if obj['name'] == '管理员':
                continue
            role = Roles.objects.get(agent=request.user.userinfo.agent, id=obj['id'])
            role.two_factor = int(obj['status'])
            role.save()
        return Response({
            "status": 200,
            "msg": "修改成功",
            "data": {}
        })
