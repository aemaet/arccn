import networkx as nx
from networkx.drawing.nx_agraph import to_agraph
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
from networkx.utils import (powerlaw_sequence, create_degree_sequence)
import math, random, os
import pygraphviz as pgv
from uniparse import create_net

class Topology():
	def __init__(self):
		self.backbone = []
		self.aggregation = []
		self.access = []

	def fat_tree(self,k):
		res = []
		core = int(k*k/4)
		print core
		struct = {'core': range(core),
		'agg': set(),
		'edge': set(),
		'server': set()
		}
		core_l = list(split(range(core),k/2))
		agg = slice_l(int(k/2),range(core, core + k*k/2))
		for i in range(k/2):
			for j in core_l[i]:
				for l in agg[i]:
					res.append((j,l))
					struct['agg'].add(l)
						
		agg_s = list(split(sorted(struct['agg']),k))
		agg = max(struct['agg']) + 1
		for i in range(k):
			for j in agg_s[i]:
				for l in range(int(k/2)):
					res.append((j,l+agg))
					struct['edge'].add(l+agg)
			agg+=k/2
		edge = max(struct['edge']) + 1
		for i in struct['edge']:
			for j in range(k/2):
				res.append((i,edge+j))
				struct['server'].add(edge+j)
			edge+=k/2
		return res,struct

	def bcube(self,n,k):
		servers = int(math.pow(n,k+1))
		switches = int(math.pow(n,k))
		res = []
		for i in range(servers):
				res.append((servers + i/n,i))
		limit = max(list(sum(res, ()))) + 1
		for i in range(1,k+1):
			level = slice_l(int(math.pow(n,i)),range(servers))
			for l in level:
				for j in l:
					c = 0
					res.append((limit + c/n,j))
					c+=1
				limit += c/n + 1
				c = 0
		return res, sorted(set(sum(res, ())))[-int(math.pow(n,k)):]


	def create_star(self,node):
		sequence = create_degree_sequence(node, powerlaw_sequence, exponent=2.5)
		graph = nx.configuration_model(sequence)
		loops = graph.selfloop_edges()
		graph = nx.Graph(graph)
		graph.remove_edges_from(loops)
		components = sorted(nx.connected_components(graph), key=len, reverse=True)
		lcc = graph.subgraph(components[0])
		#pos = nx.spring_layout(lcc)
		#nx.draw_networkx(lcc, pos)
		graph = list(nx.generate_edgelist(lcc))
		edges = lcc.edges()
		#print(edges)
		flat = list(sum(edges, ()))
		return edges, max(flat,key=flat.count)
		#plt.show()

	def create_ring(self,node):
		res = []
		for i in range(node-1):
			res.append((i,i+1))
		return res

	def aggregate(self,n,access_type,k=0,c=()):
		num_node = 0
		adjust = lambda x: (x[0] + num_node,x[1]+num_node)
		adjust_struct = lambda a: [x + num_node for x in a]
		res = []
		ring = self.create_ring(n)
		res += map(adjust,ring)
		num_node += n
		if access_type == 'star':
			for i in range(n):
				temp, center = self.create_star(k)
				temp = map(adjust,temp)
				res += temp
				res.append((i,center+num_node))
				num_node=max(list(sum(temp, ()))) + 1
		elif access_type == 'ftree':
			struct = {'core': [],
					'agg': [],
					'edge': [],
					'server': []
					}
			for i in range(n):
				temp, struct_t = self.fat_tree(k)
				temp = map(adjust,temp)
				struct = add_dict(struct,dict(zip(struct_t, map(adjust_struct, struct_t.values()))))
				res += temp
				res += [(i,x) for x in [y+num_node for y in struct_t['core']]]
				num_node=max(list(sum(temp, ()))) + 1
			elist = []
		elif access_type == 'bcube':
			servers = []
			for i in range(n):
				cube, center = self.bcube(c[0],c[1])
				print cube,center
				cube = map(adjust, cube)
				servers += [x+num_node for x in range(int(math.pow(c[0],c[1]+1)))]
				res += cube + [(i,x+num_node) for x in center]
				num_node=max(list(sum(cube, ()))) + 1
		return res, num_node

	def create_topology(self, backbone='zoo/Atmnet.graphml', agg_n=2, a_type='star', k=1, c=()):
		node,edge = parse_zoo(backbone)
		G = nx.Graph(edge)
		G.add_nodes_from(node)
		A=to_agraph(G)        # convert to a graphviz graph
		A.layout()            # neato layout
		A.draw("core.ps") 
		self.backbone = []
		self.aggregation = []
		self.access = { 'star':[],
						'ftree':[],
						'bcube':[]}
		self.backbone += node
		#node,edge = [0,1,2], self.create_ring(3) + [(2,0)]
		res = edge
		agg = []
		adjust = lambda x: (x[0] + num_node,x[1]+num_node)
		num_node = len(node)
		output = open('topo/{}.txt'.format(backbone),'w+')
		output.write('name: {}; backbone nodes: {}\n'.format(backbone,len(node)))
		for i in set(sum(res, ())):
			a_type = random.choice(['star','ftree','bcube'])
			if a_type == 'star':
				k = random.randint(3,7)
			if a_type == 'ftree':
				k = random.choice([2,4])
			if a_type == 'bcube':
				c = (random.randint(2,6),random.randint(0,1))
			tmp, t = self.aggregate(agg_n,a_type,k=k,c=c)
			tmp = map(adjust,tmp)
			print 'agg', self.aggregation
			self.aggregation += [x+num_node for x in range(agg_n)]
			#print tmp, [(n,tmp[0][0]),(n,tmp[0][1])]
			agg += [tmp[0][0],tmp[0][-1]]
			self.access[a_type] += tmp
			res += tmp + [(node[i],tmp[0][0]),(node[i],tmp[0][-1])]
			num_node = max(list(sum(res, ()))) + 1
			output.write('Node {}, type: {}, params: {}, nodes: {}\n'.format(i,a_type,(k,c),len(set(sum(tmp, ())))))
			#print(max(list(sum(res, ()))), num_node)
		output.close()
		'''
		elist = []
		for p in res:
			elist.append(u'{} {}'.format(p[0],p[1]))
		#print elist, len(elist)
		graph = nx.read_edgelist(elist)	
		print graph.nodes(), graph.edges(), len(graph.nodes())
		print agg
		pos = nx.spring_layout(graph)
		nx.draw_networkx(graph, pos)
		nx.draw_networkx_nodes(graph,pos,
		                       nodelist=map(str,node),
		                       node_color='g')
		nx.draw_networkx_nodes(graph,pos,
		                       nodelist=map(str,agg),
		                       node_color='y')
		plt.show()
		'''
		return res





