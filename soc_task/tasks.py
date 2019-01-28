# coding=utf-8
from __future__ import absolute_import

import json
import logging
import os
import time
import uuid
from datetime import datetime, timedelta

from celery.schedules import crontab
from django.db import connection
from django.utils import timezone
# es
from elasticsearch import Elasticsearch, helpers
# hdfs
from hdfs.client import InsecureClient

# 报表
from soc import settings
from soc.celery import app
from soc_assets.models import Assets, TermGroup
from soc_knowledge.models import SmWord
from soc_ssa import models
from soc_ssa.models import SSADataTag, SelfServiceConf
from soc_ssa.tools.make_docx.docx_plugin import MakeDocx
from soc_ssa.tools.make_pdf.pdf_plugin import MakePdf
from soc_ssa.tools.report.report_data import ReportData
from soc_user.models import WorkTime
from soc_knowledge.models import AlarmLog, AlarmRule
from utils.es_select import exec_es_sql

logger = logging.getLogger('task')
# celery -A soc  worker -B
HDFS_HOSTS = settings.HDFS_HOSTS
HDFS_USER = settings.HDFS_USER


@app.task(name='tasks.statistics_asset_task')
def statistics_asset_task():
    """
    资产表的维护
    :return:
    """
    logger.info("statistics_asset_task start time = %s", timezone.now())
    data_tag_list = SSADataTag.objects.all().values('path')
    cursor = connection.cursor()
    try:
        for data_tag in data_tag_list:
            path = data_tag['path']
            start_time, end_time, indexs = get_index_by_count_type(0, path)
            if indexs:
                if path == "ssa-ag-all-terminal":
                    assets_type = 4
                    sql = "select * FROM {} ".format(
                        ", ".join(indexs))
                    result_list = exec_es_sql(sql)
                    for data in result_list:
                        log_type = data['log_type']
                        if log_type == 2:
                            dst_ip = data['login_ip']
                        else:
                            dst_ip = data['term_ip']
                        term_group_id = data['term_group_id']
                        term_group_name = data['term_group_name']
                        term_duty = data['term_duty']
                        if term_group_id:
                            term_group_maintain(term_group_id, term_group_name)
                        asset = Assets.objects.filter(ip=dst_ip, assets_type=assets_type).first()
                        if asset:
                            sql_update = "update soc_assets set last_date = \'{0}\' where ip = \'{1}\' ".format(
                                end_time[0:10], dst_ip)
                            cursor.execute(sql_update)
                        else:
                            sql_insert = "insert into soc_assets(ip,add_date,last_date,assets_name,assets_type,term_group_id,term_duty) " \
                                         "values(\'{0}\',\'{1}\',\'{2}\',\'{3}\',{4},\'{5}\',\'{6}\')".format(dst_ip,
                                                                                                              datetime.now(),
                                                                                                              end_time[
                                                                                                              0:10],
                                                                                                              "",
                                                                                                              assets_type,
                                                                                                              data[
                                                                                                                  'term_group_id'],
                                                                                                              term_duty)
                            cursor.execute(sql_insert)
                elif path == "ssa-ag-fw" or path == "ssa-ag-bd" or path == "ssa-ag-360" or path == "ssa-ag-database" or path == "ssa-ag-gl" or path == "ssa-ag-ids":
                    if path == "ssa-ag-fw":
                        assets_type = 1
                        param_name = "device_name"
                    if path == "ssa-ag-gl":
                        assets_type = 2
                        param_name = "comp_ip"
                    if path == "ssa-ag-bd":
                        assets_type = 3
                        param_name = "comp_ip"
                    if path == "ssa-ag-360":
                        assets_type = 5
                        param_name = "host_ip"
                    if path == "ssa-ag-database":
                        assets_type = 6
                        param_name = "server_ip"
                    if path == "ssa-ag-ids":
                        assets_type = 7
                        param_name = "source"
                    sql = "select {} FROM {} ".format(param_name, ", ".join(indexs))
                    result_list = exec_es_sql(sql)
                    for data in result_list:
                        dst_ip = data[param_name]
                        if dst_ip:
                            asset = Assets.objects.filter(ip=dst_ip, assets_type=assets_type).first()
                            if asset:
                                sql_update = "update soc_assets set last_date = \'{0}\' where ip = \'{1}\' ".format(
                                    end_time[0:10], dst_ip)
                                cursor.execute(sql_update)
                            else:
                                sql_insert = "insert into soc_assets(ip,add_date,last_date,assets_name,assets_type,term_group_id,term_duty) " \
                                             "values(\'{0}\',\'{1}\',\'{2}\',\'{3}\',{4},\'{5}\',\'{6}\')".format(
                                    dst_ip,
                                    datetime.now(),
                                    end_time[0:10],
                                    "",
                                    assets_type,
                                    "",
                                    "")
                                cursor.execute(sql_insert)
                    logger.info("statistics_asset_task end time = %s", timezone.now())
    except Exception as e:
        logger.error("statistics_asset_task error %s ", str(e))
    finally:
        cursor.close()


