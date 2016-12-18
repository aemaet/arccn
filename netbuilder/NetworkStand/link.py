class Link(object):
    def __init__(self, pair1=None, pair2=None, throughput=None,latency=None):
        self.a_node, self.a_port = (None, None) if pair1 is None else pair1
        self.b_node, self.b_port = (None, None) if pair2 is None else pair2
        self.throughput = throughput
        self.latency = latency

    def get_linked(self, node, port):
        if self.a_node == node and self.a_port == port:
            return self.b_node, self.b_port
        elif self.b_node == node and self.b_port == port:
            return self.a_node, self.a_port
        raise ValueError("resolve link for unknown source")

    def __eq__(self, link):
        return (self.a_node, self.a_port) == (link.a_node, link.a_port) and \
               (self.b_node, self.b_port) == (link.b_node, link.b_port) or \
               (self.a_node, self.a_port) == (link.b_node, link.b_port) and \
               (self.b_node, self.b_port) == (link.a_node, link.a_port)

    def __str__(self):
        return "n1: {}; p1: {}; n2: {}; p2: {};".format(self.a_node, self.a_port, self.b_node, self.b_port)

    def __repr__(self):
        return "n1: {}; p1: {}; n2: {}; p2: {};".format(self.a_node, self.a_port, self.b_node, self.b_port)        

    def __contains__(self, node, port):
        return (self.a_node, self.a_port) == (node, port) or \
               (self.b_node, self.b_port) == (node, port)
