import time, socket, threading, random, pickle, subprocess, datetime

class Cmd():
	def __init__(self,time=0):
		self.time = time
		self.states = {}
		self.startState = None
		self.endStates = []

	def __str__(self):
		return str(self.time)
	def __repr__(self):
		return str(self.time)

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
		procs = []
		while True:
			for arg in state['instruction'].args:
				print(arg)
				f = open(state['instruction'].dir + '/' + arg,'wb+')
				f.write(state['instruction'].args[arg])
				f.close()
			for inst in state['instruction'].instruction:
				proc = subprocess.Popen(inst.split(),cwd=state['instruction'].dir,stdout=subprocess.PIPE)
				stdout_lines = iter(proc.stdout.readline, "")
				trigger = ''
				with open("log.txt", "a") as text_file:
					for stdout_line in stdout_lines:
						if not stdout_line: break
						print(stdout_line.decode('ascii'))
						text_file.write(datetime.datetime.today().ctime())
						text_file.write(stdout_line.decode('ascii'))
						if stdout_line in state['transition'].keys():
							trigger = stdout_line
							break
					proc.wait()
				proc.stdout.close()
				procs.append(proc)
			if self.startState in self.endStates: 
				break
			print(trigger)
			try:
				newState = state['transition'][trigger]
			except:
				print('invalid/empty transition, closing', trigger)
				for proc in procs:
					proc.wait()
				break
			if newState in self.endStates:
				print("reached ", newState)
				for proc in procs:
					proc.kill()
				break 
			else:
				state = self.states[newState]

class Instruction():
	def __init__(self,instr='',args=[],directory=None):
		self.instruction = instr
		self.args = args
		self.dir = directory

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
		print(address['ip'], address['port'])
		s.connect((address['ip'], address['port']))
		s.send(self.make_message(cmd,time))
		s.close()

	def make_message(self,cmd,time):
		cmd.time = time 
		print(cmd)
		t = pickle.dumps(cmd)
		return t

	def run(self, tasks): 
		threads = []
		for task in tasks:
			t = threading.Thread(target=self.call,args=(task.address,task.cmd, task.time))
			t.start()
			threads.append(t)
		for t in threads:
			print('join')
			t.join()
			#self.call(task,time.time())