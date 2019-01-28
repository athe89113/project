#coding=utf-8
"""
数据管理 - 管理HDFS数据
"""
import os
import time
import json
from django.db.models import Q
from django.http import StreamingHttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from pywebhdfs.webhdfs import PyWebHdfsClient
from pywebhdfs.errors import FileNotFound, PyWebHdfsException
from requests.exceptions import ConnectionError
from soc_ssa import models

__all__ = ["FileList", "FileListDts", "FileDownload", "FilePreiewDts"]


def get_hdfs_obj(request):
    """
    获取hdfs对象
    """
    agent = request.user.userinfo.agent
    company = request.user.userinfo.company
    try:
        hdfs_obj = models.SelfServiceConf.objects.get(
            service='hdfs', agent=agent, company=company)
    except models.SelfServiceConf.DoesNotExist:
        return False
    host, port = hdfs_obj.host.split(":")
    hdfs = PyWebHdfsClient(host=host, port=int(port),
                           user_name=hdfs_obj.username)
    return hdfs


def parase_data(request, data, search="name"):
    """
    解析数据 搜索 排序
    """
    method = request.method
    if method == "GET":
        req_data = request.query_params
    else:
        req_data = request.data

    search = req_data.get("search", req_data.get("search[value]"))
    start = req_data.get("start") or 0
    length = req_data.get("length")
    order = req_data.get("order")
    # 排序类型desc asc
    order_type = req_data.get("order_type", "asc")
    try:
        start = int(start)
        length = int(length)
    except (ValueError, TypeError):
        start = length = None

    if search:
        data = filter(lambda x: search in x['name'], data)
    if length:
        data = data[start:start + length]
    if order:
        if order_type == "desc":
            reverse = True
        else:
            reverse = False
        data = sorted(data, key=lambda k: k[order], reverse=reverse)

    return data


class FileList(APIView):
    """
    文件列表
    """

    def get_dir_file(self, request):
        """
        获取文件列表
        """
        agent = self.request.user.userinfo.agent
        company = self.request.user.userinfo.company
        method = self.request.method
        # 默认取根目录
        if method == "GET":
            path = request.query_params.get("path") or "/"
        else:
            path = request.data.get("path") or "/"
        hdfs = get_hdfs_obj(request)
        if not hdfs:
            return Response({"status": 500, "msg": "未配置数据服务器地址"})

        try:
            result = hdfs.list_dir(path)
        except ConnectionError:
            return Response({"status": 500, "msg": "数据服务器地址错误"})
        except FileNotFound:
            return Response({"status": 500, "msg": "路径错误，{}不存在".format(path)})
        files = result['FileStatuses']['FileStatus']
        rsp_data = {
            "msg": "获取成功",
            "result": "ok",
            "status": "200",
            "recordsFiltered": len(files),
            "recordsTotal": len(files),
        }
        data = []
        tags = models.SSADataTag.objects.filter(
            Q(agent=agent, company=company) | Q(agent=None, company=None)).values()
        for i in files:
            file_tag = ""
            full_path = os.path.join(path, i['pathSuffix'])
            for tag in tags:
                if full_path.startswith("/data/{}".format(tag['path'])):
                    file_tag = tag['name']
            if full_path.startswith("/data"):
                lock = 1
            else:
                lock = 0
            data.append({
                "name": i['pathSuffix'],
                "id": i['pathSuffix'],
                "owner": i['owner'],
                "group": i['group'],
                "path": full_path,
                "size": i['length'],
                "tag": file_tag,
                # directory, file
                "type": i['type'].lower(),
                "lock": lock,
                "selected": 0,
                "change_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(i['modificationTime'] / 1000))
            })
        rsp_data['dir_count'] = len(
            filter(lambda x: x['type'] == "directory", data))
        rsp_data['data'] = parase_data(request, data, search="name")
        return Response(rsp_data)

    def get(self, request):
        """
        获取文件列表
        """
        return self.get_dir_file(request)

    def post(self, request):
        """
        添加文件夹
        """
        path = request.data.get("path")
        if not path:
            return Response({"status": 500, "msg": "文件夹名称不能为空"})
        if path.startswith("/data"):
            return Response({"status": 500, "msg": "该文件夹不允许新建"})
        hdfs = get_hdfs_obj(request)
        if not hdfs:
            return Response({"status": 500, "msg": "未配置数据服务器地址"})
        try:
            hdfs.get_file_dir_status(path)
        except FileNotFound:
            pass
        else:
            return Response({"status": 500, "msg": "该文件夹已存在"})

        hdfs.make_dir(path)
        return Response({"status": 200, "msg": "添加成功"})

    def put(self, request):
        """
        修改名称
        """
        old_name = request.data.get("old_name")
        new_name = request.data.get("new_name")
        if not all([old_name, new_name]):
            return Response({"status": 500, "msg": "路径不能为空"})
        if old_name.startswith("/data") or new_name.startswith("/data"):
            return Response({"status": 500, "msg": "该文件不允许修改"})
        hdfs = get_hdfs_obj(request)
        if not hdfs:
            return Response({"status": 500, "msg": "未配置数据服务器地址"})
        try:
            hdfs.get_file_dir_status(new_name)
        except FileNotFound:
            pass
        else:
            return Response({"status": 500, "msg": "该文件夹已存在"})
        hdfs.rename_file_dir(old_name, new_name)
        return Response({"status": 200, "msg": "修改成功"})

    def delete(self, request):
        """
        删除
        """
        # 支持删除多个
        path = request.data.get("path")
        paths = request.data.get("paths")
        if not any([path, paths]):
            return Response({"status": 500, "msg": "路径不能为空"})
        hdfs = get_hdfs_obj(request)

        if isinstance(paths, list):
            paths = paths
        else:
            paths = [path]

        for path in paths:
            if path.startswith("/data"):
                return Response({"status": 500, "msg": "该文件不允许删除"})
            if not hdfs:
                return Response({"status": 500, "msg": "未配置数据服务器地址"})
            try:
                hdfs.delete_file_dir(path)
            except PyWebHdfsException:
                return Response({"status": 500, "msg": "该目录下存在文件"})
        return Response({"status": 200, "msg": "删除成功"})


