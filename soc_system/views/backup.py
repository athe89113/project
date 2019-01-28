# coding=utf-8
from __future__ import unicode_literals
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView
from utils.auth import AllowAdminWithPassword
from soc_system.tasks import backup_data


class BackupData(APIView):
    """
    备份数据
    """

    # permission_classes = (AllowAdminWithPassword, )

    def get(self, request):
        """
        获取备份数据
        :param request:
        :return:
        """

        agent_now = request.user.userinfo.agent
        cached_key = "system:backup_db:agent_{0}".format(agent_now.id)
        data = cache.get(cached_key, {"status": 0, "name": 'backup-db', "percent": 0, "backup_time": "", "download_url": ""})

        context = {
            "status": 200,
            "msg": "获取状态成功",
            "data": [data]
        }
        return Response(context)

    def post(self, request):
        """
        备份数据
        :param request:
        :return:
        """
        # agents = soc_models.Agent.objects.exclude(id=1).count()
        # if agents > 1:
        #     context = {
        #         "status": 200,
        #         "msg": "当前操作不允许",
        #         "error": "当前操作不允许",
        #     }
        #     return Response(context)
        if request.user.userinfo.role_type == 3:
            context = {
                "status": 500,
                "msg": "无权操作",
                "error": "无权操作",
            }
            return Response(context)

        agent_now = request.user.userinfo.agent
        backup_data.delay(agent_now.id)
        # backup_data(agent_now.id)

        context = {
            "status": 200,
            "msg": "正在备份数据，请等待",
        }
        return Response(context)
