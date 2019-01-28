# coding: utf-8
"""
datatable
"""
import logging
import sys
import time
import elasticsearch
from django.conf import settings
from django.db.models import Q
from django.views.debug import ExceptionReporter
from rest_framework.views import APIView
from django_datatables_view.base_datatable_view import BaseDatatableView
from django_datatables_view.mixins import JSONResponseView
from utils.es import get_by_any
from utils.files import excel_export
from utils.message import notify_administrator
logger = logging.getLogger("soc_datatable")


class DatatableView(BaseDatatableView, APIView):
    """
    基础列表
    处理功能:
        1. 处理前后端变量对应关系
    """
    # 前后端转换的对应关系, 如果没有指定, 默认返回查询到的结果的全部
    render_columns = []

    # 递归查询
    key_model = {}

    # search_by_es
    enable_es = False
    es_result = []

    # 自定义模板
    custom_template = False

    def search_from_es(self, qs):
        return []

    def query_dict(self):
        if self.request.method == 'POST':
            return self.request.POST
        else:
            return self.request.GET

    def get_render_columns(self):
        return self.render_columns

    def get_columns(self):
        """ Returns the list of columns that are returned in the result set
        """
        r_columns = [r_column[1] for r_column in self.get_render_columns()]
        return r_columns if r_columns else self.columns

    def get_request_columns(self):
        """获取前端可以请求的参数列表
        """
        r_columns = [r_column[0] for r_column in self.get_render_columns()]
        return r_columns if r_columns else self.columns

    def get_searchable_columns(self):
        """返回服务器端限制的搜索可否列表
        默认可以搜索
        ("id", "id") => 可以搜索
        ("id", "id", 0) => 不可搜索
        ("id", "id", 1) => 可以搜索
        ("id", "id", 2) => 待定
        """
        r_columns = [r_column[2] if len(
            r_column) == 3 else 1 for r_column in self.get_render_columns()]
        return r_columns

    def get_key_model(self):
        """ 获取表名和 Model 名对应
        """
        return self.key_model

    def get_order_columns(self):
        """ Return list of columns used for ordering
        """
        if not self.order_columns:
            self.order_columns = self.get_columns()
        return self.order_columns

    def render_dict(self, old_dict):
        """
        {
            "dict1": { "key1": "value1", }
        }
        =>
        {
            "dict1__key1": "value1"
        }
        """

        if not type(old_dict) is dict:
            pass
        new_dict = dict()
        for key, val in old_dict.iteritems():
            if type(val) is dict:
                for sub_key, sub_val in val.iteritems():
                    new_dict[key + '__' + sub_key] = sub_val
            else:
                new_dict[key] = val
        return new_dict

    def custom_filter_queryset(self, qs, search):
        """自定义过滤
        """
        return ""

    def filter_queryset(self, qs):
        """ If search['value'] is provided then filter all searchable columns using '__icontains'
        """
        if not self.pre_camel_case_notation:
            q_search = ''
            # get global search value
            search = self.request.data.get('search[value]', None)
            col_data = self.extract_datatables_column_data()
            q = Q()
            columns = self.get_columns()
            searchable_columns = self.get_searchable_columns()
            once = True
            for col_no, col in enumerate(col_data):
                once = False
                # apply global search to all searchable columns
                if searchable_columns[col_no] == 2:
                    q_search = self.custom_filter_queryset(qs, search)
                    continue
                # 判断是否可以搜索(服务器端)
                if searchable_columns[col_no] == 0:
                    continue
                if search and col['searchable']:
                    q |= Q(
                        **{'{0}__icontains'.format(columns[col_no].replace('.', '__')): search})

                # column specific filter
                if col['search.value']:
                    qs = qs.filter(
                        **{'{0}__icontains'.format(columns[col_no].replace('.', '__')): col['search.value']})
            if search and once:
                for idx, val in enumerate(searchable_columns):
                    if searchable_columns[idx] == 1:
                        q |= Q(
                            **{'{0}__icontains'.format(columns[idx].replace('.', '__')): search})

            qs = qs.filter(q)
            if q_search:
                qs |= q_search
        return qs

    def ordering(self, qs):
        """ Get parameters from the request and prepare order by clause
        """

        # Number of columns that are used in sorting
        sorting_cols = 0
        if self.pre_camel_case_notation:
            try:
                sorting_cols = int(self._querydict.get('iSortingCols', 0))
            except ValueError:
                sorting_cols = 0
        else:
            sort_key = 'order[{0}][column]'.format(sorting_cols)
            while self.request.DATA.has_key(sort_key):
                sorting_cols += 1
                sort_key = 'order[{0}][column]'.format(sorting_cols)

        order = []
        order_columns = self.get_order_columns()
        request_columns = self.get_request_columns()

        for i in range(sorting_cols):
            # sorting column
            sort_dir = 'asc'
            sortable = self.request.DATA.get(
                'columns[{0}][orderable]'.format(i))
            if not sortable == 'true':
                continue
            try:
                if self.pre_camel_case_notation:
                    sort_col = int(self._querydict.get(
                        'iSortCol_{0}'.format(i)))
                    # sorting order
                    sort_dir = self._querydict.get('sSortDir_{0}'.format(i))
                else:
                    sort_col = int(self.request.DATA.get(
                        'order[{0}][column]'.format(i)))
                    # sorting order
                    sort_dir = self.request.DATA.get(
                        'order[{0}][dir]'.format(i))
            except ValueError:
                sort_col = 0

            sdir = '-' if sort_dir == 'desc' else ''
            column_name = self.request.DATA.get(
                'columns[{0}][data]'.format(sort_col))
            column_index = request_columns.index(column_name)
            # sortcol = order_columns[sort_col]
            sortcol = order_columns[column_index]

            if isinstance(sortcol, list):
                for sc in sortcol:
                    order.append('{0}{1}'.format(sdir, sc.replace('.', '__')))
            else:
                order.append('{0}{1}'.format(sdir, sortcol.replace('.', '__')))

        if order:
            return qs.order_by(*order)
        return qs

    def get_queryset(self):
        """
        做之前 get 的事情, 返回 QuerySet 列表.
        """
        return self.model.objects.all()

    def get_initial_queryset(self):
        if not self.model:
            raise NotImplementedError(
                "Need to provide a model or implement get_initial_queryset!")
        return self.model.objects.all()

    def render_column(self, row, column):
        """ Renders a column on a row
        """
        if hasattr(row, 'get_%s_display' % column):
            # It's a choice field
            text = getattr(row, 'get_%s_display' % column)()
        else:
            # 外键方向查询
            if column.split('.')[0].endswith("_set"):
                obj = row
                if obj is not None:
                    parts = column.split('.')
                    if len(parts) == 2:
                        obj = getattr(obj, parts[0], None)
                        if obj is not None:
                            obj = obj.values(parts[1])
                        else:
                            obj = []
                        # obj = [sl[parts[1]] for sl in set_list]
                    if len(parts) == 1:
                        if self.get_key_model():
                            filters = getattr(
                                self.get_key_model(), parts[0][:-4], None)
                            if not isinstance(filters, list):
                                if filters is None:
                                    filters = []
                                else:
                                    filters = [filters]
                            if len(filters) == 2:
                                filters = filters[1]
                                obj = getattr(obj, parts[0]).values(*filters)
                            else:
                                obj = getattr(obj, parts[0]).values()
                        else:
                            obj = getattr(obj, parts[0]).values()
                    obj = list(obj)
                text = obj
            else:
                # 获取值
                try:
                    text = getattr(row, column)
                except AttributeError:
                    obj = row
                    for part in column.split('.'):
                        if obj is None:
                            break
                        obj = getattr(obj, part)
                    text = obj

        if text is None:
            # 尝试用外键
            text = self.none_string

        if text and hasattr(row, 'get_absolute_url'):
            return '<a href="%s">%s</a>' % (row.get_absolute_url(), text)
        else:
            return text

    def paging(self, qs):
        """ Paging
        """
        if self.pre_camel_case_notation:
            limit = min(int(self._querydict.get(
                'iDisplayLength', 10)), self.max_display_length)
            start = int(self._querydict.get('iDisplayStart', 0))
        else:
            limit = min(int(self.request.data.get('length', 10)),
                        self.max_display_length)
            start = int(self.request.data.get('start', 0))

        # if pagination is disabled ("paging": false)
        if limit == -1:
            return qs

        offset = start + limit

        return qs[start:offset]

    def prepare_results(self, qs):
        """
        格式化输出形式, 最终输出的 data(>1.10)/aaData
        """
        data = []
        # 有 column 的话返回对应 column 值字典
        columns = self.get_columns()
        for item in qs:
            data_dict = {
                self.render_columns[columns.index(column)][0]: self.render_column(item, '.'.join(column.split('__')))
                for column in columns
            }
            data_dict = self.prepare_one_result(item, data_dict)
            data.append(data_dict)
        return data

    def prepare_one_result(self, item, data_dict):
        """
        格式化输出每一个形式
        :param item: 每一条数据对象
        :param data_dict: 每一条数据待修改
        :return: 修改后的数据
        """
        return data_dict

    def handle_custom_template(self):
        return (), ()

    def get_context_data(self, *args, **kwargs):
        try:
            self.initialize(*args, **kwargs)

            qs = self.get_initial_queryset()

            # number of records before filtering
            total_records = qs.count()

            qs = self.filter_queryset(qs)

            # number of records after filtering
            total_display_records = qs.count()

            qs = self.ordering(qs)
            # 导出多少条日志
            download_numbers = self.request.DATA.get("download_numbers", 0)
            if download_numbers != 0:
                qs = qs[:int(download_numbers)]
            else:
                qs = self.paging(qs)
            if self.enable_es:
                self.es_result = self.search_from_es(qs)

            # prepare output data
            if self.pre_camel_case_notation:
                aaData = self.prepare_results(qs)

                ret = {
                    'sEcho': int(self._querydict.get('sEcho', 0)),
                    'iTotalRecords': total_records,
                    'iTotalDisplayRecords': total_display_records,
                    'aaData': aaData
                }
            else:
                data = self.prepare_results(qs)

                ret = {
                    'draw': int(self._querydict.get('draw', 0)),
                    'recordsTotal': total_records,
                    'recordsFiltered': total_display_records,
                    'data': data
                }
        except Exception as e:
            logger.error(e.message, exc_info=True)

            if settings.DEBUG:
                reporter = ExceptionReporter(None, *sys.exc_info())
                text = "\n" + reporter.get_traceback_text()
            else:
                reporter = ExceptionReporter(None, *sys.exc_info())
                err_text = "\n" + reporter.get_traceback_text()
                notify_administrator(content=err_text, title='Datatable错误')
                text = "\nAn error occured while processing an AJAX request."
            if self.pre_camel_case_notation:
                ret = {'result': 'error',
                       'sError': text,
                       'text': text,
                       'aaData': [],
                       'sEcho': int(self._querydict.get('sEcho', 0)),
                       'iTotalRecords': 0,
                       'iTotalDisplayRecords': 0, }
            else:
                ret = {'error': text,
                       'data': [],
                       'recordsTotal': 0,
                       'recordsFiltered': 0,
                       'draw': int(self._querydict.get('draw', 0))}

        if self.request.DATA.get("dts_download", 0) == 1:

            datatable = ret.get("data", []) or ret.get("aaData", [])
            filename = getattr(self.request, "filename", "数据表")
            filename = filename + "_%s.xls"
            filename = filename % int(time.time())
            if self.custom_template:
                labels, headers = self.handle_custom_template()
            else:
                labels = getattr(self.request, "labels", ())
                headers = getattr(self.request, "headers", ())
            file_path = excel_export(filename, labels, headers, datatable)
            file_path = "http://%s/%s" % (
                self.request.META.get('HTTP_HOST'), file_path)
            # ret = dict()
            ret["status"] = 200
            ret["msg"] = "下载成功"
            ret["file_path"] = file_path
            min_len = min(len(datatable), 10)
            if min_len:
                ret["data"] = []
        return ret

    def get(self, request, *args, **kwargs):
        response = super(DatatableView, self).get(request, *args, **kwargs)
        response.renderer_context = {"view": self.__class__}
        return response


