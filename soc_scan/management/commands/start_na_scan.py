# -*- coding:utf-8 -*-
import logging

from django.core.management.base import BaseCommand

from soc_scan.tools.nascan import NAScan

logger = logging.getLogger('soc_scan')


class Command(BaseCommand):
    def handle(self, *args, **options):
        logger.info(u'开启NAScan扫描!')
        NAScan.na_start()
