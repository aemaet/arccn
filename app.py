from cmd import Cmd, App, Task


a = App()
c = Cmd()
c.add_state('A','',{'a': 'B','b': 'C'})
c.add_state('B','',{'a': 'B','b': 'C'})
c.add_state('C','',{'a': 'A','b': 'D'})
c.add_state('D','',{},True)
c.set_start('A')
a.run([	
		Task({'ip': '', 'port': 8888},5,c),
		Task({'ip': '', 'port': 8888},10,c),
		])	