@app.task(name='tasks.save_terminal_sm_message')
def save_terminal_sm_message():
    """
    SM信息保存
    :return:
    """
    try:
        logger.info("save_terminal_sm_message start time = %s", timezone.now())
        word_dict_list = SmWord.objects.all().values('word')
        word_list = []
        for word in word_dict_list:
            word_list.append(word['word'])
        start_time, end_time, indexs = get_index_by_count_type(1, "ssa-ag-all-terminal")
        sql = "select * FROM {} where log_type in (5,6,7)".format(", ".join(indexs))
        new_result_list = exec_es_sql(sql)
        index = "ssa-event-terminal-" + datetime.now().strftime("%Y-%m-%d-%H")
        # 需要存入到es的数据
        es_data_list = []
        hdfs_data_list = ""
        for data in new_result_list:
            log_type = data['log_type']
            param_time = "act_time"
            if log_type == 7:
                param_name = "act_info"
            if log_type == 5:
                param_name = "print_doc"
            if log_type == 6:
                param_name = "file_name"
            if "term_ip" in data and data['term_ip']:
                ip = data['term_ip']
                term_duty = data['term_duty']
                organization = data['term_group_name']
                event_index = "ssa-ag-all-terminal"
                sm_content = data[param_name]
                event_source = "定时任务"
                event_time = data[param_time]
                if ip and sm_content != '':
                    for word in word_list:
                        if word in sm_content:
                            data = dict()
                            data['event_id'] = str(uuid.uuid4())
                            data['event_top_type'] = "违规事件"
                            data['event_type'] = "SM"
                            data['event_source'] = event_source
                            data['event_index'] = event_index
                            data['term_duty'] = term_duty
                            data['remark'] = json.dumps({"word": word, "sm_content": sm_content}, ensure_ascii=False)
                            data['organization'] = organization
                            data['event_level'] = 1
                            data['terminal'] = ip
                            data['event_time'] = str(
                                datetime.strptime(event_time, "%Y%m%d%H%M%S").strftime('%Y%m%d%H%M%S'))
                            es_data = {
                                "_type": "logs",
                                "_index": index,
                                "@timestamp": datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
                                "event_id": str(uuid.uuid4()),
                                "event_top_type": "违规事件",
                                "event_type": "SM",
                                "event_source": event_source,
                                "event_index": event_index,
                                "term_duty": term_duty,
                                "remark": json.dumps({"word": word, "sm_content": sm_content}, ensure_ascii=False),
                                "organization": organization,
                                "event_level": 1,
                                "terminal": ip,
                                "event_time": str(
                                    datetime.strptime(event_time, "%Y%m%d%H%M%S").strftime('%Y%m%d%H%M%S')),
                            }
                            es_data_list.append(es_data)
                            if hdfs_data_list:
                                hdfs_data_list = hdfs_data_list + "\n" + json.dumps(data)
                            else:
                                hdfs_data_list = json.dumps(data)
        if len(es_data_list) > 0:
            add_doc_list(es_data_list)
            save_data_to_file(hdfs_data_list, get_file_path("sm"))
            upload_and_delete_file(get_file_path("sm"), get_upload_path("sm"))
        logger.info("save_terminal_sm_message end time = %s", timezone.now())
    except Exception as e:
        logger.error("save_terminal_sm_message error = %s", str(e))


