import wrappers as wps


class Node(object):
    def __init__(self, **opts):
        self.ID = opts.pop('ID', int(id(self)))
        self.name = opts.pop('name', "n{}".format(self.ID))
        self.ports = opts.pop('ports', {})

        self.ip = opts.pop('ip', None)
        if self.ip is not None:
            self.ip = wps.CW_ip(self.ip)

        self.msk = opts.pop('msk', None)
        if self.msk is not None:
            self.msk = wps.CW_ip(self.msk)

        self.opts = opts

    def __getitem__(self, item):
        if hasattr(self, item):
            return getattr(self, item)
        elif item in self.opts:
            return self.opts[item]
        raise KeyError

    def __setitem__(self, key, value):
        if hasattr(self, key):
            self.key = value
        else:
            self.opts[key] = value

    def __eq__(self, node):
        return self.ID == node.ID and self.name == node.name and self.ip == node.ip \
               and self.msk == node.msk and self.ports == node.ports

    def __str__(self):
        return "name: {}, ports: {}, ip: {}, msk: {}, ID: {}".format(self.name, self.ports, self.ip, self.msk, self.ID)


    def __repr__(self):
        return "name: {}, ports: {}, ip: {}, msk: {}, ID: {}".format(self.name, self.ports, self.ip, self.msk, self.ID)


class Switch(Node):
    def __init__(self, **opts):
        self.mac = None
        self.dpid = opts.pop('dpid', None)
        if self.dpid is not None:
            # lowest 48 bits are the switch MAC
            # TODO: find out how to avoid implicit type conversion
            self.mac = wps.CW_eth(int(self.dpid & ~(0xFFFF << 48)))

        self.tables = opts.pop('tabs', [])
        Node.__init__(self, **opts)


class Host(Node):
    def __init__(self, **opts):
        self.mac = opts.pop('mac', None)
        """#FIXME"""
        self.msk = None
        self.gw = None
        Node.__init__(self, **opts)