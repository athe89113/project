# coding=utf-8
import logging
from django.core.management.base import BaseCommand
from django.core.cache import cache
from django.utils import timezone
from soc_system import models
from soc_system import system_common
from utils.api import NodeApi
from utils import version
from common import send_msg
logger = logging.getLogger('soc_system')
console = logging.getLogger('console')
HEARTBEAT_TIMEOUT = 10


class Command(BaseCommand):

    def handle(self, *args, **options):
        """
        心跳检查, 获取子节点的级联关系
        :param args:
        :param options:
        :return:
        """
        # 更新本级中心版本
        models.Node.objects.filter(role='self').update(version=version.get_version())
        # 获取本中心的组件
        self_nodes = models.Node.objects.filter(role='self')
        for self_node in self_nodes:
            console.info('self_node: {}'.format(self_node.uuid))
            comps = system_common.Component(self_node.agent).fetch_all()
            for comp in comps:
                key = system_common.node_components_cache_key.format(
                    **{"agent_id": self_node.agent.id, "node_uuid": self_node.uuid, "component_name": comp}
                )
                cache.set(key, comps[comp], 24 * 60 * 60)

        # 活跃状态的中心每1小时发一次心跳，断线状态的中心心跳发送时间会越来越长
        time_now = timezone.now()
        # 不检查上级中心状态
        active_child_nodes = models.Node.objects.filter(next_check__lte=time_now, status=1).exclude(role__in=['self', 'parent'])
        for node in active_child_nodes:
            console.info("node: {}".format(node.uuid))
            good = self.send_heartbeat(node)

            if good:
                console.info('  => heartbeat good')
                # 获取下级中心的级联关系
                if node.role == 'child' and node.type == 'sub_center':
                    console.info("  => topo")
                    topo = self.fetch_node_topo(node)
                    # 缓存1天
                    cache.set(system_common.node_child_topo_cache_key.format(
                        **{"agent_id": node.agent.id, "node_uuid": node.uuid}
                    ), topo, 24*60*60)

                    # 获取中心的下级中心的组件 python manage.py check_node_heartbeat
                    children_components = self.fetch_node_children_compoments(node)
                    console.info("  => children components")
                    for child in children_components:
                        console.info("    - {}".format(child))
                        for cc in children_components[child]:
                            cache.set(system_common.node_components_cache_key.format(
                                **{"agent_id": node.agent.id, "node_uuid": node.uuid, "component_name": cc}
                            ), children_components[child][cc], 24 * 60 * 60)

                # 获取中心的拓扑
                components = self.fetch_node_compoments(node)
                console.info("  => components")
                for com in components:
                    cache.set(system_common.node_components_cache_key.format(
                        **{"agent_id": node.agent.id, "node_uuid": node.uuid, "component_name": com}
                    ), components[com], 24 * 60 * 60)
            else:
                console.info('  => heartbeat bad')

        # 检查上级中心状态
        parent_nodes = models.Node.objects.filter(role='parent')
        for parent in parent_nodes:
            console.info('  => parent heart {}'.format(parent.uuid))
            result = self.check_parent_heartbeat(parent)
            if result.get("status", 0) == 1:
                console.info(" => parent heart good")
                parent.status = 1
                parent.type = result.get('type')
                parent.name = result.get('name')
                parent.version = result.get("version")
                parent.last_heartbeat = timezone.now()
            else:
                logger.error(result)
                parent.status = 2
            parent.save()
            self.update_next_check_time(parent)

    def check_parent_heartbeat(self, node):
        """
        查看上级中心的状态，以及角色变化
        :param node:
        :return:
        """
        self_node = models.Node.objects.filter(agent=node.agent, role='self').first()
        if not self_node:
            return False
        # 使用本中心的 key 作为认证
        node_api = NodeApi(
            base_url='http://' + node.ip, auth_key=self_node.auth_key)
        data, msg = node_api.get_parent_status()
        return data

    def get_node_api(self, node):
        """
        api
        :param node:
        :return:
        """
        api = NodeApi(
            base_url='http://' + node.ip, secret_id=node.secret_id, secret_key=node.secret_key)
        return api

    def fetch_node_topo(self, node):
        """
        获取中心 topo
        :param node:
        :return:
        """
        node_api = NodeApi(
            base_url='http://' + node.ip, secret_id=node.secret_id, secret_key=node.secret_key)
        topo = node_api.get_topo()
        if topo.get('role') == 'parent':
            topo = topo.get("children")
            if len(topo) == 1:
                topo = topo[0].get("children", [])
            else:
                topo = []
        elif topo.get('role') == 'self':
            topo = topo.get("children", [])
        else:
            topo = []
        return topo

    def fetch_node_compoments(self, node):
        """
        获取中心的组件
        :param node:
        :return:
        """
        components = self.get_node_api(node).get_components()
        return components

    def fetch_node_children_compoments(self, node):
        """
        获取中心的组件
        :param node:
        :return:
        """
        components = self.get_node_api(node).get_children_components()
        return components

    def send_heartbeat(self, node):
        """
        心跳检测
        :param node: obj
        :return:
        """
        if not node.auth_key:
            # 没有配置级联秘钥
            node.status = 2
            node.save()
            self.update_next_check_time(node)
            self.send_node_alert(node, "级联秘钥错误")
            return False
        if not node.secret_key or not node.secret_id:
            # fetch secret_key and secret_id
            node_api = NodeApi(base_url='http://' + node.ip, auth_key=node.auth_key)
            result = node_api.fetch_auth(self_node_info=node.get_dict())
            if result["status"] == 200:
                node.secret_id = result["data"]["secret_id"]
                node.secret_key = result["data"]["secret_key"]
                node.save()
            else:
                # 级联秘钥获取 token 错误
                node.status = 2
                node.save()
                self.update_next_check_time(node)
                self.send_node_alert(node, "级联秘钥错误")
                return False
        # check status
        node_api = NodeApi(
            base_url='http://' + node.ip, secret_id=node.secret_id, secret_key=node.secret_key)
        data, msg = node_api.get_detailed_status()
        if not data:
            node.status = 2
            node.save()
            self.send_node_alert(node, msg[1])
            return False
        # 更新状态和信息
        node.status = 1
        node.last_heartbeat = timezone.now()
        node.type = data['type']
        node.save()

        self.update_next_check_time(node)

        return True

    def update_next_check_time(self, node):
        """
        更新下次检测时间
        :param node:
        :return:
        """
        if node.status == 1:
            total_seconds = 1 * 60 * 60
        elif node.status == 2:
            total_seconds = (node.next_check - node.last_heartbeat).total_seconds()
            if total_seconds <= 0:
                total_seconds = 60
            else:
                total_seconds *= 1.5
        else:
            total_seconds = 5 * 60
        node.next_check = node.last_heartbeat + timezone.timedelta(seconds=total_seconds)
        node.save()
        return

    def send_node_alert(self, node, msg=''):
        """
        发送节点错误信息
        :param node:
        :param msg:
        :return:
        """
        logger.error("{} {}".format(node.id, msg))
        self_node = models.Node.objects.filter(agent=node.agent, role='self').first()
        if not self_node or not self_node.notify_when_lose_children:
            # "当下级失联时告警"设置为否时不告警
            return

        title = "中心链接错误"
        node_type = '分中心' if node.type == 'sub_center' else '子中心'
        body = msg if msg else "下级{node_type}-{node_name}({node_ip})无法连接，数据和配置将无法同步，请及时处理".format(**{
            "node_type": node_type,
            "node_name": node.name,
            "node_ip": node.ip
        })
        userinfos = node.agent.userinfo_set.filter(is_admin=1)
        user_emails = [ui.user.email for ui in userinfos]
        for email in user_emails:
            send_msg(msg_type=4, to=email, content=body, title=title, agent=node.agent)