# 非工作时间
@app.task(name='tasks.save_no_work_time_term_log')
def save_no_work_time_term_log():
    """
    保存非工作时间的终端日志信息
    :return:
    """
    try:
        logger.info("save_no_work_time_term_log start time = %s", timezone.now())
        flag, start_save_time, end_save_time = judge_work_time()
        if flag:
            start_time, end_time, indexs = get_index_by_count_type(-1, "ssa-ag-all-terminal")
            param_time = "act_time"
            index = "ssa-event-terminal-" + datetime.now().strftime("%Y-%m-%d-%H")
            sql = "select * FROM {0} where {1} > {2} and {3} < {4}".format(", ".join(indexs), param_time,
                                                                           start_save_time, param_time,
                                                                           end_save_time)
            result_list = exec_es_sql(sql)
            # 需要存入到es的数据
            es_data_list = []
            hdfs_data_list = ""
            for result in result_list:
                log_type = result['log_type']
                if log_type == 2:
                    term_ip = result['login_ip']
                else:
                    term_ip = result['term_ip']
                if term_ip:
                    data = dict()
                    data['event_id'] = str(uuid.uuid4())
                    data['event_top_type'] = "违规事件"
                    data['event_type'] = "非工作时间操作"
                    data['event_source'] = "定时任务"
                    data['event_index'] = "ssa-ag-all-terminal"
                    data['term_duty'] = result['term_duty']
                    data['remark'] = ""
                    data['organization'] = result['term_group_name']
                    data['event_level'] = 1
                    data['terminal'] = term_ip
                    data['event_time'] = result[param_time]
                    es_data = {
                        "_type": "logs",
                        "_index": index,
                        "@timestamp": datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
                        "event_id": str(uuid.uuid4()),
                        "event_top_type": "违规事件",
                        "event_type": "SM",
                        "event_source": "定时任务",
                        "event_index": "ssa-ag-all-terminal",
                        "term_duty": result['term_duty'],
                        "remark": "",
                        "organization": result['term_group_name'],
                        "event_level": 1,
                        "terminal": term_ip,
                        "event_time": result[param_time],
                    }
                    es_data_list.append(es_data)
                    if hdfs_data_list:
                        hdfs_data_list = hdfs_data_list + "\n" + json.dumps(data)
                    else:
                        hdfs_data_list = json.dumps(data)
            if len(es_data_list) > 0:
                add_doc_list(es_data_list)
                save_data_to_file(hdfs_data_list, get_file_path("no_work"))
                upload_and_delete_file(get_file_path("no_work"), get_upload_path("no_work"))
            logger.info("save_no_work_time_term_log end time = %s", timezone.now())
    except Exception as e:
        logger.error("save_no_work_time_term_log error= %s", str(e))


# 每小时执行一次生成要定时的文档
@app.task(name='tasks.ssa_make_report')
def ssa_make_report():
    """
    生成 ssa 报告
    :return:
    """
    logger.info("ssa_make_report start time = %s", timezone.now())
    time_now = timezone.localtime(timezone.now())
    version = timezone.datetime.strftime(time_now, '%Y%m%d%H%M%S')
    all_planned_tasks = models.SSAReportTemplate.objects.filter(
        schedule_type__in=[2, 3, 4, 5, 6, 7],
        next_scan_time__lte=time_now,
        # status=0,
    )
    for task in all_planned_tasks:
        # 启动报告任务 python manage.py ssa_make_report
        docx_path = os.path.join('media', 'reports', 'ssa_report_docx')
        if not os.path.exists(docx_path):
            os.makedirs(docx_path)
        pdf_path = os.path.join('media', 'reports', 'ssa_report_pdf')
        if not os.path.exists(pdf_path):
            os.makedirs(pdf_path)
        report_data = ReportData(template_id=task.id)
        data = report_data.data()
        m = MakeDocx(template_id=task.id)
        p = MakePdf(template_id=task.id)
        docx_path = os.path.join(docx_path, str(task.id) + '_' + version) + '.doc'
        pdf_path = os.path.join(pdf_path, str(task.id) + '_' + version) + '.pdf'
        try:
            m.generate_docx(path=docx_path, data=data)
            p.generate_pdf(path=pdf_path, data=data)
            for item in data:
                if 'chart_path' in item and item['chart_path']:
                    os.remove(item['chart_path'])
        except Exception as e:
            logger.error('task id = {0} run error!!'.format(task.id))
            logger.error(str(e))
            # 执行错误
            # task.status = 2
            # task.save()
            # todo 重试
        else:
            result = models.SSAReportResult()
            result.name = task.name + '_' + version
            result.template = task
            result.docx_path = docx_path
            result.docx_size = os.path.getsize(docx_path) if os.path.exists(docx_path) else 0
            result.pdf_path = pdf_path
            result.pdf_size = os.path.getsize(pdf_path) if os.path.exists(pdf_path) else 0
            result.agent = task.agent
            result.company = task.company
            result.template_type = task.template_type
            result.save()

            logger.info('task id = {0} run success!'.format(task.id))
            next_scan_time = get_next_scan_time(
                start_date=time_now,
                time_s=task.schedule_time,
                period_type=task.schedule_type,
                days=task.schedule_days,
                months=task.schedule_months
            )
            # 下次执行时间
            task.next_scan_time = next_scan_time
            task.save()
            logger.info("ssa_make_report end time = %s", timezone.now())


