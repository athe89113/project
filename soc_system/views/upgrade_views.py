# coding=utf-8
from __future__ import unicode_literals
import random
import os
from django.utils import timezone
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from soc_system import models
from soc_system import serializers
from utils.media_handler import save_uploaded_file
from soc_system.tasks import send_status, upgrade_targets
from soc_system.system_common import get_node_detail
from soc_system.tools.upgrade import GPG
from utils.exceptions import SocException
import logging
logger = logging.getLogger('console')


class SystemUpgradeFileUpload(APIView):
    """
    服务器文件
    """
    parser_classes = (MultiPartParser,)

    def get(self, request):
        """
        上传进度
        :param request:
        :return:
        """
        progress_id = request.query_params.get("progress_id")

        cache_key = "upload_file:%s:%s" % (request.META['REMOTE_ADDR'], progress_id)

        cached_data = cache.get(cache_key, {"percent": 0, "status": 0, "step": 0, "error_msg": "未获取到对应上传过程"})

        data = {
            "percent": cached_data.get("percent"),
            "status": cached_data.get("status"),
            "error_msg": cached_data.get("error_msg"),
            "step": cached_data.get('step'),
        }

        context = {
            "status": 200,
            "msg": "获取进度成功",
            "data": data
        }
        return Response(context)

    def _update_cache(self, request, progress_id, data):
        """
        更新
        :param request:
        :param progress_id:
        :param data: 字典
        :return:
        """
        if progress_id:
            cache_key = "upload_file:%s:%s" % (request.META['REMOTE_ADDR'], progress_id)
            cache_data = cache.get(cache_key, {})
            cache_data.update(data)
            cache.set(cache_key, cache_data, 300)

    def post(self, request):
        """
        上传系统更新文件
        :param request:
        :return:

            - file_name             文件名称
            - browser_download_url  可下载地址
            - file_id               升级文件 ID（之后的接口中要用到）
            - type                  解析出的文件类型，对应7种文件类型
            - upgrade_type          升级包为{系统/事件/引擎}升级包
            - version               版本为xx.xx.xx，
            - build_date            构建时间xxxx-xx-xx
        """

        upgrade_file = request.FILES.get("upgrade_file")
        if not upgrade_file:
            context = {
                "status": 500,
                "msg": "请指定上传文件",
                "error": "请指定上传文件",
            }
            return Response(context)

        upgrade_type = request.POST.get('upgrade_type')
        if not upgrade_type:
            context = {
                "status": 500,
                "msg": "请指定升级类型",
                "error": "请指定升级类型",
            }
            return Response(context)

        progress_id = None
        if 'progress_id' in self.request.GET:
            progress_id = self.request.GET['progress_id']
        elif 'HTTP_X_PROGRESS_ID' in self.request.META:
            progress_id = self.request.META['HTTP_X_PROGRESS_ID']
        # step = 2 暂存文件
        self._update_cache(request, progress_id, {"percent": 55, 'step': 2})
        dest, dest_url = save_uploaded_file(upgrade_file)
        if not dest:
            logger.error(dest_url)
            self._update_cache(request, progress_id, {"error_msg": '暂存文件失败', "status": 2})
            context = {
                "status": 500,
                "msg": "保存文件失败",
                "error": "保存文件失败",
            }
            return Response(context)
        # step = 3 正在校验文件
        self._update_cache(request, progress_id, {"percent": 60, 'step': 3})
        file_name = dest.split('/')[-1]

        # verify upload file
        random_name = ''.join([random.choice('1234567890abcdefghijklmnopqrstuvwxyz') for i in range(25)])
        random_file = '/tmp/{}.tar.gz'.format(random_name)
        try:
            gpg = GPG()
            status, result = gpg.decrypt(dest, random_file)
            f_type, version = gpg.info(random_file)
        except Exception as e:
            logger.error(e)
            if 'sign_error' in e:
                error_msg = '上传文件签名错误'
            elif 'Package Error' in e:
                error_msg = "上传完整性校验错误"
            elif "Decryption Error" in e:
                error_msg = '上传文件校验错误'
            elif 'Please Install gunpg' in e:
                error_msg = '系统校验配置错误'
            else:
                error_msg = '上传文件解析错误'

            self._update_cache(request, progress_id, {"error_msg": error_msg, "status": 2})
            context = {
                "status": 500,
                "msg": error_msg,
                "error": error_msg,
            }
            return Response(context)

        self._update_cache(request, progress_id, {"percent": 70, "step": 4})
        # 检查文件类型和升级类型是否匹配
        # TODO 扩展其他类型，现在只支持中心和 nids
        supported = {
            "system": ['center'],
            "event": ['vul'],
            "engine": ['nids']
        }
        if f_type not in supported.get(upgrade_type, []):
            self._update_cache(request, progress_id, {"error_msg": "升级类型与上传的文件类型不符合", "status": 2})
            context = {
                "status": 500,
                "msg": "升级类型与上传的文件类型不符合",
                "error": "升级类型与上传的文件类型不符合",
            }
            return Response(context)

        # 检查版本是否正确
        if not len(version[1:].split('.')) > 1:
            self._update_cache(request, progress_id, {"error_msg": "文件版本错误", "status": 2})
            context = {
                "status": 500,
                "msg": "上传文件校验错误",
                "error": "上传文件校验错误",
            }
            return Response(context)
        self._update_cache(request, progress_id, {"percent": 80, "step": 4})

        data = {
            "agent": request.user.userinfo.agent,
            "name": file_name,
            "u_type": f_type,
            "upgrade_type": upgrade_type,
            "version": version,
            "path": dest,
            "build_date": timezone.now()
        }

        # 保存信息
        try:
            new_file = models.SystemUpgradeFile.objects.create(**data)
            self._update_cache(request, progress_id, {"percent": 90, "step": 4})
        except Exception as e:
            logger.error(e)
            self._update_cache(request, progress_id, {"error_msg": "上传文件保存错误", "status": 2})
            new_file = None
        if not new_file:
            # 删除文件
            if os.path.exists(dest):
                os.remove(dest)
            context = {
                "status": 500,
                "msg": "保存文件失败",
                "error": "保存文件失败",
            }
            return Response(context)

        build_date = timezone.localtime(new_file.build_date).strftime("%Y-%m-%d %H:%M:%S")
        self._update_cache(request, progress_id, {"percent": 100, "status": 1, "step": 5})
        success_msg = "升级文件正常，升级包为 {upgrade_type} 升级包，版本为 {version}，构建时间 {build_date}".format(**{
            "upgrade_type": {"system": "系统", "event": "事件", "engine": "引擎"}.get(upgrade_type, ''),
            "version": version,
            "build_date": build_date
        })
        self._update_cache(request, progress_id, {"success_msg": success_msg})

        context = {
            "status": 200,
            "msg": "ok",
            "data": {
                "file_name": file_name,
                "browser_download_url": dest_url,
                "file_id": new_file.id,
                "u_type": f_type,
                "upgrade_type": upgrade_type,
                "version": version,
                "build_date": build_date,
            }
        }
        return Response(context)


