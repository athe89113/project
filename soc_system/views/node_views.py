# coding=utf-8
from __future__ import unicode_literals
import json
import logging
import uuid
from hashlib import md5
from django.core.cache import cache
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from soc_system import serializers
from soc_system import models
from soc_system import system_common
from soc_user import models as user_models
from utils.api import NodeApi
from utils.auth import AllowAdminWithPassword
logger = logging.getLogger("soc_system")


class SystemNodeList(APIView):
    """
    系统中心
    """

    permission_classes = (AllowAdminWithPassword,)

    def get(self, request):
        """
        获取当前中心的上下级数据
        :param request:
        :param type: 中心类型
        :return:
        """
        node_type = request.query_params.get('type')
        if node_type == 'parent':
            needed = ["parent"]
        elif node_type == 'children':
            needed = ["children"]
        else:
            needed = ["children", "parent"]

        parent_dict = {}
        children_list = []
        if "parent" in needed:
            parent = models.Node.objects.filter(agent=request.user.userinfo.agent, role='parent').first()
            if parent:
                parent_dict = parent.get_dict()
        if "children" in needed:
            children = models.Node.objects.filter(agent=request.user.userinfo.agent, role='child')
            children_list = []
            for child in children:
                children_list.append(child.get_dict())

        data = {
            "children": children_list,
            "parent": parent_dict
        }
        context = {
            "status": 200,
            "msg": "获取中心数据成功",
            "data": data
        }
        return Response(context)

    def post(self, request):
        """
        添加
        :param request:
        :return:
        """
        agent_now = request.user.userinfo.agent

        data = dict()
        if request.data.get("role") == 'self':
            data["name"] = agent_now.title
            data["ip"] = "127.0.0.1"
        data.update(request.data)
        node_serializer = serializers.NodeSerializers(data=data, context={"request": request, "agent": agent_now})
        if node_serializer.is_valid():
            node_obj = node_serializer.save()
            context = {
                'status': 200,
                'msg': '添加中心成功',
                'data': node_obj.get_dict()
            }
            return Response(context)
        else:
            msg = '添加中心错误'
            for error in node_serializer.errors:
                msg = node_serializer.errors[error][0]
                break
            context = {
                'status': 500,
                'msg': msg,
                'error': node_serializer.errors
            }
            return Response(context)


class SystemNodeDetail(APIView):
    """
    中心详情
    """

    permission_classes = (AllowAdminWithPassword,)

    def get_object(self, request, node_id):
        agent_now = request.user.userinfo.agent
        try:
            node = models.Node.objects.get(id=node_id, agent=agent_now)
        except models.Node.DoesNotExist:
            node = None
        return node

    def put(self, request, node_id):
        """
        修改中心
        :param request:
        :param node_id:
        :return:
        """
        node = self.get_object(request, node_id)
        if not node:
            context = {
                "status": 500,
                "msg": "获取中心错误",
                "error": "获取中心错误",
            }
            return Response(context)
        agent_now = request.user.userinfo.agent
        node_serializer = serializers.NodeSerializers(instance=node, data=request.data, partial=True,
                                                      context={"request": request, "agent": agent_now})
        if node_serializer.is_valid():
            node_serializer.save()
            context = {
                'status': 200,
                'msg': '修改中心成功',
            }
            return Response(context)
        else:
            msg = '修改中心错误'
            for error in node_serializer.errors:
                msg = node_serializer.errors[error][0]
                break
            context = {
                'status': 500,
                'msg': msg,
                'error': node_serializer.errors
            }
            return Response(context)

    def get(self, request, node_id):
        """
        获取中心
        :param request:
        :param node_id:
        :return:
        """
        node = self.get_object(request, node_id)
        if not node:
            context = {
                "status": 500,
                "msg": "获取中心错误",
                "error": "获取中心错误",
            }
            return Response(context)
        data = node.get_dict()
        context = {
            "status": 200,
            "msg": "获取数据成功",
            "data": data
        }

        return Response(context)

    def delete(self, request, node_id):
        """
        删除中心信息
        :param request:
        :param node_id:
        :return:
        """
        node = self.get_object(request, node_id)
        if not node:
            context = {
                "status": 500,
                "msg": "获取中心错误",
                "error": "获取中心错误",
            }
            return Response(context)
        if node.role == "self":
            context = {
                "status": 500,
                "msg": "中心删除错误",
                "error": "中心删除错误",
            }
            return Response(context)
        node.delete()
        agent_now = request.user.userinfo.agent
        self_node = models.Node.objects.filter(agent=agent_now, role='self').last()
        if node.role == 'child':
            node_api = NodeApi(
                base_url='http://' + node.ip, secret_id=node.secret_id, secret_key=node.secret_key)

            params = json.dumps({'node_type': 'parent'})
            status = node_api.clear_node(params)
            if status == 200:
                context = {
                    "status": 200,
                    "msg": "删除中心成功",
                }
            else:
                context = {
                    "status": 500,
                    "msg": "删除错误",
                }
        else:
            context = {
                "status": 500,
                "msg": "删除错误",
            }
        return Response(context)


