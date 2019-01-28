# -*- coding:utf-8 -*-
from __future__ import division
import logging

from rest_framework.response import Response
from rest_framework.views import APIView

from soc_user.models import WorkTime
from soc_user.serializers import WorkTimeSerializers

logger = logging.getLogger('soc_assets')


class WorkTimeView(APIView):
    """
    查询一天的工作时间
    """

    def get(self, request):
        """
        获取工作时间信息
        """
        work_time = WorkTime.objects.all().first()
        if work_time:
            data = {
                "id": id,
                "morning_start_time": work_time.morning_start_time,
                "morning_end_time": work_time.morning_end_time,
                "afternoon_start_time": work_time.afternoon_start_time,
                "afternoon_end_time": work_time.afternoon_end_time
            }
        else:
            data = {}
        return Response({"status": 200, "msg": "获取工作时间信息", "data": data})

    def post(self, request):
        """
        # "添加或者修改工作时间信息"
        :param request:
        :return:
        """
        # 序列话操作
        serializer = WorkTimeSerializers(data=request.data)
        if not serializer.is_valid():
            # 验证不通过
            msg = ""
            for error in serializer.errors:
                msg = serializer.errors[error][0]
                break
            return Response({"status": 500, "msg": msg, "error": serializer.errors})
        else:
            morning_start_time = serializer.validated_data.get('morning_start_time')
            morning_end_time = serializer.validated_data.get('morning_end_time')
            afternoon_start_time = serializer.validated_data.get('afternoon_start_time')
            afternoon_end_time = serializer.validated_data.get('afternoon_end_time')
            work_time = WorkTime.objects.all().first()
            # 是否已经保存过信息
            if work_time:
                work_time.update(morning_start_time=morning_start_time, morning_end_time=morning_end_time,
                                 afternoon_start_time=afternoon_start_time, afternoon_end_time=afternoon_end_time)
            else:
                work_time = WorkTime(morning_start_time=morning_start_time, morning_end_time=morning_end_time,
                                       afternoon_start_time=afternoon_start_time, afternoon_end_time=afternoon_end_time)
                work_time.save()
            return Response({"status": 200, "msg": "保存成功"})
