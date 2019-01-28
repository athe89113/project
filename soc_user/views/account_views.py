# coding=utf-8
from __future__ import unicode_literals
import base64
import logging
import qrcode
import uuid
import random
import re
import itsdangerous
from io import BytesIO
from django.contrib.auth.models import (User as ModelUser, )
from django.db import transaction
from django.contrib import auth
from django.contrib.sites.shortcuts import get_current_site
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import DjangoModelPermissions, AllowAny
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework import status
from rest_framework import renderers
from django.contrib.auth import logout
from soc_user.models import (
    UserInfo,
    WorkGroup as ModelWorkGroup,
    VerifyTmp,
    Roles
)
from soc.models import (
    Perms as ModelPerms,
    Agent as ModelAgent,
    AgentPerms as ModelAgentPerms,
    Company as ModelCompany,
    SocLog
)
from oath import accept_totp
from django.conf import settings
from django.forms import model_to_dict
from common import modify_values
from common import generate_google_url
from common import soc_log
from utils.select2 import select2_filter
from common import soc_system_log
from soc_user.user_common import PhoneCaptchaTools, GoogleTwoFactorTools
from soc_user.serializers import UserSerializer
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
from utils.auth import AllowAdminWithPassword
from utils.ip import find_ip_location

DEFAULT_AGENT_PERMS = range(1, 9)
logger = logging.getLogger("soc")


