# coding=utf-8
# from __future__ import unicode_literals
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import os
import socket
import struct
import re
import xlwt
import time
import telnetlib
import logging
import urllib2
import requests
import math
import copy
import json
import datetime
import ssl
import qrcode
import uuid
import pytz
from functools import wraps
from requests.auth import HTTPBasicAuth
from urlparse import urlparse
from django.db.models import Sum
from base64 import b32encode
from binascii import b2a_hex, a2b_hex
from binascii import hexlify, unhexlify
from urllib import urlencode
from Crypto.Cipher import AES
from django.conf import settings
from django.core.mail.message import EmailMultiAlternatives
from django.core.mail import send_mail
from django.utils import timezone
from django.db.models import Count, Max
from django.core.cache import cache
from rest_framework.response import Response
from elasticsearch import Elasticsearch
from elasticsearch import helpers

# Secure random generators
import random
from django.core.mail.backends.smtp import EmailBackend

try:
    random = random.SystemRandom()
except:
    pass
try:
    from os import urandom
except:
    urandom = None

topHostPostfix = (
    '.com', '.la', '.io', '.co', '.info', '.net', '.org', '.me', '.mobi', '.us', '.biz', '.xxx', '.ca', '.co.jp',
    '.com.cn', '.net.cn', '.org.cn', '.mx', '.tv', '.ws', '.ag', '.com.ag', '.net.ag', '.org.ag', '.am', '.asia', '.at',
    '.be', '.com.br', '.net.br', '.bz', '.com.bz', '.net.bz', '.cc', '.com.co', '.net.co', '.nom.co', '.de', '.es',
    '.com.es', '.nom.es', '.org.es', '.eu', '.fm', '.fr', '.gs', '.in', '.co.in', '.firm.in', '.gen.in', '.ind.in',
    '.net.in', '.org.in', '.it', '.jobs', '.jp', '.ms', '.com.mx', '.nl', '.nu', '.co.nz', '.net.nz', '.org.nz', '.se',
    '.tc', '.tk', '.tw', '.com.tw', '.idv.tw', '.org.tw', '.hk', '.co.uk', '.me.uk', '.org.uk', '.vg', '.cn', '.name'
)
logger = logging.getLogger("soc")
console_logger = logging.getLogger("console")


def _random_seed(rawsize=10):
    """ Generates a random seed, which is hex encoded. """
    if urandom:
        randstr = urandom(rawsize)
    else:
        randstr = ''.join([chr(random.randint(0, 255)) for i in range(rawsize)])
    return hexlify(randstr)


def _get_google_url(hex_secret, hostname=None):
    """
    :param hex_secret:
    :param hostname:
    :return:
    """
    # Note: Google uses base32 for it's encoding rather than hex.
    b32secret = b32encode(unhexlify(hex_secret))
    if not hostname:
        hostname = socket.gethostname()
    data = "otpauth://totp/%(hostname)s?secret=%(secret)s&issuer=%(issuer)s" % {
        "hostname": hostname,
        "secret": b32secret,
        "issuer": settings.QSSEC_SOC,
    }
    url = "https://chart.googleapis.com/chart?" + urlencode({
        "chs": "200x200",
        "chld": "M|0",
        "cht": "qr",
        "chl": data
    })
    return b32secret, url, data


def generate_google_url(hostname=None):
    """
    生成google二次验证
    :param hostname: 可以是用户名
    :return:
        hex_secret: 随机种子(保存到数据库中作为认证)
        b32secret: 安全密钥(添加二次验证时输入用)
        url: 二维码url
        otpauth: otpauth://TYPE/LABEL?PARAMETERS
    """
    """生成google二次验证"""
    hex_secret = _random_seed()
    return (hex_secret,) + _get_google_url(hex_secret, hostname=hostname)


