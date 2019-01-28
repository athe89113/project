# -*- coding:utf-8 -*-
from __future__ import unicode_literals

import copy
import json
import logging
import os
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Table, TableStyle

from soc import settings
from soc_ssa import models
from soc_ssa.ssa_common import ESSQL
from soc_ssa.tools.make_docx import fetch_new_data
from soc_ssa.tools.make_docx.charts import Charts
from soc_ssa.tools.make_docx.docx_common import underline_to_camel

logger = logging.getLogger('soc_ssa')


class MakePdf(object):
    """
    通过ES中数据生成图表
    """

    def __init__(self, template_id):
        self.template_id = template_id
        self.index = 1
        self.content = []
        self.chart_path_list = []

        path = os.path.join('soc_ssa', 'tools', 'make_pdf', 'fonts')
        pdfmetrics.registerFont(TTFont('song', '{}/simsun.ttc'.format(path)))
        pdfmetrics.registerFont(TTFont('fs', '{}/simfang.ttf'.format(path)))
        stylesheet = getSampleStyleSheet()
        self.normalStyle = stylesheet['Normal']

    def generate_section(self, title, desc, remark, chart=None, table_data=None, data_type=None):
        """
        生成段落
        """
        if chart:
            self.create_chart_image(path=chart)
        if table_data:
            self.add_table(name='', data=table_data, data_type=data_type)
        self.index += 1
        if remark:
            title = '<para autoLeading="off" fontSize=10 align=left>' \
                    '<b><font face="song">{0}</font></b>' \
                    '<br/>' \
                    '</para>'.format(remark)
            self.content.append(Paragraph(title, self.normalStyle))
        self.content.append(Paragraph('<br/><br/>', self.normalStyle))

    def create_chart_image(self, path):
        '''
        创建图片
        '''
        img = Image(settings.BASE_DIR + '/' + path)
        img.drawHeight = 380
        img.drawWidth = 500
        chart_data = [[img]]
        chart_table = Table(chart_data, colWidths=[550])
        self.content.append(chart_table)

    def add_table(self, name, data, data_type):
        """
        添加表格
        """
        if name:
            self.create_pdf_text(content=name)
        lables = [''] + data['labels']
        rows = []
        rows.append(lables)
        for i in data['data']:
            if data_type == 99:
                rows.append([i['name']] + i['data'])
            else:
                rows.append([data['data'].index(i) + 1] + i['data'])
        colWidths = (6.4 / len(lables)) * inch  # 每列的宽度
        rows = self.format_table_width(rows=rows)
        # 创建表格对象，并设定各列宽度
        component_table = Table(rows, colWidths=colWidths)
        # 添加表格样式
        component_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'song'),  # 字体
            ('FONTSIZE', (0, 0), (-1, -1), 8),  # 字体大小
            # ('BACKGROUND', (0, 0), (-1, 0), colors.lightskyblue),  # 设置第一行背景颜色
            ('LINEBEFORE', (0, 0), (0, -1), 0.1, colors.grey),  # 设置表格左边线颜色为灰色，线宽为0.1
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),  # 设置表格内文字颜色
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  # 设置表格框线为红色，线宽为0.5
        ]))
        self.content.append(component_table)

    def add_table_merge(self, data, merges):
        '''
        创建合并表格
        '''
        lables = data['labels']
        rows = data['data']
        rows.insert(0, lables)

        colWidths = (6.4 / len(lables)) * inch  # 每列的宽度
        rows = self.format_table_width(rows=rows)
        table_rows = self.formate_table_merge_data(data=rows, merges=merges)
        # 创建表格对象，并设定各列宽度
        component_table = Table(table_rows['data'], colWidths=colWidths)
        table_style = TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'song'),  # 字体
            ('FONTSIZE', (0, 0), (-1, -1), 10),  # 字体大小
            # ('BACKGROUND', (0, 0), (-1, 0), colors.lightskyblue),  # 设置第一行背景颜色
            ('LINEBEFORE', (0, 0), (0, -1), 0.1, colors.grey),  # 设置表格左边线颜色为灰色，线宽为0.1
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),  # 设置表格内文字颜色
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  # 设置表格框线为红色，线宽为0.5
        ])
        for index in table_rows['index']:
            for m in merges:
                table_style.add('SPAN', (m, index[0]), (m, index[1]))
        # 添加表格样式
        component_table.setStyle(table_style)
        self.content.append(component_table)

    def formate_table_merge_data(self, data, merges):
        '''
        封装表格合并数据
        '''
        name_list = []
        index_list = []
        for index, item in enumerate(data):
            if index != 0 and name_list[-1] == item[0]:
                index_list[-1].append(index)
            else:
                name_list.append(item[0])
                index_list.append([index])
        indexs = []
        for item in index_list:
            if len(item) > 1:
                indexs.append([item[0], item[-1]])
                for index in item:
                    if index != item[0]:
                        for m in merges:
                            data[index][m] = ''

        result = {
            'index': indexs,
            'data': data
        }
        return result

    def format_table_width(self, rows):
        '''
        格式化表格宽度
        '''
        cols = [90, 90, 44, 29, 21, 16, 13, 11, 9, 8, 7, 6, 6, 5, 5, 4]
        result = []
        for i in range(len(rows)):
            if i == 0:
                result.append(rows[i])
            else:
                length = len(rows[i])
                sep = cols[length if length < 15 else 15]
                row = []
                for item in rows[i]:
                    if item:
                        if isinstance(item, int) or isinstance(item, float):
                            item = str(item)
                        if not isinstance(item, unicode):
                            item = unicode(item, "utf-8")
                        b = []
                        for n in range(len(item)):
                            if n % sep == 0:
                                b.append('{}\n'.format(item[n:n + sep]))
                        row.append(''.join(b))
                    else:
                        row.append(item)
                result.append(row)
        return result

    def generate_pdf(self, path, data):
        """
        生成pdf
        version 为日期版本
        """
        doc = SimpleDocTemplate(path)
        if not data:
            return ValueError("模版不存在")
        for row in data:
            if row['type'] == 'module':  # 报告名称
                time = row['params']['time'] if 'time' in row['params'] else ''
                self.create_pdf_modle(content=row['params']['title'], time=time)
            elif row['type'] == 'title1':  # 一级标题
                self.create_pdf_title(content=row['params']['title'], level=1)
            elif row['type'] == 'title2':  # 二级标题
                self.create_pdf_title(content=row['params']['title'], level=2)
            elif row['type'] == 'title3':  # 三级标题
                self.create_pdf_title(content=row['params']['title'], level=3)
            elif row['type'] == 'title4':  # 四级标题
                self.create_pdf_title(content=row['params']['title'], level=4)
            elif row['type'] == 'text':  # 正文
                self.create_pdf_text(content=row['params']['title'])
            elif row['type'] == 'echart':  # 图表
                self.create_pdf_chart(row=row)
            else:
                logger.info(row['type'])

        # save函数：保存文件并关闭canvas
        doc.build(self.content)

    def create_pdf_modle(self, content, time):
        '''
        报告名称
        '''
        temp = '<para autoLeading="off" fontSize={0} align=center><b><font face="song">{1}</font></b>'
        titles = []
        if content:
            titles.append(temp.format(str(20), content))
        if time:
            titles.append('<br/><br/>')
            titles.append(temp.format(str(14), time))
        titles.append('<br/><br/></para>')
        self.content.append(Paragraph(''.join(titles), getSampleStyleSheet()['Title']))

    def create_pdf_title(self, content, level):
        '''
        标题
        '''
        fone_size = 10
        if level == 1:
            fone_size = 15
        elif level == 2:
            fone_size = 13
        elif level == 3:
            fone_size = 11
        elif level == 4:
            fone_size = 9
        else:
            pass
        title = '<para autoLeading="off" fontSize={0} align=left>' \
                '<br/><br/>' \
                '<b><font face="song">{1}</font></b>' \
                '<br/><br/>' \
                '</para>'.format(str(fone_size), content)
        self.content.append(Paragraph(title, self.normalStyle))

    def create_pdf_text(self, content):
        '''
        正文
        '''
        title = '<para autoLeading="off" fontSize=10 align=left>' \
                '<b><font face="song">{0}</font></b>' \
                '<br/><br/><br/>' \
                '</para>'.format(content)
        self.content.append(Paragraph(title, self.normalStyle))

    def create_chart_number(self, name, data):
        '''
        计数类型
        '''
        count = 0
        for item in data['data']:
            for _ in item['data']:
                count += _
        title = '<para autoLeading="off" fontSize=10 align=left>' \
                '<b><font face="song">{0}:{1}</font></b>' \
                '<br/><br/><br/>' \
                '</para>'.format(name, str(count))
        self.content.append(Paragraph(title, self.normalStyle))

    def create_pdf_chart(self, row):
        if row['chart_type'] == 'table':  # 表格类型
            self.add_table(name=row['name'], data=row['data'], data_type=row['data_type'])
        elif row['chart_type'] == 'table_merge':  # 合并表格类型
            data = copy.deepcopy(row)
            self.add_table_merge(data=data['data'], merges=data['merges'])
        elif row['chart_type'] == 'number':  # 计数
            self.create_chart_number(name=row['name'], data=row['data'])
        else:
            if 'has_table' in row and row['has_table']:
                table_data = row['data']
            else:
                table_data = None
            if 'data_type' in row and row['data_type']:
                data_type = row['data_type']
            else:
                data_type = None
            self.generate_section(title=row['name'],
                                  desc=row['description'],
                                  remark=row['remark'],
                                  chart=row['chart_path'],
                                  table_data=table_data,
                                  data_type=data_type)