class User(APIView):
    """ 用户API """

    model = ModelUser

    # permission_classes = (DjangoModelPermissions,)

    def log(self):
        pass

    def get(self, request, user_id=None):
        """
        获取用户信息
        ---
        parameters:
            # - name: agent_id
            #   description: 合作伙伴id
            #   type: integer
            #   paramType: form
            #   required: false
            # - name: company_id
            #   description: 企业id
            #   type: integer
            #   paramType: form
            #   required: false
              - name: user_id
                description: 用户id
                type: integer
                required: false


        """
        # company_id = request.query_params.get("company_id", None)
        agent_now = request.user.userinfo.agent
        user_data = {}
        user = None
        if not user_id:
            context = {
                "status": 500,
                "msg": u"请选择用户",
                "error": u"请选择用户"
            }
            return Response(context)
        if request.user.userinfo.is_admin != 1:
            if int(user_id) != int(request.user.id):
                context = {
                    "status": 500,
                    "error": u"无权操作",
                    "msg": u"无权操作"
                }
                # soc_system_log(category='系统管理-管理设置', info='无权操作',
                #               request=request, url=request.path)
                return Response(context)
        if request.user.userinfo.role_type == 3:
            user = ModelUser.objects.filter(id=user_id, userinfo__company=request.user.userinfo.company).first()
        else:
            user = ModelUser.objects.filter(id=user_id, userinfo__agent=agent_now).first()
        if not user:
            context = {
                "status": 500,
                "msg": u"错误的用户ID",
                "error": u"错误的用户ID"
            }
            # soc_system_log(category='系统管理-管理设置', info='获取用户错误',
            #              request=request, url=request.path)
            return Response(context)
        user_data['id'] = user.id
        user_data['username'] = user.username
        user_data['email'] = user.email
        user_data['phone'] = user.userinfo.phone
        user_data['is_locked'] = user.userinfo.is_locked
        user_data['is_admin'] = user.userinfo.is_admin
        user_data['employee_id'] = user.userinfo.employee_id
        user_data['gs_status'] = user.userinfo.gs_status

        context = {
            "status": 200,
            "msg": u"获取用户成功",
            "data": user_data
        }
        roles_obj = user.userinfo.roles.all()
        role_name = ''
        for i in roles_obj:
            role_name = i.name
        if not role_name:
            role_name = '普通用户'
        # soc_system_log(category='系统管理-管理设置', info='获取用户名为{0}角色为{1}的信息'.format(user.username, role_name),
        #               request=request, url=request.path)
        # soc_system_log(category='系统管理-管理设置', info='获取用户{0}信息'.format(user.username),
        #                request=request)
        return Response(context)

    @soc_log('用户管理', '创建用户')
    def post(self, request):
        """
        创建用户
        ---
        parameters:
            - name: username
              description: 用户名
              type: string
              paramType: form
              required: true
            # - name: first_name
            #   description: 姓名
            #   type: string
            #   paramType: form
            #   required: true
            - name: password
              description: 密码
              type: string
              paramType: form
              required: true
            - name: email
              description: email
              type: string
              paramType: form
              required: true
            - name: phone
              description: 电话
              type: string
              paramType: form
              required: false
            # - name: work_group_id
            #   description: 工作组id
            #   type: string
            #   paramType: form
            #   required: false
            - name: agent_id
              description: 合作伙伴id
              type: string
              paramType: form
              required: false
            - name: company_id
              description: 企业id
              type: string
              paramType: form
              required: false
            - name: is_locked
              description: 用户状态,1是锁定,0是正常
              type: string
              paramType: form
              required: false
        """

        # username = request.DATA.get('username')
        context = {
            "agent": request.user.userinfo.agent,
            "company": request.user.userinfo.company,
            "request": request,
        }
        serializer = UserSerializer(data=request.data, context=context)
        if serializer.is_valid():
            user = serializer.save()
            context = {
                "status": 200,
                "msg": u"创建用户成功",
                "data": {'user_id': user.id}
            }
            roles_obj = user.userinfo.roles.all()
            role_name = ''
            for i in roles_obj:
                role_name = i.name
            if not role_name:
                role_name = '普通用户'
            # soc_system_log(category='系统管理-管理设置', info='创建用户名为{0}角色为{1}用户'.format(user.username, role_name),
            #               request=request, url=request.path)
            return Response(context)
        else:
            context = {
                "status": 500,
                "msg": serializer.errors.items()[0][1][0],
                "errors": serializer.errors
            }
            # soc_system_log(category='系统管理-管理设置', info='创建用户错误',
            #               request=request, url=request.path)
            return Response(context)

    @soc_log('用户管理', '修改用户信息')
    def put(self, request, user_id):
        """
        修改用户信息, 
        管理员只能修改其下用户的信息,普通用户只能修改自己的信息,
                    不能删除和锁定自己,不能更改自己的权限
        ---
        parameters:
            - name: user_id
              description: 用户名id
              type: string
              paramType: form
              required: true
            - name: username
              description: 姓名
              type: string
              paramType: form
              required: false
            - name: password
              description: 密码
              type: string
              paramType: form
              required: false
            - name: email
              description: email
              type: string
              paramType: form
              required: false
            - name: phone
              description: 电话
              type: string
              paramType: form
              required: false
            - name: is_active
              description: 是否激活  1激活 0锁定
              type: string
              paramType: form
              required: false
            - name: is_locked
              description: 锁定用户 1是 0否
              type: string
              paramType: form
              required: false
            - name: work_group_id
              description: 组id
              type: string
              paramType: form
              required: false
        """

        context = {
            "agent": request.user.userinfo.agent,
            "company": request.user.userinfo.company,
            "request": request,
        }

        try:
            edit_user = ModelUser.objects.get(id=user_id)
        except ModelUser.DoesNotExist:
            context = {
                "status": 500,
                "error": u"用户不存在",
                "msg": u"用户不存在"
            }
            # soc_system_log(category='系统管理-管理设置', info='用户不存在',
            #               request=request, url=request.path)
            return Response(context)
        roles_obj = edit_user.userinfo.roles.all()
        role_name = ''
        for i in roles_obj:
            role_name = i.name
        if not role_name:
            role_name = '普通用户'
        if request.user.userinfo.role_type == 3:
            if int(user_id) != int(request.user.id) and request.user.userinfo.is_admin == 0:
                context = {
                    "status": 500,
                    "error": u"无权操作",
                    "msg": u"无权操作"
                }
                # soc_system_log(category='系统管理-管理设置',
                #              info='无权修改用户名为{0}角色为{1}的用户信息'.format(edit_user.username, role_name),
                #               request=request, url=request.path)
                return Response(context)
        else:
            if int(user_id) != int(request.user.id) and request.user.userinfo.is_admin == 0:
                if not edit_user.userinfo.role_type == 3:
                    context = {
                        "status": 500,
                        "error": u"无权操作",
                        "msg": u"无权操作"
                    }
                    # soc_system_log(category='系统管理-管理设置',
                    #               info='无权修改用户名为{0}角色为{1}的用户信息'.format(edit_user.username, role_name),
                    #               request=request, url=request.path)
                    return Response(context)

        if request.user.userinfo.is_admin == 0:
            if request.user.userinfo.role_type == 3:
                if int(user_id) != int(request.user.id):
                    context = {
                        "status": 500,
                        "error": u"无权操作",
                        "msg": u"无权操作"
                    }
                    # soc_system_log(category='系统管理-管理设置',
                    #               info='无权修改用户名为{0}角色为{1}的用户信息'.format(edit_user.username, role_name),
                    #              request=request, url=request.path)
                    return Response(context)

        serializer = UserSerializer(data=request.data, context=context, instance=edit_user)
        if serializer.is_valid():
            user, info = serializer.save()
            context = {
                "status": 200,
                "msg": u"修改用户成功",
                "data": {'user_id': user.id}
            }
            # soc_system_log(category='系统管理-管理设置',
            #               info='修改用户名为{0}角色为{1}的用户{2}信息成功'.format(edit_user.username, role_name, info),
            #               request=request, url=request.path)
            return Response(context)
        else:
            context = {
                "status": 500,
                "msg": serializer.errors.items()[0][1][0],
                "errors": serializer.errors
            }
            # soc_system_log(category='系统管理-管理设置', info='修改用户名为{0}角色为{1}的用户信息错误'.format(edit_user.username, role_name),
            #               request=request, url=request.path)
            return Response(context)

    @soc_log('用户管理', '删除用户')
    def delete(self, request, user_id):
        """
        删除用户
        ---
        parameters:
            - name: user_id
              description: 用户id
              type: string
              paramType: form
              required: true
        """
        if not request.user.userinfo.is_admin:
            context = {
                "status": 500,
                "msg": u"非管理员，无权操作",
                "error": u"非管理员，无权操作"
            }
            # soc_system_log(category='系统管理-管理设置', info='非管理员，无权操作',
            #               request=request, level='warning', url=request.path)
            return Response(context)
        delete_user = ModelUser.objects.get(id=user_id)
        roles_obj = delete_user.userinfo.roles.all()
        role_name = ''
        for i in roles_obj:
            role_name = i.name
        if not role_name:
            role_name = '普通用户'
        # user_id = request.DATA.get('user_id')
        role_type = request.user.userinfo.role_type
        if role_type == 3:
            user_to_be_deleted = ModelUser.objects.filter(id=user_id, userinfo__company=request.user.userinfo.company,
                                                          userinfo__role_type=role_type).exclude(
                id=request.user.id).first()
        else:
            user_to_be_deleted = ModelUser.objects.filter(id=user_id, userinfo__agent_id=request.user.userinfo.agent.id
                                                          ).exclude(id=request.user.id).first()
        if user_to_be_deleted:
            # soc_system_log(category='系统管理-管理设置', info='删除用户名为{0}的用户'.format(user_to_be_deleted.username, role_name),
            #               request=request, level='warning', url=request.path)
            # user_to_be_deleted.deviceip_set.all().update(user=None)
            # user_to_be_deleted.cloudserverip_set.all().update(belong_user=None)
            user_to_be_deleted.delete()
        else:
            # soc_system_log(category='系统管理-管理设置', info='删除用户名为{0}的用户失败'.format(user_to_be_deleted.username),
            #               request=request, level='warning', url=request.path)
            context = {
                "status": 500,
                "error": u"删除用户失败",
                "msg": u"删除用户失败"
            }
            return Response(context)

        context = {
            "status": 200,
            "msg": "删除用户成功"
        }
        return Response(context)


