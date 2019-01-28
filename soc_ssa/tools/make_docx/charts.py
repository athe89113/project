# coding=utf-8
# pip install matplotlib==2.2.2
# pip install python-docx==0.8.6
from __future__ import unicode_literals
import os
import copy
import time
import random

import numpy as np

try:
    import matplotlib

    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    plt.rcParams['font.sans-serif'] = ['SimHei']
    # plt.rcParams['font.family'] = ['STFangsong']
except ImportError:
    print("Please Install matplotlib")

PIE_COLORS = ['#00bd85', '#e96157', '#dabb61', '#0c67ff',
              '#4a92ff', '#8375d0', '#5dc962', '#008974']

BAR_X_COLOR = '#4a92ff'
BAR_Y_COLOR = '#4a92ff'

LINE_COLORS = ['#00bd85', '#4a92ff', '#dabb61', '#0c67ff',
               '#4a92ff', '#8375d0', '#5dc962', '#008974']


class Charts(object):
    """
    通过ES中数据生成图表
    """

    def __init__(self, data, title, unit, figsize=(6, 4)):
        self._data = data
        self.title = title
        self.index = 0
        self.plt = plt
        self.unit = unit

        self.plt.figure(figsize=figsize)
        # plt.figure(figsize=(6, 9))

    @property
    def data(self):
        return copy.deepcopy(self._data)

    @property
    def pie_data(self):
        """
        转为饼图数据
        """
        all_data = self.data
        label = all_data['labels']
        data = all_data['data']

        # 数据类型超过1个按 数据类型 否则按时间
        if len(data) > 1:
            label = []
            pie_data = []
            for i in data:
                label.append(i['name'])
                pie_data.append(sum(i['data']))
        else:
            pie_data = [0 for i in range(len(label))]
            for _d in data:
                _l = _d['data']
                for index, num in enumerate(pie_data):
                    pie_data[index] = _l[index] + num

        data = {
            "labels": label,
            "data": pie_data
        }
        return data

    def get_unit(self, data):
        '''
        获取计量单位
        '''
        unit, u = '', 1
        if len(data) > 0:
            data_list = []
            for item in data:
                data_list = data_list + item['data']
            if data_list:
                max_ = max(data_list)
            else:
                max_ = 0
            # 流量
            if self.unit and self.unit == 'band':
                if max_ and (isinstance(max_, int) or isinstance(max_, float) or isinstance(max_, long)):
                    if max_ < 1024:
                        unit = u'b'
                        u = 1
                    elif max_ < (1024 * 1024) and max_ >= 1024:
                        unit = u'Kb'
                        u = 1024
                    elif max_ < (1024 * 1024 * 1024) and max_ >= (1024 * 1024):
                        unit = u'Mb'
                        u = 1024 * 1024
                    elif max_ > (1024 * 1024 * 1024):
                        unit = u'Gb'
                        u = 1024 * 1024 * 1024
                    else:
                        pass
            else:  # 次数
                if max_ and (isinstance(max_, int) or isinstance(max_, float) or isinstance(max_, long)):
                    if max_ < 100000000 and max_ >= 10000:
                        unit = u'万'
                        u = 10000
                    elif max_ < 1000000000000 and max_ >= 100000000:
                        unit = u'亿'
                        u = 100000000
                    elif max_ > 1000000000000:
                        unit = u'万亿'
                        u = 1000000000000
                    else:
                        pass
            if unit:
                for item in data:
                    for i in range(len(item['data'])):
                        val = item['data'][i]
                        item['data'][i] = round(val / u, 0)
        return unit, data

    def number_data(self):
        """
        转为总数
        """
        data = self.pie_data
        data['labels'] = "{} ~ {}".format(data['labels'][0], data['labels'][-1])
        data['data'] = sum(data['data'])
        return data

    def table_data(self):
        """
        转为表格
        """
        return self.data

    def bar_x(self):
        """
        峰柱状图 柱状图
        """
        labels = self.data['labels']
        unit, data = self.get_unit(self.data['data'])
        width = 0.2
        fig, ax = self.plt.subplots()
        plt.title(self.title)
        for index, i in enumerate(data):
            col = index % len(PIE_COLORS)
            if index == 0:
                tmp_list = list(range(len(labels)))
                ax.bar(tmp_list, i['data'], width=width, color=PIE_COLORS[col], label=i['name'])
            else:
                tmp_list = [k + index * width for k in range(len(labels))]
                ax.bar(tmp_list, i['data'], width=width,
                       color=PIE_COLORS[col], tick_label=labels, label=i['name'])
        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels)
        if unit:
            ax.set_ylabel('单位({0})'.format(unit))
        fig.autofmt_xdate()
        plt.legend()
        return self

    def bar_pile_x(self):
        """
        堆叠柱状图
        """

        labels = self.data['labels']
        unit, data = self.get_unit(self.data['data'])
        fig, ax = plt.subplots()
        plt.title(self.title)
        bottom_data = []

        for index, i in enumerate(data):
            index = index % len(PIE_COLORS)
            tmp_list = [0 for k in range(len(i['data']))]
            if index == 0:
                bottom_data.append([0 for k in range(len(i['data']))])
                for k in range(len(i['data'])):
                    tmp_list[k] = i['data'][k]
                ax.bar(range(len(i['data'])), i['data'], label=i['name'], facecolor=PIE_COLORS[index])
            else:
                for k in range(len(i['data'])):
                    tmp_list[k] = bottom_data[index][k] + i['data'][k]
                ax.bar(range(len(i['data'])), i['data'], bottom=bottom_data[index], tick_label=labels,
                       label=i['name'], facecolor=PIE_COLORS[index])
            bottom_data.append(tmp_list)
        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels)
        if unit:
            ax.set_ylabel('单位({0})'.format(unit))
        fig.autofmt_xdate()
        plt.legend()
        return self

    def bar_y(self):
        """
        岭柱状图 条形图
        """

        unit, data = self.get_unit(self.data['data'])
        labels = self.data['labels']

        fig, ax = plt.subplots()
        fig.set_size_inches(12, 8, forward=True)
        plt.title(self.title)
        height = 0.2

        for index, i in enumerate(data):
            col = index % len(PIE_COLORS)
            if index == 0:
                tmp_list = list(range(len(labels)))
                ax.barh(tmp_list, i['data'], color=PIE_COLORS[col], height=height, label=i['name'])
            else:
                tmp_list = [k + index * height for k in range(len(labels))]
                ax.barh(tmp_list, i['data'], color=PIE_COLORS[col], height=height,
                        tick_label=labels, label=i['name'])
        ax.set_yticks(range(len(labels)))
        ax.set_yticklabels(labels)
        ax.invert_yaxis()
        if unit:
            ax.set_xlabel('单位({0})'.format(unit))
        plt.legend()
        return self

    def bar_pile_y(self):
        """
        堆叠条形图
        """
        labels = self.data['labels']
        unit, data = self.get_unit(self.data['data'])

        fig, ax = plt.subplots()
        fig.set_size_inches(12, 8, forward=True)
        '''
        if len(labels) > 30 and len(labels) <= 70:
            fig.set_size_inches(12, 10, forward=True)
        elif len(labels) > 70:
            fig.set_size_inches(12, 16, forward=True)
        '''
        plt.title(self.title)

        bottom_data = []
        for index, i in enumerate(data):
            index = index % len(PIE_COLORS)
            tmp_list = [0 for k in range(len(i['data']))]
            if index == 0:
                bottom_data.append([0 for k in range(len(i['data']))])
                for k in range(len(i['data'])):
                    tmp_list[k] = i['data'][k]

                ax.barh(range(len(i['data'])), i['data'], label=i['name'], facecolor=PIE_COLORS[index])
            else:
                for k in range(len(i['data'])):
                    tmp_list[k] = bottom_data[index][k] + i['data'][k]

                ax.barh(range(len(i['data'])), i['data'], label=i['name'], facecolor=PIE_COLORS[index],
                        left=bottom_data[index], tick_label=labels)
            bottom_data.append(tmp_list)
        ax.set_yticks(range(len(labels)))
        ax.set_yticklabels(labels)
        ax.invert_yaxis()
        if unit:
            ax.set_xlabel('单位({0})'.format(unit))
        plt.legend()
        return self

    def pie(self):
        """
        饼图
        :data [12, 10, 33]
        :labels [u'第一', u'第二', u'第三']
        """
        data = self.pie_data['data']
        labels = self.pie_data['labels']
        plt.figure(figsize=(8, 6))
        plt.title(self.title)
        _, l_text, p_text = plt.pie(data, explode=None, labels=labels, colors=PIE_COLORS,
                                    labeldistance=0.8, autopct='%3.1f%%', shadow=False,
                                    startangle=90, pctdistance=0.6, wedgeprops={'linewidth': 3})

        for t in l_text:
            t.set_size = (30)
        for t in p_text:
            t.set_size = (20)
        # 设置x，y轴刻度一致，这样饼图才能是圆的
        plt.axis('equal')
        plt.legend()
        # plt.show()
        return self

    def line(self):
        """
        折线图
        labels: ['第一', '第二', '第三', '第四', '第五']
        data: [
            [1, 2, 3, 3, 5],
            [1, 2, 3, 3, 5],
            [1, 2, 3, 3, 5],
            [1, 2, 3, 3, 5],
            [1, 2, 3, 3, 5],
        ]
       
        
        """
        labels = self.data['labels']
        unit, data = self.get_unit(self.data['data'])
        x_labels = range(len(labels))
        fig, ax = plt.subplots()
        plt.title(self.title)
        for index, i in enumerate(data):
            index = index % len(LINE_COLORS)
            ax.plot(x_labels, i['data'], color=LINE_COLORS[index], label=i['name'], marker='o')
        ax.set_xticks(x_labels)
        ax.set_xticklabels(labels)
        if unit:
            ax.set_ylabel('单位({0})'.format(unit))

        fig.autofmt_xdate()
        plt.legend(loc='upper right')
        return self

    def table(self, line_width=1):
        """
        表格
        data: [
            [1, 2, 3, 3, 5],
            [1, 2, 3, 3, 5],
            [1, 2, 3, 3, 5],
            [1, 2, 3, 3, 5],
            [1, 2, 3, 3, 5],
        ]
        labels: ['第一', '第二', '第三', '第四', '第五']
        """

        labels = [''] + self.data['labels']
        rows = []
        for i in self.data['data']:
            rows.append([i['name']] + i['data'])

        _, ax = plt.subplots()

        ax.axis('off')
        ax.axis('tight')
        if len(rows) == 0:
            rows = [['' for i in labels]]
        t = ax.table(cellText=rows, colLabels=labels, loc='center')
        for _, cell in t.get_celld().items():
            cell.set_linewidth(line_width)
        t.set_fontsize(20)
        t.scale(1, 2)
        return self

    def number(self):
        """
        数据
        """
        return self.table(line_width=0)

    def scatter(self):
        '''
        散点图
        '''
        unit, data = self.get_unit(self.data['data'])
        labels = self.data['labels']
        plt.figure(figsize=(8, 4))
        fig, ax = plt.subplots()
        plt.title(self.title)
        for item in data:
            plt.scatter(labels, item['data'], s=30, c=random.choice(PIE_COLORS), marker='o', alpha=0.5,
                        label=item['name'])
        plt.legend(loc='upper right')
        if unit:
            ax.set_ylabel('单位({0})'.format(unit))

        return self

    def loop(self):
        '''
        圆形图
        '''
        """
        饼图
        :data [12, 10, 33]
        :labels [u'第一', u'第二', u'第三']
        """
        data = self.pie_data['data']
        labels = self.pie_data['labels']
        plt.figure(figsize=(8, 4))

        fig, ax = plt.subplots()
        plt.title(self.title)
        ax.pie(data, explode=None, labels=labels, colors=PIE_COLORS,
               labeldistance=0.8, autopct='%3.1f%%', shadow=False,
               startangle=90, pctdistance=0.6, wedgeprops={'linewidth': 3})
        ax.pie([1], radius=0.6, colors='w')
        ax.set(aspect="equal")
        # plt.legend()
        plt.legend(labels, bbox_to_anchor=(1.05, 1), borderaxespad=0.)

        # plt.show()
        return self

    def funnel(self):
        '''
        漏斗图
        '''
        return self.pie()

    def save(self):
        path = os.path.join('media', 'reports', 'tmp_imgs', "{}.png".format(time.time()))
        self.plt.savefig(path, format="png", dpi=200)
        self.index += 1
        self.plt.close()
        self.plt = ''
        return path


if __name__ == "__main__":
    x = random.randint(1, 10)
    y = random.randint(1, 6)
    data = {
        "labels": ['测试{}'.format(a) for a in range(x)],
        "data": []
    }
    for i in range(y):
        data['data'].append({
            'name': '测试数据{0}'.format(str(random.randint(100, 1000))),
            'data': [random.randint(10000, 20000) for y in range(x)]
        })
    print data
    chart = Charts(data=data, title='111111111111111', unit='number')
    chart.line().save()
