# coding=utf-8
import logging
from django.core.management.base import BaseCommand
from utils.monitor import CpuMonitor, MenMonitor, DiskMonitor, NetMonitor
logger = logging.getLogger('soc_system')


class Command(BaseCommand):

    def handle(self, *args, **options):
        for m in [CpuMonitor, MenMonitor, DiskMonitor, NetMonitor]:
            instance = m()
            d = instance.fetch()
            instance.save(d)