class SystemNodeStatusRefresh(APIView):
    """
    中心状态刷新
    """

    def get_object(self, request, node_id):
        agent_now = request.user.userinfo.agent
        try:
            node = models.Node.objects.get(id=node_id, agent=agent_now)
        except models.Node.DoesNotExist:
            node = None
        return node

    def post(self, request, node_id):
        """
        刷新中心状态
        :param request:
        :param node_id:
        :return:
        """

        node = self.get_object(request, node_id)
        if not node:
            context = {
                "status": 500,
                "msg": "获取中心错误",
                "error": "获取中心错误",
            }
            return Response(context)

        data, msg = system_common.get_node_detailed_status(node)
        logger.info(data)
        if not data:
            status = 2
        else:
            status = 1
            node.type = data['type']
        # 更新状态和信息
        node.status = status
        node.save()

        context = {
            "status": 200 if status == 1 else 500,
            "msg": msg[1],
            "data": {
                "status": status
            }
        }
        return Response(context)


class SystemNodeClearStatus(APIView):
    """级联"""

    def post(self, request):
        """判断上下级关系是否清除"""
        parent_status = False
        children_status = False
        # userinfo = request.user.userinfo.agent.userinfo_set.get(role_type=2, is_admin=1, is_ghost=1)
        # keys = user_models.SecretKey.objects.filter(user_id=userinfo.id)
        # if keys and keys[0].key:
        #     parent_status = True
        children = models.Node.objects.filter(agent=request.user.userinfo.agent, role='child')
        parent = models.Node.objects.filter(agent=request.user.userinfo.agent, role='parent')
        if children:
            children_status = True
        if parent:
            parent_status = True
        return Response({
            "status": 200,
            "data": {
                "parent": parent_status,
                "children": children_status
            }
        })


class SystemNodeClear(APIView):
    """
    级联
    """
    def delete(self, request):
        """清除上下级级联关系"""
        node_type = request.DATA.get('node_type')
        msg = ''
        agent = request.user.userinfo.agent
        self_node = models.Node.objects.filter(agent=agent, role='self').last()
        if node_type == 'parent':
            parents = models.Node.objects.filter(agent=agent, role='parent')
            for pa in parents:
                node_api = NodeApi(
                    base_url='http://' + pa.ip, auth_key=self_node.auth_key)
                status = node_api.clear_node_parent()
                if status == 200:
                    pa.delete()
            msg = '上级中心解除成功'
        elif node_type == 'children':
            children = models.Node.objects.filter(agent=request.user.userinfo.agent, role='child')
            for chi in children:
                node_api = NodeApi(
                    base_url='http://' + chi.ip, secret_id=chi.secret_id, secret_key=chi.secret_key)
                params = json.dumps({'node_type': 'parent'})
                status = node_api.clear_node(params)
                if status == 200:
                    chi.delete()
            msg = '下级中心解除成功'
        return Response({
            "status": 200,
            "msg": msg,
        })


class SystemNodeClearApiParent(APIView):
    """
    级联删除父节点
    下级中心通知本级中心删除子节点
    """
    permission_classes = (AllowAny,)

    def delete(self, request):
        parent_status = serializers.ParentStatusSerializers(data=request.DATA)
        if parent_status.is_valid():
            auth_key = parent_status.validated_data.get("auth_key")
            try:
                # 级联密钥
                child_node = models.Node.objects.get(role='child', auth_key=auth_key)
            except models.Node.DoesNotExist:
                return Response({
                    "status": 500,
                    "msg": "认证错误",
                    "error": "认证错误",
                })
            else:
                child_node.delete()
                msg = '上级中心解除成功'
                context = {
                    "status": 200,
                    "msg": msg,
                }

                return Response(context)

        else:
            logger.error(parent_status.errors)
            msg = '认证错误'
            for error in parent_status.errors:
                msg = parent_status.errors[error][0]
                break
            return Response({
                "status": 500,
                "msg": msg,
                "error": msg
            })


