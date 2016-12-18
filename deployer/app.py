from cmd import Cmd, App, Task, Instruction
import random

a = App()
perf = Cmd()
f = open('mydump','rb')
tmp = f.read()
f.close()
i = Instruction(['sudo python3 net_manager.py -stat mydump'],{'mydump':tmp},r'/home/aemaet/pr/arccn/netbuilder/NetworkStand')
perf.add_state('A',i,{})
perf.add_state('END',Instruction(),{},True)
perf.set_start('A')
a.run([Task({'ip': '', 'port':8888},5,perf)])


