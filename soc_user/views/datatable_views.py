# coding=utf-8
from django.utils import timezone
from utils.datatable import DatatableView
from django.contrib.auth.models import User
from ..models import Company
DATIME_FORMAT = '%Y-%m-%d %H:%M:%S'

__all__ = ['UserDataTableList', 'CompanyDataTableList']


class UserDataTableList(DatatableView):
    """
    用户基本信息
    """
    render_columns = [
        ("id", "id", 0),
        ("username", "username"),
        ("email", "email"),
        ("phone", "userinfo__phone"),
        ("is_locked", "userinfo__is_locked", 0),
        ("avatar", "userinfo__avatar", 0),
        ("last_login_ip", "userinfo__last_login_ip"),
        ("is_admin", "userinfo__is_admin", 0),
        ("last_login", "last_login", 0),
        ("employee_id", "userinfo__employee_id", 1),
    ]

    def get_initial_queryset(self):
        company_id = self.request.data.get('company_id')
        agent = self.request.user.userinfo.agent
        company = self.request.user.userinfo.company
        query = User.objects.filter(userinfo__agent=agent)
        # 有company 为公司用户，获取当前公司下用户
        if company:
            query = query.filter(userinfo__company=company)
        # 无company但有company_id 参数 为代理商用户，筛选特殊公司用户
        elif company_id:
            query = query.filter(userinfo__company_id=company_id)
        # 无company 无company_id 参数 为代理商用户，不做进一步筛选
        return query

    def prepare_results(self, qs):
        """
        格式化输出形式, 最终输出的 data(>1.10)/aaData
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
            data_dict["avatar"] = data_dict["avatar"].url if data_dict["avatar"] else ''
            data_dict["lock_status"] = u"正常" if data_dict["is_locked"] == 0 else u"锁定"
            if item.last_login:
                data_dict["last_login"] = timezone.localtime(item.last_login).strftime(DATIME_FORMAT)
            else:
                pass
            if data_dict['is_admin']:
                data_dict['is_admin'] = u"管理员"
            else:
                data_dict['is_admin'] = u"用户"

            roles_obj = item.userinfo.roles.all()
            roles = []
            role_name = ''
            for i in roles_obj:
                role_name = i.name
                roles.append(
                    {
                        "id": i.id,
                        "name": i.name
                    }
                )
            if not role_name:
                role_name = '普通用户'
            data_dict['roles'] = roles
            data_dict['role_name'] = role_name
            data.append(data_dict)
        return data


class CompanyDataTableList(DatatableView):
    """获取公司信息"""
    render_columns = [
        ("id", "id", 0),
        ("id", "id", 0),
        ("name", "name"),
        ("email", "email"),
        ("phone", "phone"),
        ("address", "address"),
        ("id", "id", 0),
        ("id", "id", 0),
        ("id", "id", 0),
        ("id", "id", 0),

    ]

    def get_initial_queryset(self):
        # 在中间件中过滤
        agent = self.request.user.userinfo.agent
        company = self.request.user.userinfo.company
        query = Company.objects.filter(agent=agent)
        if company:
            query = query.filter(id=company.id)
        return query

    def prepare_results(self, qs):
        """
            格式化输出形式, 最终输出的 data(>1.10)/aaData
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
            data_dict["set_meal"] = ""
            data_dict["other_meal"] = ""
            data_dict["end_time"] = ""
            data_dict["end_days"] = ""
            data_dict["service_status"] = u"正常"
            data.append(data_dict)
        return data

