from ovsswitch import OVSSwitch
from link import Link
import networkx as nx
import pickle
import argparse, subprocess, io,re

from vswitch import ovs_vsctl_add_bridge
from vswitch import ovs_vsctl_add_port_to_bridge
from vswitch import ovs_vsctl_set
from vswitch import ovs_vsctl_del_bridge


# Loads network from given resource and starts/finishes ovs network.

def route(start=2,end=129):
	sp = nx.shortest_path(network.topology,start,end)
	reversed_ID_map = {v: k for k, v in network.ID_map.items()}  
	mapped_sp = [reversed_ID_map[x] for x in sp]
	r = re.compile(r'\d+')
	print(sp,mapped_sp)
	for i in range(len(mapped_sp)):
		ports = {}
		show = "sudo ovs-ofctl show".split()
		br = "ovs-sw{}".format(mapped_sp[i])
		print(show,br)
		show.append(br)
		proc = subprocess.Popen(args=show,stdout=subprocess.PIPE)
		for line in io.TextIOWrapper(proc.stdout):
			if 'addr' in line:
				if 'LOCAL' in line: continue
				print(line)
				num = r.findall(line)
				if 'ens' in line:
					ports['ens'] = num[0]
				else:
					ports[int(num[3])] = num[0]
		print(ports)
		print(mapped_sp,i)
		if i == 0:
			#p1 = subprocess.Popen("sudo ovs-vsctl add-port ovs-sw{} ens3".format(mapped_sp[i]))
			#p1.wait()
			flow = ("sudo ovs-ofctl add-flow ovs-sw{} in_port={},actions=output:{}".format(mapped_sp[i],ports['ens'],ports[mapped_sp[i+1]]).split())
			rev_flow = ("sudo ovs-ofctl add-flow ovs-sw{} in_port={},actions=output:{}".format(mapped_sp[i],ports[mapped_sp[i+1]],ports['ens']).split())
			p1 = subprocess.Popen(flow)
			p2 = subprocess.Popen(rev_flow)
		elif i == len(mapped_sp)-1:
			#p1 = subprocess.Popen("sudo ovs-vsctl add-port ovs-sw{} ens8".format(mapped_sp[i]))
			#p1.wait()
			flow = ("sudo ovs-ofctl add-flow ovs-sw{} in_port={},actions=output:{}".format(mapped_sp[i],ports[mapped_sp[i-1]],ports['ens']).split())
			rev_flow = ("sudo ovs-ofctl add-flow ovs-sw{} in_port={},actions=output:{}".format(mapped_sp[i],ports['ens'],ports[mapped_sp[i-1]]).split())
			p1 = subprocess.Popen(flow)
			p2 = subprocess.Popen(rev_flow)
		if i in range(1,len(mapped_sp)-1):
			flow = ("sudo ovs-ofctl add-flow ovs-sw{} in_port={},actions=output:{}".format(mapped_sp[i],ports[mapped_sp[i-1]],ports[mapped_sp[i+1]]).split())
			rev_flow = ("sudo ovs-ofctl add-flow ovs-sw{} in_port={},actions=output:{}".format(mapped_sp[i],ports[mapped_sp[i+1]],ports[mapped_sp[i-1]]).split())
			p1 = subprocess.Popen(flow)
			p2 = subprocess.Popen(rev_flow)
		p1.wait()
		p2.wait()

		proc.wait()






parser = argparse.ArgumentParser(description='Manage OVS network deployment.')
parser.add_argument('-stat', action="store_true", default=False, help='print nodes and links number')
parser.add_argument('file', type=str, help='path to network dump')
parser.add_argument('-r', action="store_true", dest='to_run', default=False, help='run chosen network')
parser.add_argument('-c', action="store_true", dest='to_cln', default=False, help='clean chosen network')
parser.add_argument('-route', action="store_true", dest='to_route', default=False, help='clean chosen network')
args = parser.parse_args()

dump = open(args.file, 'rb')
network = pickle.load(dump)

#route()

if args.stat:
	print(list(network.nodes()))
	print(network.topology.degree())
	sp = nx.shortest_path(network.topology,2,129)
	reversed_ID_map = {v: k for k, v in network.ID_map.items()}  
	mapped_sp = [reversed_ID_map[x] for x in sp]
	r = re.compile(r'\d+')
	print(sp,mapped_sp)
	#print(network.topology[2])
	#print(network.ID_map[177])
	print(network.meta)
	print("Number of nodes: {}".format(network.topology.number_of_nodes()))
	print("Number of links: {}".format(network.topology.number_of_edges()))

if args.to_run:
	for switch in network.switches():
		switch.start()
	for link in network.links():
		if isinstance(network.node(link.a_node), OVSSwitch) and \
		   isinstance(network.node(link.b_node), OVSSwitch):
			network.node(link.a_node).connect(link.a_port, network.node(link.b_node), link.b_port)

if args.to_cln:
	for switch in network.switches():
		switch.cleanup()

