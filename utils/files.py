# coding: utf-8
"""
文件处理
"""
import os
import xlwt
import time
import hashlib
import datetime
from django.conf import settings


def file_size(size):
    """
    文件大小处理
    :param size  int  单位b: 
    :return 字符串加合适的单位 Kb Mb Gb Tb: 
    """
    if size < 1024:
        return str(size) + 'b'
    elif 1024 <= size < 1024 * 1024:
        return str(round(size / 1024.0, 2)) + 'Kb'
    elif (1024 ** 2) <= size < (1024 ** 3):
        return str(round(size / (1024.0 ** 2), 2)) + 'Mb'
    elif (1024 ** 3) <= size < (1024 ** 4):
        return str(round(size / (1024.0 ** 3), 2)) + 'Gb'
    elif (1024 ** 4) <= size < (1024 ** 5):
        return str(round(size / (1024.0 ** 4), 2)) + 'Tb'
    return str(size)


def file_md5_new_name(request, name):
    """
    重命名文件名称
    name 为字符串
    返回改名后的文件类 和旧文件名称
    """
    if name in request.FILES:
        agent = request.user.userinfo.agent
        my_file = request.FILES[name]
        old_name = my_file.name
        m1 = hashlib.md5(str(time.time()))
        my_file.name = agent.name + "_" + \
                       m1.hexdigest() + "." + my_file.name.split(".")[-1]
        return my_file, old_name


def excel_export(filename, labels, headers, values):
    """
    excel export
    :param filename:
    :param labels:
    :param headers:
    :param values:
    :return:
    """
    wb = xlwt.Workbook(style_compression=2, encoding='utf-8')
    ws = wb.add_sheet('data')

    col = 0
    for item in labels:
        ws.write(0, col, item)
        col += 1

    row = 1
    col = 0
    for item in values:
        for header in headers:
            if not header:
                ws.write(row, col, "")
            else:
                if type(item) is dict:
                    value = item.get(header, "")
                else:
                    value = getattr(item, header, "")
                if type(value) == datetime.date:
                    ws.write(
                        row, col, value,
                        xlwt.easyxf(num_format_str='YYYY-MM-DD'))
                else:
                    ws.write(row, col, value)
            col += 1
        col = 0
        row += 1

    file_path = os.path.join('download')
    save_path = os.path.join(settings.MEDIA_ROOT, file_path)
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    wb.save(os.path.join(save_path.encode("utf-8"), filename.encode("utf-8")))
    return os.path.join('media', file_path, filename)
