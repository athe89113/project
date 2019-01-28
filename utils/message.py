# coding: utf-8
"""
消息处理
"""
import re
import urllib2
import logging
import requests
from django.conf import settings
from django.core.mail import send_mail
logger = logging.getLogger('soc_message')


TELCOMM = [133, 153, 180, 181, 189, 177, 173, 149]
CMCC = [130, 131, 132, 155, 156, 145, 148, 185, 186, 176, 175]
# 1340-1348
MOBILE = range(1340, 1349, 1) + [135, 136, 137, 138, 139, 150,
                                 151, 152, 157, 158, 159, 182, 183, 184, 187, 188, 147, 178]
# 170[1700/1701/1702(电信)、1703/1705/1706(移动)、1704/1707/1708/1709(联通)]、171（联通）
VIRTUAL = [170, 171]
PHONE_PREFIX = map(str, TELCOMM + CMCC + MOBILE + VIRTUAL)


# 与消息有关的工具，发短信，邮件等

def send_http_request(url):
    if not url:
        return 'error'
    req = urllib2.Request(url)
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.151 Safari/534.16')
    try:
        response = urllib2.urlopen(req, timeout=3)
    except Exception as e:
        return e
    result = response.read()
    return result


def send_phone_message(phone, content):
    """发送短信"""
    url = settings.SEND_PHONE_MESSAGE_URL % (
        settings.CORP_ID, urllib2.quote(settings.CORP_PWD), phone, content)
    # encoding gb2312
    url = url.encode('gb2312')
    result = send_http_request(urllib2.quote(url, safe="%/:=&?~#+!$,;'@()*[]"))
    logger.info(phone)
    logger.info(result)
    return True


def send_email(subject, body, send_from, send_to):
    """
    返回：发送返回信息
    """

    url = "https://sendcloud.sohu.com/webapi/mail.send.xml"
    if isinstance(send_from, (list, tuple)):
        if len(send_from) >= 2:
            sendfrom = send_from[0]
            sendfrom_name = send_from[1]
        else:
            return 'false'
    else:
        return 'false'
    # send_from, send_from_name = ('donotreply@sendcloud.com', 'alarm')

    # 不同于登录SendCloud站点的帐号，您需要登录后台创建发信域名，获得对应发信域名下的帐号和密码才可以进行邮件的发送。
    params = {"api_user": settings.SOHU_EMAIL_API_USER,
              "api_key": settings.SOHU_EMAIL_API_KEY,
              "to": send_to,
              "from": sendfrom,
              "fromname": sendfrom_name,
              "subject": subject,
              "html": body,
              }
    result = requests.post(url, data=params)
    return result


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
    send_mail(title, html_content, settings.SERVER_EMAIL,
              notify_email, fail_silently=False)


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