class EsDatatableMixin(object):
    """ JSON data for datatables
    """
    # 文档类型
    doc_type = ""
    # 索引名
    index = ""

    q = ""  # - 查询指定匹配, 使用Lucene查询语法
    from_ = 0  # - 查询起始点, 默认0
    size = ""  # - 指定查询条数默认10
    field = ""  # - 指定字段,逗号分隔
    sort = "asc"  # - 排序字段：asc / desc
    body = ""  # - 使用Query DSL
    scroll = ""  # - 滚动查询

    # 查询字典
    es_query_dict = dict()
    # 查询json
    es_query_json = dict()

    # max limit of records returned, do not allow to kill our server by huge sets of data
    max_display_length = 100
    # datatables 1.10 changed query string parameter names
    pre_camel_case_notation = False
    none_string = ''
    # 前后端转换的对应关系, 如果没有指定, 默认返回查询到的结果的全部
    render_columns = []
    order_columns = []

    @property
    def querydict(self):
        if self.request.method == 'POST':
            return self.request.POST
        else:
            return self.request.GET

    def initialize(self, *args, **kwargs):
        """
        新旧版本
        """
        if 'iSortingCols' in self.querydict:
            self.pre_camel_case_notation = True

    def get_render_columns(self):
        """
        获取render_columns
        :return:
        """
        return self.render_columns

    def get_request_columns(self):
        """获取前端可以请求的参数列表, 即 render_columns 第一列
        """
        r_columns = [r_column[0] for r_column in self.get_render_columns()]
        return r_columns if r_columns else []

    def get_response_columns(self):
        """ Returns the list of columns that are returned in the result set
        返回结果中需要的字段, 即 render_columns 第二列
        """
        r_columns = [r_column[1] for r_column in self.get_render_columns()]
        return r_columns if r_columns else []

    def get_searchable_columns(self):
        """返回服务器端限制的搜索可否列表, 即 render_columns 第三列
        默认可以搜索,
        ("id", "id", 0) => 不可搜索
        ("id", "id", 1) => 可以搜索
        ("id", "id", 2) => 待定
        """
        r_columns = [r_column[2] if len(
            r_column) == 3 else 1 for r_column in self.get_render_columns()]
        return r_columns

    def get_order_columns(self):
        """ Return list of columns used for ordering
        """
        if not self.order_columns:
            self.order_columns = self.get_response_columns()
        return self.order_columns

    def get_queryset(self):
        """
        做之前 get 的事情, 返回 QuerySet 列表.
        """
        return self.none_string

    def get_initial_queryset(self):
        # if not self.model:
        #     raise NotImplementedError("Need to provide a model or implement get_initial_queryset!")
        return self.none_string

    def ordering(self):
        """ Get parameters from the request and prepare order by clause
        从请求中获取可以排序的参数, 并写好排序列表
        """

        order_list = []

        # Number of columns that are used in sorting
        sorting_cols = 0
        if self.pre_camel_case_notation:
            try:
                sorting_cols = int(self.querydict.get('iSortingCols', 0))
            except ValueError:
                sorting_cols = 0
        else:
            sort_key = 'order[{0}][column]'.format(sorting_cols)
            while sort_key in self.querydict:
                sorting_cols += 1
                sort_key = 'order[{0}][column]'.format(sorting_cols)

        order_columns = self.get_order_columns()
        request_columns = self.get_request_columns()

        for i in range(sorting_cols):
            # sorting column
            sort_dir = 'asc'
            sortable = self.querydict.get('columns[{0}][orderable]'.format(i))
            if not sortable == 'true':
                # 该列不可排序
                continue
            try:
                if self.pre_camel_case_notation:
                    sort_col = int(self.querydict.get(
                        'iSortCol_{0}'.format(i)))
                    # 排序方向
                    sort_dir = self.querydict.get('sSortDir_{0}'.format(i))
                else:
                    sort_col = int(self.querydict.get(
                        'order[{0}][column]'.format(i)))
                    # 排序方向
                    sort_dir = self.querydict.get('order[{0}][dir]'.format(i))
            except ValueError:
                sort_col = 0

            # 排序方向
            column_name = self.querydict.get(
                'columns[{0}][data]'.format(sort_col))

            column_index = request_columns.index(column_name)
            sortcol = order_columns[column_index]

            if isinstance(sortcol, list):
                for sc in sortcol:
                    order_list.append(
                        {
                            sc: {
                                "order": sort_dir
                            }
                        }
                    )
            else:
                order_list.append(
                    {
                        sortcol: {
                            "order": sort_dir
                        }
                    }
                )
                self.es_query_dict["sort_field"] = sortcol
                self.es_query_dict["sort_model"] = sort_dir

        if order_list:
            self.es_query_json["sort"] = order_list

        return order_list

    def paging(self):
        """ 分页
        """

        if self.pre_camel_case_notation:
            limit = min(int(self.querydict.get('iDisplayLength', 10)),
                        self.max_display_length)
            start = int(self.querydict.get('iDisplayStart', 0))
        else:
            limit = min(int(self.querydict.get('length', 10)),
                        self.max_display_length)
            start = int(self.querydict.get('start', 0))

        # 不分页 ("paging": false)
        if limit == -1:
            pass
        # offset = start + limit
        self.es_query_dict["page"] = start / limit + 1
        self.es_query_dict["per_page_count"] = limit
        # self.es_query_dict["from_"] = start
        # self.es_query_dict["size"] = limit

        return start, limit

    def extract_datatables_column_data(self):
        """ Helper method to extract columns data from request as passed by Datatables 1.10+
        获取所有请求字段的数据
        """
        request_dict = self.querydict
        col_data = []
        if not self.pre_camel_case_notation:
            counter = 0
            data_name_key = 'columns[{0}][name]'.format(counter)
            while data_name_key in request_dict:
                searchable = True if request_dict.get(
                    'columns[{0}][searchable]'.format(counter)) == 'true' else False
                orderable = True if request_dict.get(
                    'columns[{0}][orderable]'.format(counter)) == 'true' else False

                col_data.append({
                    'name': request_dict.get(data_name_key),
                    'data': request_dict.get('columns[{0}][data]'.format(counter)),
                    'searchable': searchable,
                    'orderable': orderable,
                    'search.value': request_dict.get('columns[{0}][search][value]'.format(counter)),
                    'search.regex': request_dict.get('columns[{0}][search][regex]'.format(counter)),
                })
                counter += 1
                data_name_key = 'columns[{0}][name]'.format(counter)
        return col_data

    def filter_queryset(self):
        """ If search['value'] is provided then filter all searchable columns using '__icontains'
        搜索
        """
        must_list = []
        if not self.pre_camel_case_notation:

            # 全局搜索字段
            global_search = self.querydict.get(
                'search[value]', self.none_string)
            if global_search:
                self.es_query_dict["query_str"] = global_search
                must_list.append({
                    "query_string": {
                        "query": "*" + global_search + "*",
                    }
                })

            # 分字段搜索
            col_data = self.extract_datatables_column_data()
            request_colums = self.get_request_columns()
            response_columns = self.get_response_columns()
            # 是否服务器可查询(如果前端可查询设置错误)
            searchable_columns = self.get_searchable_columns()
            for col_no, col in enumerate(col_data):
                try:
                    index = request_colums.index(col["data"])
                except ValueError:
                    continue

                # 对所有可搜索的字段进行搜索
                # if searchable_columns[col_no] == 2:
                #     q_search = self.custom_filter_queryset(global_search)
                #     continue
                # 判断是否可以搜索(服务器端)
                if not searchable_columns[index]:
                    continue

                # 全局搜并且该字段可以搜索
                # if global_search and col['searchable']:
                #     q |= Q(**{'{0}__icontains'.format(response_columns[col_no].replace('.', '__')): global_search})

                # column specific filter
                if col['searchable'] and col['search.value']:
                    must_list.append(
                        {"match": {response_columns[index]: col['search.value']}})
                    self.es_query_dict[response_columns[index]] = col['search.value']
            if must_list:
                self.es_query_json["query"] = {
                    "bool": {
                        "must": must_list
                    }
                }
        return must_list

    def custom_filter_queryset(self, qs, search):
        """自定义锅过滤
        """
        return ""

    def prepare_results(self, qs):
        """
        格式化输出形式, 最终输出的 data(>1.10)/aaData
        """
        data = []
        response_columns = self.get_response_columns()
        for item in qs:
            data_dict = dict()
            len_response_columns = len(response_columns)
            for i in range(len_response_columns):
                data_dict[self.render_columns[i][0]] = item.get(
                    response_columns[i], "")
            # 可以添加其他处理条件 2016-07-15T19:32:04.947028

            data.append(data_dict)
        return data

    def get_context_data(self, *args, **kwargs):
        try:
            self.es_query_dict = dict()
            self.doc_type = ""
            # 新旧版本区分 √
            self.initialize(*args, **kwargs)
            # 不知道要做什么先
            qs = self.get_initial_queryset()

            # 添加过滤条件 √
            self.filter_queryset()

            # 排序字典 √
            self.ordering()
            # 分页 √
            self.paging()

            # 加index
            self.es_query_dict["index"] = self.index

            # 从es获取数据
            result = get_by_any(**self.es_query_dict)

            # 获取查询结果集
            all_hits = result['hits']['hits']

            qs = [ah['_source'] for ah in all_hits]

            # 总条数
            total_records = result['hits']['total']
            # 总显示条数
            total_display_records = total_records

            # 处理数据 √
            output_data = self.prepare_results(qs)

            if self.pre_camel_case_notation:

                ret = {
                    'sEcho': int(self.querydict.get('sEcho', 0)),
                    'iTotalRecords': total_records,
                    'iTotalDisplayRecords': total_display_records,
                    'aaData': output_data
                }
            else:

                ret = {
                    'draw': int(self.querydict.get('draw', 0)),
                    'recordsTotal': total_records,
                    'recordsFiltered': total_display_records,
                    'data': output_data
                }
        except (Exception, elasticsearch.TransportError, elasticsearch.NotFoundError) as e:
            logger.exception(str(e))

            if settings.DEBUG:
                reporter = ExceptionReporter(None, *sys.exc_info())
                text = "\n" + reporter.get_traceback_text()
            else:
                reporter = ExceptionReporter(None, *sys.exc_info())
                err_text = "\n" + reporter.get_traceback_text()
                notify_administrator(content=err_text, title='Datatable错误')
                text = "\nAn error occured while processing an AJAX request."

            if self.pre_camel_case_notation:
                ret = {
                    'result': 'error',
                    'sError': text,
                    'text': text,
                    'aaData': [],
                    'sEcho': int(self.querydict.get('sEcho', 0)),
                    'iTotalRecords': 0,
                    'iTotalDisplayRecords': 0,
                }
            else:
                ret = {
                    'data': [],
                    'recordsTotal': 0,
                    'recordsFiltered': 0,
                    'draw': int(self.querydict.get('draw', 0))}
                if settings.DEBUG:
                    ret["error"] = text

        return ret

    def perdelta(self, start, end, delta):
        """
        从start到end,每隔delta
        """
        curr = start
        while curr <= end:
            yield curr
            curr += delta


class EsDatatableView(EsDatatableMixin, JSONResponseView, APIView):
    """Datatable with ES backend
    """
    pass