# 定时任务测试
@app.task(name='tasks.test')
def test():
    print("222222222222")


# 安全规则
@app.task(name='tasks.alarm_rule_task')
def alarm_rule_task():
    '''
    安全规则定时任务
    '''
    logger.info("alarm_rule_task start time = %s", timezone.now())
    try:
        day = datetime.strftime(datetime.now() - timedelta(days=1), "%Y-%m-%d")
        alarm_rule_list = AlarmRule.objects.filter(status=1, time_type=2)
        for item in alarm_rule_list:
            logging.info('执行规则{}'.format(item.rule_name))
            sql_list = item.sql
            for sql_str in sql_list.split('@'):
                sqls = sql_str.split('|')
                sql = sqls[0]
                count = 0
                if len(sqls) == 2:
                    count = int(sqls[1])
                # 防火墙规则
                if item.id in (1, 2, 3):
                    ip_sql = sql.replace('$', day.replace('-', '')).replace('all-event-*',
                                                                            'all-event-{}-*'.format(day))
                    ip_sql = ip_sql.replace(' * ',
                                            ' src_ip,count(*) count_ ') + ' and event_source = 1 group by src_ip'
                    result = exec_es_sql(sql=ip_sql)
                    ip_list = []
                    for count_ in result:
                        if count_['count_'] >= count:
                            ip_list = ['\'{}\''.format(count_['src_ip'])]
                    if ip_list:
                        sql = sql.replace('$', day.replace('-', '')).replace('all-event-*',
                                                                             'all-event-{}-*'.format(day))
                        sql = sql + ' and event_source = 1 and src_ip in ({})'.format(','.join(ip_list))
                        logging.info('执行规则sql:{}'.format(sql))
                        data_list = exec_es_sql(sql=sql)
                        add_alarm_log(alarm_rule=item, data_list=data_list)
                else:
                    sql = sql.replace('$', day.replace('-', '')).replace('all-event-*', 'all-event-{}-*'.format(day))
                    logging.info('执行规则sql:{}'.format(sql))
                    data_list = exec_es_sql(sql=sql)
                    if (count == 0) or (count > 0 and len(data_list) >= count):
                        add_alarm_log(alarm_rule=item, data_list=data_list)
    except Exception as e:
        logger.error("alarm_rule_task error= %s", str(e))


def add_alarm_log(self, alarm_rule, data_list):
    '''
    批量添加告警数据
    '''
    logs = []
    for item in data_list:
        alarm_log = AlarmLog()
        alarm_log.rule = alarm_rule
        alarm_log.group_name = alarm_rule.group.group_name
        alarm_log.rule_name = alarm_rule.rule_name
        alarm_log.src_ip = item['src_ip']
        alarm_log.src_port = item['src_port']
        alarm_log.dst_ip = item['dst_ip']
        alarm_log.dst_port = item['dst_port']
        alarm_log.tran_protocol = item['tran_protocol']
        alarm_log.app_protocol = item['app_protocol']
        alarm_log.event_host = item['event_host']
        alarm_log.event_time = datetime.now()
        alarm_log.alarm_time = datetime.now()
        alarm_log.alarm_level = alarm_rule.level
        uuids = item['uuids'] if 'uuids' in item else []
        alarm_log.old_log_list = [uuid.encode("utf-8") for uuid in uuids]
        alarm_log.event_source = item['event_source']
        logs.append(alarm_log)

        if len(logs) > 100:
            AlarmLog.objects.bulk_create(logs)
            logs = []
    if logs:
        AlarmLog.objects.bulk_create(logs)