class Prpcrypt():
    def __init__(self, key):
        self.key = key
        self.mode = AES.MODE_ECB

    # 加密函数，如果text不足16位就用空格补足为16位，
    # 如果大于16当时不是16的倍数，那就补足为16的倍数。以‘\0’补足。
    def encrypt(self, text):
        cryptor = AES.new(self.key, self.mode)
        # 这里密钥key 长度必须为16（AES-128）,
        length = 16
        count = len(text)
        if count < length:
            add = (length - count)
            text = text + ('\0' * add)
        elif count > length:
            add = (length - (count % length))
            text = text + ('\0' * add)
        self.ciphertext = cryptor.encrypt(text)
        # 统一把加密后的字符串转化为16进制字符串
        return b2a_hex(self.ciphertext)
        # 解密后，去掉补足的空格用strip() 去掉

    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, )
        plain_text = cryptor.decrypt(a2b_hex(text))
        return plain_text.rstrip('\0')


class SendEmail(object):
    """ 发送邮件 """

    def __init__(self, url):
        self.url = url

    def send_email(self, contact, content):
        # 不同于登录SendCloud站点的帐号，您需要登录后台创建发信域名，获得对应发信域名下的帐号和密码才可以进行邮件的发送。
        params = {"api_user": settings.API_USER,
                  "api_key": settings.API_KEY,
                  "to": contact,
                  "from": settings.SEND_FROM,
                  "fromname": settings.SEND_FROM_NAME,
                  "subject": '报警',
                  "html": content,
                  }
        requests.post(self.url, data=params)


def Ip2Int(ip):
    return struct.unpack("!I", socket.inet_aton(ip))[0]


def Int2Ip(i):
    return socket.inet_ntoa(struct.pack("!I", i))


def cidr2mask(prefix):
    # 8 to 255.0.0.0
    return socket.inet_ntoa(struct.pack(">I",
                                        (0xffffffff << (32 - prefix))
                                        & 0xffffffff))


def mask2cidr(prefix):
    # 255.0.0.0 to 8
    if not is_valid_mask(prefix):
        context = {
            "status": 500,
            "msg": u"子网掩码错误",
            "error": u"子网掩码错误"
        }
        return Response(context)
    return sum(bin(int(i)).count('1')
               for i in prefix.split('.'))


def Int2net(data_list):
    """把int值的ip、mask、gateway转换成字符串形式"""
    for item in data_list:
        for k, v in item.items():
            if k == 'mask':
                item[k] = cidr2mask(int(v))
            elif k in ('ip', 'gateway'):
                item[k] = Int2Ip(int(v))
    return data_list


def modify_values(data_values, key_model, ip_flag=None):
    """根据 key_model 对应模型实例化 data_values 中的ID, 可选字段实例化
    key_model:
        key: [Model, (name1, name2, )]
        或者
        key: Model
    """
    for item in list(data_values):
        for key, model in key_model.items():
            model_list = model if type(model) is list else [model]
            if (key + "_id") in item.keys():
                obj_id = item.pop('%s_id' % key)
                if len(model_list) > 1:
                    obj_values = model_list[0].objects.filter(id=obj_id).values(*model_list[1])
                else:
                    obj_values = model_list[0].objects.filter(id=obj_id).values()
                if ip_flag and key in ip_flag:
                    obj_values = Int2net(obj_values)
                if obj_values:
                    item[key] = obj_values[0]
                else:
                    item[key] = {}
    return data_values


def _chk_ipaddr(ipaddr):
    IP_PATTERN = '^((0|[1-9]\d?|[0-1]\d{2}|2[0-4]\d|25[0-5])\.){3}(0|[1-9]\d?|[0-1]\d{2}|2[0-4]\d|25[0-5])$'
    if not ipaddr:
        return False

    ipcheck = re.compile(IP_PATTERN, re.I)
    return True if ipcheck.match(ipaddr) else False


def chk_ipaddr(ip):
    return _chk_ipaddr(ip)


