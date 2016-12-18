import os
from nodes import Switch
from vswitch import ovs_vsctl_add_bridge
from vswitch import ovs_vsctl_add_port_to_bridge
from vswitch import ovs_vsctl_set
from vswitch import ovs_vsctl_del_bridge


class OVSSwitch(Switch):
    # Open vSwitch switch. Depends on ovs-vsctl.

    def __init__(self, **opts):
        Switch.__init__(self, **opts)

    def start(self):
        ovs_vsctl_add_bridge(self.name)	

    def attach_port(self, port_name):
        ovs_vsctl_add_port_to_bridge(self.name, port_name)

    def detach_port(self, port_name):
        os.system("ovs-vsctl del-port " + self.name + " " + port_name)

    def connect_ports(self, src_port_name, dst_port_name):
        self.ports.add(src_port_name)
        os.system("ovs-vsctl add-port " + self.name + " " + src_port_name)
        os.system("ovs-vsctl set interface " + src_port_name + " type=patch")
        os.system("ovs-vsctl set interface " + src_port_name + " options:peer=" + dst_port_name)

    def conn_by_patch(self, another):
        src_port_name = "patch" + str(self.ID) + "-" + str(another.ID)
        dst_port_name = "patch" + str(another.ID) + "-" + str(self.ID)
        self.attach_port(src_port_name)
        another.attach_port(dst_port_name)
        os.system("ovs-vsctl set interface " + src_port_name + " type=patch")
        os.system("ovs-vsctl set interface " + src_port_name + " options:peer=" + dst_port_name)
        os.system("ovs-vsctl set interface " + dst_port_name + " type=patch")
        os.system("ovs-vsctl set interface " + dst_port_name + " options:peer=" + src_port_name)

    def connect(self, src_port, dst_sw, dst_port):
        src_port_name = "p" + str(self.ID) + ':' + str(src_port) + '-' + str(dst_sw.ID) + ':' + str(dst_port)
        dst_port_name = "p" + str(dst_sw.ID) + ':' + str(dst_port) + '-' + str(self.ID) + ':' + str(src_port)

        self.attach_port(src_port_name)
        dst_sw.attach_port(dst_port_name)

        ovs_vsctl_set('interface', src_port_name, 'type', None, 'patch')
        ovs_vsctl_set('interface', src_port_name, 'options', 'peer', dst_port_name)
        ovs_vsctl_set('interface', dst_port_name, 'type', None, 'patch')
        ovs_vsctl_set('interface', dst_port_name, 'options', 'peer', src_port_name)

    def conn_by_veth(self, dst_sw, id):
        src_port_name = "veth" + str(id)
        dst_port_name = "veth" + str(id + 1)
        os.system("ip link add " + src_port_name + " type veth peer name " + dst_port_name)
        # os.system("ifconfig " + src_port_name + " up")
        # os.system("ifconfig " + dst_port_name + " up")
        self.attach_port(src_port_name)
        dst_sw.attach_port(dst_port_name)

    def cleanup(self):
        ovs_vsctl_del_bridge(self.name)