# 添加数据到es
def add_doc_list(doc_list):
    # 数据的批量写入
    es_hosts = getattr(settings, "ELASTICSEARCH_HOSTS", ["http://127.0.0.1:9200/"])
    es = Elasticsearch(hosts=es_hosts)
    while len(doc_list) > 0:
        if len(doc_list) > 500:
            res = helpers.bulk(es, doc_list[0:500])
            del doc_list[0:500]
        else:
            res = helpers.bulk(es, doc_list)
            doc_list = []


# 保存json数据到文件中
def save_data_to_file(data_list, file_path):
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    file_name = datetime.now().strftime("%Y-%m-%d-%H")
    if data_list:
        try:
            if os.path.exists(file_path + file_name):
                file = open(file_path + file_name, 'a')
            else:
                file = open(file_path + file_name, 'wb')
            file.write(data_list)
            file.close()
        except Exception as e:
            logger.error("save_data_to_file  error = %s", timezone.now())


# 上传文件到HDFS并且删除本地文件
def upload_and_delete_file(file_path, upload_path):
    for file_name in os.listdir(file_path):
        try:
            # session = Session()
            # session.auth = HTTPBasicAuth('username', 'password')
            # client = InsecureClient(url=HDFS_HOSTS, user="hdfs", session=session)
            client = InsecureClient(url=HDFS_HOSTS, user=HDFS_USER)
            # client.delete("/data/scan/sm_word_log_message-2018-06-27-20")
            # print(client.list("/data/scan/sm/", status=False))
            path = client.upload(upload_path + file_name, file_path + file_name, cleanup=True)
            if path:
                os.remove(file_path + file_name)
        except Exception as e:
            logger.error("upload_and_delete_file  error = %s", str(e))