def is_valid_mask(mask):
    """
    Return the validity of the mask

    >>> is_valid_mask("255.255.255.0")
    True
    >>> is_valid_mask("192.168.0")
    False
    >>> is_valid_mask("test")
    False
    >>> is_valid_mask("0.0.0.0")
    False
    >>> is_valid_mask("255.255.255.255")
    True

    etc.
    """
    try:
        if _chk_ipaddr(mask):
            mask_num, = struct.unpack("!I", socket.inet_aton(mask))
            if mask_num == 0:
                return False

            # get inverted
            mask_num = ~mask_num + 1
            binstr = bin(mask_num)[3:]
            # convert to positive integer
            binstr = '0b%s' % ''.join('1' if b == '0' else '0' for b in binstr)
            mask_num = int(binstr, 2) + 1
            # check 2^n
            return mask_num & (mask_num - 1) == 0
        return False
    except Exception:
        return False


def excel_export(filename, labels, headers, values):
    wb = xlwt.Workbook(style_compression=2, encoding='utf-8')
    ws = wb.add_sheet('data')

    col = 0
    for item in labels:
        ws.write(0, col, item)
        col += 1

    row = 1
    col = 0
    for item in values:
        for header in headers:
            if not header:
                ws.write(row, col, "")
            else:
                if type(item) is dict:
                    value = item.get(header, "")
                else:
                    value = getattr(item, header, "")
                if type(value) == datetime.date:
                    ws.write(
                        row, col, value,
                        xlwt.easyxf(num_format_str='YYYY-MM-DD'))
                else:
                    ws.write(row, col, value)
            col += 1
        col = 0
        row += 1

    file_path = os.path.join('download')
    save_path = os.path.join(settings.MEDIA_ROOT, file_path)
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    wb.save(os.path.join(save_path.encode("utf-8"), filename.encode("utf-8")))
    return os.path.join('media', file_path, filename)


send_to_list = ('qiuwh@qssec.com', 'wuzx@qssec.com', 'guoyang@qssec.com', 'caokq@qssec.com')


def SendMail(title, content):
    send_mail('SOC: ' + title, content, 'alarm@qssec.com',
              send_to_list, fail_silently=False)


def notify_administrator(content, title="", flag=0):
    """发送邮件通知管理员"""
    # from django.core.mail.message import EmailMultiAlternatives
    env = getattr(settings, 'ENV', 'None')
    if flag == 1:
        notify_email = settings.NOTIFY_WORKER_ORDER_EMAIL
        title = u'[' + env + u' 系统工单处理通知]'
    elif flag == 2:
        notify_email = settings.ASIC_ERROR_EMAIL
        title = u'[' + env + u' ASIC错误]'
    else:
        notify_email = settings.ADMINISTRATORS
        if not title:
            title = u'[' + env + u']'
        else:
            title = u'[' + env + u' ' + unicode(title) + u']'
    html_content = unicode(content)
    title = unicode(title)
    # mail = EmailMultiAlternatives(title,
    #                               html_content,
    #                               settings.SERVER_EMAIL,
    #                               notify_email)
    # mail.attach_alternative(html_content, "text/html")
    # mail.send()
    send_mail(title, html_content, settings.SERVER_EMAIL, notify_email, fail_silently=False)


def send_message(title, content, user_id, type=0, priority=3):
    """发送消息通知
    默认消息类型为通知, 等级为一般
    title: 消息标题
    content: 消息内容
    user_id: 发送给消息的人
    type: 消息类型: 0: 其他消息, 1: 安全扫描, 2: 监控告警
    priority: 消息等级: 1非常紧急,2紧急,3一般,4不紧急
    """

    new_message = ModelMessage.objects.create(
        title=title,
        content=content,
        type=type,
        priority=priority,
        is_read=0,
        user_id=user_id
    )
    if new_message:
        return new_message.id
    else:
        return {'result': 'failed'}


def get_data_zmq(key):
    import gevent
    from gevent_zeromq import zmq
    context = zmq.Context()
    # address = "tcp://" + ip + ":" + port
    # address = "tcp://139.217.7.23:4869"
    address = "tcp://192.168.31.201:4869"

    def client(key):
        client_socket = context.socket(zmq.REQ)
        client_socket.connect(address)

        client_socket.send(key.encode("utf-8"))
        # print "data"
        data = client_socket.recv()
        # client_socket.close()
        return data

    client = gevent.spawn(client, key)
    gevent.joinall([client], timeout=1)
    # context.term()
    if client.value:
        return client.value
    else:
        return ""


