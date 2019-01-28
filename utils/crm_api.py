# coding=utf-8
from __future__ import unicode_literals
import requests
import json
import logging
from django.conf import settings
logger = logging.getLogger("soc_purchase")
crm_api_url = settings.CRM_URL


class Crm(object):
    """
    crm接口 => 针对用户
    """

    def __init__(self, api_url=crm_api_url, user=None, timeout=0, private_key='', ys_token=''):
        """
        :param api_url: api地址，比如 'https://crm.qssec.com'
        :param user: 用户
        """
        self.url = api_url
        self.user = user
        self.timeout = int(timeout)
        self.ys_token = ys_token
        self.private_key = private_key

    def access_api(self, api_url, method="POST", args=None, headers=None):
        """
        请求接口
        :param api_url: api 地址
        :param method: 请求方法，默认为"POST"
        :param args: 请求参数
        :param headers: 请求头
        :return:
        """
        api_url = "api/soc" + api_url
        api_url = self.url + api_url
        # 访问api
        headers = {}
        if not headers:
            return {'status': 500, 'msg': "请求认证错误", "error": "请求错误(#no_sign)"}
        headers['Content-Type'] = "application/json"

        if args and method != "GET":
            args = json.dumps(args)

        # print("-------- API Start --------")
        # print(u"API URL--------", api_url)
        # print(u"Headers--------", headers)
        # print(u"Method--------", method)
        # print(u"args--------", args)

        try:
            if self.timeout:
                timeout = self.timeout
            else:
                timeout = self.user.userinfo.agent.qs_api_timeout
            r = requests.request(method, url=api_url, params=args, data=args,
                                 timeout=timeout, headers=headers)
            # check sign
            # if not check_response_sign(r, self.user):
            #     context = {
            #         "return_code": 500,
            #         "message": "请求认证错误，请联系管理员",
            #         "error": "返回验证错误(#return_sign_error)"
            #     }
            #     return context
            logger.info(r.content)
            result = json.loads(r.content)
        except requests.exceptions.SSLError as e:
            logger.error(e)
            context = {
                "status": 500,
                "msg": "请求认证错误，请联系管理员",
                "error": "证书错误(#wrong_cert)"
            }
            return context
        except requests.exceptions.Timeout as e:
            logger.error(e)
            return {'status': 500, 'msg': "请求超时", "error": "请求超时(#timeout)"}
        except Exception as e:
            logger.error(e)
            print(e)
            return {'status': 500, 'msg': "数据请求错误", "error": "请求错误(#request_error1)"}

        if result.get('return_code', 500) != 1:
            error = result.get("message", '')
            logger.error(error)
            return {'status': 500, 'msg': error if error else "数据请求错误(#request_error2)", "error": "数据请求错误(#request_error2)"}
        else:
            result.update(
                {
                    "status": 200,
                    "msg": "ok"
                }
            )
        # 返回结果 json
        # print(result)
        return result

    def get_agent_info(self):
        """
        获取当前代理商在CRM上的信息
        :return: 
        """
        api = "/agent/"
        result = self.access_api(api, "GET")
        return result

if __name__ == '__main__':
    pass
    # r = auth_license("ca8350d0e8d011e49051d4bed97233e4")
    # license = "ca8350d0e8d011e49051d4bed97233e4"
    # crm = Crm(api_url='', api_token='', api_license=license)
    # token = crm.access_token()["access_token"]
    # data = {'custom_name': '青松test2',
    #         'custom_price': 222,
    #         'status': 0}
    # id = 30
    # r = put_hw_agent_service(license, token, data, id)
    # r = get_hw_agent_service(license, token)
    # r = crm.service_config_home_data(license, token)
    # print access_token("7407e7aebe3511e4b385d4bed97233e4")
