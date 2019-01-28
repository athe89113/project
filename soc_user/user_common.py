# coding: utf-8
import base64
import datetime
import random
import time
import qrcode
from oath import accept_totp
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from hashlib import md5
from operator import itemgetter
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from django.core.cache import cache
from soc_user.models import VerifyTmp
from utils.message import send_phone_message, send_email
from common import generate_google_url


def now_plus_minutes(minutes):
    """
    现在往后 minutes 分钟
    :param minutes:
    :return:
    """
    if not isinstance(minutes, int):
        return
    return timezone.now() + timezone.timedelta(minutes=minutes)


def verify_phone_captcha(email, phone, captcha):
    """
    验证短信验证码
    :param email:
    :param phone:
    :param captcha:
    :return:
    """
    vtmp = VerifyTmp.objects.filter(type=1, email=email, phone=phone).last()
    # print(vtmp)
    if not vtmp:
        return False, '验证码错误，请重新申请'

    if vtmp.expire_time < timezone.now():
        return False, '验证码过期'

    md5_value = md5(captcha).hexdigest()
    if vtmp.captcha and md5_value != vtmp.captcha:
        return False, '验证码错误'

    return True, ''


def verify_email_link_code(email, link_code):
    """
    验证链接
    :param email:
    :param link_code:
    :return:
    """

    link_code_hash = md5(link_code).hexdigest()
    try:
        email_tmp = VerifyTmp.objects.get(email=email, link_code=link_code_hash, type=2)
    except VerifyTmp.DoesNotExist:
        return False, '验证链接错误'
    else:
        if email_tmp.expire_time <= timezone.now():
            return False, '验证链接超时'

    # 验证邮箱用户
    user = User.objects.filter(email=email)
    if not user or len(user) == 2:
        return False, '邮箱错误'

    return True, ''


def get_random_string(num_length):
    """
    返回 num_length 长度的随机数字
    """
    str_random = "%12s" % random.random()
    str_random = str_random.split('.')[1]
    list_random = random.sample(str_random, num_length)
    return ''.join(list_random)


def send_phone_captcha(phone, captcha, host='【云松】'):

    content = u'注册验证码：%s，您需在30分钟内完成验证，如非本人操作，请忽略此短信。' \
              u'勿回复此短信，详情请咨询 %s' % (captcha, host)
    print(content)
    send_phone_message(phone, content)

    return True


def send_forgot_password_mail(email, link, host='云松'):
    """
    发送找回密码邮件
    :param email:
    :param link:
    :param host:
    :return:
    """
    subject = u'找回密码邮件'
    send_from = ('donotreply@sendcloud.com', host)
    email_body = u"""<p><span style="line-height: 1.6em;">尊敬的用户，您好：</span></p>

    <p>&nbsp;&nbsp;&nbsp;&nbsp;感谢您使用%s的相关服务，请于30分钟以内点击以下链接完成密码修改：<a href="%s">%s</a></p>

    <p align="right">%s运营团队</p>
    """ % (host, link, link, host)
    send_to = email

    # send email
    print(subject, email_body, send_from, send_to)
    send_email(subject, email_body, send_from, send_to)
    return True


def dict2str(d):
    return "&".join(["{0}={1}".format(k, d[k]) for k in sorted(d.keys())])


def str2dict(s):
    d = {}
    for i in s.split("&"):
        d[i.split("=")[0]] = i.split("=")[1]
    return d


def verify_sign(pub, c_string, sign_str):
    rsakey = RSA.importKey(pub)
    verifier = Signature_pkcs1_v1_5.new(rsakey)
    digest = SHA256.new()
    digest.update(str(c_string))
    is_verify = verifier.verify(digest, base64.b64decode(sign_str))
    return is_verify


def rsa_decrypt(pem, string):
    d = RSA.importKey(pem)
    cipher = Cipher_pkcs1_v1_5.new(d)
    return cipher.decrypt(base64.b64decode(string), 1)


def now_timestamp():
    datetime_obj = datetime.datetime.now()
    return long(time.mktime(datetime_obj.timetuple()) * 1000.0 + datetime_obj.microsecond / 1000.0)


def set_login_ip(request, user):
    try:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            real_ip = x_forwarded_for.split(',')[0]
        else:
            real_ip = request.META.get('REMOTE_ADDR')
    except Exception:
        real_ip = ""
    user.userinfo.last_login_ip = real_ip
    user.userinfo.save()


class PhoneCaptchaTools(object):

    @classmethod
    def create(cls, phone, user_key=None, timeout=60*30):
        captcha = get_random_string(6)
        key = "phone_captcha_user_{0}_{}".format(user_key, phone)
        data = md5(captcha).hexdigest()
        cache.set(key, data, timeout=timeout)
        return captcha

    @classmethod
    def v_captcha(cls, phone, captcha, user_key=None):
        key = "phone_captcha_user_{0}_{}".format(user_key, phone)
        data = cache.get(key)
        if md5(captcha).hexdigest() == data:
            return True
        return False


class GoogleTwoFactorTools(object):

    @classmethod
    def create(cls, username, user_key=None, timeout=60 * 30):
        key = "google_two_factor_user_{}_{}".format(user_key, username)
        google_qrcode = generate_google_url(username)
        qr = qrcode.QRCode(version=1)
        qr.add_data(google_qrcode[3])
        qr.make()
        img = qr.make_image()
        cache.set(key, google_qrcode[0], timeout=timeout)
        return img

    @classmethod
    def v_captcha(cls, username, captcha, user_key=None):
        key = "google_two_factor_user_{}_{}".format(user_key, username)
        google_secret = cache.get(key)
        result = accept_totp(google_secret, captcha, "dec6")
        return bool(result[0]), google_secret


class EmailCaptchaTools(object):

    @classmethod
    def create(cls, email, user_key=None, timeout=60 * 60):
        captcha = get_random_string(12)
        data = md5(captcha).hexdigest()
        key = "email_captcha_user_{0}_{}".format(user_key, email)
        cache.set(key, data, timeout=timeout)
        return captcha

    @classmethod
    def v_captcha(cls, email, captcha, user_key=None):
        key = "email_captcha_user_{0}_{}".format(user_key, email)
        data = cache.get(key)
        if captcha == data:
            return True
        return False
