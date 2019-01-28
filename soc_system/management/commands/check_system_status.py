# coding=utf-8
import logging
from django.core.management.base import BaseCommand
from soc_system.tools.sys_check import SysCheck
from soc.models import Agent
from soc_user.models import UserInfo
logger = logging.getLogger('soc_system')


class Command(BaseCommand):

    def handle(self, *args, **options):
        for agent in Agent.objects.all():
            logger.debug("start check system status, Agent: {}".format(agent.name))
            try:
                user_id = UserInfo.objects.filter(agent=agent).first().user_id
                s = SysCheck(agent_id=agent.id, user_id=user_id)
                s.v_all()
            except Exception as e:
                logger.error("error check system status, Agent: {}, Error: {}".format(agent.name, e.message))