def soc_log(category, text):
    """
    记录日志装饰器
    新版本改为中间件记录日志，所以废弃此装饰器
    若有需要 使用下面soc_log_old装饰器
    """
    import functools
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            res = func(self, *args, **kwargs)
            return res

        return wrapper

    return decorator


def soc_log_old(category, text):
    """记录日志"""

    import functools

    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            # print category.
            # print '%s %s():' % (text, func.__name__)
            level = "info"
            if func.__name__ == "delete():":
                level = "warning"
            info = text
            MoldelSocLog.objects.create(category=category,
                                        level=level,
                                        info=info,
                                        user=self.request.user)
            request = args[0]
            res = func(self, *args, **kwargs)
            # 记录文件日志
            if res.data.has_key('status'):
                if 'msg' in res.data:
                    res_data = res.data['msg']
                elif 'error' in res.data:
                    res_data = res.data['error']
                else:
                    res_data = '未返回data'
                if res.data['status'] == 200:
                    logger.info("{} {} {} 操作成功:{}".format(category, text, request.path_info, res_data))
                else:
                    logger.error("{} {} {} 操作失败:{}".format(category, text, request.path_info, res_data))
            return res

        return wrapper

    return decorator


def active_required(func):
    """检查代理商是否激活"""
    import functools

    @functools.wraps(func)
    def decorator(self, request, *args, **kwargs):
        active = request.user.userinfo.agent.status
        if not active:
            context = {
                "status": 200,
                "msg": u"Agent没有激活",
                "data": []
            }
            return Response(context)
        return func(self, request, *args, **kwargs)

    return decorator


def get_current_agent(request):
    """
    获取当前代理商,如果是轻松管理员,则会根据 agent_id 对应代理商
    """

    agent_now = request.user.userinfo.agent
    # if agent_now.is_super_admin:
    # if request.user.userinfo.role_type == 1:
    #     agent_id = request.DATA.get("agent_id")
    #     agent_now = ModelAgent.objects.get(id=agent_id)
    return agent_now


def del_add(list_old, list_new):
    """两个列表的差
    返回 第一个与第二个的差， 第二个与第一个的差
    del_add([1, 2], [2, 3,4])
    => [1], [3, 4]
    """
    old_minus_new = list(set(list_old).difference(set(list_new)))
    new_minus_old = list(set(list_new).difference(set(list_old)))
    return old_minus_new, new_minus_old


def telnet(host, user, password):
    # HOST = '192.168.31.231'
    # user = 'admin'
    # password = 'Admin@1234'
    tn = telnetlib.Telnet(host)
    tn.expect([re.compile(b"Username:"), ])
    tn.write(user + "\n")
    tn.expect([re.compile(b"Password:"), ])
    tn.write(password + "\n")
    time.sleep(.1)
    tn.read_until("<HWJC.HL-DDoS.SDA>")
    tn.write("display clock\n")
    tn.read_until("display clock")
    time.sleep(.1)
    data = tn.read_very_eager()
    tn.close()
    return data


def send_notify(message_type, contact, content):
    """ 发邮件 """
    if message_type == 1:
        import requests
        url = "https://sendcloud.sohu.com/webapi/mail.send.xml"
        send_from, send_from_name = ('donotreply@sendcloud.com', '青松抗D')
        # 不同于登录SendCloud站点的帐号，您需要登录后台创建发信域名，获得对应发信域名下的帐号和密码才可以进行邮件的发送。
        params = {"api_user": 'postmaster@qstest.sendcloud.org',
                  "api_key": 'a9CipOZuIthB41bs',
                  "to": contact,
                  "from": send_from,
                  "fromname": send_from_name,
                  "subject": '报警',
                  "html": content,
                  }
        requests.post(url, data=params)
    elif message_type == 2:
        import requests, json
        # url = "https://sendcloud.sohu.com/webapi/mail.send.xml"
        url = "http://sendcloud.sohu.com/webapi/mail.send_template.json"
        send_from, send_from_name = ('donotreply@sendcloud.com', '青松抗D')
        sub_vars = {
            'to': ['to1@domain.com', 'to2@domain.com'],
            'sub': {
                '%name%': ['user1', 'user2'],
            }
        }
        params = {"api_user": 'postmaster@qstest.sendcloud.org',
                  "api_key": 'a9CipOZuIthB41bs',
                  "from": send_from,
                  "fromname": send_from_name,
                  "subject": '报警',
                  "template_invoke_name": "test_template",
                  "substitution_vars": json.dumps(sub_vars),
                  }
        requests.post(url, data=params)


