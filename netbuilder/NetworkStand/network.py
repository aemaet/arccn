import networkx as nx
from nodes import Host, Switch
from ovsswitch import OVSSwitch
from link import Link

# TODO:
# 1. Link object should contain pair of node/port data with no direction.


class Network(object):
    def __init__(self,meta=""):
        self.topology = nx.MultiGraph()
        # map switch_ID on network_ID
        self.ID_map = {}
        self.meta = meta

    def __len__(self):
        return len(self.topology)

    def node(self, node):
        return self.topology.node[self.ID_map[node]]['node']

    def nodes(self):
        for node_id in self.topology:
            yield self.topology.node[node_id]['node']

    def nodes_id(self):
        for node_id in self.topology:
            yield self.topology[node_id]['node'].ID

    def hosts(self):
        for node_id in self.topology:
            node = self.topology.node[node_id]['node']
            if isinstance(node, Host):
                yield node

    def switches(self):
        for node_id in self.topology:
            node = self.topology.node[node_id]['node']
            if isinstance(node, Switch):
                yield node

    def neighbour_nodes(self, node):
        for dst in self.topology[self.ID_map[node]].keys():
            yield self.topology.node[self.ID[dst]]['node']

    def remove_nodes(self, nodes):
        self.topology.remove_nodes_from(nodes)
        for node in nodes:
            del self.ID_map[node]

    def has_node(self, node):
        return self.topology.has_node(self.ID_map[node])

    def has_link(self, src_node, dst_node):
        return self.topology.has_edge(self.ID_map[src_node], self.ID_map[dst_node])

    def link(self, src_node, dst_node):
        return self.topology.get_edge_data(self.ID_map[src_node], self.ID_map[dst_node])[0]['link']

    def links(self):
        # for src, dst, key, data in self.topology.edges(data=True, keys=True):
        for src, dst, data in self.topology.edges(data=True):
            yield data['link']

    def add_node(self, node):
        if node.ID in self.ID_map:
            ValueError("Node already exists")
        net_id = self.topology.number_of_nodes() + 1
        self.ID_map[node.ID] = net_id
        self.topology.add_node(net_id, node=node)

    def add_link(self, a_node, a_port, b_node, b_port,tp=None,latency=None):
        if self.ID_map[a_node] not in self.topology:
            raise ValueError("unknown node id: {}".format(a_node))
        if self.ID_map[b_node] not in self.topology:
            raise ValueError("unknown node id: {}".format(b_node))
        if a_port is None:
            a_port = len(self.topology.node[self.ID_map[a_node]]['node'].ports)
        if b_port is None:
            b_port = len(self.topology.node[self.ID_map[b_node]]['node'].ports)
        for key, data in self.topology[self.ID_map[a_node]].get(self.ID_map[b_node], {}).items():
            link = data['link']
            for ln, lp in ((link.a_node, link.a_port), (link.b_node, link.b_port)):
                for n, p in ((a_node, a_port), (b_node, b_port)):
                    if ln == n and lp == p:
                        raise ValueError("link already exists")
        link = Link((a_node, a_port), (b_node, b_port),tp,latency)
        self.topology.node[self.ID_map[a_node]]['node'].ports[a_port] = link
        self.topology.node[self.ID_map[b_node]]['node'].ports[b_port] = link
        self.topology.add_edge(self.ID_map[a_node], self.ID_map[b_node], link=link)

