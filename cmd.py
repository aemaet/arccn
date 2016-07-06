import time, socket, threading, random, pickle

class Cmd():
	def __init__(self,time=0):
		self.time = time
		self.states = {}
		self.startState = None
		self.endStates = []

	def add_state(self, name, instruction, transition, end_state=0):
		state = {'instruction': instruction,
				 'transition': transition}
		self.states[name] = (state)
		if end_state:
			self.endStates.append(name)

	def set_start(self, name):
		self.startState = name

	def run(self):
		try:
			state = self.states[self.startState]
		except:
			raise KeyError("must call .set_start() before .run()")
		if not self.endStates:
			raise  InitializationError("at least one state must be an end_state")
	
		while True:
			trigger = random.choice(['a','b'])
			print trigger
			try:
				newState = state['transition'][trigger]
			except:
				raise KeyError("invalid transition")
			if newState in self.endStates:
				print("reached ", newState)
				break 
			else:
				state = self.states[newState]

class Task():
	def __init__(self,address,time, cmd):
		self.address = address
		self.time = time
		self.cmd = cmd

class App():
	def __init__(self, params = {}):
		self.params = params

	def __str__(self):
		return self.params()

	def call(self, address, cmd, time):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((address['ip'], address['port']))
		s.send(self.make_message(cmd,time))
		s.close()

	def make_message(self,cmd,time):
		cmd.time = time 
		t = pickle.dumps(cmd)
		return t

	def run(self, tasks): 
		threads = []
		for task in tasks:
			t = threading.Thread(target=self.call,args=(task.address,task.cmd, task.time))
			t.start()
			threads.append(t)
		for t in threads:
			print 'join'
			t.join()
			#self.call(task,time.time())