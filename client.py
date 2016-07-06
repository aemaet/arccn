import socket, pickle, time, threading
import sys
import subprocess
from cmd import Cmd

def runthread(start,cmd):
	print "started"
	while True:
		tmp = int(time.time() - start)
		print tmp
		if int(time.time() - start) >= cmd.time: 
			cmd.run()
			break
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
start = time.time()
schedule = {}
threads = []

while 1:
	conn, addr = s.accept()
	data = conn.recv(BUFFER_SIZE)
	if data: 
		cmd = pickle.loads(data)
		t = threading.Thread(target=runthread,args=(start,cmd))
		t.start()
		threads.append(t)
		print len(threads)
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
