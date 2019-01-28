# coding: utf-8
"""序列化相关
"""
from __future__ import unicode_literals


def generate_error_msg(msg):
    """error msg"""
    error_messages = {
        'required': '{msg}不能为空'.format(msg=msg),
        'invalid': '{msg}错误'.format(msg=msg),
        'blank': '{msg}不能为空'.format(msg=msg),
        'null': '{msg}不能为空'.format(msg=msg),
        'max_length': '{0}不能长度不能超过{1}'.format(msg, '{max_length}'),
        'min_length': '{0}不能长度不能少于{1}'.format(msg, '{min_length}'),
        'min_value': '{0}最小值不能小于{1}'.format(msg, '{min_value}'),
        'max_value': '{0}最大值不能大过{1}'.format(msg, '{max_value}'),
    }
    return error_messages
