import xml.etree.ElementTree as ET
import network as net
import pickle, os, parser, argparse

def parse_zoo(xml):
	print(xml)
	tree = ET.parse(xml)
	root = tree.getroot()
	node = []
	edge = {}
	for child in root.find('graph').findall('node'):
		node.append(int(child.attrib['id']))
	#print(node)
	for child in root.find('graph').findall('edge'):
		temp = [(int(child.attrib['target']),int(child.attrib['source'])),(int(child.attrib['source']),int(child.attrib['target']))]
		for x,y in temp:
			if x in edge: edge[x].append(y)
			else: edge[x] = [y]
	#print(edge)
	return node, edge

class IntNode(object):
	def __init__(self, ID, neighbors):
		self.uid = ID
		self.neighbors = set(neighbors)


def create_net(ids,links,meta,name='netdump',attrib={}):
	"""
	Build network graph from RocketFuel configuration file.
	IMPORTANT: it is supposed, topology has no parallel edges!
	"""
	nodes = []
	for i in ids:
		try:
			nodes.append(IntNode(i,links[i]))
		except KeyError:
			print('stray node, warning!')
			continue
	res_net = net.Network(meta)

	for x in nodes:
		res_net.add_node(net.OVSSwitch(ID=x.uid, name="ovs-sw{}".format(x.uid)))

	for x in nodes:
		for yid in x.neighbors:
			# suppose there are no parallel edges
			if not res_net.has_link(x.uid, yid):
				try:
					res_net.add_link(x.uid, None, yid, None,attrib[(x.uid,yid)]['weight'],attrib[(x.uid,yid)]['latency'])
				except KeyError:
					res_net.add_link(x.uid, None, yid, None,attrib[(yid,x.uid)]['weight'],attrib[(yid,x.uid)]['latency'])
	print(res_net.meta)
	print("Number of nodes: {}".format(res_net.topology.number_of_nodes()))
	print("Number of links: {}".format(res_net.topology.number_of_edges()))
	f = open(name, 'wb+')
	pickle.dump(res_net, f)

def parse_merlin(fname):
	f = open(fname,'r')
	i = 1
	is_node = True
	node = []
	edge = {}
	for line in f:
		l = line.split()
		#print(l)
		if '*Vertices' in l: continue
		if '*Arcs' in l: 
			is_node = False
			continue
		if '*Edges' in l: break
		if is_node:
			node.append(int(l[0]))
		else:
			i,o = int(l[0]),int(l[1])
			if i in edge: edge[i].append(o)
			else: edge[i] = [o]
			if o in edge: edge[o].append(i)
			else: edge[o] = [i]
	f.close()
	return node, edge 

def clear():
	source = 'ZOO/'
	for root, dirs, filenames in os.walk(source):
		for f in filenames:
			print(f)
			this_file = open(os.path.join(source, f), "r")
			this_files_data = this_file.readlines()
			this_file.close()
			# rewrite the file with all line except the one you don't want
			this_file = open(os.path.join(source, f), "w")
			for line in this_files_data:
				if 'xml' in line:
					this_file.write('''<?xml version="1.0" encoding="utf-8"?><graphml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">\n''')
				else:
					this_file.write(line)
			this_file.close()

#n, l =parse_zoo_xml('Abvt.graphml')
#n,l = parse_merlin('PAJEK/701-2005-04-29-pajek.NET')
'''
argparser = argparse.ArgumentParser(description='Topology parser')
argparser.add_argument('--dir', type=str,
				   help='parse whole directory')
argparser.add_argument('--file', type=str,
				   help='parse single file')
argparser.add_argument('type', type=str,
				   help='type of topologies: zoo, merlin or rf')

args = argparser.parse_args()
if args.dir:
	files = os.listdir(args.dir)
	for f in files:
		print(f)
		if args.type == 'zoo':
			n,l = parse_zoo(args.dir + '/' + f)
			create_net(n,l,'zoo-net ' + f,args.dir + '_net/' + f)
		elif args.type == 'merlin':
			n,l = parse_merlin(args.dir + '/' + f)
			create_net(n,l,'merlin-net ' + f,args.dir + '_net/' + f)
		elif args.type == 'rf':
			n = parser.parse_rocketfuel_file(args.dir + '/' + f)
			pf = open(args.dir + '_net/' + f, 'wb+')
			pickle.dump(n, pf)
if args.file:
	f = args.file
	print(f)
	if args.type == 'zoo':
		n,l = parse_zoo(args.dir + '/' + f)
		create_net(n,l,'zoo-net ' + f,args.dir + '_net/' + f)
	elif args.type == 'merlin':
		n,l = parse_merlin(args.dir + '/' + f)
		create_net(n,l,'merlin-net ' + f,args.dir + '_net/' + f)
	elif args.type == 'rf':
		n = parser.parse_rocketfuel_file(args.dir + '/' + f)
		pf = open(args.dir + '_net/' + f, 'wb+')
		pickle.dump(n, pf)
'''

#create_net(n,l)