class AdminUser(User):
    """管理员"""
    permission_classes = (AllowAdminWithPassword,)
    pass


class Perms(APIView):
    """ 权限 API """

    model = ModelPerms
    permission_classes = (DjangoModelPermissions,)

    def get(self, request):
        """ 获取权限项 """
        if not request.user.userinfo.role_type == 1:
            context = {
                "status": 400,
                "msg": u"非超级管理员，无权操作",
                "error": u"非超级管理员，无权操作"
            }
            return Response(context)
        perms = ModelPerms.objects.values()
        context = {
            "status": 200,
            "msg": u"获取权限成功",
            "data": perms
        }
        return Response(context)

    @soc_log('用户管理', '创建权限')
    def post(self, request):
        """创建权限
        ---
        parameters:
            - name: name
              description: 权限名
              type: string
              paramType: form
              required: true
            - name: perms_id
              description: 权限id
              type: string
              paramType: form
              required: true
        """

        if not request.user.userinfo.role_type == 1:
            context = {
                "status": 400,
                "msg": u"非超级管理员，无权操作",
                "error": u"非超级管理员，无权操作"
            }
            return Response(context)
        name = request.DATA.get('name')
        if ModelPerms.objects.filter(name=name).count():
            context = {
                "status": 500,
                "msg": u"创建权限失败，权限重名",
                "error": u"创建权限失败, {} 权限已存在".format(name)
            }
            return Response(context)
        perms_id = request.DATA.get('perms_id')
        if ModelPerms.objects.filter(perms_id=perms_id).count():
            context = {
                "status": 500,
                "msg": u"创建权限失败，权限重名",
                "error": u"创建权限失败, {} 权限id已存在".format(perms_id)
            }
            return Response(context)

        ModelPerms.objects.create(name=name, perms_id=perms_id)
        context = {
            "status": 200,
            "msg": u"创建权限成功"
        }
        return Response(context)

    @soc_log('用户管理', '修改权限')
    def put(self, request):
        """修改权限
        ---
        parameters:
            - name: id
              description: 权限的id
              type: string
              paramType: form
              required: false
            - name: name
              description: 权限名
              type: string
              paramType: form
              required: false
            - name: perms_id
              description: 权限id
              type: string
              paramType: form
              required: false
        """

        if not request.user.userinfo.role_type == 1:
            context = {
                "status": 400,
                "msg": u"非超级管理员，无权操作",
                "error": u"非超级管理员，无权操作"
            }
            return Response(context)
        id = request.DATA.get("id")
        name = request.DATA.get('name')
        update_dict = {}
        if name:
            if ModelPerms.objects.filter(name=name).count():
                context = {
                    "status": 500,
                    "msg": u"修改权限失败，权限重名",
                    "error": u"修改权限失败, {} 权限已存在".format(name)
                }
                return Response(context)
            update_dict['name'] = name
        perms_id = request.DATA.get('perms_id')
        if perms_id:
            if ModelPerms.objects.filter(perms_id=perms_id).count():
                context = {
                    "status": 500,
                    "msg": u"修改权限失败，权限重名",
                    "error": u"修改权限失败, {} 权限id已存在".format(perms_id)
                }
                return Response(context)
            update_dict['perms_id'] = perms_id
        if update_dict:
            ModelPerms.objects.filter(id=id).update(**update_dict)
        context = {
            "status": 200,
            "msg": u"修改权限成功"
        }
        return Response(context)

    @soc_log('用户管理', '删除权限')
    def delete(self, request):
        """删除权限
        ---
        parameters:
            - name: id
              description: 权限的id
              type: string
              paramType: form
              required: true
        """
        if not request.user.userinfo.role_type == 1:
            context = {
                "status": 400,
                "msg": u"非超级管理员，无权操作",
                "error": u"非超级管理员，无权操作"
            }
            return Response(context)
        id = request.DATA.get("id")
        if not id:
            context = {
                "status": 500,
                "msg": u"删除权限失败，没有id参数",
                "error": u"修改权限失败"
            }
            return Response(context)
        ModelPerms.objects.filter(id=id).delete()
        context = {
            "status": 200,
            "msg": u"删除权限成功"
        }
        return Response(context)


