import socket, subprocess, pickle
import sys
from cmd import Cmd
HOST = ''  
PORT = 7777 
BUFFER_SIZE = 4096
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
 


conn, addr = s.accept()
print 'server'
process = subprocess.Popen('iperf -s'.split())
print 'Connected with ' + addr[0] + ':' + str(addr[1])
data = conn.recv(BUFFER_SIZE)
t = pickle.loads(data)
t.run()
     
s.close()