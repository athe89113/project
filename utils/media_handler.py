# coding: utf-8
import os
import uuid
from django.conf import settings
# 处理media文件目录
FILE_UPLOAD_LOCATION = os.path.join(settings.MEDIA_ROOT, 'file_upload')
if not os.path.exists(FILE_UPLOAD_LOCATION):
    os.makedirs(FILE_UPLOAD_LOCATION)


def save_uploaded_file(f, dest=None):
    """
    处理上传文件
    :param f: an UploadedFile object, for example, a_file = request.FILES['file']
    :param dest: 目标文件位置，相对上传文件目录的相对路径, 如 a/b/c.tar.gz
    :return: 文件绝对路径和 url 路径
    """

    if not dest:
        file_name = str(uuid.uuid4())
        dest = '/'.join([file_name[0], file_name[1], file_name])
        dest_url = dest
    else:
        dest_url = dest

    dest_location = os.path.join(FILE_UPLOAD_LOCATION, dest_url)
    folder = os.path.dirname(dest_location)
    if not os.path.exists(folder):
        os.makedirs(folder)

    with open(dest_location, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    return dest_location, '/media/file_upload/' + dest_url
