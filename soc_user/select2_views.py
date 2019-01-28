# coding=utf-8
from rest_framework.views import APIView
from rest_framework.response import Response
from utils.select2 import select2_filter
from django.contrib.auth.models import User


class UserSelect2(APIView):
    """用户信息"""
    @staticmethod
    def post(request):
        """获取用户信息"""
        agent_now = request.user.userinfo.agent
        q = request.DATA.get("q", "")
        data_list = User.objects.filter(username__contains=q, userinfo__agent_id=agent_now.id). \
            values("id", "username")
        data_list = [{"id": i['id'], "name": i['username']} for i in data_list]
        result = select2_filter(request, data_list)
        return Response(result)
