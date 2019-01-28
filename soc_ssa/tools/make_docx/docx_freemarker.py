# -*- coding:utf-8 -*-


import base64
import json
import logging
import os
import subprocess
import uuid
from datetime import datetime

import jpype

from soc.settings import BASE_DIR

logger = logging.getLogger('soc_ssa')


def make_template_docx(template, path, data):
    '''
    封装 模版数据
    '''
    content = dict()
    imgs = []
    # if template.id <= 12 and template.id > 0:  # 固定报表
    tpl = 'template.ftl'
    for item in data:
        if item['type'] == 'echart':
            if item['chart_type'] == 'table':  # 表格类型
                pass
            elif item['chart_type'] == 'table_merge':  # 合并表格类型
                if len(item['merges']) > 0:
                    table = formate_table_merge_data(data=item['data']['data'], merges=item['merges'])
                    item['data']['index'] = table['index']
                    item['data']['data'] = table['data']
            elif item['chart_type'] == 'number':  # 计数
                count = 0
                for i in item['data']['data']:
                    for _ in i['data']:
                        count += _
                item['count'] = count
            else:  # 图片
                img_path = item['chart_path']
                base64 = get_img_base64(img_path)
                item['chart_type'] = 'img'
                item['img_index'] = len(imgs)
                imgs.append(base64)
        else:
            pass
    content['content'] = data
    content['imgs'] = imgs
    make_freemarker_docx(template=tpl, doc_file=path, content=content)


def get_img_base64(path):
    '''
    获取图片base64
    '''
    f = open(path, 'rb')  # 二进制方式打开图文件
    base64_image = base64.b64encode(f.read())  # 读取文件内容，转换为base64编码
    f.close()
    return base64_image


def formate_table_merge_data(data, merges):
    '''
    封装表格合并数据
    '''
    name_list = []
    index_list = []
    for index, item in enumerate(data):
        if index != 0 and name_list[-1] == item[0]:
            index_list[-1].append(index)
        else:
            name_list.append(item[0])
            index_list.append([index])
    indexs = []
    for item in index_list:
        if len(item) > 1:
            indexs.append(item[0])
            for index in item:
                if index != item[0]:
                    for m in merges:
                        data[index][m] = ''

    result = {
        'index': indexs,
        'data': data
    }
    return result


def make_freemarker_docx(template, doc_file, content):
    '''
    生成word文档
    :param template:  模版文件
    :param doc_file:  生成doc文件路径+名称
    :param content:   模版替换内容 需为dict类型 或json字符串
    :return:
    '''
    try:
        logger.info('Freemarker生成work文档开始.{}'.format(datetime.now()))

        if isinstance(content, dict):
            data = json.dumps(content)

        elif isinstance(content, str):
            data = content
        else:
            pass
            logger.info('Freemarker数据格式存在问题,请检查!')

        # 将数据写入文件
        data_file = os.path.join(BASE_DIR, 'media', 'reports', 'tmp_data', 'data_{}.json'.format(uuid.uuid4()))
        fh = open(data_file, 'w')
        fh.write(data)
        fh.close()

        jar_path = os.path.join(BASE_DIR, 'soc_ssa', 'tools', 'libs', 'freemarkerUtils.jar')
        template_path = os.path.join(BASE_DIR, 'soc_ssa', 'tools', 'make_docx', 'template')
        doc_file = os.path.join(BASE_DIR, doc_file)
        cmd = 'java -jar {} "{}" "{}" "{}" "{}"'.format(jar_path, template_path, template, doc_file, data_file)
        logger.info('cmd:{}'.format(cmd))
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while True:
            buff = p.stdout.readline()
            if buff == '' and p.poll() != None:
                break
            else:
                logger.info('result: {}'.format(buff))

        logger.info('Freemarker生成work文档结束.{}'.format(datetime.now()))

        return True
    except Exception as e:
        logger.error(e)

        return False


def make_freemarker_docx1(template, doc_file, content):
    '''
    生成word文档
    :param template:  模版文件
    :param doc_file:  生成doc文件路径+名称
    :param content:   模版替换内容 需为dict类型 或json字符串
    :return:
    '''
    try:
        logger.info('Freemarker生成work文档开始.{}'.format(datetime.now()))
        jar_fastjson = os.path.join('soc_ssa', 'tools', 'libs', 'fastjson-1.2.7.jar')
        jar_freemarker = os.path.join('soc_ssa', 'tools', 'libs', 'freemarker-2.3.23.jar')
        jar_freemarkerUtils = os.path.join('soc_ssa', 'tools', 'libs', 'freemarkerUtils.jar')

        if not jpype.isJVMStarted():
            jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", '-Xmx1024m',
                           "-Djava.class.path=%s;%s;%s" % (jar_fastjson, jar_freemarker, jar_freemarkerUtils))
            # if not jpype.isThreadAttachedToJVM():
            # 开启多线程支持
            # jpype.attachThreadToJVM()

        myFreemarker = jpype.JClass('cn.secray.MyFreemarker')

        template_path = os.path.join('soc_ssa', 'tools', 'make_docx', 'template')

        if isinstance(content, dict):
            data = json.dumps(content)

        elif isinstance(content, str):
            data = content
        else:
            pass
            logger.info('Freemarker数据格式存在问题,请检查!')
        result = myFreemarker.creatWord(template_path, template, doc_file, data)
        # jpype.shutdownJVM()
        logger.info('Freemarker生成work文档结束.{}'.format(datetime.now()))

        return result
    except Exception as e:
        logger.error(e)
        # jpype.shutdownJVM()
        return False