class SystemNodeClearApi(APIView):
    """级联"""

    def delete(self, request):
        """清除上下级级联关系"""

        node_type = request.DATA.get('node_type')
        msg = ''
        agent = request.user.userinfo.agent
        self_node = models.Node.objects.filter(agent=agent, role='self').last()
        if node_type == 'parent':
            parents = models.Node.objects.filter(agent=agent, role='parent')
            for pa in parents:
                pa.delete()
            msg = '上级中心解除成功'
        elif node_type == 'children':
            children = models.Node.objects.filter(agent=request.user.userinfo.agent, role='child')
            for chi in children:
                chi.delete()
            msg = '下级中心解除成功'
        return Response({
            "status": 200,
            "msg": msg,
        })


class SystemNodeSelfDetail(APIView):
    """
    当前当前中心信息
    """
    permission_classes = (AllowAdminWithPassword,)

    def get_object(self, request):
        agent_now = request.user.userinfo.agent
        try:
            node = models.Node.objects.get(role='self', agent=agent_now)
        except models.Node.DoesNotExist:
            node = None
        return node

    def get(self, request):
        """
        获取当前中心信息
        :param request:
        :return:
        """
        self_node = self.get_object(request)

        if self_node:
            data = self_node.get_dict()
        else:
            data = {
                "accept_parent_connection": 0,
                "accept_apply_policy": 0,
                "accept_apply_event_db": 0,
                "accept_apply_engine": 0,
                "accept_apply_center": 0,
                "ip": "127.0.0.1",
                "role": "self",
                "name": "127.0.0.1",
            }
        status_code = 200
        # 处理 API 请求
        if request.is_api:
            node_api = NodeApi(base_url="http://127.0.0.1:80", auth_key=self_node.auth_key)
            # todo 判断级联状态
            # 401: "下级中心不允许级联管理",
            # 403: "中心版本需要升级",
            # 404: "上级中心未添加级联",
            if data["accept_parent_connection"] == 0:
                status_code = 401
                return Response({
                    "status": status_code,
                    "msg": "下级中心不允许级联",
                    "error": "下级中心不允许级联"
                })

        context = {
            "status": status_code,
            "msg": "获取成功",
            "data": data
        }
        return Response(context)

    def put(self, request):
        """
        修改自己信息
        :param request:
        :return:
        """
        self_node = self.get_object(request)
        if not self_node:
            # 创建
            snl = SystemNodeList()
            return snl.post(request=request)
        else:
            # 修改
            snl = SystemNodeDetail()
            return snl.put(request=request, node_id=self_node.id)


class SystemNodeAuth(APIView):
    """
    中心认证
    """
    permission_classes = (AllowAny,)
    # 频率控制 2/m
    throttle_scope = 'get_auth_key'

    def post(self, request):
        """
        接受上级的级联 key，返回状态和对应 API token
        :param request:
        :return:
        """
        auth_serializer = serializers.AuthSerializers(data=request.data)
        if auth_serializer.is_valid():
            auth_key = auth_serializer.validated_data.get("auth_key")
            try:
                # 级联密钥
                self_node = models.Node.objects.get(role='self', auth_key=auth_key)
            except models.Node.DoesNotExist:
                return Response({
                    "status": 500,
                    "msg": "级联密钥错误",
                    "error": "级联密钥错误",
                })
            else:
                # 本中心不允许级联
                if not self_node.accept_parent_connection:
                    return Response({
                        "status": 500,
                        "msg": "下级中心不允许级联",
                        "error": "下级中心不允许级联",
                    })
                parent_type = auth_serializer.validated_data.get('type')
                self_type = self_node.type
                # 判断是否可以接受上级中心的级联
                if not parent_type:
                    return Response({
                        "status": 500,
                        "msg": "请传递中心角色",
                        "error": "请传递中心角色",
                    })
                else:
                    if (parent_type, self_type) not in [('center', 'sub_center'), ('center', 'child_center'), ('sub_center', 'child_center')]:
                        return Response({
                            "status": 500,
                            "msg": "下级中心角色无法进行级联",
                            "error": "下级中心角色无法进行级联",
                        })

                # 添加上级中心信息，之前上级中心可以重复认证
                node_uuid = auth_serializer.validated_data.get('uuid')
                if not node_uuid:
                    return Response({
                        "status": 500,
                        "msg": "请传递中心信息",
                        "error": "请传递中心信息",
                    })
                existing_parent = models.Node.objects.filter(role='parent', agent=self_node.agent).first()
                if existing_parent and str(existing_parent.uuid) != str(node_uuid):
                    return Response({
                        "status": 500,
                        "msg": "下级中心已经被级联，请联系下级中心修改",
                        "error": "下级中心已经被级联，请联系下级中心修改",
                    })
                version = auth_serializer.validated_data.get("version")
                name = auth_serializer.validated_data.get("name", '上级中心')
                ip = auth_serializer.validated_data.get("ip", '127.0.0.1')
                # 添加上级中心， 存在重新连接的情况
                models.Node.objects.update_or_create(
                    role='parent', agent=self_node.agent, uuid=node_uuid,
                    defaults={
                        "name": name,
                        "status": 1,
                        "ip": ip,
                        "port": 80,
                        "type": parent_type,
                        "version": version,
                    }
                )
                # 获取隐藏用户
                try:
                    # 只有一个
                    userinfo = self_node.agent.userinfo_set.get(role_type=2, is_admin=1, is_ghost=1)
                except user_models.UserInfo.DoesNotExist:
                    return Response({
                        "status": 500,
                        "msg": "中心未设置",
                        "error": "中心未设置(#noghostuser)",
                    })
                # 更新或者创建认证密钥
                # TODO enable==0 表示启用，what the F**K!
                new_user_secret_key, created = user_models.SecretKey.objects.update_or_create(
                    user_id=userinfo.id, defaults={"enable": 0, "key": md5(str(uuid.uuid4())).hexdigest()[:20]})

                context = {
                    "status": 200,
                    "msg": "ok",
                    "data": {
                        "secret_id": new_user_secret_key.id,
                        "secret_key": new_user_secret_key.key,
                        "type": self_node.type,
                        "version": self_node.version,
                    }
                }
                return Response(context)
        else:
            logger.error(auth_serializer.errors)
            msg = '级联密钥错误'
            for error in auth_serializer.errors:
                msg = auth_serializer.errors[error][0]
                break
            return Response({
                    "status": 500,
                    "msg": msg,
                    "error": msg
                })


