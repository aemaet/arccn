import socket, pickle, time, threading
import sys
import subprocess
from cmd import Cmd
'''
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
'''
def runthread(start,cmd):
	wait = cmd.time - int(time.time() - start)
	print(wait)
	if wait > 0: time.sleep(wait)
	cmd.run()

HOST = ''   
PORT = 8888 
BUFFER_SIZE = 1048576
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')
 


try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()
     
print('Socket bind complete')
 

s.listen(10)
print('Socket now listening')
while True:
	s.settimeout(None)
	conn, addr = s.accept()
	start = time.time()
	cmd = []
	while True:
		data = conn.recv(BUFFER_SIZE)
		if data:
			cmd.append(pickle.loads(data))
		try: 
			s.settimeout(5.0)
			conn, addr = s.accept()
		except socket.timeout:
			break
	cmd.sort(key=lambda x: x.time)
	print(cmd)
	for c in cmd:
		t = threading.Thread(target=runthread,args=(start,c))
		t.start()
#print "received data:", data

s.close()
