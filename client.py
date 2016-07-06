import socket, pickle, time, threading
import sys
import subprocess
from cmd import Cmd

def runthread(start,cmd):
	print "started"
	while cmd:
		tmp = int(time.time() - start)
		print tmp, cmd[0].time
		if int(time.time() - start) >= cmd[0].time: 
			cmd[0].run()
			cmd.pop(0)
			continue
		time.sleep(1)

HOST = ''   
PORT = 8888 
BUFFER_SIZE = 8192
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
 


try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'
 

s.listen(10)
print 'Socket now listening'
while True:
	s.settimeout(None)
	conn, addr = s.accept()
	start = time.time()
	cmd = []
	while True:
		data = conn.recv(BUFFER_SIZE)
		if data:
		#	print 'gottem' 
			cmd.append(pickle.loads(data))
		#t.start()
		#threads.append(t)
		#print len(threads)
		try: 
		#	print 'fetching'
			s.settimeout(5.0)
			conn, addr = s.accept()
		#	print 'setting'
		except socket.timeout:
		#	print 'timeout'
			break
	cmd.sort(key=lambda x: x.time)
	print cmd
	t = threading.Thread(target=runthread,args=(start,cmd))
	t.start()
	t.join()
	'''
	to_remove = [] 
	curr_time = time.time() - start
	
	print int(curr_time)
	for k in schedule:
		if int(curr_time) >= int(k):
			threads.append(threading.Thread(target=schedule[k].run()))
			to_remove.append(k)
	for k in to_remove:
		schedule.pop(k)
	print len(schedule)
	#process = subprocess.Popen('iperf -c localhost'.split())
	print 'Connected with ' + addr[0] + ':' + str(addr[1])
	data = conn.recv(BUFFER_SIZE)

	if data: 
		t = pickle.loads(data)
		schedule[t.time] = t
	#todo = collections.OrderedDict(sorted(schedule.items()))
	time.sleep(1)
	'''
#print "received data:", data

s.close()
