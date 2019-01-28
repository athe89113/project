# coding=utf-8
import logging
import os

from django.core.management.base import BaseCommand
from django.utils import timezone

from common import get_next_scan_time
from soc_ssa import models
from soc_ssa.tools.make_docx.docx_plugin import MakeDocx
from soc_ssa.tools.make_pdf.pdf_plugin import MakePdf
from soc_ssa.tools.report.report_data import ReportData

logger = logging.getLogger('soc_ssa')


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        生成 ssa 报告
        """
        time_now = timezone.localtime(timezone.now())
        version = timezone.datetime.strftime(time_now, '%Y%m%d%H%M%S')
        all_planned_tasks = models.SSAReportTemplate.objects.filter(
            schedule_type__in=[3, 4, 5, 6, 7],
            next_scan_time__lte=time_now,
            # status=0,
        )

        docx_path = os.path.join('media', 'reports', 'ssa_report_docx')
        if not os.path.exists(docx_path):
            os.makedirs(docx_path)
        pdf_path = os.path.join('media', 'reports', 'ssa_report_pdf')
        if not os.path.exists(pdf_path):
            os.makedirs(pdf_path)

        for task in all_planned_tasks:
            # 启动报告任务 python manage.py ssa_make_report
            report_data = ReportData(template_id=task.id)
            data = report_data.data()
            m = MakeDocx(template_id=task.id)
            p = MakePdf(template_id=task.id)
            docx_path = os.path.join(docx_path, str(task.id) + '_' + version) + '.doc'
            pdf_path = os.path.join(pdf_path, str(task.id) + '_' + version) + '.pdf'
            try:
                m.generate_docx(path=docx_path, data=data)
                p.generate_pdf(path=pdf_path, data=data)
                for item in data:
                    if 'chart_path' in item and item['chart_path']:
                        os.remove(item['chart_path'])

            except Exception as e:
                logger.error('task id = {0} run error!!'.format(task.id))
                logger.error(str(e))
                # 执行错误
                # task.status = 2
                # task.save()
                # todo 重试
            else:
                result = models.SSAReportResult()
                result.name = task.name + '_' + version
                result.template = task
                result.docx_path = docx_path
                result.docx_size = os.path.getsize(docx_path) if os.path.exists(docx_path) else 0
                result.pdf_path = pdf_path
                result.pdf_size = os.path.getsize(pdf_path) if os.path.exists(pdf_path) else 0
                result.agent = task.agent
                result.company = task.company
                result.template_type = task.template_type
                result.save()

                logger.info('task id = {0} run success!'.format(task.id))

                next_scan_time = get_next_scan_time(
                    start_date=time_now,
                    time_s=task.schedule_time,
                    period_type=task.schedule_type,
                    days=task.schedule_days,
                    months=task.schedule_months
                )
                # 下次执行时间
                task.next_scan_time = next_scan_time
                task.save()