def add_dict(d1,d2):
	for k in d1:
		d1[k] += d2[k]
	return d1

def parse_zoo(xml):
	print(xml)
	tree = ET.parse(xml)
	root = tree.getroot()
	node = []
	edge = []
	for child in root.find('graph').findall('node'):
		node.append(int(child.attrib['id']))
	#print(node)
	for child in root.find('graph').findall('edge'):
		edge.append((int(child.attrib['target']),int(child.attrib['source'])))
	return node, edge

def slice_l(n,lst):
	return [ lst[i::n] for i in xrange(n) ]

def split(a, n):
    k, m = len(a) / n, len(a) % n
    return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in xrange(n))

def draw(res,f):
	G = nx.Graph(res)
	#G.add_edges_from(res)
	for i in set(sum(res, ())):
		if i in t.backbone:
			G.add_node(i,style='filled',fillcolor='green')
		elif i in t.aggregation:
			G.add_node(i,style='filled',fillcolor='yellow')
	A=to_agraph(G)        # convert to a graphviz graph
	A.layout()            # neato layout
	A.draw("topo/zoo/"+f+".ps")

def draw_test(res,struct):
	G = nx.Graph(res)
	#G.add_edges_from(res)
	for i in set(sum(res, ())):
		if i in struct['core']:
			G.add_node(i,style='filled',fillcolor='green')
		elif i in struct['agg']:
			G.add_node(i,style='filled',fillcolor='yellow')
		elif i in struct['edge']:
			G.add_node(i,style='filled',fillcolor='red')
	A=to_agraph(G)        # convert to a graphviz graph
	A.layout()            # neato layout
	A.draw("topo/test/1.ps")
#t.fat_tree(6)

#t.create_topology(agg_n=2,a_type='star',k=3,c=(2,0))
nets = ['Ai3.graphml',
'Cesnet1993.graphml',
'Nsfcnet.graphml',
'Sprint.graphml',
'Abilene.graphml',
'Singaren.graphml',
'Itnet.graphml',
'TLex.graphml',
'JanetExternal.graphml',
'Cesnet1997.graphml'
]

       # write postscript in k5.ps with neato layout
t = Topology()
n, l = t.fat_tree(4)
print(n,l)
a = range(10)
print list(split(a,3))
draw_test(n,l)
'''
for n in nets:
	top = t.create_topology(backbone='zoo/'+n)
	draw(top,n)
	ids = list(set(sum(top, ())))
	attrib = {}
	for x,y in top:
		if x in t.backbone and y in t.backbone:
			attrib[(x,y)] = {'weight':10,'latency':70}
		elif (x,y) in t.access['star']:
			attrib[(x,y)] = {'weight':1,'latency':10}
		elif (x,y) in t.access['ftree']:
			attrib[(x,y)] = {'weight':10,'latency':10}
		elif (x,y) in t.access['bcube']:
			attrib[(x,y)] = {'weight':10,'latency':10}
		elif x in t.aggregation and y in t.aggregation:
			attrib[(x,y)] = {'weight':10,'latency':10}
		else:
			attrib[(x,y)] = {'weight':10,'latency':10}
	edge = {}
	for l in top:
		temp = [l,l[::-1]]
		for x,y in temp:
			if x in edge: edge[x].append(y)
			else: edge[x] = [y]
	create_net(ids,edge,n,'topo/zoo/{}'.format(n),attrib)

'''

	



	