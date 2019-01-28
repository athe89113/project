# -*- coding:utf-8 -*-

import copy
import json
import logging
import os

from datetime import datetime, timedelta

from soc import settings
from soc_ssa import models
from soc_assets.models import TermGroup
from soc_ssa.ssa_common import ESSQL
from soc_ssa.tools.make_docx import fetch_new_data
from soc_ssa.tools.make_docx.charts import Charts
from soc_ssa.tools.make_docx.docx_common import underline_to_camel
from soc_ssa.tools.report import terminal_security_data, innernet_security_data

logger = logging.getLogger('soc_ssa')


class ReportData(object):
    '''
    封装报表数据
    '''

    def __init__(self, template_id):
        self.template_id = template_id

    def data(self, start_day='', end_day=''):
        '''
        封装数据
        '''
        template_obj = models.SSAReportTemplate.objects.get(id=self.template_id)
        result = ''
        # 自定义模版
        if template_obj.template_type == 1:
            content = template_obj.content
            if not content:
                return ValueError("模版不存在")
            content = json.loads(content)
            result = self.custom_report(content=content)
        # 固定模版
        elif template_obj.template_type == 2:
            result = self.fixed_report(template_obj, start_day, end_day)
        return result

    def custom_report(self, content):
        '''
        通用模版
        '''
        result_list = []
        for row in content:
            if row['type'] == 'echart':  # 图表
                report_type = row['report_type']
                char_id = row['id']
                logger.info("start make chart data: name: {}, type: {}, has_table: {}".format(
                    row['name'], row['chart_type'], row['has_table']
                ))

                if report_type == 'report':  # 报告图表
                    char_data = models.SSAReportCell.objects.get(id=char_id)
                    if not char_data:
                        return ValueError('图表不存在!')
                    if 'section' in row:
                        if len(row['section']) == 1 and row['section'][0]['id'] == '-1':
                            term_list = TermGroup.objects.all()
                            for term in term_list:
                                result = copy.deepcopy(row)
                                result['section'] = [{"id": term.term_group_id, "name": term.term_group_name}]
                                data = self.get_report_data(char_data=char_data, row=result)
                                result['name'] = u'{}-{}'.format(row['name'], term.term_group_name)
                                result['data'] = data
                                result['chart_path'] = self.create_chart_image(data=data, row=result)
                                result['description'] = char_data.description
                                result_list.append(result)

                        else:
                            for section in row['section']:
                                result = copy.deepcopy(row)
                                result['section'] = [section]
                                data = self.get_report_data(char_data=char_data, row=result)
                                result['name'] = u'{}-{}'.format(row['name'], section['name'])
                                result['data'] = data
                                result['chart_path'] = self.create_chart_image(data=data, row=result)
                                result['description'] = char_data.description
                                result_list.append(result)
                    else:
                        result = copy.deepcopy(row)
                        data = self.get_report_data(char_data=char_data, row=result)
                        result['data'] = data
                        result['chart_path'] = self.create_chart_image(data=data, row=row)
                        result['description'] = char_data.description
                        result_list.append(result)
                elif report_type == 'custom':  # 自定义图表
                    # 自定义图表
                    result = copy.deepcopy(row)
                    char_data = models.SSAChart.objects.get(id=char_id)
                    data = self.get_custom_data(char_data)
                    result['data'] = data
                    result['chart_path'] = self.create_chart_image(data=data, row=row)
                    result['description'] = char_data.description
                    result_list.append(result)
                else:
                    return ValueError('报告类型不存在!')
            else:
                result_list.append(row)
        return result_list

    def fixed_report(self, template, sday='', eday=''):
        '''
        固定模版
        '''
        now_day = datetime.now()
        title = template.name
        if template.schedule_type in [1, 2]:  # 一次生成
            start_day = sday
            end_day = eday
        elif template.schedule_type == 3:  # 日报
            start_day = datetime.strftime(now_day - timedelta(days=1), "%Y-%m-%d")
            end_day = datetime.strftime(now_day - timedelta(days=1), "%Y-%m-%d")
        elif template.schedule_type == 4:  # 周报
            start_day = datetime.strftime(now_day - timedelta(days=now_day.weekday() + 7), "%Y-%m-%d")
            end_day = datetime.strftime(now_day - timedelta(days=now_day.weekday() + 1), "%Y-%m-%d")
        elif template.schedule_type == 5:  # 月报
            last_month_end = datetime(now_day.year, now_day.month, 1) - timedelta(days=1)
            start_day = datetime.strftime(datetime(last_month_end.year, last_month_end.month, 1), "%Y-%m-%d")
            end_day = datetime.strftime(last_month_end, "%Y-%m-%d")
        elif template.schedule_type == 6:  # 季报
            month = (now_day.month - 1) - (now_day.month - 1) % 3 + 1
            last_quarter_end = datetime(now_day.year, month, 1) - timedelta(days=1)
            start_day = datetime.strftime(datetime(last_quarter_end.year, last_quarter_end.month - 2, 1), "%Y-%m-%d")
            end_day = datetime.strftime(last_quarter_end, "%Y-%m-%d")
        elif template.schedule_type == 7:  # 年报
            this_year_start = datetime(now_day.year, 1, 1)
            last_year_end = this_year_start - timedelta(days=1)
            start_day = datetime.strftime(datetime(last_year_end.year, 1, 1), "%Y-%m-%d")
            end_day = datetime.strftime(last_year_end, "%Y-%m-%d")
        else:
            last_month_end = datetime(now_day.year, now_day.month, 1) - timedelta(days=1)
            start_day = datetime.strftime(datetime(last_month_end.year, last_month_end.month, 1), "%Y-%m-%d")
            end_day = datetime.strftime(last_month_end, "%Y-%m-%d")
            title = ''
        if template.id in [1, 2, 3, 4, 5, 11]:
            content = self.fixed_terminal_report_data(title=title, start_day=start_day, end_day=end_day)
        elif template.id in [6, 7, 8, 9, 10, 12]:
            content = self.fixed_innernet_report_data(title=title, start_day=start_day, end_day=end_day)
        else:
            pass
        return content

    def get_report_data(self, char_data, row):
        '''
        封装固定图表数据
        '''
        if "_" in char_data.data_key:
            data_class_name = underline_to_camel(char_data.data_key)
        else:
            data_class_name = char_data.data_key
        try:
            data_class = getattr(fetch_new_data, data_class_name)
            data_class_obj = data_class(top=row['top'], term=row['section'] if 'section' in row else '',
                                        cycle=row['cycle'] if 'cycle' in row else 1)
            data = data_class_obj.data()
            return data
        except Exception as e:
            logger.error("get_report_data exception {}".format(e))
            return fetch_new_data.demo_data()

    def get_custom_data(self, data):
        '''
        封装自定义图表数据
        '''
        es_host = getattr(settings, "ELASTICSEARCH_HOSTS")[0]
        wheres = ""
        if data.data_type == 1:
            index_path = models.SSADataTag.objects.get(id=data.data_tag)
        elif data.data_type == 2:
            index_path = models.SECDataTag.objects.get(id=data.data_tag)
            wheres = "where {} = {}".format("event_source", data.data_tag)
        else:
            pass

        es_sql = ESSQL(es_host=es_host.replace('http://', ''),
                       limit=data.limit,
                       x=json.loads(data.x),
                       y=json.loads(data.y),
                       ssa_data_tag=index_path.path,
                       query_time=data.query_time)
        is_ok, result = es_sql.exec_serach(wheres=wheres, data_type=data.data_type, data_tag=index_path.path)
        if is_ok:
            y_data = []
            for key in result['y']:
                y_data.append({"name": key, "data": result['y'][key]})
            if len(list(result['x'].items())) > 0:
                char_data = {
                    'labels': list(result['x'].items())[0][1],
                    'data': y_data
                }
            else:
                char_data = {
                    'labels': [],
                    'data': []
                }
            return char_data
        else:
            return is_ok

    def create_chart_image(self, data, row):
        '''
        创建图片
        '''
        chart_path = ''
        try:
            if data:
                c = Charts(data=data, title=row['name'], unit=row['unit'])
                # 表格类型或计数类型
                if row['chart_type'] and row['chart_type'] not in ['table', 'number']:
                    chart_path = getattr(c, row['chart_type'])().save()
        except Exception as e:
            logger.error("make chart error chart type: {}  chart name:{}".format(row['chart_type'], row['name']),
                         exc_info=True)
            return ValueError('生成图表出错!')
        return chart_path

    def create_fixed_report_data(self, type, title=None, time=None):
        '''
        固定模版-文本
        '''
        content = {'type': type, 'params': {}}
        if title:
            content['params']['title'] = title
        if time:
            content['params']['time'] = time
        return content

    def create_fixed_report_chart(self, type, chart_type, title, data, unit='number'):
        '''
        固定模版-图片
        '''
        chart_path = ''
        try:
            chart = Charts(data=data, title=title, unit=unit)
            chart_path = getattr(chart, chart_type)().save()
        except Exception as e:
            logger.error("生成图表出错!:{}".format(e))
        return {'type': type, 'chart_type': chart_type, 'name': title, 'data': data,
                'chart_path': chart_path, 'description': '', 'remark': ''}

    def create_fixed_report_table(self, type, chart_type, data, merges, widths=[]):
        '''
        固定模版-表格
        '''
        # table_data = self.formate_table_merge_data(data=data, merges=merges)
        return {'type': type, 'chart_type': chart_type, 'data': data, 'merges': merges, 'widths': widths}

    def fixed_terminal_report_data(self, title, start_day, end_day):
        '''
        终端安全检查分析报告
        '''
        content = []
        content.append(self.create_fixed_report_data(type='module',
                                                     title=title,
                                                     time='{}~{}'.format(start_day, end_day)))
        content.append(self.create_fixed_report_data(type='title1',
                                                     title=u'一、部门违规情况统计'))
        content.append(self.create_fixed_report_data(type='title2',
                                                     title=u'1.1  违规总量占比'))
        days = self.get_index_days(start_day=start_day, end_day=end_day)
        # 违规总量占比
        security_count_data = terminal_security_data.security_count(days=days)
        content.append(self.create_fixed_report_chart(type='echart',
                                                      chart_type='pie',
                                                      title=u'违规总量占比',
                                                      data=security_count_data))

        content.append(self.create_fixed_report_data(type='title2',
                                                     title=u'1.2  各单位违规类总量统计'))
        # 各单位违规总量型统计
        security_type_count_data = terminal_security_data.security_type_count(days=days)
        content.append(self.create_fixed_report_chart(type='echart',
                                                      chart_type='bar_pile_y',
                                                      title=u'各单位违规总量统计',
                                                      data=security_type_count_data))

        content.append(self.create_fixed_report_data(type='title2',
                                                     title=u'1.3  违规类型详情统计'))
        # 违规类型详情统计
        security_terminal_count_data = terminal_security_data.security_terminal_count(days=days)
        content.append(self.create_fixed_report_table(type='echart',
                                                      chart_type='table_merge',
                                                      data=security_terminal_count_data,
                                                      merges=[0, 1],
                                                      widths=[1.5, 1, 2.5, 1]
                                                      ))

        content.append(self.create_fixed_report_data(type='title1',
                                                     title=u'二、各部门违规情况统计'))

        # 单位列表
        term_list = terminal_security_data.get_term_list()
        # 终端操作系统类别
        os_list = terminal_security_data.terminal_info_os(days=days)
        # 是否关闭共享
        share_list = terminal_security_data.terminal_info_share(days=days)
        # 是否禁用guest用户
        guest_user_list = terminal_security_data.terminal_info_guest_user(days=days)
        # 是否安装终端安全管理系统
        sec_app_list = terminal_security_data.terminal_info_security_app(days=days)
        # 是否安装网盾桌面安全套件
        sec_shield_list = terminal_security_data.terminal_info_security_shield(days=days)
        # 是否安装杀毒软件
        sec_loophole_list = terminal_security_data.terminal_info_security_loophole(days=days)
        # 明文存储
        plaintext_list = terminal_security_data.terminal_info_plaintext(days=days)
        # USB存储设备使用痕迹
        usb_list = terminal_security_data.terminal_info_usb(days=days)
        # 手机充电情况
        phone_list = terminal_security_data.terminal_info_phone(days=days)
        # 终端安全管理系统卸载记录
        uninstall_list = terminal_security_data.terminal_info_uninstall(days=days)

        index = 0
        for term in term_list:
            index += 1
            content.append(self.create_fixed_report_data(type='title2',
                                                         title=u'2.{0}  {1}'.format(str(index),
                                                                                    term.term_group_name)))
            content.append(self.create_fixed_report_data(type='title3',
                                                         title=u'2.{0}.1  终端违规情况TOP10'.format(str(index))))
            # 终端违规情况统计
            terminal_count_data = terminal_security_data.org_security_terminal_count(days=days,
                                                                                     org=term.term_group_name)
            content.append(self.create_fixed_report_chart(type='echart',
                                                          chart_type='bar_pile_y',
                                                          title=u'终端违规情况TOP10',
                                                          data=terminal_count_data))

            # 终端违规情况详情
            terminal_detail_count_data = terminal_security_data.org_security_terminal_detail_count(
                days=days, org=term.term_group_name)
            content.append(self.create_fixed_report_table(type='echart',
                                                          chart_type='table_merge',
                                                          data=terminal_detail_count_data,
                                                          merges=[0, 1, 2],
                                                          widths=[2, 1.5, 0.5, 1.5, 0.5]))
            content.append(self.create_fixed_report_data(type='title3',
                                                         title=u'2.{0}.2  终端安全检查详情'.format(str(index))))
            # 存在违规IP
            ips = terminal_detail_count_data['ips']
            if ips:

                ip_index = 0
                for ip in ips:
                    ip_index += 1
                    content.append(self.create_fixed_report_data(type='title4',
                                                                 title=u'2.{0}.2.{1}  {2}'.format(str(index),
                                                                                                  str(ip_index), ip)))
                    assets = terminal_security_data.get_assets_by_ip(ip=ip, org=term.term_group_name)
                    asset_name, asset_duty = '', ''
                    if assets:
                        asset_name = assets.assets_name
                        asset_duty = assets.term_duty
                    content.append(self.create_fixed_report_data(type='text',
                                                                 title=u'终端IP：{0}   主机名：{1}    责任人：{2}'.format(ip,
                                                                                                               asset_name,
                                                                                                               asset_duty)))
                    # 明文存储
                    plaintext_data = terminal_security_data.get_terminal_plaintext_data(data=plaintext_list, ip=ip)
                    # USB存储设备使用痕迹
                    usb_data = terminal_security_data.get_terminal_usb_data(data=usb_list, ip=ip)
                    # 手机充电情况
                    phone_data = terminal_security_data.get_terminal_phone_data(data=phone_list, ip=ip)
                    # 终端安全管理系统卸载记录
                    uninstall_data = terminal_security_data.get_terminal_uninstall_data(data=uninstall_list, ip=ip)
                    terminal_detail_data = {
                        "labels": [u"序号", u"检查项目", u"检查结果"],
                        "data": [
                            [u"1", u"终端操作系统类别", terminal_security_data.get_terminal_os(data=os_list, ip=ip)],
                            [u"2", u"是否关闭共享",
                             terminal_security_data.get_terminal_info(data=share_list, key='term_ip', ip=ip)],
                            [u"3", u"是否禁用guest用户",
                             terminal_security_data.get_terminal_info(data=guest_user_list, key='term_ip', ip=ip)],
                            [u"4", u"是否安装终端安全管理系统",
                             terminal_security_data.get_terminal_info(data=sec_app_list, key='term_ip', ip=ip)],
                            [u"5", u"是否安装网盾桌面安全套件",
                             terminal_security_data.get_terminal_info(data=sec_shield_list, key='term_ip', ip=ip)],
                            [u"6", u"是否安装杀毒软件",
                             terminal_security_data.get_terminal_info(data=sec_loophole_list, key='term_ip', ip=ip)],
                            [u"7", u"明文存储情况", len(plaintext_data)],
                            [u"8", u"USB存储设备使用痕迹", len(usb_data)],
                            [u"9", u"手机充电情况", len(phone_data)],
                            [u"10", u"终端安全管理系统卸载记录", len(uninstall_data)],
                        ],
                    }
                    content.append(self.create_fixed_report_table(type='echart',
                                                                  chart_type='table_merge',
                                                                  data=terminal_detail_data,
                                                                  merges=[],
                                                                  widths=[1, 4, 1]))
                    if plaintext_data or usb_data or phone_data or uninstall_data:
                        content.append(self.create_fixed_report_data(type='text',
                                                                     title=u'安全检查附表'))
                        data_list = {
                            'labels': [u"检查项", u"详情", u"时间"],
                            'data': plaintext_data + usb_data + phone_data + uninstall_data
                        }
                        content.append(self.create_fixed_report_table(type='echart',
                                                                      chart_type='table_merge',
                                                                      data=data_list,
                                                                      merges=[0, 1],
                                                                      widths=[2, 3, 1]))

        return content

    def fixed_innernet_report_data(self, title, start_day, end_day):
        '''
        内网安全统计报表
        '''
        content = []
        days = self.get_index_days(start_day=start_day, end_day=end_day)
        content.append(self.create_fixed_report_data(type='module',
                                                     title=title,
                                                     time='{}~{}'.format(start_day, end_day)))
        content.append(self.create_fixed_report_data(type='title1',
                                                     title=u'一、内网对接资产设备情况'))
        innernet_asset_status = innernet_security_data.asset_status(days=days)
        content.append(self.create_fixed_report_table(type='echart',
                                                      chart_type='table_merge',
                                                      data=innernet_asset_status,
                                                      merges=[],
                                                      widths=[2, 1, 1, 1, 1]))
        content.append(self.create_fixed_report_data(type='title1',
                                                     title=u'二、各资产设备事件量占比'))
        event_num_count = innernet_security_data.event_num_count(days=days)
        content.append(self.create_fixed_report_chart(type='echart',
                                                      chart_type='pie',
                                                      title=u'各资产设备事件量占比',
                                                      data=event_num_count))
        content.append(self.create_fixed_report_data(type='title1',
                                                     title=u'三、事件趋势统计'))
        event_thred_count = innernet_security_data.event_thred_count(days=days)
        content.append(self.create_fixed_report_chart(type='echart',
                                                      chart_type='line',
                                                      title=u'事件趋势统计',
                                                      data=event_thred_count))
        content.append(self.create_fixed_report_data(type='title1',
                                                     title=u'四、风险统计'))
        content.append(self.create_fixed_report_data(type='title2',
                                                     title=u'4.1  风险事件统计'))
        risk_event_count = innernet_security_data.risk_event_count(days=days)
        content.append(self.create_fixed_report_table(type='echart',
                                                      chart_type='table_merge',
                                                      data=risk_event_count,
                                                      merges=[0],
                                                      widths=[2.5, 2.5, 1]))
        content.append(self.create_fixed_report_data(type='title2',
                                                     title=u'4.2  风险资产统计'))
        risk_assets_count = innernet_security_data.risk_assets_count(days=days)
        content.append(self.create_fixed_report_table(type='echart',
                                                      chart_type='table_merge',
                                                      data=risk_assets_count,
                                                      merges=[],
                                                      widths=[3, 1.5, 1.5]))
        content.append(self.create_fixed_report_data(type='title2',
                                                     title=u'4.3  风险部门统计'))
        risk_org_count = innernet_security_data.risk_org_count(days=days)
        content.append(self.create_fixed_report_table(type='echart',
                                                      chart_type='table_merge',
                                                      data=risk_org_count,
                                                      merges=[],
                                                      widths=[2.5, 1.5, 1.5, 1.5]))
        content.append(self.create_fixed_report_data(type='title1',
                                                     title=u'五、违规统计'))
        content.append(self.create_fixed_report_data(type='title2',
                                                     title=u'5.1  违规来源统计'))
        irregularly_source_count = innernet_security_data.irregularly_source_count(days=days)
        content.append(self.create_fixed_report_chart(type='echart',
                                                      chart_type='pie',
                                                      title=u'违规来源统计',
                                                      data=irregularly_source_count))
        content.append(self.create_fixed_report_data(type='title2',
                                                     title=u'5.2  违规类型统计'))
        irregularly_type_count = innernet_security_data.irregularly_type_count(days=days)
        content.append(self.create_fixed_report_table(type='echart',
                                                      chart_type='table_merge',
                                                      data=irregularly_type_count,
                                                      merges=[0],
                                                      widths=[1, 3, 1, 1]))
        content.append(self.create_fixed_report_data(type='title2',
                                                     title=u'5.3  违规终端统计'))
        irregularly_ip_count = innernet_security_data.irregularly_ip_count(days=days)
        content.append(self.create_fixed_report_table(type='echart',
                                                      chart_type='table_merge',
                                                      data=irregularly_ip_count,
                                                      merges=[0],
                                                      widths=[2, 3, 1]))
        content.append(self.create_fixed_report_data(type='title2',
                                                     title=u'5.4  违规单位统计'))
        irregularly_org_count = innernet_security_data.irregularly_org_count(days=days)
        content.append(self.create_fixed_report_table(type='echart',
                                                      chart_type='table_merge',
                                                      data=irregularly_org_count,
                                                      merges=[0],
                                                      widths=[1.5, 2.5, 1, 1]))
        content.append(self.create_fixed_report_data(type='title1',
                                                     title=u'六、病毒统计'))
        content.append(self.create_fixed_report_data(type='title2',
                                                     title=u'6.1  病毒类型统计'))
        viruses_type_count = innernet_security_data.viruses_type_count(days=days)
        content.append(self.create_fixed_report_chart(type='echart',
                                                      chart_type='pie',
                                                      title=u'病毒类型统计',
                                                      data=viruses_type_count))
        content.append(self.create_fixed_report_data(type='title2',
                                                     title=u'6.2  感染病毒终端统计（未处理）'))
        viruses_ip_count = innernet_security_data.viruses_ip_count(days=days)
        content.append(self.create_fixed_report_table(type='echart',
                                                      chart_type='table_merge',
                                                      data=viruses_ip_count,
                                                      merges=[0],
                                                      widths=[1.5, 2, 1, 1.5]))
        content.append(self.create_fixed_report_data(type='title1',
                                                     title=u'七、攻击统计'))
        content.append(self.create_fixed_report_data(type='title2',
                                                     title=u'7.1  攻击类型统计'))
        attack_type_count = innernet_security_data.attack_type_count(days=days)
        content.append(self.create_fixed_report_chart(type='echart',
                                                      chart_type='pie',
                                                      title=u'攻击类型统计',
                                                      data=attack_type_count))
        content.append(self.create_fixed_report_data(type='title2',
                                                     title=u'7.2  攻击源统计TOP10'))
        attack_source_count = innernet_security_data.attack_source_count(days=days)
        content.append(self.create_fixed_report_chart(type='echart',
                                                      chart_type='bar_y',
                                                      title=u'攻击源统计TOP10',
                                                      data=attack_source_count))
        content.append(self.create_fixed_report_data(type='title2',
                                                     title=u'7.3  被攻击终端统计'))
        attack_ip_count = innernet_security_data.attack_ip_count(days=days)
        content.append(self.create_fixed_report_table(type='echart',
                                                      chart_type='table_merge',
                                                      data=attack_ip_count,
                                                      merges=[0],
                                                      widths=[2, 3, 1]))
        content.append(self.create_fixed_report_data(type='title1',
                                                     title=u'八、终端行为审计'))
        content.append(self.create_fixed_report_data(type='title2',
                                                     title=u'8.1  各部门开关机详情'))

        term_list = TermGroup.objects.all()
        for term in term_list:
            content.append(self.create_fixed_report_data(type='text', title=term.term_group_name))
            terminal_on_off_count = innernet_security_data.terminal_on_off_count(days=days,
                                                                                 term_id=term.term_group_id)
            content.append(self.create_fixed_report_table(type='echart',
                                                          chart_type='table_merge',
                                                          data=terminal_on_off_count,
                                                          merges=[],
                                                          widths=[0.5, 1.5, 1, 1, 1, 1]))
        content.append(self.create_fixed_report_data(type='title2',
                                                     title=u'8.2  登录失败统计TOP10'))
        terminal_login_fail_count = innernet_security_data.terminal_login_fail_count(days=days)
        content.append(self.create_fixed_report_chart(type='echart',
                                                      chart_type='bar_y',
                                                      title=u'登录失败统计TOP10',
                                                      data=terminal_login_fail_count))
        content.append(self.create_fixed_report_data(type='title2',
                                                     title=u'8.3  打印情况统计'))
        content.append(self.create_fixed_report_data(type='title3',
                                                     title=u'8.3.1  打印情况统计TOP10'))
        terminal_print_count = innernet_security_data.terminal_print_count(days=days)
        content.append(self.create_fixed_report_chart(type='echart',
                                                      chart_type='bar_pile_y',
                                                      title=u'打印情况统计TOP10',
                                                      data=terminal_print_count))
        content.append(self.create_fixed_report_data(type='title3',
                                                     title=u'8.3.2  各部门打印详情'))
        for term in term_list:
            content.append(self.create_fixed_report_data(type='text', title=term.term_group_name))
            terminal_print_list = innernet_security_data.terminal_print_list(days=days,
                                                                             term_id=term.term_group_id)
            content.append(self.create_fixed_report_table(type='echart',
                                                          chart_type='table_merge',
                                                          data=terminal_print_list,
                                                          merges=[],
                                                          widths=[0.5, 1.5, 1, 1, 1, 1]))
        content.append(self.create_fixed_report_data(type='title3',
                                                     title=u'8.3.3  下班打印统计TOP10'))
        terminal_offwork_print_count = innernet_security_data.terminal_offwork_print_count(days=days)
        content.append(self.create_fixed_report_chart(type='echart',
                                                      chart_type='bar_pile_y',
                                                      title=u'下班打印统计TOP10',
                                                      data=terminal_offwork_print_count))
        content.append(self.create_fixed_report_data(type='title2',
                                                     title=u'8.4  移动盘违规使用统计'))
        content.append(self.create_fixed_report_data(type='title3',
                                                     title=u'8.4.1  移动盘违规使用统计TOP10'))
        terminal_usb_count = innernet_security_data.terminal_usb_count(days=days)
        content.append(self.create_fixed_report_chart(type='echart',
                                                      chart_type='bar_pile_y',
                                                      title=u'移动盘违规使用统计TOP10',
                                                      data=terminal_usb_count))
        content.append(self.create_fixed_report_data(type='title3',
                                                     title=u'8.4.2  各部门移动盘违规使用详情'))
        for term in term_list:
            content.append(self.create_fixed_report_data(type='text', title=term.term_group_name))
            terminal_usb_list = innernet_security_data.terminal_usb_list(days=days, term_id=term.term_group_id)
            content.append(self.create_fixed_report_table(type='echart',
                                                          chart_type='table_merge',
                                                          data=terminal_usb_list,
                                                          merges=[],
                                                          widths=[0.5, 1.5, 1, 1.5, 1.5]))
        content.append(self.create_fixed_report_data(type='title2',
                                                     title=u'8.5  明文存储统计'))
        content.append(self.create_fixed_report_data(type='title3',
                                                     title=u'8.5.1  明文存储终端统计TOP10'))
        terminal_txt_count = innernet_security_data.terminal_txt_count(days=days)
        content.append(self.create_fixed_report_chart(type='echart',
                                                      chart_type='bar_y',
                                                      title=u'明文存储统计TOP10',
                                                      data=terminal_txt_count))
        content.append(self.create_fixed_report_data(type='title3',
                                                     title=u'8.5.2  各单位明文存储详情'))
        for term in term_list:
            content.append(self.create_fixed_report_data(type='text', title=term.term_group_name))
            terminal_txt_list = innernet_security_data.terminal_txt_list(days=days, term_id=term.term_group_id)
            content.append(self.create_fixed_report_table(type='echart',
                                                          chart_type='table_merge',
                                                          data=terminal_txt_list,
                                                          merges=[],
                                                          widths=[0.5, 1.5, 1, 1, 1, 1]))
        content.append(self.create_fixed_report_data(type='title2',
                                                     title=u'8.6  手机充电统计'))
        content.append(self.create_fixed_report_data(type='title3',
                                                     title=u'8.6.1  手机充电统计TOP10'))
        terminal_battery_count = innernet_security_data.terminal_battery_count(days=days)
        content.append(self.create_fixed_report_chart(type='echart',
                                                      chart_type='bar_y',
                                                      title=u'手机充电统计TOP10',
                                                      data=terminal_battery_count))
        content.append(self.create_fixed_report_data(type='title3',
                                                     title=u'8.6.2  各部门手机充电详情'))
        for term in term_list:
            content.append(self.create_fixed_report_data(type='text', title=term.term_group_name))
            terminal_battery_list = innernet_security_data.terminal_battery_list(days=days, term_id=term.term_group_id)
            content.append(self.create_fixed_report_table(type='echart',
                                                          chart_type='table_merge',
                                                          data=terminal_battery_list,
                                                          merges=[],
                                                          widths=[0.5, 1.5, 1, 1.5, 1.5]))
        content.append(self.create_fixed_report_data(type='title2',
                                                     title=u'8.7  卸载统计'))
        content.append(self.create_fixed_report_data(type='title3',
                                                     title=u'8.7.1  卸载统计TOP10'))
        terminal_uninstall_count = innernet_security_data.terminal_uninstall_count(days=days)
        content.append(self.create_fixed_report_chart(type='echart',
                                                      chart_type='bar_y',
                                                      title=u'卸载统计TOP10',
                                                      data=terminal_uninstall_count))
        content.append(self.create_fixed_report_data(type='title3',
                                                     title=u'8.7.2  各部门卸载详情'))
        for term in term_list:
            content.append(self.create_fixed_report_data(type='text', title=term.term_group_name))
            terminal_uninstall_list = innernet_security_data.terminal_uninstall_list(days=days,
                                                                                     term_id=term.term_group_id)
            content.append(self.create_fixed_report_table(type='echart',
                                                          chart_type='table_merge',
                                                          data=terminal_uninstall_list,
                                                          merges=[],
                                                          widths=[0.5, 1.5, 1, 1.5, 1.5]))
        content.append(self.create_fixed_report_data(type='title1',
                                                     title=u'九、服务器端审计'))
        content.append(self.create_fixed_report_data(type='title2',
                                                     title=u'9.1  终端违规操作数据库统计TOP10'))
        detabase_terminal_opt_count = innernet_security_data.detabase_terminal_opt_count(days=days)
        content.append(self.create_fixed_report_chart(type='echart',
                                                      chart_type='bar_y',
                                                      title=u'终端违规操作数据库统计TOP10',
                                                      data=detabase_terminal_opt_count))
        content.append(self.create_fixed_report_data(type='title2',
                                                     title=u'9.2  数据库操作违规类型统计'))
        detabase_type_opt_count = innernet_security_data.detabase_type_opt_count(days=days)
        content.append(self.create_fixed_report_chart(type='echart',
                                                      chart_type='pie',
                                                      title=u'数据库操作违规类型统计',
                                                      data=detabase_type_opt_count))
        content.append(self.create_fixed_report_data(type='title1',
                                                     title=u'十、网络审计'))
        content.append(self.create_fixed_report_data(type='title2',
                                                     title=u'10.1  防火墙'))
        firewall_flow_count = innernet_security_data.firewall_flow_count(days=days)
        content.append(self.create_fixed_report_chart(type='echart',
                                                      chart_type='line',
                                                      title=u'防火墙流量趋势',
                                                      data=firewall_flow_count,
                                                      unit='band'))
        firewall_prot_flow_count = innernet_security_data.firewall_prot_flow_count(days=days)
        content.append(self.create_fixed_report_chart(type='echart',
                                                      chart_type='bar_y',
                                                      title=u'防火墙各协议流量统计',
                                                      data=firewall_prot_flow_count,
                                                      unit='band'))
        firewall_src_ip_count = innernet_security_data.firewall_src_ip_count(days=days)
        content.append(self.create_fixed_report_chart(type='echart',
                                                      chart_type='bar_y',
                                                      title=u'防火墙源IP流量排行TOP10',
                                                      data=firewall_src_ip_count,
                                                      unit='band'))
        firewall_dst_ip_count = innernet_security_data.firewall_dst_ip_count(days=days)
        content.append(self.create_fixed_report_chart(type='echart',
                                                      chart_type='bar_y',
                                                      title=u'防火墙目标IP流量排行TOP10',
                                                      data=firewall_dst_ip_count,
                                                      unit='band'))
        firewall_type_count = innernet_security_data.firewall_type_count(days=days)
        content.append(self.create_fixed_report_chart(type='echart',
                                                      chart_type='pie',
                                                      title=u'防火墙事件类型统计',
                                                      data=firewall_type_count))
        content.append(self.create_fixed_report_data(type='title2',
                                                     title=u'10.2  网闸'))
        gl_flow_count = innernet_security_data.gl_flow_count(days=days)
        content.append(self.create_fixed_report_chart(type='echart',
                                                      chart_type='line',
                                                      title=u'隔离设备接收发送流量趋势',
                                                      data=gl_flow_count,
                                                      unit='band'))
        gl_src_ip_flow_count = innernet_security_data.gl_src_ip_flow_count(days=days)
        content.append(self.create_fixed_report_chart(type='echart',
                                                      chart_type='bar_y',
                                                      title=u'隔离设备源IP发送流量统计TOP10',
                                                      data=gl_src_ip_flow_count,
                                                      unit='band'))
        gl_dst_ip_flow_count = innernet_security_data.gl_dst_ip_flow_count(days=days)
        content.append(self.create_fixed_report_chart(type='echart',
                                                      chart_type='bar_y',
                                                      title=u'隔离设备目标IP接收流量统计TOP10',
                                                      data=gl_dst_ip_flow_count,
                                                      unit='band'))
        gl_type_count = innernet_security_data.gl_type_count(days=days)
        content.append(self.create_fixed_report_chart(type='echart',
                                                      chart_type='pie',
                                                      title=u'隔离事件类型统计',
                                                      data=gl_type_count))
        content.append(self.create_fixed_report_data(type='title1',
                                                     title=u'十一、入侵监测事件统计'))
        ids_attack_count = innernet_security_data.ids_attack_count(days=days)
        content.append(self.create_fixed_report_chart(type='echart',
                                                      chart_type='line',
                                                      title=u'IDS监测攻击趋势',
                                                      data=ids_attack_count))
        ids_event_count = innernet_security_data.ids_event_count(days=days)
        content.append(self.create_fixed_report_chart(type='echart',
                                                      chart_type='pie',
                                                      title=u'IDS监测事件名称占比',
                                                      data=ids_event_count))
        ids_attack_src_count = innernet_security_data.ids_attack_src_count(days=days)
        content.append(self.create_fixed_report_chart(type='echart',
                                                      chart_type='bar_y',
                                                      title=u'IDS监测攻击源攻击次数统计TOP10',
                                                      data=ids_attack_src_count))
        ids_attack_dst_count = innernet_security_data.ids_attack_dst_count(days=days)
        content.append(self.create_fixed_report_chart(type='echart',
                                                      chart_type='bar_y',
                                                      title=u'IDS监测终端被攻击次数统计TOP10',
                                                      data=ids_attack_dst_count))
        return content

    def get_index_days(self, start_day, end_day):
        '''
        获取时间索引
        :return:
        '''
        data = [end_day]
        start = datetime.strptime(start_day, "%Y-%m-%d")
        end = datetime.strptime(end_day, "%Y-%m-%d")
        for d in self.gen_dates(start, (end - start).days):
            d = datetime.strftime(d, "%Y-%m-%d")
            data.append(d)
        return data

    def gen_dates(self, b_date, days):
        day = timedelta(days=1)
        for i in range(days):
            yield b_date + day * i