class AgentPerms(APIView):
    """ 代理商权限 API """

    model = ModelAgentPerms
    permission_classes = (DjangoModelPermissions,)

    def get(self, request):
        """
        获取代理商权限
        ---
        parameters:
            - name: agent_id
              description: 代理商id
              type: string
              paramType: form
              required: true
        """

        if not request.user.userinfo.role_type == 1:
            context = {
                "status": 400,
                "msg": u"非超级管理员，无权操作",
                "error": u"非超级管理员，无权操作"
            }
            return Response(context)
        agent_id = request.query_params.get("agent_id")
        agent_perms = ModelAgentPerms.objects.filter(agent_id=agent_id).values()
        agent_perms = modify_values(agent_perms, {'perms': ModelPerms})
        context = {
            "status": 200,
            "msg": u"获取权限成功",
            "data": agent_perms
        }
        return Response(context)

    def post(self, request):
        """创建权限"""
        pass

    @soc_log('用户管理', '修改代理商权限')
    def put(self, request):
        """
        修改代理商权限
        请求参数式例：
        {
            "agent_id": 2,
            "perms_1": 1,
            "perms_2": 2,
            "perms_3": 3,
        ｝
        ---
        parameters:
            - name: agent_id
              description: 代理商id
              type: string
              paramType: form
              required: true
            - name: perms_权限id
              description: 所有的权限 # 没有传送过的权限做为删除, 传过来的权限为添加权限
              type: string
              paramType: form
              required: false
        """

        if not request.user.userinfo.role_type == 1:
            context = {
                "status": 400,
                "msg": u"非超级管理员，无权操作",
                "error": u"非超级管理员，无权操作"
            }
            return Response(context)
        agent_id = request.DATA.get("agent_id")
        # new_perms_list = request.DATA.get("perms")

        new_perms_list = []
        for k, v in request.DATA.items():
            if k.find('perms_') == 0:
                if int(k[6:]) == int(request.DATA.get(k)):
                    new_perms_list.append(int(request.DATA.get(k)))

        old_perms = ModelAgentPerms.objects.filter(agent_id=agent_id)
        old_perms_list = [op['perms_id'] for op in old_perms.values('perms_id')]

        delete_list = list(set(old_perms_list).difference(set(new_perms_list)))
        create_list = list(set(new_perms_list).difference(set(old_perms_list)))
        if delete_list:
            ModelAgentPerms.objects.filter(agent_id=agent_id, perms_id__in=delete_list).delete()
        if create_list:
            for cl in create_list:
                ModelAgentPerms.objects.create(agent_id=agent_id, perms_id=cl)

        context = {
            "status": 200,
            "msg": u"更新权限成功"
        }
        return Response(context)

    def delete(self, request):
        """删除权限"""
        pass


