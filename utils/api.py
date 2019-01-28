# coding: utf-8
import json
import logging
import requests
import urlparse
from hashlib import md5
from django.utils import timezone
from utils import version
logger = logging.getLogger("soc")

class NodeApi:
    """
    中心操作 API
    """

    def __init__(self, base_url, auth_key="", secret_id="", secret_key=""):
        """
        assert not auth_key or not (secret_id and secret_key)
        :param base_url:
        :param auth_key:
        :param secret_id:
        :param secret_key:
        """
        self.base_url = base_url
        self.auth_key = auth_key
        self.secret_id = secret_id
        self.secret_key = secret_key
        assert not auth_key or not (secret_id and secret_key)

    def get_pem(self):
        """
        签名
        :return:
        """
        _timestamp = timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S")
        _signature = md5(str(self.secret_id) + _timestamp + self.secret_key).hexdigest()
        _data = {
            "X-SECRET-ID": self.secret_id,
            "X-TIMESTAMP": _timestamp,
            "X-SIGNATURE": _signature,
        }
        return _data

    def request(self, api, method='POST', params=None, headers=None, files=None, timeout=20, is_api=True):
        """
        请求
        :param api:
        :param method:
        :param params:
        :param headers:
        :param files:
        :param timeout:
        :param is_api:
        :return:
        """
        url = urlparse.urljoin(self.base_url, api)
        if not headers:
            new_headers = {"Content-Type": 'application/json; charset=utf-8'}
            if files:
                new_headers = {}
        else:
            new_headers = dict()
            new_headers.update(headers)
        if is_api:
            new_headers.update(self.get_pem())
        # api 参数
        try:
            if method.lower() == "get":
                rsp = requests.get(url, params=params, headers=new_headers, timeout=timeout)
            elif method.lower() in ['post', 'put', 'delete']:
                if params:
                    params = json.dumps(params)
                access = getattr(requests, method.lower())
                rsp = access(url, data=params, headers=new_headers, timeout=timeout, files=files)
            else:
                raise Exception("Error request method")
        except requests.exceptions.ConnectionError as e:
            logger.error(e)
            context = {
                "status": 500,
                "msg": "请求连接错误",
                "error": "请求连接错误(#connection_error)"
            }
            return context
        except Exception as e:
            logger.error(e)
            context = {
                "status": 500,
                "msg": "请求错误",
                "error": "请求错误(#error)"
            }
            return context
        # 处理API接口错误
        if rsp.status_code != 200:
            logger.error(rsp.status_code)
            logger.error(rsp.text)
            context = {
                "status": 500,
                "msg": "请求下级中心错误(" + str(rsp.status_code) + ")",
                "error": "请求错误(" + str(rsp.status_code) + ")"
            }
            return context
        result = rsp.json()
        if str(result.get("status") or 500).startswith('5'):
            context = {
                "status": 500,
                "msg": result.get("msg") or '访问请求错误',
                "error": "请求错误(#5xx)"
            }
            return context
        else:
            return result

    def api(self):
        """
        ys api
        :return:
        """
        return YSApi(base_url=self.base_url, secret_id=self.secret_id, secret_key=self.secret_key)

    def fetch_auth(self, self_node_info):
        """
        获取认证
        :param self_node_info: node info
        :return:
        """
        params = {
            "auth_key": self.auth_key,
            "version": version.get_version(self_node_info['version'], type='string'),
            "type": self_node_info['type'],
            "name": self_node_info['name'],
            "ip": self_node_info['ip'],
            "uuid": self_node_info['uuid'],
        }
        # 不通过 token 验证
        result = self.request('/api/system/nodes/auth', method="POST", params=params, is_api=False, timeout=5)
        if result["status"] == 500:
            if "connection_error" in result['error']:
                result["msg"] = '请求中心错误，地址不可达'
                result["error"] = '请求中心错误，地址不可达'
        return result

    def get_parent_status(self):
        """
        获取上级中心状态
        :return:
        """
        params = {
            "auth_key": self.auth_key,
        }
        result = self.request('/api/system/nodes/p_status', method="GET", params=params, is_api=False)
        if result["status"] == 500:
            if "connection_error" in result['error']:
                result["msg"] = '请求中心错误，地址不可达'
                result["error"] = '请求中心错误，地址不可达'

        if result["status"] == 200:
            # 链接正常
            return result["data"], (200, '获取状态成功')
        elif result["status"] == 500:
            # 请求 API
            return {}, (500, '地址不可达')
        else:
            # 根据 code 处理信息
            return {}, (result["status"], self.get_status_msg(result["status"]))

    def get_status(self):
        """
        获取状态
        :return: (code, code_msg)
        """
        result = self.api().get('/api/system/nodes/self')
        if result["status"] == 200:
            # 链接正常
            return 1, (200, '获取状态成功')
        elif result["status"] == 500:
            # 请求 API
            return 0, (500, '地址不可达')
        else:
            # 根据 code 处理信息
            return 0, (result["status"], self.get_status_msg(result["status"]))

    def get_detailed_status(self):
        """
        详细状态状态
        :return: (code, code_msg)
        """
        result = self.api().get('/api/system/nodes/self')
        if result["status"] == 200:
            # 链接正常
            return result["data"], 'ok'
        elif result["status"] == 500:
            # 请求 API
            return {}, (500, '地址不可达')
        else:
            # 根据 code 处理信息
            return {}, (result["status"], self.get_status_msg(result["status"]))

    def get_topo(self):
        """
        get topo
        :return:
        """
        result = self.api().get('/api/system/nodes/topo')
        if result["status"] == 200:
            # 正常
            return result["data"]
        else:
            return []

    def get_components(self):
        """
        组件
        :return:
        """
        result = self.api().get('/api/system/nodes/components')
        if result["status"] == 200:
            # 正常
            return result["data"]
        else:
            return {}

    def get_children_components(self):
        """
        子中心组件
        :return:
        """
        result = self.api().get('/api/system/nodes/children/components')
        if result["status"] == 200:
            # 正常
            return result["data"]
        else:
            return {}

    def get_status_msg(self, status):
        """
        :param status:
        :return:
        """
        code = {
            200: "级联连接正常",
            500: "地址不可达",
            401: "下级中心不允许级联管理",
            402: "级联秘钥错误",
            403: "中心版本需要升级",
            404: "上级中心未添加级联",
        }
        return code.get(status, '请求错误')

    def fetch_report_log_list(self, params):
        """
        获取中心的日志
        :return:
        """
        result = self.api().post('/api/nids/report/log/dts', params=json.dumps(params))
        result['recordsFiltered'] = result.get('recordsFiltered', 0)
        result['recordsTotal'] = result.get('recordsTotal', 0)
        result['data'] = result.get('data', [])
        return result

    def get_one_report_log(self, params):
        """
        获取单条日志
        :param params:
        :return:
        """
        result = self.api().get('/api/nids/report/log', params=params)
        return result

    def fetch(self, method, api, params=None):
        """
        通用调用API接口
        """
        result = self.api().request(method=method, api=api, params=params, timeout=10)
        return result

    def clear_node(self, params):
        """通知节点删除其父/子节点"""
        result = self.api().delete("/api/system/nodes/clear/api", params=params)
        logger.info(result)
        if result['status'] == 200:
            return result['status']
        else:
            return 500

    def clear_node_parent(self):
        """通知父节点删除子节点"""
        params = {
            "auth_key": self.auth_key,
        }
        result = self.request('/api/system/nodes/clear/api/parent', method="DELETE", params=params, is_api=False)
        logger.info(result)
        if result['status'] == 200:
            return 200
        return 500

if __name__ == "__main__":
    # 设置 django 环境
    import os
    import django

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "soc.settings")
    django.setup()

    s_id = 1
    s_key = "VvvX1nAuOiTkqwfEbzSeupwWcBQBGsM9"
    ys_url = 'http://127.0.0.1:8000'

    a = YSApi(base_url='http://127.0.0.1:8000', secret_id=s_id, secret_key=s_key)
    rp = a.get('/api/system/menu')
    print(rp)
