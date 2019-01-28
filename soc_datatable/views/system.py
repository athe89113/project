# coding: utf-8
import logging
from soc.models import SocLog
from django.utils import timezone
from common import soc_system_log
from utils.ip import find_ip_location
from utils.datatable import DatatableView

logger = logging.getLogger("soc_datatable")
console = logging.getLogger("django")


class Soclog(DatatableView):
    """操作日志记录"""
    model = SocLog
    log_type = 0
    user_type = 0
    render_columns = [
        ("username", "user__username"),
        ("ip", "ip"),
        ("company", "company__name"),
        ("info", 'info', 1),
    ]
    custom_template = True

    def log(self):
        pass

    def get_initial_queryset(self):
        # 日志类型 1操作日志 2登陆日志
        self.log_type = int(self.request.data.get("log_type", 0))
        # 用户类型 2机房 3用户
        self.user_type = int(self.request.data.get("user_type", 0))

        agent = self.request.user.userinfo.agent
        company = self.request.user.userinfo.company
        if self.user_type == 2:
            # 机房日志
            logobjs = SocLog.objects.filter(agent=agent, logtype=self.log_type, company=None).order_by('-create_time')
        elif self.user_type == 3:
            # 操作日志
            logobjs = SocLog.objects.filter(agent=agent, logtype=self.log_type).exclude(company=None).order_by('-create_time')
        else:
            logobjs = []

        soc_system_log(category='系统管理-日志审计',
                       info='查询{0}{1}审计日志'.format({2: "机房", 3: "用户"}.get(self.user_type),
                                                  {1: "操作", 2: "登录"}.get(self.log_type)),
                       request=self.request, url=self.request.path)
        return logobjs

    def prepare_results(self, qs):
        """
        qs 为查询集合
        """
        data = []
        # 有 column 的话返回对应 column 值字典
        columns = self.get_columns()
        for item in qs:
            data_dict = {
                self.render_columns[columns.index(column)][0]: self.render_column(item, '.'.join(column.split('__')))
                for column in columns
            }
            temp = {
                "username": item.user.username,
                "datetime": timezone.localtime(item.create_time).strftime("%Y-%m-%d %H:%M:%S"),
                "ip": item.ip,
                "address": find_ip_location(item.ip),
                "info": item.info,
                "id": item.id
            }

            if self.user_type == 3:
                # 如果是普通用户 添加公司类
                temp["company"] = item.company.name
            if self.log_type == 2:
                # 如果是登陆日志 添加状态类
                temp["status"] = {1: "成功", 2: "失败"}.get(item.login_status, '')
            # temp.update(data_dict)
            data.append(temp)
        return data

    def handle_custom_template(self):
        # 日志类型 1操作日志 2登陆日志
        log_type = int(self.request.data.get("log_type", 0))
        # 用户类型 2机房 3用户
        user_type = int(self.request.data.get("user_type", 0))

        labels = tuple()
        headers = tuple()
        if user_type == 2:
            # 机房日志
            if log_type == 1:
                labels = ('用户名', '操作时间', '操作IP', '操作地点', '操作内容')
                headers = ('username', 'datetime', 'ip', 'address', 'info')
            elif log_type == 2:
                labels = ('用户名', '登录时间', '登录IP', '登录地点', '状态')
                headers = ('username', 'datetime', 'ip', 'address', 'status')
        elif user_type == 3:
            # 用户日志
            if log_type == 1:
                labels = ('用户名', '公司', '操作时间', '操作IP', '操作地点', '操作内容')
                headers = ('username', 'company', 'datetime', 'ip', 'address', 'info')
            elif log_type == 2:
                labels = ('用户名', '公司', '登录时间', '登录IP', '登录地点', '状态')
                headers = ('username', 'company', 'datetime', 'ip', 'address', 'status')
        soc_system_log(category='系统管理-日志审计',
                       info='下载{0}{1}审计日志'.format({2: "机房", 3: "用户"}.get(user_type),
                                                  {1: "操作", 2: "登录"}.get(log_type)),
                       request=self.request, url=self.request.path)
        return labels, headers
