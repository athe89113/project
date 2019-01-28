# coding=utf-8
from __future__ import unicode_literals
from rest_framework.views import APIView
from rest_framework.response import Response
from soc_system.tools import sys_check
from django.core.cache import cache
from soc_system.tasks import run_check


class SysStatusView(APIView):
    """系统配置"""
    def get(self, request):
        """获取系统健康情况"""
        re_check = request.query_params.get('re_check')
        print(re_check)
        user_id = self.request.user.id
        agent_id = self.request.user.userinfo.agent_id
        data = dict()
        s = sys_check.SysCheck(agent_id=agent_id, user_id=user_id)
        if re_check == 'all':
            data['system_status'] = 'loading'
            data['system_check_progress'] = 5
            if not cache.get(str(agent_id) + '_system_check_start'):
                run_check.delay(agent_id=agent_id, user_id=user_id)
        elif re_check == 'sys':
            s.c_sys()
            data['system_status'] = cache.get(str(agent_id) + '_system_status', 'loading')
            data['sys'] = cache.get(str(agent_id) + '_system_monitor_sys')
        elif re_check == 'sys_b':
            s.c_sys_b()
            data['sys_b'] = cache.get(str(agent_id) + '_system_monitor_sys_b')

        elif re_check == 'soc_component':
            s.c_component()
            data['soc_component'] = cache.get(str(agent_id)+'_system_monitor_soc_component')

        elif not cache.get(str(agent_id)+'_system_monitor_sys'):
            data['system_status'] = 'loading'
            data['system_check_progress'] = cache.get(str(agent_id)+'_system_check_progress', 10)
            if not cache.get(str(agent_id)+'_system_check_start'):
                run_check.delay(agent_id=agent_id, user_id=user_id)
        else:
            data['sys'] = cache.get(str(agent_id)+'_system_monitor_sys')
            data['sys_b'] = cache.get(str(agent_id)+'_system_monitor_sys_b')
            data['soc_component'] = cache.get(str(agent_id)+'_system_monitor_soc_component')
            data['system_status'] = cache.get(str(agent_id)+'_system_status', '')
            if data['system_status'] == "loading":
                data['system_check_progress'] = cache.get(str(agent_id)+'_system_check_progress', 1)
            else:
                data['system_check_progress'] = 100

        data['last_time'] = cache.get(str(agent_id) + '_system_monitor_lastitme')
        return Response({"status": 200, "data": data})