def send_phone_message(phone, content, url=settings.SEND_PHONE_MESSAGE_URL, user=settings.CORP_ID,
                       pwd=settings.CORP_PWD):
    """发送短信"""
    # url = settings.SEND_PHONE_MESSAGE_URL % (settings.CORP_ID, urllib2.quote(settings.CORP_PWD), phone, content)
    url = url % (user, urllib2.quote(pwd), phone, content)
    # encoding gb2312
    url = url.encode('gb2312')
    status = send_http_request(urllib2.quote(url, safe="%/:=&?~#+!$,;'@()*[]"))
    try:
        code = status.split('<code>')[1].split('</code>')[0]
        if code == '03':
            return {"result": 'ok'}
        return {"result": "error", "error": "发送失败"}
    except Exception, e:
        return {"result": "error", "error": str(status)}


def send_http_request(url):
    if not url:
        return 'error'
    req = urllib2.Request(url)
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.151 Safari/534.16')
    try:
        response = urllib2.urlopen(req, timeout=3)
    except Exception, e:
        return e
    result = response.read()
    return result


def send_sohu_email(title, content, url, api_user, api_key, to):
    """
    :param title: 标题
    :param content:  内容
    :param url: 发送邮箱的url
    :param api_user:  用户名
    :param api_key:  密码
    :param to:  收件人 字符串 
    :return: 
    """
    send_from, send_from_name = ('donotreply@sendcloud.com', 'alarm')
    params = {"api_user": api_user,
              "api_key": api_key,
              "to": to,
              "from": send_from,
              "fromname": send_from_name,
              "subject": title,
              "html": content,
              }
    status = requests.post(url, data=params)
    return status


def send_msg(msg_type, to, content, agent=None, **params):
    """
    :param msg_type: 发送类型 必需
    :param to: 接受者 必需，格式根据发送类型不同而不同
                        当 msg_type为 1 的时候,为有一个邮件地址
                        当 msg_type为 2 的时候,为一个手机号码
                        当 msg_type为 3 的时候，为一个user_id
    :param agent 代理商 Agent 对象 或 Agent 的 id
    :param content: 发送内容 必需
    :param params: 关键字参数，具体参数根据发送类型不同而不同
                    当 msg_type为 1 的时候,关键字参数为 title,必需
                    当 msg_type为 2 的时候,关键字参数不需要
                    当 msg_type为 3 的时候，关键字参数包括 title 消息标题 必需,
                    type: 消息类型: 0通知,1扫描,2漏洞,3工单回复  可选,
                    priority 消息等级: 1非常紧急,2紧急,3一般,4不紧急 可选

    :return:
    """
    if isinstance(agent, int):
        agent_id = agent
    else:
        agent_id = agent.id
    # 发搜狐邮件
    if msg_type == 4:
        title = params.get('title', u"通知")
        Email = SendEmailCloud(target_id=None, agent_id=agent_id, to=to, content={"title": title, 'content': content})
        return Email.send()
    # 发短信
    elif msg_type == 2:

        # def __init__(self, target_id, content, agent_id, to='', sender_type_id=0, api='', api_user='', api_pwd=''):
        title = params.get('title', u"通知")
        Msg = SendMessage(target_id=None, content={"content": title + " " + content}, to=to, agent_id=agent_id)
        return Msg.send()
    # 发站内消息
    elif msg_type == 3:
        title = params.get('title', u"通知")
        # def __init__(self, type, target_id, agent_id, content):
        SendStationMessage(type=0, target_id=to, agent_id=0,
                           content={"title": title, 'content': content, 'priority': 3})
        return SendStationMessage.send()

    # alarm 服务发送 发送smtp邮件
    elif msg_type == 1:
        title = params.get('title', u"通知")
        Email = SendEmailSMTP(target_id=None, agent_id=agent_id, to=to, content={"title": title, "content": content})
        return Email.send()
    else:
        pass


