# coding=utf-8
from __future__ import unicode_literals


class BaseData(object):
    """数据基类"""

    def __init__(self, top="", term="", cycle=""):
        self.top = top
        self.term = term
        self.cycle = cycle

    def data(self):
        """
        实体数据
        """
        data = {
            "labels": ['2018-04-10', '2018-04-11', '2018-04-12', '2018-04-13', '2018-04-14'],
            "data": [
                {"name": "张三", "data": [11, 55, 99, 13, 13]},
                {"name": "李四", "data": [11, 55, 99, 13, 13]},
                {"name": "王五", "data": [11, 55, 99, 13, 13]},
            ]

        }
        return data

    def structure_term_sql_param(self):
        if self.term != "" and len(self.term) > 0 and self.term[0]['id'] != '-1':
            term = " and term_group_id in (" + ','.join([item['id'] for item in self.term]) + ")"
        else:
            term = ""
        if self.top != "":
            top = "limit " + str(self.top)
        else:
            top = ""
        return term, top


if __name__ == "__main__":
    pass
