# coding=utf-8
from __future__ import unicode_literals
from django.core.cache import cache
from utils.api import NodeApi
from utils.version import get_version
from soc_system import models

node_components_cache_key = "system:node_components:node_{node_uuid}:{component_name}"
node_child_topo_cache_key = "system:node_child_topo:node_{node_uuid}"


def get_node_status(node):
    """
    获取中心状态
    :param node: node_obj
    :return:
    """
    if not node.secret_id or not node.secret_key:
        return 0, '中心配置错误'
    node_api = NodeApi(
        base_url='http://' + node.ip, secret_id=node.secret_id, secret_key=node.secret_key)
    status, msg = node_api.get_status()
    return status, msg


def get_node_detailed_status(node):
    """
    获取中心状态
    :param node: node_obj
    :return:
    """
    if not node.secret_id or not node.secret_key:
        return {}, (500, '中心配置错误')
    node_api = NodeApi(
        base_url='http://' + node.ip, secret_id=node.secret_id, secret_key=node.secret_key)
    data, msg = node_api.get_detailed_status()
    return data, msg


def get_single_node_status(file_version, self_version):
    """
    检查单个中心可否升级状态
    :param file_version: 文件版本
    :param self_version: 本级版本
    :return:
    """
    if file_version > self_version:
        self_status = 1
    elif file_version == self_version:
        self_status = 2
    else:
        # file_version < self_version
        self_status = 0
    return self_status


def judge_status(self_node, file_info, parent_node=None, child_node=None):
    """
    判断状态, 假定 parent_version >= self_version >= child_version

    :param self_node: 包含 version 的字典
    :param file_info: 包含 version，u_type 的字典和 u_type
    :param parent_node: 包含 version 的字典
    :param child_node: 包含 version 的字典
    :return:

        0: 不可升级
        1: 可升级
        2: 已升级到相应版本
        3: 上级未升级
    """
    parent_status, self_status, child_status = (0, 0, 0)
    if file_info['u_type'] == 'center':
        # 可比较版本
        self_version = get_version(self_node["version"], 'int')
        file_version = get_version(file_info["version"], 'int')

        # 不可升级：1. 文件版本小 2.上级限制
        # 上级
        if parent_node:
            parent_version = get_version(parent_node["version"], 'int')
            if file_version > parent_version:
                # 上级未升级
                parent_status = 3
                self_status = 0
            elif file_version == parent_version:
                # 本级正常检查
                parent_status = 2
                self_status = get_single_node_status(file_version, self_version)
            else:
                # file_version < parent_version:
                parent_status = 0
                self_status = get_single_node_status(file_version, self_version)
        else:
            self_status = get_single_node_status(file_version, self_version)

        # 有下级，下级根据本级的升级状态确定即可
        if child_node:
            child_version = get_version(child_node["version"], 'int')
            if self_status in [2]:
                child_status = get_single_node_status(file_version, child_version)
            else:
                child_status = 0
    elif file_info['u_type'] == 'vul':
        # 漏洞库暂不需要限制版本
        return (1, 1, 1)
    return parent_status, self_status, child_status


def get_cached_components(node_uuid, name, upgrade_version=None):
    """

    :param node_uuid:
    :param name: u_type
    :param upgrade_version: v2.23.1
    :return:
    """
    cached_key = node_components_cache_key.format(**{"node_uuid": node_uuid, "component_name": name})
    components = cache.get(cached_key, [])
    for comp in components:
        if upgrade_version:
            # 检查版本
            file_version = get_version(upgrade_version, 'int')
            self_version = get_version(comp['version'], 'int')
            status = get_single_node_status(file_version, self_version)
        else:
            status = 0
        comp.update({"is_self": 0, 'u_type': name, "status": status, "uuid": node_uuid})

    return components


