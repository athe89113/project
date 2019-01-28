# coding: utf-8
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers


class IPField(serializers.CharField):
    """IP Field"""

    def __init__(self, **kwargs):
        super(IPField, self).__init__(**kwargs)

    @classmethod
    def run_valid(cls, data):
        """检查IP正确性"""
        q = data.split('.')
        return len(q) == 4 and len(filter(lambda x: x >= 0 and x <= 255,
                                          map(int, filter(lambda x: x.isdigit(), q)))) == 4

    def run_validation(self, data=''):
        # Test for the empty string here so that it does not get validated,
        # and so that subclasses do not need to handle it explicitly
        # inside the `to_internal_value()` method.

        # 检测符不符合字符串
        super(IPField, self).run_validation(data)

        if data:
            if not self.run_valid(data):
                self.fail('invalid')
        return data


class PortField(serializers.IntegerField):
    """端口"""
    default_error_messages = {
        'invalid': _('端口不能为空'),
        'max_value': _('端口不能大于 {max_value}'),
        'min_value': _('端口不能小于 {min_value}'),
        'max_string_length': _('端口过长')
    }

    def __init__(self, **kwargs):
        kwargs['min_value'] = kwargs.get('min_value', 0)
        kwargs['max_value'] = kwargs.get('max_value', 65535)
        super(PortField, self).__init__(**kwargs)

    def run_validation(self, data=''):
        # 检测符不符合字符串
        super(PortField, self).run_validation(data)

        return data
