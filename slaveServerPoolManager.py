import sys
import socket
import os
from subprocess import call

TCP_IP = '0.0.0.0'
TCP_PORT = 9000

BUFFER_SIZE = 1024

hostDict = {"host2":{"user":"arakhade",
						"ip":"152.46.16.115"
					},
			"host1":{
						"user":"ghanams",
						"ip":"152.46.17.63"
					}
			}

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
tcpServer.bind((TCP_IP, TCP_PORT)) 

while True:
	tcpServer.listen(10)
	conn, addr = tcpServer.accept()
	#(conn, (ip,port)) = tcpServer.accept() 
	data = ''
	while True:
		data += conn.recv(1024)
		if '*' in data:
			conn.close()
			break
	data = data.split('#')
	vmName = data[0]
	print "slave trying to scale up vm:",vmName
	username = hostDict[sys.argv[1]]['user']
	serverIp = hostDict[sys.argv[1]]['ip']
	try:
		call(['bash', 'stopClone.sh',vmName, username, serverIp])
		print "slave successfully scaled vm:",vmName
	except:
		print "Error in scaling up vm", vmName
