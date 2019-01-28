#coding=utf-8
from rest_framework.views import APIView
from rest_framework.response import Response
from soc_ssa import models
from soc_ssa.serializers import SSAAlarmConfSerializers


class SSAAlarmConfDetail(APIView):
    """
    态势感知-预警/告警配置
    """

    def get(self, request, conf_type):
        """
        获取配置
        """
        conf_type = int(conf_type)
        if conf_type not in [1, 2, 3, 4]:
            return Response({"status": 500, "msg": "配置类型错误"})

        agent = request.user.userinfo.agent
        company = request.user.userinfo.company
        obj, _ = models.SSAAlarmConf.objects.get_or_create(
            conf_type=conf_type, agent=agent, company=company)
        data = {
            "conf_type": conf_type,
            "conf_name": models.ALARM_CONF_TYPES.get(conf_type),
            "max_alarm_count": obj.max_alarm_count,
            "toggle_condition": obj.toggle_condition
        }
        cell_list = []
        for cell in models.SSAAlarmCell.objects.filter(conf_type=conf_type):
            user_cell, _ = models.SSAAlarmConfCell.objects.get_or_create(
                cell_id=cell.id, agent=agent, company=company, defaults={
                    "warning": cell.warning,
                    "alarm": cell.alarm,
                    "enable": 0
                })
            cell_data = {
                "id": user_cell.id,
                "name": cell.name,
                "unit": cell.unit,
                "expression": cell.expression,
                "enable": user_cell.enable,
                "warning": user_cell.warning,
                "alarm": user_cell.alarm,
            }
            cell_list.append(cell_data)

        data['cells'] = cell_list
        notify_list = []
        for user in models.UserInfo.objects.filter(agent=agent, company=company):
            notify_obj, _ = models.SSAAlarmNotifyConf.objects.get_or_create(
                agent=agent, company=company, user_id=user.user_id,
                conf_type=conf_type
            )
            notify_list.append({
                "id": notify_obj.id,
                "username": notify_obj.user.username,
                "sms": notify_obj.sms,
                "email": notify_obj.email,
            })
        data['notifys'] = notify_list
        return Response({"status": 200, "msg": "获取配置成功", "data": data})


    def put(self, request, conf_type):
        """
        修改配置
        """
        conf_type = int(conf_type)
        if conf_type not in [1, 2, 3, 4]:
            return Response({"status": 500, "msg": "配置类型错误"})

        agent = request.user.userinfo.agent
        company = request.user.userinfo.company
        try:
            obj = models.SSAAlarmConf.objects.get(
                conf_type=conf_type, agent=agent, company=company)
        except models.SSAAlarmConf.DoesNotExist:
            return Response({"status": 500, "msg": "配置不存在"})

        obj_serializer = SSAAlarmConfSerializers(
            instance=obj,
            data=request.data,
            context={'request': request},
        )

        if obj_serializer.is_valid():
            obj_serializer.save()
            return Response({"status": 200, "msg": "修改成功"})
        else:
            errors = obj_serializer.errors
            return Response({"status": 500, "msg": errors.items()[0][1][0], "error": errors})