class WorkGroup(APIView):
    """工作组，部门"""

    def get(self, request):
        """
        获取工作组
        """
        work_group = ModelWorkGroup.objects.filter(agent=request.user.userinfo.agent).values()
        context = {
            'status': 200,
            "msg": u"获取工作组成功",
            'data': work_group
        }
        return Response(context)

    @soc_log('用户管理', '创建工作组')
    def post(self, request):
        """
        创建工作组
        ---
        parameters:
            - name: name
              description: 工作组名称
              type: string
              paramType: form
              required: true
            - name: user_用户id
              description: 所有的用户 # 传过来的用户为添加到组
              type: string
              paramType: form
              required: false
        """

        if not (request.user.userinfo.role_type == 2):
            context = {
                "status": 500,
                "msg": u"非管理员，无权操作",
                "error": u"非管理员，无权操作"
            }
            return Response(context)
        name = request.DATA.get('name')
        create_dict = {}
        if name:
            if ModelWorkGroup.objects.filter(agent=request.user.userinfo.agent, name=name).count():
                context = {
                    "status": 500,
                    "msg": u"创建工作组失败，{} 已经存在".format(name),
                    "error": u"创建工作组失败，{} 已经存在".format(name)
                }
                return Response(context)
            create_dict["name"] = name
        if create_dict:
            new_work_group = ModelWorkGroup.objects.create(agent=request.user.userinfo.agent, name=name)

        new_user_list = []
        for k, v in request.DATA.items():
            if k.find('user_') == 0:
                if int(k[5:]) == int(request.DATA.get(k)):
                    new_user_list.append(int(request.DATA.get(k)))

        if new_user_list:
            if create_dict:
                for nuid in new_user_list:
                    UserInfo.objects.filter(user_id=nuid).update(work_group=new_work_group)

        context = {
            "status": 200,
            "msg": u"创建工作组成功"
        }
        return Response(context)

    @soc_log('用户管理', '修改工作组')
    def put(self, request, wg_id):
        """
        修改工作组
        ---
        parameters:
            # - name: work_group_id
            #   description: 工作组id
            #   type: string
            #   paramType: form
            #   required: true
            - name: name
              description: 工作组名称
              type: string
              paramType: form
              required: false
            - name: user_用户id
              description: 所有的用户 # 传过来的用户为添加到组，没传过来的做为删除
              type: string
              paramType: form
              required: false
        """
        if not (request.user.userinfo.role_type == 2):
            context = {
                "status": 500,
                "msg": u"非管理员，无权操作",
                "error": u"非管理员，无权操作"
            }
            return Response(context)
        # wg_id = request.DATA.get('work_group_id')
        if not wg_id:
            context = {
                "status": 500,
                "msg": u"缺少参数: work_group_id",
                "error": u"需要传入 work_group_id"
            }
            return Response(context)
        name = request.DATA.get('name')
        update_dict = {}
        if name:
            if ModelWorkGroup.objects.filter(agent=request.user.userinfo.agent, name=name).exclude(id=wg_id).count():
                context = {
                    "status": 500,
                    "msg": u"创建工作组失败，{} 已经存在".format(name),
                    "error": u"创建工作组失败，{} 已经存在".format(name)
                }
                return Response(context)
            update_dict["name"] = name
        if update_dict:
            ModelWorkGroup.objects.filter(id=wg_id).update(**update_dict)

        new_user_list = []
        for k, v in request.DATA.items():
            if k.find('user_') == 0:
                if int(k[5:]) == int(request.DATA.get(k)):
                    new_user_list.append(int(request.DATA.get(k)))

        old_user_list = UserInfo.objects.filter(work_group_id=wg_id).values("user_id")
        old_user_list = [ou['user_id'] for ou in old_user_list]

        delete_list = list(set(old_user_list).difference(set(new_user_list)))
        update_list = list(set(new_user_list).difference(set(old_user_list)))

        if delete_list:
            UserInfo.objects.filter(user_id__in=delete_list, work_group_id=wg_id).update(work_group_id=None)
        if update_list:
            UserInfo.objects.filter(user_id__in=update_list).update(work_group_id=wg_id)
        context = {
            "status": 200,
            "msg": u"修改工作组成功"
        }
        return Response(context)

    @soc_log('用户管理', '删除工作组')
    def delete(self, request, wg_id):
        """
        删除工作组
        # ---
        # parameters:
        #     - name: work_group_id
        #       description: 工作组id
        #       type: string
        #       paramType: form
        #       required: true
        """

        if not (request.user.userinfo.role_type == 2):
            context = {
                "status": 500,
                "msg": u"非管理员，无权操作",
                "error": u"非管理员，无权操作"
            }
            return Response(context)
        # wg_id = request.DATA.get("work_group_id")
        if not wg_id:
            context = {
                "status": 500,
                "msg": u"缺少参数: work_group_id",
                "error": u"需要传入 work_group_id"
            }
            return Response(context)
        tobe_deleted = ModelWorkGroup.objects.get(id=wg_id)
        tobe_update_userinfo = UserInfo.objects.filter(work_group_id=wg_id, agent=request.user.userinfo.agent)
        tobe_update_userinfo.update(work_group=None)
        tobe_deleted.delete()
        context = {
            "status": 200,
            "msg": u"删除工作组成功"
        }
        return Response(context)


