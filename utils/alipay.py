# coding: utf-8
# from __future__ import unicode_literals
import base64
import hashlib
import requests
import sys
import types
import urllib
import logging
from urllib import urlencode, quote
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA

logger = logging.getLogger("soc")


class Alipay(object):
    """
    支付宝api
    """

    def __init__(self, partner, private_key, seller_id, seller_email='', alipay_public_key_string=''):
        """
        初始化参
        :param partner:
        :param private_key:
        :param seller_id:
        :param seller_email:
        :param alipay_public_key_string: 支付宝公钥
        """
        self.gateway_url = "https://mapi.alipay.com/gateway.do"
        self.alipay_public_key_string = alipay_public_key_string

        self.private_key = private_key
        self.partner = partner
        self.default_params = {
            '_input_charset': 'utf-8',
            'partner': partner,
            'payment_type': '1',  # 支付类型。默认值为：1（商品购买）
        }

        if seller_id:
            self.default_params['seller_id'] = seller_id
        if seller_email:
            self.default_params['seller_email'] = seller_email
        if not seller_id and not seller_email:
            raise ParameterValueError("seller_email and seller_id must have one.")

    def _check_params(self, params, names):
        """
        检查参数
        :param params: 所有参数
        :param names: 需要检查的参数
        :return:
        """
        if not all(k in params for k in names):
            raise MissingParameter('missing parameters')

    def _encode_dict(self, params):
        """
        :param params:
        :return:
        """
        encoded = dict()
        for key, value in params.items():

            if isinstance(value, unicode):
                v = value.encode(self.default_params['_input_charset'])
            else:
                if hasattr(value, 'decode'):
                    if sys.stdin.encoding:
                        v = value.decode(sys.stdin.encoding).encode(self.default_params['_input_charset'])
                    else:
                        logger.error("{0}: {1}".format(key, value))
                        logger.error(self.default_params['_input_charset'])
                        logger.error(sys.stdin.encoding)
                        v = value
                else:
                    print("not decodes")
                    v = value
            try:
                v = quote(v)
            except (AttributeError, TypeError):
                print("error {0} {1}".format(key, value))
                pass
            encoded[key] = v
        return encoded

    def smart_str(self, s, encoding='utf-8', strings_only=False, errors='strict'):
        """
        Returns a bytestring version of 's', encoded as specified in 'encoding'.
        If strings_only is True, don't convert (some) non-string-like objects.
        """
        if strings_only and isinstance(s, (types.NoneType, int)):
            return s
        if not isinstance(s, basestring):
            try:
                return str(s)
            except UnicodeEncodeError:
                if isinstance(s, Exception):
                    # An Exception subclass containing non-ASCII data that doesn't
                    # know how to print itself properly. We shouldn't raise a
                    # further exception.
                    return ' '.join([self.smart_str(arg, encoding, strings_only, errors) for arg in s])
                return unicode(s).encode(encoding, errors)
        elif isinstance(s, unicode):
            return s.encode(encoding, errors)
        elif s and encoding != 'utf-8':
            return s.decode('utf-8', errors).encode(encoding, errors)
        else:
            return s

    def create_direct_pay_by_user_url(self, **kw):
        """
        即时到帐
            out_trade_no:
            subject:
            total_fee:
            body: 可空
            notify_url: 可空，服务器异步通知页面路径
            # return_url: 可空，页面跳转同步通知页面路径
        """
        logger.info(kw)
        self._check_params(kw, ('out_trade_no', 'subject', 'total_fee'))

        # bug?
        if not kw.get('total_fee') and not (kw.get('price') and kw.get('quantity')):
            raise ParameterValueError(
                'total_fee or (price && quantity) must have one.')
        url = self._build_url('create_direct_pay_by_user', **kw)
        return url

    def _build_url(self, service, requires=None, **kw):
        """
        创建带签名的请求地址，requires为需要包含的参数名，用于避免出现过多的参数，默认使用全部参数
        """
        params = self.default_params.copy()
        params['service'] = service
        params.update(kw)
        if requires:
            params = dict([(k, params[k]) for k in requires if k in params])

        sign_type = kw.pop("sign_type", "MD5")
        kw.pop("sign", '')

        sign_method = getattr(
            self,
            '_generate_%s_sign' % sign_type.lower(),
            None  # getattr raise AttributeError if not default provided
        )
        if sign_method is None:
            raise NotImplementedError(
                "This type '%s' of sign is not implemented yet."
                % sign_type)
        md5_sum = sign_method(params)
        params.update({
            "sign_type": sign_type,
            "sign": md5_sum
        })
        params = self._encode_dict(params)
        params = '&'.join(['%s=%s' % (k, v) for k, v in params.items()])
        return '%s?%s' % (self.gateway_url, params.encode("utf-8"))

    def _generate_md5_sign(self, params):
        """
        生成MD5签名，作为请求时的签名
        :param params:
        :return:
        """
        params = sorted(params.items())
        src = '%s%s' % ('&'.join(['%s=%s' % (key, value) for key, value in params if key not in ["sign", "sign_type"]]), self.private_key)
        hmd5 = hashlib.md5()
        src = src.encode('utf-8')
        # print(src)
        hmd5.update(src)
        return hmd5.hexdigest()

    def _generate_rsa_sign(self, params):
        """
        生成RSA签名，作为异步回调是的签名验证
        :param params:
        :return:
        """
        # 排序后的字符串
        unsigned_items = sorted(params.items)
        unsigned_string = "&".join("{}={}".format(k, v) for k, v in unsigned_items if k not in ["sign", "sign_type"])

        # 开始计算签名
        key = RSA.importKey(self.alipay_public_key_string)
        signer = PKCS1_v1_5.new(key)
        signature = signer.sign(SHA.new(unsigned_string.encode("utf8")))
        # base64 编码，转换为unicode表示并移除回车
        sign = base64.encodestring(signature).decode("utf8").replace("\n", "")
        return sign

    def verify_sign(self, params):
        """
        验证签名
        :param params: 所有回调参数
        :return:
        """
        signature = params.pop("sign")
        sign_type = params.pop("sign_type")
        if sign_type.upper() == "RSA":
            unsigned_items = sorted(params.items())
            message = "&".join("{}={}".format(k, v) for k, v in unsigned_items if k not in ["sign", "sign_type"])
            try:
                key = RSA.importKey(self.alipay_public_key_string)
                signer = PKCS1_v1_5.new(key)
                digest = SHA.new()
                digest.update(message.encode("utf8"))
                if signer.verify(digest, base64.decodestring(signature.encode("utf8"))):
                    return True
            except Exception as e:
                return False
        elif sign_type.upper() == "MD5":
            sign_method = getattr(
                self,
                '_generate_%s_sign' % sign_type.lower(),
                None  # getattr raise AttributeError if not default provided
            )
            if sign_method is None:
                return False
            md5_sum = sign_method(params)
            if md5_sum == signature:
                return True
        return False

    def verify_notify(self, notify_id):
        """
        验证是否是支付宝发来的通知
        :param notify_id:
        :return:
        """
        payload = {
            'service': 'notify_verify',
            'partner': self.partner,
            'notify_id': notify_id
        }
        result = requests.get(url=self.gateway_url, params=payload)
        return result.text == 'true'