def soc_send_email(title, content, host, username, password, use_tls, use_ssl, send_address, to):
    """
    :param title:  标题
    :param content:     内容
    :param host:    服务器
    :param username:    用户名
    :param password:    密码
    :param use_tls:     tls加密
    :param use_ssl:     ssl加密
    :param send_address:    发件人 一般和用户名一致
    :param to:  收件人
    :return: 
    构造一个smtp 然后发送邮件
    返回的status不为0则为成功
    """
    try:
        smtp = EmailBackend(host=host, username=username,
                            password=password, use_ssl=bool(int(use_ssl)), use_tls=bool(int(use_tls)))
        status = send_mail(title, content, send_address,
                           [to], fail_silently=False, auth_user=username,
                           auth_password=password, connection=smtp)
        return status, 'ok'
    except Exception, e:
        return 0, str(e)


def localtime_to_timestamp(local_time):
    """
    当地时间字符转为时间戳
    :param local_time: string, 当地时间 xxxx-xx-xx xx:xx:xx
    :return:
    """
    # local_time_obj = timezone.datetime.strptime(local_time, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.get_current_timezone())
    # time.mktime(local_time_obj.timetuple())
    # "2017-11-28 15:18:52" => 1511853532.0
    datetime_format = '%Y-%m-%d %H:%M:%S'
    local_time = timezone.get_current_timezone().localize(datetime.datetime.strptime(local_time, datetime_format))
    utc_time = local_time.astimezone(pytz.utc)
    timestamp = int(time.mktime(time.strptime(utc_time.strftime(datetime_format), datetime_format))) - time.timezone
    return timestamp


def timestamp_to_localtime(timestamp, time_format='%Y-%m-%d %H:%M:%S'):
    """
    timestamp to localtime format xxxx-xx-xx xx:xx:xx
    :param timestamp:
    :param time_format: time format
    :return:
    """
    return timezone.datetime.fromtimestamp(timestamp).strftime(time_format)


def get_minute_time(start_time, end_time):
    """将时间转换成时间戳，并返回时间是每一分钟的时间戳列表
    """
    if not start_time or not end_time:
        time_now = timezone.now()
        time_24hr_ago = timezone.now() - timezone.timedelta(hours=24)

        start = timezone.localtime(time_24hr_ago)
        end = timezone.localtime(time_now)
    else:
        start = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        end = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')

    start_date = int(time.mktime(start.timetuple()))
    end_date = int(time.mktime(end.timetuple()))
    if start_date > end_date:
        context = {
            'status': 500,
            'msg': u'时间范围不正确',
            'error': u'时间范围不正确',
        }
        return Response(context)
    times = []
    time_interval = (end_date - start_date) / 60
    for t in range(time_interval):
        time_now = start_date + t * 60
        times.append(time_now)

    return start_date, end_date, times


def soc_cache(timeout=60 * 60, key='url', level='company'):
    """soc 缓存装饰器
    :timeout 缓存超时时间 单位秒 默认 一小时
    :key     缓存的key，       默认为当前url
    :level   缓存级别，agent，company，user， 默认为company级别
    """

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kw):
            """缓存"""
            request = args[1]
            if key == 'url':
                first_key = request.path.replace('/', '_')
            else:
                first_key = key
            first_key = 'soc_cache' + first_key
            agent_id = int(request.user.userinfo.agent_id)
            company_id = int(request.user.userinfo.company_id or 0)
            if level == 'user':
                second_key = 'user_{0}'.format(int(request.user.id)),
            elif level == 'company':
                second_key = 'agent_{}_company_{}'.format(agent_id, company_id),
            elif level == 'agent':
                second_key = 'agent_{0}'.format(agent_id),
            else:
                second_key = level
            cache_key = '{0}_{1}'.format(first_key, str(second_key[0]))
            data = cache.get(cache_key)
            console_logger.debug('soc_cache 获取缓存 key: {0}'.format(cache_key))
            if not data:
                console_logger.debug('soc_cache 未命中缓存 key: {0}'.format(cache_key))
                rsp = func(*args, **kw)
                data = rsp.data
                cache.add(cache_key, data, timeout)
            return Response(data=data)

        return wrapper

    return decorator