class AvatarView(APIView):
    """用户信息"""
    model = ModelUser
    permission_classes = (DjangoModelPermissions,)
    parser_classes = (MultiPartParser, FormParser,)

    def get(self, request):
        """
        获取头像
        """
        user_id = request.query_params.get("user_id")
        user = ModelUser.objects.get(id=user_id)
        avatar = {
            "id": user_id,
            "avatar": user.userinfo.avatar.url,
        }
        context = {
            "status": 200,
            "msg": "获取头像成功",
            "data": avatar
        }
        return Response(data=context, status=status.HTTP_200_OK)

    def put(self, request, user_id=None):
        """
        修改头像
        ---
        parameters:
            - name: user_id
              description: 用户id
              type: string
              paramType: form
              required: true
            - name: avatar
              description: 头像文件
              type: file
              paramType: form
              required: true
        """
        if not user_id:
            user_id = request.DATA.get("user_id")
        avatar = request.FILES.get("avatar")
        user = ModelUser.objects.filter(id=user_id, userinfo__agent_id=request.user.userinfo.agent.id).first()
        if not user:
            context = {
                "status": 500,
                "msg": u"不存在这个用户",
                "error": u"不存在这个用户"
            }
            return Response(context)
        if avatar:
            user.userinfo.avatar.save(avatar.name, avatar)

        context = {
            "status": 200,
            "msg": u"修改头像成功"
        }
        return Response(context)


class CurrentUserProfile(APIView):
    """
    获取当前用户信息
    """

    def get(self, request):
        """ 获取当前用户信息 """
        user = request.user

        user_dict = dict()
        user_dict["id"] = user.id
        user_dict["username"] = user.username
        user_dict["first_name"] = user.first_name
        # user_dict["is_active"] = user.is_active
        user_dict["email"] = user.email

        if user.userinfo.work_group:
            user_dict["work_group"] = model_to_dict(ModelWorkGroup.objects.filter(
                id=user.userinfo.work_group.id
            ).first())
        else:
            user_dict["work_group"] = {}
        user_dict["phone"] = user.userinfo.phone
        user_dict["agent"] = {
            'id': user.userinfo.agent.id,
            "name": user.userinfo.agent.name,
            "title": user.userinfo.agent.title,
        }
        user_dict["is_locked"] = user.userinfo.is_locked
        user_dict["is_admin"] = user.userinfo.is_admin
        user_dict["avatar"] = user.userinfo.avatar.url if user.userinfo.avatar else ''
        user_dict["role_type"] = user.userinfo.role_type
        if user.userinfo.role_type == 2:
            user_dict["role"] = "管理员"
        elif user.userinfo.role_type == 3:
            user_dict["role"] = "管理员"
        elif user.userinfo.role_type == 1:
            user_dict["role"] = "青松"
        else:
            user_dict["role"] = "未知"

        # 最后登录时间
        try:
            last_log_in_info = SocLog.objects.filter(logtype=2, user=request.user, login_status=1).order_by('-id')[1]
        except IndexError:
            last_log_in_info = None
            last_login_time = ""
            last_login_ip = ""

        if last_log_in_info:
            last_login_time = timezone.localtime(last_log_in_info.create_time).strftime(
                '%Y-%m-%d %H:%M:%S') if last_log_in_info.create_time else ""
            last_login_ip = last_log_in_info.ip

        user_dict["last_login"] = last_login_time
        user_dict["last_login_ip"] = last_login_ip

        # 安全级别
        user_dict["sec_level"] = 50
        # 套餐状态
        user_dict["package"] = {
            "asset": {"status": 0, "left": 0},
            "monitor": {"status": 0, "left": 0},
            "scan": {"status": 0, "left": 0},
            "hids": {"status": 0, "left": 0},
            "ddos": {"status": 0, "left": 0},
            "waf": {"status": 0, "left": 0}
        }
        user_dict["login_timeout"] = user.userinfo.agent.login_timeout

        agent_info = {"phone": user.userinfo.agent.server_phone}
        user_dict["agent"] = agent_info

        context = {
            "status": 200,
            "msg": u"获取用户成功",
            "data": user_dict
        }
        return Response(context)

    @soc_log('用户管理', '修改当前用户信息')
    def put(self, request):
        """
        修改当前用户信息
        ---
        parameters:
            - name: user_id
              description: 用户名id
              type: string
              paramType: form
              required: true
            - name: first_name
              description: 姓名
              type: string
              paramType: form
              required: false
            - name: password
              description: 密码
              type: string
              paramType: form
              required: false
            - name: email
              description: email
              type: string
              paramType: form
              required: false
            - name: phone
              description: 电话
              type: string
              paramType: form
              required: false
        """
        user_id = request.DATA.get('user_id')
        first_name = request.DATA.get('first_name')
        password = request.DATA.get('password')
        email = request.DATA.get('email')
        phone = request.DATA.get('phone')
        user = ModelUser.objects.get(id=user_id)
        if user.id != request.user.id:
            context = {
                "status": 500,
                "msg": u"不存在这个用户",
                "error": u"不存在这个用户",
            }
            return Response(context)
        if password:
            user.set_password(password)
        if first_name:
            user.first_name = first_name
        if email:
            user.email = email
        if phone:
            user.userinfo.phone = phone
        user.save()
        user.userinfo.save()
        context = {
            "status": 200,
            "msg": u"修改用户信息成功",
        }
        return Response(context)


