# coding=utf-8
from __future__ import unicode_literals
import os
import json
import subprocess
import hashlib
from django.conf import settings
from django.core.cache import cache
from django.core.management import call_command
from django.utils import timezone
from soc.models import SocLog
from soc_system.models import Node, SystemUpgradeTask
from celery.task import task
from tools.sys_check import SysCheck
from utils.api import NodeApi
from utils.media_handler import FILE_UPLOAD_LOCATION
from soc_system.tools.upgrade import GPG
from soc_system.system_common import Component
import logging
import tarfile
from soc_knowledge.models import VulStore, VulStoreVersion

logger = logging.getLogger('soc_system')

TEMP_DIR = '/tmp/upgrade_temp'
SYSTEM_PATH = '/usr/local/qs-project'


@task()
def run_check(agent_id, user_id):
    s = SysCheck(agent_id=agent_id, user_id=user_id)
    s.v_all()


def run_cmd(cmd, path=TEMP_DIR):
    if not os.path.exists(path):
        os.mkdir(path)
    cmd = "cd {}; {}".format(path, cmd)
    logger.debug(cmd)
    s = subprocess.Popen(cmd, shell=True, executable='/bin/bash', stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    output, error = s.communicate()
    logger.error("run cmd returncode: {}, output: {}, error: {}".format(s.returncode, output, error))
    return s.returncode, output, error


def update_db(data):
    target_task = SystemUpgradeTask.objects.filter(id=data['task_id']).first()
    if target_task:
        target_task.status = data["status"]
        target_task.percent = data["progress"]
        target_task.save()
        Component(target_task.agent, target_task.u_type).update_by_task(data['task_id'])


def send_status(src, task_id, msg='', status=1, init=False, f_type=None, center_level=0):
    data = {"msg": msg, "task_id": task_id, 'src': src, 'status': status}

    cached_key = 'system:node_upgrade:task_{}'.format(task_id)
    # if status is None:
    #     data['status'] = 1
    # else:
    #     data['status'] = status

    self = Node.objects.get(role='self')
    if init and src == self.uuid:
        all_step = 7 + center_level
        if f_type == 'system':
            # 系统更新
            all_step += 5
        else:
            # 功能组件更新
            all_step += 2

        data['all_step'] = all_step
        data['now_step'] = 0
        cache.delete(cached_key)
        cache.set(cached_key, data)
    else:
        if data['status'] == 0:
            data['status'] = 1

    cache_data = cache.get(cached_key, {})
    cache_data.update(data)

    cache_data['now_step'] = cache_data.get('now_step', 0) + 1
    progress = round(cache_data.get('now_step') / float(cache_data.get('all_step')), 2) * 100
    cache_data['progress'] = int(progress)
    if src == self.uuid:
        cache.set(cached_key, cache_data)
        # 更新数据库
        update_db(cache_data)
    else:
        parent = Node.objects.get(role='parent')
        if parent.api_url:
            url = parent.api_url
        else:
            url = "http://{}".format(parent.ip)
        api = NodeApi(base_url=url, secret_id=parent.secret_id, secret_key=parent.secret_key)
        api.request('/api/system/upgrade/progress', params=data)
    logger.error(json.dumps(cache_data, encoding="UTF-8", ensure_ascii=False))


def get_real_path(file_name):

    dest = '/'.join([file_name[0], file_name[1], file_name])
    return os.path.join(FILE_UPLOAD_LOCATION, dest)


def upgrade_system(src, task_id, bin_file):
    """升级自身系统"""
    bin_file = get_real_path(bin_file)
    logger.error("start upgrade_system binfile: {}".format(bin_file))
    bin_file_name = bin_file.split('/')[-1]
    g = GPG()
    try:
        g.decrypt(bin_file, os.path.join(TEMP_DIR, bin_file_name))
    except Exception as e:
        # send_status(src, task_id, msg=e.message, status=3)
        logger.error("errot upgrade_system binfile: {}, error: {}".format(bin_file, e))
        # return False

    send_status(src, task_id, msg='解开压缩包')

    result = run_cmd('tar zxvf {}'.format(bin_file_name))
    if not result[0] == 0:
        send_status(src, task_id, msg='解开压缩包失败', status=3)
        return False
    # run_cmd('rm {}'.format(bin_file_name))
    send_status(src, task_id, msg='配置项目')
    run_cmd('cp {}/soc/soc/local_settings.py ./soc/soc/local_settings.py'.format(SYSTEM_PATH))
    send_status(src, task_id, msg='备份代码')
    run_cmd('mv {}/soc /tmp/soc_backup`date "+%Y%m%d%H%M%S"`'.format(SYSTEM_PATH))
    send_status(src, task_id, msg='替换代码')
    result = run_cmd('mv soc {}'.format(SYSTEM_PATH))
    if not result[0] == 0:
        send_status(src, task_id, msg='替换代码失败', status=3)
        return

    send_status(src, task_id, msg='重新启动')
    run_cmd('supervisorctl restart soc')
    send_status(src, task_id, status=2, msg='更新成功')


def upgrade_child(child_center, bin_file, targets, src, task_id, f_type):

    """升级下级"""
    bin_file = get_real_path(bin_file)
    for target in targets:
        if not target.get("id"):
            target['id'] = target.get("device_id")
    logger.error("start upgrade_child, child_center: {}".format(child_center.name))
    data = {
        "src": src,
        "type": f_type,
        "targets": targets,
        "task_id": task_id,
    }

    if child_center.api_url:
        url = child_center.api_url
    else:
        url = "http://{}".format(child_center.ip)
    api = NodeApi(base_url=url, secret_id=child_center.secret_id, secret_key=child_center.secret_key)
    files = {'upgrade_file': open(bin_file, 'rb')}
    send_status(src, task_id, msg='向下发送更新包')
    logger.error("start upgrade_child, child_center: {} 向下发送更新包".format(child_center.name))
    req = api.request('/api/system/upgrade/file/upload', files=files, headers={})
    # os.remove(bin_file)
    if req.get("status") != 200:
        error = json.dumps(req, encoding="UTF-8", ensure_ascii=False)
        send_status(src, task_id, status=3, msg='向下发送更新包失败')
        logger.error("start upgrade_child, child_center: {} 向下发送更新包失败, errors: {}".format(child_center.name, error))
        return False
    send_status(src, task_id, msg='向下发送更新指令')
    logger.error("start upgrade_child, child_center: {} 向下发送更新指令".format(child_center.name))

    logger.debug(req)
    data['file_id'] = req['data']['file_id']
    data['u_type'] = req['data']['u_type']
    req = api.request('/api/system/upgrade', params=data)
    if req.get("status") != 200:
        error = json.dumps(req, encoding="UTF-8", ensure_ascii=False)
        params = json.dumps(data, encoding="UTF-8", ensure_ascii=False)
        send_status(src, task_id, status=3, msg='向下发送更新指令失败')
        logger.error(
            "start upgrade_child, child_center: {} 向下发送更新指令失败, 参数: {} error: {}".format(child_center.name, params, error))


def upgrade_components(src, task_id, bin_file, type, device_id, version=""):
    """升级功能组件"""
    bin_file = get_real_path(bin_file)
    logger.error("start upgrade_components, device_id: {}".format(device_id))

    g = GPG()
    decrypt_file = bin_file + '.decrypt'
    try:
        g.decrypt(bin_file, decrypt_file)
    except Exception:
        pass
        # send_status(src, task_id, msg=e.message, status=3)
        # return False


def update_event(src, task_id, bin_file):
    """ 更新数据包
    tar包内数据json文件格式：
        {
        "publish_date": "2018-03-01",
        "type": "VUL",
        "data": [
            {"vul_id": "CVE-123", ....}, // vul_store数据
            ...
        ]
        }
    """
    bin_file = get_real_path(bin_file)
    logger.info("start update event binfile: {}".format(bin_file))
    bin_file_name = bin_file.split('/')[-1]
    tmp_file_name = os.path.join('/tmp', bin_file_name + 'tar.gz')
    g = GPG()
    try:
        g.decrypt(bin_file, tmp_file_name)
    except Exception as e:
        send_status(src, task_id, msg=e.message, status=3)
        logger.error("errot update event binfile: {}, error: {}".format(bin_file, e))
        return False
    send_status(src, task_id, msg='更新数据')
    t = tarfile.open(tmp_file_name, 'r:gz')
    json_name = ''
    for i in t:
        if 'json' in i.name:
            json_name = i.name
            break
    json_data = json.loads(t.extractfile(json_name).read())
    data_type = json_data.get('type')
    if data_type != 'VUL':
        return
    data = json_data.get('data')
    for d in data:
        if d['vul_id']:
            try:
                VulStore.objects.update_or_create(vul_id=d['vul_id'], defaults=d)
            except Exception as e:
                logger.error("errot update_or_create_vul:{}, error: {}".format(d['vul_id'], e))
    vul_version = VulStoreVersion.objects.first()
    last_version = vul_version.version
    current_date = json_data.get('publish_date')
    version = 'v%s.%s.%s' % tuple(current_date.split('-'))
    vul_version.last_version = last_version
    vul_version.version = version
    vul_version.current_date = current_date
    vul_version.save()
    send_status(src, task_id, status=2, msg='更新成功')


def upgrade_targets(agent_now, upgrade_detail):
    """
    升级
    :param agent_now:
    :param upgrade_detail:
    :return:
    """
    bin_file = upgrade_detail.get('file_name')
    f_type = upgrade_detail.get('u_type')
    version = upgrade_detail.get('file_version')
    targets = upgrade_detail.get('targets')
    src = Node.objects.get(role='self', agent=agent_now).uuid

    for target in targets:
        task_id = target.get('task_id')  # 任务 ID
        sub_id = target.get('parent_id')  # 跨级子中心对应的上级中心 ID
        uuid = target.get('uuid')  # nids所属中心的uuid
        device_id = target.get('device_id')  # nids 是 nids_host的 ID

        if Node.objects.filter(uuid=uuid, role='self', agent=agent_now).exists():
            # 本中心更新
            target_center = 'self'
            center_level = 0
        else:
            try:
                # 下级中心更新
                target_center = Node.objects.get(uuid=uuid, agent=agent_now)
                center_level = 1
            except Node.DoesNotExist:
                # 下下级中心更新
                target_center = Node.objects.get(id=sub_id, agent=agent_now)
                center_level = 2
        send_status(src, task_id, init=True, status=0, f_type=f_type, center_level=center_level)
        if target_center == 'self':
            # 初始化状态

            # 更新本中心系统
            if f_type == 'center':
                upgrade_system(bin_file=bin_file, src=src, task_id=task_id)
            elif f_type == 'vul':
                update_event(bin_file=bin_file, src=src, task_id=task_id)
            else:
                # 更新本中心功能组件
                upgrade_components(src=src, task_id=task_id, bin_file=bin_file,
                                   type=f_type, device_id=device_id, version=version)

        else:
            # 更新下级中心
            upgrade_child(child_center=target_center, bin_file=bin_file, targets=targets,
                          src=src, task_id=task_id, f_type=f_type)


@task()
def backup_data(agent_id):
    """
    备份数据
    :param agent_id:
    :return:
    """

    cached_key = "system:backup_db:agent_{0}".format(agent_id)
    data = {"status": 0, "name": "backup-db", "percent": 0, "backup_time": "", "download_url": ""}
    cache.set(cached_key, data)

    name_uuid = "backup_db_{0}".format(agent_id)
    name_uuid = hashlib.md5(name_uuid).hexdigest()
    file_name = 'backup_db_' + name_uuid + ".txt"

    file_path = '/'.join(["download", name_uuid[0], name_uuid[1]])
    save_file_folder = os.path.join(settings.MEDIA_ROOT, file_path)
    if not os.path.exists(save_file_folder):
        os.makedirs(save_file_folder)
    absolute_path = os.path.join(save_file_folder, file_name)

    data["percent"] = 30
    cache.set(cached_key, data)
    all_logs = SocLog.objects.filter(agent_id=agent_id)
    with open(absolute_path, 'w') as output:
        for log in all_logs:
            data = ";".join([
                log.user.username,
                timezone.localtime(log.create_time).strftime("%Y-%m-%d %H:%M:%S"),
                log.ip,
                log.info,
                str(log.login_status or ''),
            ])
            output.write(data + "\n")

    data = {
        "status": 1,
        "percent": 100,
        "name": "backup-db",
        "backup_time": timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
        "download_url": '/media/' + file_path + '/' + file_name
    }
    cache.set(cached_key, data)

if __name__ == '__main__':
    run_cmd('ls /')