def v_rack(rack_id, u_location, u_num, exclude=None):
    """
    验证机柜位置信息
    """
    rack = ModelRack.objects.get(id=rack_id)
    if not u_location:
        return False
    if u_location + u_num > rack.u_num + 1:
        return False

    result = [0] * rack.u_num

    for server in rack.server_set.all():
        result[server.u_location - 1] = 1
        if server.u_num > 1:
            for i in range(server.u_num):
                result[server.u_location + i - 1] = 1

    for server in rack.netdevice_set.all():
        result[server.u_location - 1] = 1
        if server.u_num > 1:
            for i in range(server.u_num):
                result[server.u_location + i - 1] = 1

    if exclude:
        for i in range(exclude[1]):
            result[exclude[0] + i - 1] = 0

    try:
        blank = result[u_location - 1:u_location + u_num - 1]
    except IndexError:
        return False
    else:
        if 1 in blank:
            return False
    return True


def soc_system_log(category, info, request, level='info', url=''):
    role = {1: "青松", 2: "管理员", 3: '企业用户'}.get(request.user.userinfo.role_type)
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    agent = request.user.userinfo.agent
    company = request.user.userinfo.company
    MoldelSocLog.objects.create(category=category, role=role, level=level, info=info, user=request.user,
                                logtype=1, agent=agent, ip=ip, company=company, url=url)


def auth_company(func):
    """如果是公司用户，返回空数据"""

    def wrapper(obj, request, *args, **kw):
        print(request, 'request')
        if request.user.userinfo.company:
            return Response(
                {
                    "status": 200,
                    "msg": "获取成功",
                    "data": {}
                }
            )
        return func(*args, **kw)

    return wrapper


def get_next_scan_time(start_date, time_s, period_type, days=1, months=None, next_scan_time=None, time_now=None):
    """
    获取下次执行的时间
    type: 1 immediately,2 runonce, 3 daily, 4 weekly, 5 monthly, 6 quarterly， 7 yearly
    """

    if time_now:
        tn = time_now
    else:
        tn = timezone.localtime(timezone.now())
    time_now = timezone.datetime(tn.year, tn.month, tn.day, tn.hour, tn.minute, tn.second)

    start_date = timezone.datetime(start_date.year, start_date.month, start_date.day)

    # 到此start_date应该为小于time_now最近的一次扫描时间, 或者是未来的开始时间
    hour, minute = time_s.hour, time_s.minute
    year = start_date.year
    month = start_date.month
    day = start_date.day
    dayth = start_date.isoweekday()  # 周日为0开始算
    start_time = timezone.datetime(year, month, day, hour, minute)

    if period_type == 1:
        # 立刻执行
        return time_now
    elif period_type == 2:
        if start_time < time_now:
            year = start_date.year + 99
            return timezone.datetime(year, month, day, hour, minute)
        return start_time
    else:
        if next_scan_time:
            next_scan_time = timezone.localtime(next_scan_time)
            next_scan_time = timezone.datetime(next_scan_time.year, next_scan_time.month, next_scan_time.day,
                                               next_scan_time.hour, next_scan_time.minute)
            if next_scan_time >= time_now:
                # 还没到下次扫描时间
                return next_scan_time

            # 从上一次的扫描时间开始算下一次的扫描时间
            # next_scan_time < time_now
            start_time = next_scan_time
            year = start_time.year
            month = start_time.month
            day = start_time.day
            hour = start_time.hour
            minute = start_time.minute
            dayth = start_time.isoweekday()
        if period_type == 3:
            # 每[days]天
            while start_time <= time_now:
                start_time = start_time + timezone.timedelta(days=days)
            return start_time
        else:
            if start_time < time_now:
                start_time = time_now
                year = start_time.year
                month = start_time.month
                day = start_time.day
                dayth = start_time.isoweekday()

            if period_type == 4:
                # 每周
                if next_scan_time:
                    if dayth >= days:
                        delta = 7 - (dayth - days)
                    else:
                        delta = days - dayth
                else:
                    if dayth > days:
                        delta = 7 - (dayth - days)
                    else:
                        delta = days - dayth
                return timezone.datetime(year, month, day, hour, minute) + timezone.timedelta(days=delta)
            elif period_type == 5:
                # 每月执行
                if next_scan_time:
                    if day >= days:
                        day = days
                        month += 1
                        if month == 13:
                            month = 1
                            year += 1
                    else:
                        day = days
                else:
                    if day > days:
                        day = days
                        month += 1
                        if month == 13:
                            month = 1
                            year += 1
                    else:
                        day = days
                return timezone.datetime(year, month, day, hour, minute)

            # 按季度
            elif period_type == 6:
                # 第一月 则 + 0 第二月 + 1
                months -= 1
                year = time_now.year
                # 取一下季度                
                month = time_now.month + (3 - time_now.month % 3)
                # 判断是否超过当前季度， 为超过则当前季度还能执行一次
                if time_now.month + months < month:
                    month = time_now.month + months
                else:
                    if month > 12:
                        month = 1
                        year += 1
                    # 加上 第X月 第一月 则 + 0 第二月 + 1
                    month += months
                return timezone.datetime(year, month, day, hour, minute)

            # 按年度
            elif period_type == 7:
                # 第一月 则 + 0 第二月 + 1
                # months -= 1
                year = time_now.year
                # 取一下季度                
                if time_now.month + months < 13:
                    year = time_now.year
                else:
                    year = time_now.year + 1
                return timezone.datetime(year, month, day, hour, minute)


