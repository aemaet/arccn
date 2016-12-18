import socket


TCP_IP = ''
BUFFER_SIZE = 1024
MESSAGE = "123"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((TCP_IP, 7777))
server.send(MESSAGE)
server.close()
client.connect((TCP_IP, 8888))
client.send(MESSAGE)
client.close()