class SystemNodeTopo(APIView):
    """系统设置"""
    permission_classes = (AllowAdminWithPassword,)

    def get(self, request):
        """
        获取本中心对应拓扑结构
        :param request:
        :return:
        """
        self_node = models.Node.objects.filter(agent=request.user.userinfo.agent, role='self').first()
        if not self_node:
            context = {
                "status": 500,
                "msg": "请先配置本级中心",
                "error": "请先配置本级中心"
            }
            return Response(context)
        parent = models.Node.objects.filter(agent=request.user.userinfo.agent, role='parent').first()
        parent_dict = parent.get_dict() if parent else {}
        children = models.Node.objects.filter(agent=request.user.userinfo.agent, role='child')

        children_list = []
        for child in children:
            # TODO fetch center children's children to cache
            child_dict = child.get_dict()
            if child.type == 'sub_center':
                csc = cache.get(system_common.node_child_topo_cache_key.format(**{"agent_id": child.agent.id, "node_uuid": child.uuid}), [])
                child_dict.update({"children": csc})
            children_list.append(child_dict)

        self_node_dict = self_node.get_dict()

        if self_node.type == "center":
            tree = self_node_dict
            tree.update({"children": children_list})
        elif self_node.type == "sub_center":
            if parent:
                tree = parent_dict
                self_node_dict.update({"children": children_list})
                tree.update({"children": [self_node_dict]})
            else:
                tree = self_node_dict
                tree.update({"children": children_list})
        else:
            # child_center
            if parent:
                tree = parent_dict
                tree.update({"children": [self_node_dict]})
            else:
                tree = self_node_dict
                tree.update({"children": children_list})

        context = {
            "status": 200,
            "msg": "获取成功",
            "data": tree
        }
        return Response(context)


class SystemNodeTree(APIView):
    """系统设置"""
    permission_classes = (AllowAdminWithPassword,)

    def get(self, request):
        """
        级联树状拓扑
        """
        try:
            # 级联树从当前中心开下
            node_tree = models.Node.objects.get(role="self").get_dict()
        except models.Node.DoesNotExist:
            node_tree = {"name": "本中心"}
        del node_tree['auth_key']
        # 当前中心为二级中心 从数据库获取三级中心
        if node_tree['type'] == "sub_center":
            childrens = models.Node.objects.filter(agent=request.user.userinfo.agent, role='child')
            children_list = []
            for children in childrens:
                children_dict = children.get_dict()
                del children_dict['auth_key']
                children_list.append(children.get_dict())
            node_tree['children'] = children_list
    
        # 当前中心为一级中心， 从数据库获取二级中心，从API接口获取三级中心
        if node_tree['type'] == "center":
            childrens = models.Node.objects.filter(agent=request.user.userinfo.agent, role='child')
            children_list = []
            for children in childrens:
                children_dict = children.get_dict()
                del children_dict['auth_key']
                if children.type == "sub_center":                 
                    node_api = NodeApi(base_url='http://{}:{}'.format(children.ip, children.port),
                           secret_id=children.secret_id, secret_key=children.secret_key)
                    result = node_api.fetch(method="get", api=request.path)
                    status = result['status']
                    if status == 200:
                        children_dict['children'] = result['data']['children']
                children_list.append(children_dict)

            node_tree['children'] = children_list

        return Response({"status": 200, "data": node_tree})