def get_hour_min(integer):
    return integer // 60, integer % 60


def formatted_hour_min(integer):
    minute = str(integer % 60)
    minute = "0" + minute if len(minute) == 1 else minute
    hour = str(integer // 60)
    hour = "0" + hour if len(hour) == 1 else hour
    return hour + ":" + minute


def add_doc_list(doc_list):
    # 数据的批量写入
    es_hosts = getattr(settings, "ELASTICSEARCH_HOSTS", ["http://127.0.0.1:9200/"])
    es = Elasticsearch(hosts=es_hosts)

    while len(doc_list) > 0:
        if len(doc_list) > 500:
            res = helpers.bulk(es, doc_list[0:500], request_timeout=100)
            # TODO
            # logger.info(res[0])
            del doc_list[0:500]
        else:
            res = helpers.bulk(es, doc_list, request_timeout=100)
            # TODO
            # logger.info(res[0])
            doc_list = []


if __name__ == '__main__':
    # data = get_data_zmq("222.111.33.99")
    # print data
    # print dev_ping("127.0.0.1")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "soc.settings")
    import django

    django.setup()
    notify_administrator(content=u"测试", title=u"内容")


def get_utz_time(datetime_obj):
    local_time = timezone.get_current_timezone().localize(datetime_obj)
    return local_time.astimezone(pytz.utc)


def is_mac(mac):
    """判断是否是有冒号分隔符的mac地址"""
    if not mac:
        return False
    if len(mac) != 17:
        return False
    macs = mac.split(":")
    if len(macs) != 6:
        return False
    for m in macs:
        if len(m) != 2:
            return False
    return True


def ip2num(ip):
    ip = [int(x) for x in ip.split('.')]
    return ip[0] << 24 | ip[1] << 16 | ip[2] << 8 | ip[3]


def num2ip(num):
    return '%s.%s.%s.%s' % (
        (num & 0xff000000) >> 24,
        (num & 0x00ff0000) >> 16,
        (num & 0x0000ff00) >> 8,
        num & 0x000000ff)


# 获取IP段所有IP
# 格式: '192.168.1.2-192.168.2.1'
def get_ip_list(ip):
    start, end = [ip2num(x) for x in ip.split('-')]
    return [num2ip(num) for num in range(start, end + 1) if num & 0xff]
