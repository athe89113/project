# coding=utf-8
from __future__ import unicode_literals
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from soc_system import models, serializers
from utils.auth import AllowAdminWithPassword


class MenuDetail(APIView):
    """
    菜单
    """

    permission_classes = (AllowAdminWithPassword,)

    def get_object(self, request, pk):
        """
        获取菜单
        :param request:
        :param pk:
        :return:
        """
        try:
            menu = models.AdvancedMenu.objects.get(id=pk, agent=request.user.userinfo.agent)
        except models.AdvancedMenu.DoesNotExist:
            menu = None
        return menu

    def get(self, request, menu_id):
        """
        获取菜单
        :param request:
        :param menu_id:
        :return:
        """
        menu = self.get_object(request, menu_id)
        if not menu:
            context = {
                "status": 500,
                "msg": "没有对应菜单",
                "error": "没有对应菜单"
            }
            return Response(context)

        data = {
            "id": menu.id,
            "name": menu.name,
            "sort": menu.sort,
            "is_landing": menu.is_landing,
            "enable": menu.enable,
        }
        context = {
            "status": 200,
            "msg": "获取菜单成功",
            "data": data
        }
        return Response(context)

    def put(self, request, menu_id):
        """
        修改菜单
        :param request:
        :param menu_id:
        :return:
        """
        menu = self.get_object(request, menu_id)
        if not menu:
            context = {
                "status": 500,
                "msg": "没有对应菜单",
                "error": "没有对应菜单"
            }
            return Response(context)

        menu_serializer = serializers.MenuSerializers(instance=menu, data=request.data, partial=True)
        if menu_serializer.is_valid():
            menu_serializer.save()
            context = {
                "status": 200,
                "msg": "修改菜单成功",
                "data": menu.get_dict()
            }
        else:
            msg = "修改菜单错误"
            for error in menu_serializer.errors:
                msg = menu_serializer.errors[error][0]
                break
            context = {
                "status": 500,
                "msg": msg,
                "error": menu_serializer.errors
            }
        return Response(context)


class MenuDetailUnlimited(APIView):
    """
    修改菜单启用状态
    """

    def put(self, request, menu_id):
        """
        修改菜单启用状态
        :param request:
        :param menu_id:
        :return:
        """
        # 非代理商管理员无法操作
        if not (request.user.userinfo.role_type in [1, 2] and request.user.userinfo.is_admin):

            return Response({
                "status": 403,
                "msg": "您无权操作",
                "error": "您无权操作"
            })
        return MenuDetail().put(request=request, menu_id=menu_id)


class MenuList(APIView):
    """
    菜单列表
    """
    permission_classes = (AllowAdminWithPassword,)

    def get(self, request):
        """
        获取所有菜单列表
        :param request:
        :return:
        """
        agent_now = request.user.userinfo.agent
        menu_type = request.query_params.get("type", "all")
        company = request.user.userinfo.company

        # 创建默认的数据
        default_menu_ids = models.AdvancedMenu.objects.filter(agent=agent_now, type='default').values_list("default_menu_id", flat=True)
        default_menus = models.DefaultMenu.objects.exclude(id__in=default_menu_ids)
        if default_menus:
            menu_list = []
            for dm in default_menus:
                menu_list.append(models.AdvancedMenu(**{
                    "agent": agent_now,
                    "default_menu": dm,
                    "name": dm.name,
                    "is_landing": dm.is_landing,
                    "enable": dm.enable,
                    "type": "default",
                    "sort": dm.sort,
                }))
            if menu_list:
                models.AdvancedMenu.objects.bulk_create(menu_list)

        # 所有菜单排序和重组
        default_menus = []
        if request.user.userinfo.role_type in [1, 2] and request.user.userinfo.is_admin:
            parents = models.DefaultMenu.objects.filter(parent__isnull=True, enable=1).order_by("index")
        else:
            parents = models.DefaultMenu.objects.filter(parent__isnull=True, enable=1, company_show=1).exclude(level='110000').order_by("index")
        for parent in parents:
            f_children = []

            first_children = parent.defaultmenu_set.filter(enable=1).all()
            if company:  # 公司用户选择性展示
                first_children = parent.defaultmenu_set.filter(enable=1, company_show=1).all()
            for child in first_children:
                s_children = []
                second_children = child.defaultmenu_set.filter(enable=1).all()
                if company:
                    second_children = child.defaultmenu_set.filter(enable=1, company_show=1).all()
                for s_child in second_children:
                    a_s_child = s_child.advancedmenu_set.filter(agent=agent_now).first()
                    s_children.append(a_s_child.get_dict())

                a_child = child.advancedmenu_set.filter(agent=agent_now).first()
                data = a_child.get_dict()
                # 排序
                s_children = sorted(s_children, key=lambda elem: "%03d %04d" % (elem['sort'], elem['index']))
                data.update({"children": s_children})
                f_children.append(data)

            a_parent = parent.advancedmenu_set.filter(agent=agent_now).first()
            data = a_parent.get_dict()
            # 排序
            f_children = sorted(f_children, key=lambda elem: "%03d %04d" % (elem['sort'], elem['index']))
            data.update({"children": f_children})
            default_menus.append(data)

        # 排序，排除首页
        if default_menus:
            default_menus = default_menus[:1] + sorted(default_menus[1:], key=lambda elem: "%03d %04d" % (elem['sort'], elem['index']))

        custom_menu = models.AdvancedMenu.objects.filter(agent=agent_now, type='custom').first()
        custom_menu = custom_menu.get_dict() if custom_menu else {}

        if menu_type == "default":
            data = {
                "default": list(default_menus),
            }
        elif menu_type == 'custom':
            data = {
                "custom": custom_menu
            }
        else:
            data = {
                "default": list(default_menus),
                "custom": custom_menu
            }
        context = {
            "status": 200,
            "msg": "获取菜单列表成功",
            "data": data
        }
        return Response(context)

    def post(self, request):
        """
        创建自定义菜单
        :param request:
        :return:
        """
        return Response(status.HTTP_405_METHOD_NOT_ALLOWED)