class CompanyList(APIView):
    """用户管理"""

    def get(self, request):
        """
        获取用户管理公司信息
        :param request:
        :return:
        """
        agent_now = request.user.userinfo.agent
        company_list = [{"key": agent_now.key, "name": agent_now.name}]
        companys = ModelCompany.objects.filter(agent=agent_now)
        for company in companys:
            company_list.append({
                "name": company.name,
                "key": company.key,
            })
        data = {
            "status": 200,
            "companys": company_list
        }
        return Response(data=data)

    @soc_log('用户管理', '创建公司信息')
    def post(self, request):
        """创建公司信息"""
        user = request.user.userinfo
        name = request.data.get("name", None)
        email = request.data.get("email", None)
        phone = request.data.get("phone", None)
        address = request.data.get("address", None)

        username = request.data.get("username", None)
        password = request.data.get("password", None)
        user_email = request.data.get("user_email", None)
        user_phone = request.data.get("user_phone", None)

        if not phone:
            phone = None
        else:
            try:
                phone = int(phone)
            except Exception:
                context = {
                    "status": 500,
                    "error": u'联系方式必须为数字',
                    "msg": u'联系方式必须为数字'
                }
                return Response(context)

        if user.role_type == 2 and user.is_admin == 1:
            agent = user.agent
        elif user.role_type == 1 and user.is_admin == 1:
            agent = user.agent
        else:
            context = {
                "status": 500,
                "error": u'权限不足',
                "msg": u'权限不足'
            }
            return Response(context)
        if not name:
            context = {
                "status": 500,
                "error": u'请输入公司名称',
                "msg": u'请输入公司名称'
            }
            return Response(context)
        if ModelCompany.objects.filter(agent=agent, name=name).count() > 0:
            context = {
                "status": 500,
                "error": u'该公司已存在',
                "msg": u'该公司已存在'
            }
            return Response(context)

        if ModelUser.objects.filter(username=username).count() > 0:
            context = {
                "status": 500,
                "error": u'用户名已被占用',
                "msg": u'用户名已被占用'
            }
            return Response(context)

        context = {
            "agent": agent,
            "request": request,
        }

        new_user = UserSerializer(data={
            "username": username,
            "password": password,
            "confirm_password": password,
            "phone": user_phone,
            "email": user_email,
            "is_admin": 1,
        }, context=context)
        if new_user.is_valid():
            user_obj = new_user.save(role_type=3)
        else:
            for error in new_user.errors:
                context = {
                    "status": 500,
                    "msg": new_user.errors[error][0],
                    "error": new_user.errors[error][0],
                }
                return Response(context)

        try:
            company = ModelCompany.objects.create(name=name, agent=agent, email=email, phone=phone, address=address)
        except Exception as e:
            context = {
                "status": 500,
                "error": u'创建公司失败',
                "msg": u'创建公司失败'
            }
            return Response(context)
        user_obj.userinfo.company_id = company.id
        user_obj.userinfo.save()

        context = {
            "status": 200,
            "msg": u'创建公司成功',
            "data": {"user_id": user_obj.id}
        }
        return Response(context)


class CompanyDetail(APIView):
    """用户管理"""

    def get_obj(self, request, id):
        try:
            company = ModelCompany.objects.get(id=id, agent=request.user.userinfo.agent)
        except ModelCompany.DoesNotExist:
            return False
        return company

    def get(self, request, id):
        """获取公司信息"""
        company = self.get_obj(request, id)
        if not company:
            context = {
                "status": 500,
                "error": u'该公司不存在',
                "msg": u'该公司不存在'
            }
            return Response(context)
        data = {
            "name": company.name,
            "email": company.email,
            "phone": company.phone,
            "address": company.address,
        }
        context = {
            "status": 200,
            "msg": u'获取公司信息成功',
            "data": data
        }
        return Response(context)

    @soc_log('用户管理', '修改公司信息')
    def put(self, request, id):
        """修改公司信息"""
        phone = request.data.get("phone", None)
        company = self.get_obj(request, id)
        if not company:
            context = {
                "status": 500,
                "error": u'该公司不存在',
                "msg": u'该公司不存在'
            }
            return Response(context)
        if not phone:
            phone = None
        else:
            try:
                phone = int(phone)
            except Exception:
                context = {
                    "status": 500,
                    "error": u'联系方式必须为数字',
                    "msg": u'联系方式必须为数字'
                }
                return Response(context)

        company.email = request.data.get("email", company.email)
        company.phone = phone
        company.address = request.data.get("address", company.address)
        company.save()
        context = {
            "status": 200,
            "msg": u'修改公司信息成功'
        }
        return Response(context)

    @soc_log('公司管理', '删除公司信息')
    def delete(self, request, id):
        """删除公司信息"""
        company = self.get_obj(request, id)
        if not company:
            context = {
                "status": 500,
                "error": u'该公司不存在',
                "msg": u'该公司不存在'
            }
            return Response(context)
        context = ""
        if context:
            return Response(context)

        # 删除用户
        userinfos = UserInfo.objects.filter(company=company)
        for userinfo in userinfos:
            userinfo.user.delete()

        company.delete()

        context = {
            "status": 200,
            "msg": u'删除公司信息成功'
        }

        return Response(context)


