# coding=utf-8
from django import forms


class PaymentReturnBaseForm(forms.Form):
    """
    Alipay回调表单
    """
    # 签名类型， MD5, RSA,
    sign_type = forms.CharField()
    # 签名
    sign = forms.CharField()
    # 商户订单号
    out_trade_no = forms.CharField(max_length=64)
    # 名称
    subject = forms.CharField(max_length=256)
    # 支付类型
    payment_type = forms.CharField(max_length=4)
    # 支付宝交易号
    trade_no = forms.CharField(max_length=64)
    # 交易状态
    trade_status = forms.CharField()
    # 通知校验ID
    notify_id = forms.CharField()
    seller_id = forms.CharField()
    seller_email = forms.CharField()
    buyer_id = forms.CharField()
    is_success = forms.CharField()
    # 通知时间 yyyy-MM-dd HH:mm:ss
    notify_time = forms.CharField()
    # 通知类型 如 trade_status_sync
    notify_type = forms.CharField()
    buyer_email = forms.CharField()
    exterface = forms.CharField()
    # 交易金额
    total_fee = forms.FloatField()
    # 商品描述
    body = forms.CharField(max_length=1000)
