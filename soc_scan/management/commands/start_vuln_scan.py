# -*- coding:utf-8 -*-
import logging

from django.core.management.base import BaseCommand

from soc_scan.tools.vulscan import VulScan

logger = logging.getLogger('soc_scan')


class Command(BaseCommand):
    def handle(self, *args, **options):
        logger.info(u'开启漏洞扫描!')
        VulScan.vuln_start()
