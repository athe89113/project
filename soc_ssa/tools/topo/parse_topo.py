#coding=utf-8
import json
from collections import defaultdict

def tree():
    return defaultdict(tree)

class HTToPoParse(object):
    """
    解析ht.js 拓扑
    """
    def __init__(self, json_data, max_level=100):
        self.json_data = json_data
        print(json_data.keys())
        self.node_tree = tree()
        self.generate_tree()
        self.max_level = max_level
        self.level = 0

    def generate_tree(self):
        """
        生成树
        """
        nodes = self.json_data['d']
        node_tree = self.node_tree
        for node in nodes:
            node_type = node['c']
            if node_type == "ht.Edge":
                source = int(node['p']['source']['__i'])
                target = int(node['p']['target']['__i'])
                node_tree[source]['children'] = target
                node_tree[target]['parent'] = source
            else:
                config = node['a']['config']
                if config.get('options'):
                    config.update(config['options'])
                    del config['options']

                node_id = int(node['i'])
                node_tree[node_id]['name'] = node['p']['name']
                node_tree[node_id]['config'] = config
                node_tree[node_id]['id'] = node_id

        self.node_tree = json.loads(json.dumps(node_tree))

    def nodes(self, parent_id=0):
        """
        获取节点
        """
        self.level += 1
        if self.level > self.max_level:
            return 
        node_tree = self.node_tree
        _nodes = filter(lambda x: x.get("parent", 0) ==
                        parent_id, node_tree.values())
        for _node in _nodes:
            _node_id = _node['id']
            self_node = node_tree[str(_node_id)]
            self_node['parent_id'] = parent_id
            if parent_id != 0:
                parent = node_tree[str(parent_id)]
                # 数据拆分节点
                split_data_tag = parent['config'].get('config', {}).get("split_data_tag")
                # 数据拆分子节点
                if not split_data_tag:
                    split_data_tag =  parent['config'].get("split_data_tag")
                # 后续节点增加tag 标识
                if split_data_tag:
                    self_node['config']['split_data_tag'] = split_data_tag
            yield self_node
            c_nodes = filter(lambda x: x.get("parent", 0) == _node_id, node_tree.values())
            if c_nodes:
                for n in self.nodes(_node_id):
                    # 处理多分支
                    if len(c_nodes) > 1:
                        # n['config']['split_data_tag'] = n['id']
                        n['config']['is_first'] = True
                    yield n

if __name__ == "__main__":
    f = open("test_topo2.json", 'rb')
    topo = json.load(f)
    topo = json.loads(topo)
    # print(json.loads(topo))
    f.close()
    ht = HTToPoParse(topo, max_level=30)
    for p, n in ht.nodes():
        print(p, n)