class AlipayException(Exception):
    """Base Alipay Exception"""


class MissingParameter(AlipayException):
    """Raised when the create payment url process is missing some
    parameters needed to continue"""


class ParameterValueError(AlipayException):
    """Raised when parameter value is incorrect"""


class TokenAuthorizationError(AlipayException):
    """The error occurred when getting token """


class SignVerifyError(AlipayException):
    """Sign verification error"""


if __name__ == "__main__":
    # 测试
    alipay_partner = '2088xxxxxxxxxxx'  # alipay return number
    alipay_private_key = '99hwjxxxxxxxxxxxxxxxxxxxxx'  # alipay return key
    alipay_seller_id = '2088xxxxxxxxxxx'
    alipay_seller_email = 'boss@qssec.com'

    alipay = Alipay(
        partner=alipay_partner,
        private_key=alipay_private_key,
        seller_id=alipay_seller_id,
        seller_email=alipay_seller_email
    )

    pay_url = 'https://www.qssec.com'
    alipay_dict = {
        'notify_url': '%s/api/alipay/return_async/' % str(pay_url),
        'sign_type': 'MD5',
        'out_trade_no': "20161216192609234533",
        'subject': "ss",
        'total_fee': '0.01',
        'body': "qiuwh_test",
        'anti_phishing_key': 'AABBCDDEG',
    }

    print(alipay.create_direct_pay_by_user_url(**alipay_dict))