class CompanySelect2(APIView):
    """网络设备信息"""

    def post(self, request):
        """
        获取网络设备类型列表
        ---
        parameters:
            - name: q
              description:查询字符串
              type: string
              paramType: form
              required: False
            - name: page
              description:第几页（默认第1页）
              type: string
              paramType: form
              required: False
            - name: page_size
              description:每页显示多少条记录（默认每页5条数据）
              type: string
              paramType: form
              required: False
        """

        agent_now = request.user.userinfo.agent
        q = request.DATA.get("q", '')
        isp_list = ModelCompany.objects.filter(name__contains=q, agent=agent_now).values("id", "name")
        context = select2_filter(request, isp_list)
        return Response(context)


class PNGRenderer(renderers.BaseRenderer):
    """用户信息"""
    media_type = 'image/png'
    format = 'png'
    charset = None
    render_style = 'binary'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """图片信息"""
        if data is None:
            return bytes()

        if renderer_context['response'].status_code != status.HTTP_200_OK:
            return bytes()

        with BytesIO() as out_buffer:
            data.save(out_buffer, "PNG")
            image_binary = out_buffer.getvalue()
            b64string = base64.b64encode(image_binary)

        return b64string


class UserTwoFactorQRcode(APIView):
    """用户信息"""
    renderer_classes = [PNGRenderer]

    def put(self, request):
        """验证用户信息"""
        step = request.DATA.get("step", None)
        captcha = request.DATA.get("captcha", None)
        user_now = request.user
        pct = PhoneCaptchaTools()
        gtft = GoogleTwoFactorTools()
        if step == 1:
            if not pct.v_captcha(user_now.phone, captcha=captcha, user_key=user_now.id):
                return Response({"status": 500, "msg": "短信验证码错误或已过期"})
            img = gtft.create(user_now.username, user_now.id)
            return Response(img, content_type='image/png')

        if step == 2:
            is_vaild, google_secret = gtft.v_captcha(username=user_now.username, captcha=captcha, user_key=user_now.id)
            if is_vaild:
                user_now.userinfo.google_secret = google_secret
                user_now.userinfo.save()
            else:
                return Response({"status": 500, "msg": "二次验证码错误或已过期"})

        return Response({"status": 500, "msg": "步骤错误"})

    def post(self, request):
        """
        生成用户的二次验证的二维码
        """
        agent_now = request.user.userinfo.agent
        user_now = request.user
        user_id = request.DATA.get("user_id")
        if user_id == user_now.id:
            # 修改自己
            user = user_now
        elif user_now.userinfo.role_type == 1:
            # 青松
            user = ModelUser.objects.filter(id=user_id).first()
        elif user_now.userinfo.role_type == 2:
            # 代理商
            user = ModelUser.objects.filter(id=user_id, userinfo__agent=agent_now).first()
        else:
            user = ModelUser.objects.filter(id=user_id, userinfo__agent=agent_now,
                                            userinfo__company=user_now.userinfo.company).first()
        google_qrcode = generate_google_url(user.username)
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=2,
        )
        qr.add_data(google_qrcode[3])
        qr.make(fit=True)
        img = qr.make_image()
        image = img.get_image()
        if user and image:
            user.userinfo.google_secret = google_qrcode[0]
            user.userinfo.save()
        # imgByteArr = io.BytesIO()
        # img.save(imgByteArr, format='PNG')
        # imgByteArr = imgByteArr.getvalue()
        # b64string = base64.b64encode(imgByteArr)

        return Response(img, content_type='image/png')

    def delete(self, request):
        """解绑"""
        captcha = request.DATA.get("captcha", None)
        user_now = request.user
        pct = PhoneCaptchaTools()
        if not pct.v_captcha(user_now.phone, captcha=captcha, user_key=user_now.id):
            return Response({"status": 500, "msg": "短信验证码错误或已过期"})
        user_now.userinfo.google_secret = ""
        user_now.userinfo.gs_status = 0
        user_now.userinfo.save()
        return Response({"status": 200, "msg": "解绑成功"})


def encrypt(text, private_key):
    cryptor = AES.new(private_key, AES.MODE_ECB)
    length = 16
    count = len(text)
    if count < length:
        add = (length - count)
        # \0 backspace
        text = text + ('\0' * add)
    elif count > length:
        add = (length - (count % length))
        text = text + ('\0' * add)
    ciphertext = cryptor.encrypt(text)
    return b2a_hex(ciphertext)