class SystemUpgradeProgress(APIView):
    """
    升级进度
    """

    def post(self, request):
        """

        :param request:
        :return:
        """
        send_status(**request.data)
        return Response({"msg": "ok", "status": 200})


class SystemUpgradeNodes(APIView):
    """
    中心升级列表，结构及状态
    """

    def get(self, request):
        """
        获取中心升级列表
        :param request:
        :return:

            - nodes
                - name      节点名称
                - status

                    0: 不可升级
                    1: 可升级
                    2: 已升级
                    3: 上级未升级

                - is_self 是否本级中心  1-是；0-否
                - reason    原因
                - type      节点类型 => 显示当前可用来升级的类型，7种之一
        """

        upg_node = serializers.UpgradeNodeSerializers(data=request.query_params, context={"request": request})
        if upg_node.is_valid():
            u_type = upg_node.validated_data.get("u_type")
            # TODO replace with file version
            upgrade_file = upg_node.validated_data.get('file')
            file_version = upgrade_file.version
            file_u_type = upgrade_file.u_type
            file_info = {"version": file_version, 'u_type': file_u_type}
        else:
            msg = "获取中心升级列表错误"
            for error in upg_node.errors:
                msg = upg_node.errors[error][0]
                break
            context = {
                "status": 500,
                "msg": msg,
                "error": upg_node.errors
            }
            return Response(context)

        agent_now = request.user.userinfo.agent
        # 本级中心
        # 可升级: 1.
        self_node = models.Node.objects.filter(agent=agent_now, role='self').first()
        if not self_node:
            context = {
                "status": 500,
                "msg": "请先配置本级中心",
                "error": "请先配置本级中心"
            }
            return Response(context)
        # 获取升级拓扑
        tree = get_node_detail(agent_now, file_info)

        context = {
            "status": 200,
            "msg": "获取成功",
            "data": tree
        }
        return Response(context)


