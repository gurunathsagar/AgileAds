import sys
import socket
import os

TCP_IP = '0.0.0.0'
TCP_PORT = '9000'

BUFFER_SIZE = 1024

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
tcpServer.bind((TCP_IP, TCP_PORT)) 

while True:
	tcpServer.listen(10)
	(conn, (ip,port)) = tcpServer.accept() 
	data = ''
	while True:
		data += conn.recv(1024)
		if '*' in data:
			conn.close()
	print data
	data = data.split('#')
