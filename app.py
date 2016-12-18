from cmd import Cmd, App, Task
import random

a = App()
c = Cmd()
c.add_state('A','',{'a': 'B','b': 'C'})
c.add_state('B','',{'a': 'B','b': 'C'})
c.add_state('C','',{'a': 'A','b': 'D'})
c.add_state('D','',{},True)
c.set_start('A')
clients, servers = [], []
for i in range(100):
	client = Cmd()
	server = Cmd()
	client.add_state('A','iperf -c 192.168.122.243 -p {0} -t 120'.format(5001 + i),{},True)
	server.add_state('A','iperf -s -p {0}'.format(5001 + i),{},True)
	client.set_start('A')
	server.set_start('A')
	clients.append(client)
	servers.append(server)
time_client = range(6,106)
time_server = range(5,105)
clients = zip(clients,time_client)
servers = zip(servers,time_server) 
perf = Cmd()
perf.add_state('A','iperf -c localhost',{'[ ID] Interval       Transfer     Bandwidth\n':'END'})
perf.add_state('END','',{},True)
perf.set_start('A')
#for i in range(99):
#	time += [(i+2)*5]*random.randint(3,10)
tasks = [Task({'ip': '192.168.122.243', 'port': 8888},d[1],d[0]) for d in servers] + [Task({'ip': '192.168.122.181', 'port': 8888},d[1],d[0]) for d in clients]
print len(tasks)
a.run(tasks)
#a.run([Task({'ip': '', 'port':8888},5,perf)])
'''
a.run([	
		Task({'ip': '', 'port':8888},5,perf),
		Task({'ip': '', 'port':8888},5,perf),
		Task({'ip': '', 'port':8888},15,perf)
		#Task({'ip': '192.168.122.243', 'port': 8888},5,server),
		#Task({'ip': '192.168.122.181', 'port': 8888},10,perf),
		#Task({'ip': '192.168.122.182', 'port': 8888},15,perf)
		#Task({'ip': '192.168.122.217', 'port': 8888},15,c),
		])	

'''