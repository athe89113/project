# coding: utf-8
from __future__ import unicode_literals
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from soc.models import (
    Agent
)
from optparse import make_option


class Command(BaseCommand):

    help = u'生成新的代理商'

    option_list = BaseCommand.option_list + (
        make_option('--name', dest='name', help='agent name'),
        make_option('--title', dest='title', help='agent title'),
        )

    def handle(self, *args, **options):
        """
        生成新的代理商
        :return: 生成的key, 请将这个key写到配置文件中
        """
        agent_name = options.get('name')
        agent_title = options.get('title')
        # print(agent_name, agent_title)
        if not agent_name or not agent_title:
            print("No name or title, please check your command!")
            return
        if Agent.objects.filter(name=agent_name).exists():
            print("Duplicate name, please check.")
            return
        try:
            agent = Agent.objects.create(name=agent_name, title=agent_title, status=1)
        except IntegrityError:
            print("Failed! Please check again or create manually!")
            return

        print("Created successfully!")
        print("agent ID: {}".format(agent.id))
