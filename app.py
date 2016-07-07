from cmd import Cmd, App, Task


a = App()
c = Cmd()
c.add_state('A','',{'a': 'B','b': 'C'})
c.add_state('B','',{'a': 'B','b': 'C'})
c.add_state('C','',{'a': 'A','b': 'D'})
c.add_state('D','',{},True)
c.set_start('A')
perf = Cmd()
perf.add_state('A','iperf -c localhost',{},True)
perf.set_start('A')
a.run([	
		Task({'ip': '', 'port':8888},5,perf),
		Task({'ip': '', 'port':8888},15,perf)
		#Task({'ip': '192.168.122.217', 'port': 8888},10,c),
		#Task({'ip': '192.168.122.217', 'port': 8888},15,c),
		])	