class FileListDts(FileList):
    """
    文件列表
    """

    def post(self, request):
        """
        获取文件列表
        """
        return self.get_dir_file(request)


class FileDownload(APIView):
    """
    文件下载
    """

    def get(self, request):
        """
        下载文件
        """
        file_path = request.query_params.get("path")
        if not file_path:
            return Response({"status": 500, "msg": "文件路径不能为空"})
        hdfs = get_hdfs_obj(request)
        if not hdfs:
            return Response({"status": 500, "msg": "未配置数据服务器地址"})

        def file_iterator(file_path, chunk_size=1024 * 10):
            """文件流"""
            offset = 0
            while True:
                try:
                    line = hdfs.read_file(
                        file_path, offset=offset, length=chunk_size)
                except PyWebHdfsException:
                    break
                if line:
                    offset += chunk_size
                    yield line
                else:
                    break

        response = StreamingHttpResponse(file_iterator(file_path))
        file_name = file_path.split("/")[-1]
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(
            file_name)
        return response


class FilePreiewDts(APIView):
    """
    数据预览
    """

    def parase_json_data(self, data):
        if len(data) == 0:
            return [], []
        headers = []
        data_list = []
        for key in data[0].keys():
            headers.append(key)
        headers.sort()
        for i in data:
            d = []
            for key in headers:
                d.append(i.get(key))
            data_list.append(d)
        return headers, data_list


    def post(self, request):
        """
        数据预览
        """
        file_path = request.data.get("path")
        if not file_path:
            return Response({"status": 500, "msg": "文件路径不能为空"})
        hdfs = get_hdfs_obj(request)
        if not hdfs:
            return Response({"status": 500, "msg": "未配置数据服务器地址"})
        try:
            file_obj = hdfs.read_file(file_path)
        except PyWebHdfsException:
            return Response({"status": 500, "msg": "读取数据错误"})
        data = []
        for i in file_obj.split("\n"):
            if not i:
                continue
            try:
                data.append(json.loads(i))
            except (ValueError, TypeError):
                data.append({"data": i})
        rsp_data = {
            "msg": "获取成功",
            "result": "ok",
            "status": "200",
            "recordsFiltered": len(data),
            "recordsTotal": len(data),
        }
        data = parase_data(request, data, search="name")
        rsp_data['headers'], rsp_data['data'] = self.parase_json_data(data)
        return Response(rsp_data)