# 根据类型生成索引
def get_index_by_count_type(count_type, data_tag):
    try:
        es_host = SelfServiceConf.objects.get(service="es")
    except SelfServiceConf.DoesNotExist:
        raise ValueError("ES服务未配置")
    start_time = datetime.now().strftime("%Y-%m-%d") + " 00:00:00"
    end_time = time.strftime("%Y-%m-%d") + " 23:59:59"
    if count_type == -1:
        start_time = (datetime.now() - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
        end_time = (datetime.now() - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
    if count_type == 0:
        start_time = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d") + " 00:00:00"
        end_time = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d") + " 23:59:59"
    if count_type == 1:
        start_time = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d") + " 00:00:00"
        end_time = time.strftime("%Y-%m-%d") + " 23:59:59"
    indexs = ""
    if data_tag:
        indexs = generate_index(datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"),
                                datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S"), data_tag, es_host.host)
    if indexs == "":
        raise ValueError("无数据")
    return start_time, end_time, indexs


def generate_index(start_time, end_time, data_tag, es_hosts):
    """
    生成需要搜索的indexs
    """
    es = Elasticsearch(hosts=es_hosts)
    all_indexs = es.indices.get_alias("*").keys()
    indexs = []
    while True:
        index = "{}-{}".format(data_tag, start_time.strftime("%Y-%m-%d-%H"))
        if index in all_indexs:
            indexs.append(index)
        start_time = start_time + timezone.timedelta(hours=1)
        if start_time > end_time:
            break
    return indexs


def only_generate_index(start_time, end_time, data_tag):
    """
    生成需要搜索的indexs
    """
    try:
        es_host = SelfServiceConf.objects.get(service="es")
    except SelfServiceConf.DoesNotExist:
        raise ValueError("ES服务未配置")
    es = Elasticsearch(hosts=es_host.host)
    all_indexs = es.indices.get_alias("*").keys()
    indexs = []
    while True:
        index = "{}-{}".format(data_tag, start_time.strftime("%Y-%m-%d-%H"))
        if index in all_indexs:
            indexs.append(index)
        start_time = start_time + timezone.timedelta(hours=1)
        if start_time > end_time:
            break
    return indexs


# 维护终端的单位组分类表
def term_group_maintain(term_group_id, term_group_name):
    cursor = connection.cursor()
    try:
        term_group = TermGroup.objects.filter(term_group_id=term_group_id).first()
        if not term_group:
            sql_insert = "insert into soc_term_group(term_group_id,term_group_name) values(\'{0}\',\'{1}\')".format(
                term_group_id, term_group_name.encode('utf8'))
            cursor.execute(sql_insert)
    except Exception as e:
        logger.error("term_group_maintain  error = %s", str(e))
    finally:
        cursor.close()


# 判断是否在工作时间
def judge_work_time():
    """
    判断是否在工作时间
    :return:
    """
    work_time = WorkTime.objects.all().first()
    if work_time:
        if work_time.morning_start_time:
            morning_start_time = datetime.now().strftime("%Y%m%d") + work_time.morning_start_time.strftime("%H%M%S")
        else:
            morning_start_time = datetime.now().strftime("%Y%m%d") + "080000"
        if work_time.morning_end_time:
            morning_end_time = datetime.now().strftime("%Y%m%d") + work_time.morning_end_time.strftime("%H%M%S")
        else:
            morning_end_time = datetime.now().strftime("%Y%m%d") + "120000"
        if work_time.afternoon_start_time:
            afternoon_start_time = datetime.now().strftime("%Y%m%d") + work_time.afternoon_start_time.strftime("%H%M%S")
        else:
            afternoon_start_time = datetime.now().strftime("%Y%m%d") + "133000"
        if work_time.afternoon_end_time:
            afternoon_end_time = datetime.now().strftime("%Y%m%d") + work_time.afternoon_end_time.strftime("%H%M%S")
        else:
            afternoon_end_time = datetime.now().strftime("%Y%m%d") + "18:00:00"
    else:
        morning_start_time = datetime.now().strftime("%Y%m%d") + "080000"
        morning_end_time = datetime.now().strftime("%Y%m%d") + "120000"
        afternoon_start_time = datetime.now().strftime("%Y%m%d") + "133000"
        afternoon_end_time = datetime.now().strftime("%Y%m%d") + "180000"
    now_hour = int(datetime.now().strftime("%H"))
    morning_start_hour = int(morning_start_time[8:10])
    morning_end_hour = int(morning_end_time[8:10])
    afternoon_start_hour = int(afternoon_start_time[8:10])
    afternoon_end_hour = int(afternoon_end_time[8:10])
    # 零点时间
    zero_time = datetime.now().strftime("%Y%m%d") + "000000"
    mid_night_time = datetime.now().strftime("%Y%m%d") + "235959"
    if morning_start_hour < now_hour < morning_end_hour or afternoon_start_hour < now_hour < afternoon_end_hour:
        return False, "", ""
    elif now_hour <= morning_start_hour:
        return True, int(zero_time), int(morning_start_time)
    elif morning_end_hour <= now_hour <= afternoon_start_hour:
        return True, int(morning_start_time), int(afternoon_start_time)
    elif afternoon_end_hour <= now_hour:
        return True, int(afternoon_start_time), int(mid_night_time)


# 获取保存文件的路径
def get_file_path(dir_name):
    file_path = os.getcwd() + "/soc_task/file/" + dir_name + "/"
    return file_path


# 获取上传文件的路径
def get_upload_path(dir_name):
    upload_path = "/data/scan/" + dir_name + "/"
    return upload_path


def get_next_scan_time(start_date, time_s, period_type, days=1, months=None, next_scan_time=None, time_now=None):
    """
    获取下次执行的时间
    type: 1 immediately,2 runonce, 3 daily, 4 weekly, 5 monthly, 6 quarterly， 7 yearly
    """

    if time_now:
        tn = time_now
    else:
        tn = timezone.localtime(timezone.now())
    time_now = timezone.datetime(tn.year, tn.month, tn.day, tn.hour, tn.minute, tn.second)

    start_date = timezone.datetime(start_date.year, start_date.month, start_date.day)

    # 到此start_date应该为小于time_now最近的一次扫描时间, 或者是未来的开始时间
    hour, minute = time_s.hour, time_s.minute
    year = start_date.year
    month = start_date.month
    day = start_date.day
    dayth = start_date.isoweekday()  # 周日为0开始算
    start_time = timezone.datetime(year, month, day, hour, minute)

    if period_type == 1:
        # 立刻执行
        return time_now
    elif period_type == 2:
        if start_time < time_now:
            year = start_date.year + 99
            return timezone.datetime(year, month, day, hour, minute)
        return start_time
    else:
        if next_scan_time:
            next_scan_time = timezone.localtime(next_scan_time)
            next_scan_time = timezone.datetime(next_scan_time.year, next_scan_time.month, next_scan_time.day,
                                               next_scan_time.hour, next_scan_time.minute)
            if next_scan_time >= time_now:
                # 还没到下次扫描时间
                return next_scan_time

            # 从上一次的扫描时间开始算下一次的扫描时间
            # next_scan_time < time_now
            start_time = next_scan_time
            year = start_time.year
            month = start_time.month
            day = start_time.day
            hour = start_time.hour
            minute = start_time.minute
            dayth = start_time.isoweekday()
        if period_type == 3:
            # 每[days]天
            while start_time <= time_now:
                start_time = start_time + timezone.timedelta(days=days)
            return start_time
        else:
            if start_time < time_now:
                start_time = time_now
                year = start_time.year
                month = start_time.month
                day = start_time.day
                dayth = start_time.isoweekday()

            if period_type == 4:
                # 每周
                if next_scan_time:
                    if dayth >= days:
                        delta = 7 - (dayth - days)
                    else:
                        delta = days - dayth
                else:
                    if dayth >= days:
                        delta = 7 - (dayth - days)
                    else:
                        delta = days - dayth
                return timezone.datetime(year, month, day, hour, minute) + timezone.timedelta(days=delta)
            elif period_type == 5:
                # 每月执行
                if next_scan_time:
                    if day >= days:
                        day = days
                        month += 1
                        if month == 13:
                            month = 1
                            year += 1
                    else:
                        day = days
                else:
                    if day >= days:
                        day = days
                        month += 1
                        if month == 13:
                            month = 1
                            year += 1
                    else:
                        day = days
                return timezone.datetime(year, month, day, hour, minute)

            # 按季度
            elif period_type == 6:
                # 第一月 则 + 0 第二月 + 1
                year = time_now.year
                # 取一下季度
                month = time_now.month + (3 - time_now.month % 3)
                # 判断是否超过当前季度， 为超过则当前季度还能执行一次
                if time_now.month + months < month:
                    month = time_now.month + months
                else:
                    if month > 12:
                        month = 1
                        year += 1
                    # 加上 第X月 第一月 则 + 0 第二月 + 1
                    month += months
                return timezone.datetime(year, month, day, hour, minute)

            # 按年度
            elif period_type == 7:
                # 第一月 则 + 0 第二月 + 1
                # months -= 1
                year = time_now.year + 1
                month = months
                day = day
                return timezone.datetime(year, month, day, hour, minute)


app.conf.beat_schedule = {
    # 'schedule': crontab(minute=0, hour=1),

    # 资产库维护
    'add_statistics_asset_task': {
        'task': 'tasks.statistics_asset_task',
        'schedule': crontab(minute=0, hour=1),
        'args': ()
    },
    # SM扫描
    'add_save_terminal_sm_message': {
        'task': 'tasks.save_terminal_sm_message',
        'schedule': crontab(minute='*/60'),
        'args': ()
    },
    # 非工作时间操作
    'add_save_no_work_time_term_log': {
        'task': 'tasks.save_no_work_time_term_log',
        'schedule': crontab(minute='*/60'),
        'args': ()
    },
    # 生成报表
    'add_ssa_make_report': {
        'task': 'tasks.ssa_make_report',
        'schedule': crontab(minute='*/30'),
        'args': ()
    },
    # 安全规则
    'add_alarm_rule_task': {
        'task': 'tasks.alarm_rule_task',
        'schedule': crontab(minute=0, hour=1),
        'args': ()
    },

}

app.conf.timezone = 'Asia/Shanghai'
