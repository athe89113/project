# coding: utf-8
from django.core.cache import cache
from django.core.files.uploadhandler import TemporaryFileUploadHandler
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework.exceptions import Throttled
from utils.exceptions import AdminPasswordException, AdminPasswordThrottled


def custom_exception_handler(exc, context):
    """
    自定义处理请求限制消息
    :param exc:
    :param context:
    :return:
    """
    # 自定义处理请求限制消息
    # 参考 http://stackoverflow.com/questions/32932357/custom-throttling-response-in-django-rest-framework

    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if isinstance(exc, Throttled):  # check that a Throttled exception is raised
        # 理论上 429 TOO MANY REQUESTS
        custom_response_data = {  # prepare custom response data
            "status": 429,
            'msg': '接口请求太频繁，请稍后再试',
            'error': 'request limit exceeded'
        }
        response.data = custom_response_data  # set the custom response data on response object

    if isinstance(exc, AdminPasswordException):
        # 管理员密码错误
        if not response:
            response = Response()
        custom_response_data = {  # prepare custom response data
            "status": 403,
            'msg': '管理员密码错误',
            'errors': {"admin_password": ['管理员密码错误'], }
        }
        response.data = custom_response_data  # set the custom response data on response object

    if isinstance(exc, AdminPasswordThrottled):
        # 管理员密码错误
        if not response:
            response = Response()
        custom_response_data = {  # prepare custom response data
            "status": 403,
            'msg': '请求次数过多，请稍后再尝试',
            'errors': '请求次数过多，请稍后再尝试'
        }
        response.data = custom_response_data  # set the custom response data on response object

    return response


class ProgressFileUploadHandler(TemporaryFileUploadHandler):
    """
    Cache system for TemporaryFileUploadHandler

    copied from https://github.com/ouhouhsami/django-progressbarupload
    """
    def __init__(self, *args, **kwargs):
        super(TemporaryFileUploadHandler, self).__init__(*args, **kwargs)
        self.progress_id = None
        self.cache_key = None
        self.original_file_name = None

    def handle_raw_input(self, input_data, META, content_length, boundary, encoding=None):
        """

        :param input_data:
        :param META:
        :param content_length:
        :param boundary:
        :param encoding:
        :return:
        """
        self.content_length = content_length
        # TODO 处理 POST 中的 progress_id 导致的死循环
        if 'progress_id' in self.request.GET:
            self.progress_id = self.request.GET['progress_id']
        elif 'HTTP_X_PROGRESS_ID' in self.request.META:
            self.progress_id = self.request.META['HTTP_X_PROGRESS_ID']
        if self.progress_id:
            self.cache_key = "upload_file:%s:%s" % (self.request.META['REMOTE_ADDR'], self.progress_id)
            cache.set(self.cache_key, {
                'size': self.content_length,
                'received': 0,
                'step': 1,
                "success_msg": '',
                "error_msg": "",
            }, 300)

    def new_file(self, field_name, file_name, content_type, content_length, charset=None, content_typ_extra=None):
        self.original_file_name = file_name

    def receive_data_chunk(self, raw_data, start):
        if self.cache_key:
            data = cache.get(self.cache_key, {})
            data['received'] += self.chunk_size
            data['status'] = 0
            data['percent'] = int(50 * data['received'] / data['size'])
            data['step'] = 1
            cache.set(self.cache_key, data, 300)
        return raw_data

    def file_complete(self, file_size):
        pass

    def upload_complete(self):
        # deprecated in favor of setting an expiry time a-la-nginx
        # setting an expiry time fixes the race condition in which the last
        # progress request happens after the upload has finished meaning the
        # bar never gets to 100%
        pass
        # if self.cache_key:
        #     cache.delete(self.cache_key)