def get_node_detail(agent_now, file_info):
    """
    获取代理商下中心升级信息
    :param agent_now:
    :param file_info:
    :return:
    """
    u_type = file_info.get('u_type')
    file_version = file_info['version']

    # 判断中心升级的状态，非系统升级中心一律不可升级

    self_node = models.Node.objects.filter(agent=agent_now, role='self').first()
    if not self_node:
        return {}
    self_node_dict = self_node.get_dict()
    self_node_dict.update({"is_self": 1, "u_type": "center", "status": 1})

    # 上级中心
    parent = models.Node.objects.filter(agent=agent_now, role='parent').first()
    parent_dict = parent.get_dict() if parent else {}
    parent_dict.update({"is_self": 0, "u_type": "center", "status": 1})

    # 直属下级中心
    children = models.Node.objects.filter(agent=agent_now, role='child')
    children_list = []
    for child in children:
        # 自己节点信息
        child_dict = child.get_dict()
        child_dict.update({"is_self": 0, "u_type": "center"})
        if child.type == 'sub_center':
            # 获取缓存中的子中心的几点
            cached_key = node_child_topo_cache_key.format(**{"agent_id": child.agent.id, "node_uuid": child.uuid})
            csc = cache.get(cached_key, [])
            for one_csc in csc:
                one_csc.update({"is_self": 0, "u_type": "center", "status": 1})
            child_dict.update({"children": csc})
        children_list.append(child_dict)

    # 组件
    self_components = get_cached_components(node_uuid=self_node_dict['uuid'], name=u_type, upgrade_version=file_version)

    if self_node.type == "center":
        # 总中心
        for child in children_list:
            _, self_status, child_status = judge_status(self_node_dict, file_info, child_node=child)
            child_components = get_cached_components(node_uuid=child['uuid'], name=u_type, upgrade_version=file_version)
            child.update({"status": child_status, 'children': child_components})

            for child_child in child.get("children"):
                child_child_components = get_cached_components(node_uuid=child_child['uuid'], name=u_type, upgrade_version=file_version)
                child_child.update({"status": child_status, 'children': child_child_components})
        else:
            _, self_status, _ = judge_status(self_node_dict, file_info)
        self_node_dict.update({"status": self_status, "children": children_list+self_components})
        tree = self_node_dict

    elif self_node.type == "sub_center":

        if parent:
            for child in children_list:
                parent_status, self_status, child_status = judge_status(self_node_dict, file_info,
                                                                        parent_node=parent_dict, child_node=child)
                child_components = get_cached_components(node_uuid=child['uuid'], name=u_type, upgrade_version=file_version)
                child.update({"status": child_status, "children": child_components})
            else:
                parent_status, self_status, _ = judge_status(self_node_dict, file_info, parent_node=parent_dict)

            parent_dict.update({"status": parent_status})

            self_node_dict.update({"status": self_status, "children": children_list + self_components})
            parent_dict.update({"children": [self_node_dict]})
            tree = parent_dict

        else:
            for child in children_list:
                _, self_status, child_status = judge_status(self_node_dict, file_info, child_node=child)
                child_components = get_cached_components(node_uuid=child['uuid'], name=u_type, upgrade_version=file_version)
                child.update({"status": child_status, "children": child_components})
            else:
                _, self_status, _ = judge_status(self_node_dict, file_info)

            self_node_dict.update({"status": self_status, "children": children_list + self_components})

            tree = self_node_dict
    else:
        # 子中心
        if parent:
            parent_status, self_status, _ = judge_status(self_node_dict, file_info, parent_node=parent_dict)
            parent_dict.update({"status": parent_status})
            self_node_dict.update({"status": self_status, "children": self_components})
            parent_dict.update({"children": [self_node_dict]})
            tree = parent_dict
        else:
            _, self_status, _ = judge_status(self_node_dict, file_info)
            self_node_dict.update({"status": self_status, 'children': self_components})
            tree = self_node_dict

    return tree


class Component(object):
    """
    代理商组件

    name 可选字段

        - center:     中心服务器
        - monitor:    监控服务器
        - scan:       漏扫服务器
        - defense:    高防服务器
        - cloud_defense: 云防服务器
        - hids:       终端安全服务器
        - nids:       网络安全服务器

    组件列表缓存格式

    """

    # todo 支持获取所有其他的组件，当前只有 nids    -- added @ 2017-08-21
    supported_components = ['nids']

    def __init__(self, agent, name=''):
        self.agent = agent
        self.name = name
        self.task = None

    def fetch_all(self):
        """
        获取所以组件，返回字典
        :return:
        """
        data = dict()
        for key in self.supported_components:
            data[key] = self.fetch_by_name(key)
        return data

    def fetch_by_name(self, name):
        """
        返回列表
        :param name:
        :return:
        """
        self.name = name
        func = getattr(self, '_fetch_' + name, None)

        return func() if func else []

    def _fetch_center(self):
        return []

    def update_by_task(self, task_id):
        """
        更新升级后的状态
        :param task_id:
        :return:
        """
        task = models.SystemUpgradeTask.objects.filter(id=task_id).first()
        if not task or task.status != 1:
            return
        self.task = task
        func = getattr(self, '_update_' + task.u_type, None)
        return func() if func else []

    def _update_center(self):
        """
        更新中心版本
        :return:
        """
        node = models.Node.objects.filter(uuid=self.task.target_uuid, agent=self.agent).first()
        if node.role == 'self':
            node.version = get_version()
            node.save()

    def _update_nids(self):
        """
        更新nids版本
        :return:
        """
        node = models.Node.objects.filter(uuid=self.task.target_uuid, agent=self.agent).first()
        if node.role == 'self':
            nids_models.NidsHost.objects.filter(id=self.task.target_id).update(version=self.task.file_version)


def get_child_components(agent):
    """
    当本机中心为`分中心`时，可从从缓存中获取下级子中心的组件列表，缓存由 crontab 更新

    :param agent:
    :return: {"child_uuid": { different components list} }
    """

    self_node = models.Node.objects.filter(agent=agent, role='self').first()
    data = dict()
    if self_node and self_node.type in ['sub_center']:
        # 分中心获取子中心的组件列表
        all_children = models.Node.objects.filter(agent=agent, role='child')
        for child in all_children:
            components = dict()
            for key in Component.supported_components:
                cache_key = node_components_cache_key.format(**{
                    "agent_id": agent.id,
                    "node_uuid": child.uuid,
                    "component_name": key
                })
                components[key] = cache.get(cache_key, [])
            data[child.uuid] = components

    return data


def get_children_with_components(agent, component_name):
    """
    获取带有组件的下级中心
    :param agent:
    :param component_name:
    :return:
    """
    data = {
        "has_child": 0,
        "children": []
    }
    if component_name not in Component.supported_components:
        return data
    self_node = models.Node.objects.filter(agent=agent, role='self').first()
    if self_node:
        all_children = models.Node.objects.filter(agent=agent, role='child')
        children = []
        for child in all_children:
            cache_key = node_components_cache_key.format(**{
                "agent_id": agent.id,
                "node_uuid": child.uuid,
                "component_name": component_name
            })
            components = cache.get(cache_key, [])
            if components:
                children.append({
                    "id": child.uuid,
                    "name": child.get_dict()['name']
                })
        if children:
            data["has_child"] = 1
            data['children'] = [{"id": self_node.uuid, "name": self_node.get_dict()["name"]}] + children

    return data