class SystemNodeParentStatus(APIView):
    """
    上级中心状态
    """

    permission_classes = (AllowAny,)
    # 与 get_auth_key 同请求频率限制
    throttle_scope = 'get_auth_key'

    def get(self, request):
        """
        获取上级中心状态
        :param request:
        :return:
        """

        parent_status = serializers.ParentStatusSerializers(data=request.query_params)
        if parent_status.is_valid():
            auth_key = parent_status.validated_data.get("auth_key")
            try:
                # 级联密钥
                child_node = models.Node.objects.get(role='child', auth_key=auth_key)
                self_node = models.Node.objects.get(role='self', agent=child_node.agent)
            except models.Node.DoesNotExist:
                return Response({
                    "status": 500,
                    "msg": "认证错误",
                    "error": "认证错误",
                })
            else:
                context = {
                    "status": 200,
                    "msg": "级联正常",
                    "data": {
                        "status": 1,
                        "type": self_node.type,
                        "name": self_node.version,
                        "version": self_node.version
                    }
                }
                return Response(context)
        else:
            logger.error(parent_status.errors)
            msg = '认证错误'
            for error in parent_status.errors:
                msg = parent_status.errors[error][0]
                break
            return Response({
                "status": 500,
                "msg": msg,
                "error": msg
            })


class SystemNodeComponents(APIView):
    """
    组件列表
    """

    def get(self, request):
        """
        获取当前中心的所包含的组件列表（可从系统进行升级的）
        :param request:
        :return: 组件列表
        """
        name = request.query_params.get("name", 'all')
        if not name:
            return Response({
                "status": 500,
                "msg": "请指定组件名称",
                "error": "请指定组件名称",
                "data": {},
            })

        if name == 'all':
            data = system_common.Component(agent=request.user.userinfo.agent).fetch_all()
        else:
            if name not in system_common.Component.supported_components:
                return Response({
                    "status": 500,
                    "msg": "不支持的组件名称",
                    "error": "不支持的组件名称",
                })
            data = dict()
            data[name] = system_common.Component(agent=request.user.userinfo.agent).fetch_by_name(name)

        return Response({
            "status": 200,
            "msg": "ok",
            "data": data
        })


class SystemNodeChildrenComponents(APIView):
    """
    当前系统的子中心的组件列表
    """

    def get(self, request):
        """

        :return:
        """
        child_components = system_common.get_child_components(agent=request.user.userinfo.agent)

        return Response({
            "status": 200,
            "msg": 'ok',
            "data": child_components
        })


class SystemNodeWithComponents(APIView):
    """
    系统
    """

    def get(self, request):
        """
        获取包含组件的当前中心系统和子中心系统列表
        :param request:
        :return:
            - has_child
            - children
        """
        name = request.query_params.get("name")
        if not name:
            return Response({
                "status": 500,
                "msg": "请指定组件名称",
                "error": "请指定组件名称",
                "data": {},
            })
        if name not in system_common.Component.supported_components:
            return Response({
                "status": 500,
                "msg": "不支持的组件名称",
                "error": "不支持的组件名称",
            })
        agent_now = request.user.userinfo.agent
        data = system_common.get_children_with_components(agent_now, name)
        context = {
            "status": 200,
            "msg": "获取中心列表成功",
            "data": data
        }
        return Response(context)


class ChildrenAPIViews(APIView):
    """
    调用子中心API接口
    """

    def post(self, request):
        """
        调用子中心API接口
        """
        api = request.data.get("api")
        node_uuid = request.data.get("uuid")
        params = request.data.get("params")
        method = request.data.get("method")

        agent = request.user.userinfo.agent
        try:
            node_obj = models.Node.objects.get(uuid=node_uuid, agent=agent)
        except models.Node.DoesNotExist:
            return Response({"status": 500, "msg": "该中心不存在", "error": "该中心不存在"})
        node_api = NodeApi(base_url='http://{}:{}'.format(node_obj.ip, node_obj.port),
                           secret_id=node_obj.secret_id, secret_key=node_obj.secret_key)
        try:
            params = json.loads(params)
        except (TypeError, ValueError):
            params = None
        result = node_api.fetch(method=method, api=api, params=params)
        return Response(result)
