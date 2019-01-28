# coding: utf-8
from django.utils import timezone
from soc_system.models import BlackIPList
from soc.models import Agent
from datetime import timedelta


def get_blackip_list(agent):
    """获取代理商下当前的黑名单"""
    if not agent:
        return []
    objs = BlackIPList.objects.filter(agent=agent, is_black=1).order_by("start_time")
    data = []
    for obj in objs:
        if obj.type == 1:
            # 手动添加的
            data.append(obj.ip)
        else:
            # 自动添加，
            fail_ban_time = agent.fail_ban_time  # 禁止时间
            now = timezone.now()
            if obj.start_time + timedelta(seconds=fail_ban_time) > now:
                data.append(obj.ip)
    return data


def get_whiteip_list(agent):
    """获取代理商下当前的白名单"""
    if not agent:
        return []
    objs = BlackIPList.objects.filter(agent=agent, is_black=2).order_by("start_time").values_list("ip", flat=True)
    return list(objs)


def delete_expired_black_ip(agent):
    """删除代理商下的过期黑名单IP"""
    fail_ban_time = agent.fail_ban_time  # 禁止时间
    delete_time = timezone.now() - timedelta(seconds=fail_ban_time)
    BlackIPList.objects.filter(agent=agent, is_black=1, start_time__lt=delete_time, type=0).delete()