class SystemUpgradeRetry(APIView):
    """
    重试
    """
    def post(self, request):
        """
        重试升级任务
        :param request:
        :return:
        """
        agent_now = request.user.userinfo.agent
        retry_ser = serializers.SystemUpgradeRetrySerializers(data=request.data, context={"request": request})
        if retry_ser.is_valid():
            # 重试任务
            task_id = retry_ser.validated_data.get('task_id')
            task = models.SystemUpgradeTask.objects.get(id=task_id)
            data = {
                "file_id": task.file_uuid,
                "u_type": task.u_type,
                "targets": [
                    {"uuid": task.target_uuid, "id": task.target_id}
                ]
            }

            upgrade_ser = serializers.SystemUpgradeSerializers(data=data,
                                                               context={"request": request, "agent": agent_now})
            if upgrade_ser.is_valid():
                upgrade_detail = upgrade_ser.save()
            else:
                msg = "重试升级任务错误"
                for error in upgrade_ser.errors:
                    msg = upgrade_ser.errors[error][0]
                    break
                context = {
                    "status": 500,
                    "msg": msg,
                    "error": upgrade_ser.errors
                }
                return Response(context)

            upgrade_targets(agent_now, upgrade_detail)

        else:
            msg = "重试升级任务错误"
            for error in retry_ser.errors:
                msg = retry_ser.errors[error][0]
                break
            context = {
                "status": 500,
                "msg": msg,
                "error": retry_ser.errors
            }
            return Response(context)
        context = {
            "status": 200,
            "msg": "任务重试中",
        }
        return Response(context)


class SystemUpgradeList(APIView):
    """
    升级处理
    """

    def get(self, request):
        """
        升级列表
        :param request:
        :return:
        """
        agent_now = request.user.userinfo.agent
        u_type = request.query_params.get("u_type")
        filter_data = dict()
        if u_type and u_type in ["center", "monitor", "scan", "defense", "cloud_defense", "hids", "nids"]:
            filter_data["u_type"] = u_type

        upgrade_tasks = models.SystemUpgradeTask.objects.filter(agent=agent_now, **filter_data)

        """
            - task_id           升级任务ID
            - name              中心名称
            - current_version   当前版本
            - upgrade_version   升级版本
            - status            状态，0-未完成，1-完成，2-错误
            - percent           完成百分比
        """
        upgrade_list = []
        for u_task in upgrade_tasks:
            upgrade_list.append({
                "task_id": u_task.id,
                "name": u_task.target_name,
                "current_version": u_task.target_version,
                "upgrade_version": u_task.file_version,
                "status": u_task.status,
                "percent": u_task.percent,
            })
        status_list = upgrade_tasks.values_list("status", flat=True)
        status = 0
        if 0 in status_list:
            # 正在升级
            status = 1

        context = {
            "status": 200,
            "msg": "获取列表成功",
            "data": {
                "status": status,
                "list": upgrade_list
            }
        }
        return Response(context)

    def post(self, request):
        """
        添加升级

        {
            {
                "file_id": 1,
                "u_type": "center",
                "targets": [
                  {"uuid": "uuid-1", "id": 1},
                  {"uuid": "uuid-2", "id": 2}
                ]
            }
        }
        :param request:
        :return:
        """
        agent_now = request.user.userinfo.agent

        upgrade_ser = serializers.SystemUpgradeSerializers(data=request.data, context={"request": request, "agent": agent_now})
        if upgrade_ser.is_valid():
            upgrade_detail = upgrade_ser.save()
        else:
            msg = "添加升级任务错误"
            for error in upgrade_ser.errors:
                msg = upgrade_ser.errors[error][0]
                break
            context = {
                "status": 500,
                "msg": msg,
                "error": upgrade_ser.errors
            }
            return Response(context)

        upgrade_targets(agent_now, upgrade_detail)

        return Response({"msg": "添加升级任务成功", "status": 200})
