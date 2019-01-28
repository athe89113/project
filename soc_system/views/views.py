# coding=utf-8
from __future__ import unicode_literals
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from utils.version import get_version


class SystemVersion(APIView):
    """
    系统版本
    """

    permission_classes = (AllowAny,)

    def get(self, request):
        """
        返回当前云松的版本, 以 CHANGELOG 为基础
        :return:
        """
        data = {
            "version": get_version()
        }
        return Response(data)
