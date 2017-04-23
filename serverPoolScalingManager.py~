#This is server pool scaling manager
#decides if one wishes to scale the number of servers

#will be listening on port number 9999
"""
Socket Server Program 
http://www.binarytides.com/python-socket-programming-tutorial/
"""
HOST = ''   # Symbolic name meaning all available interfaces
PORT = 9999 # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
print 'Socket bind complete'

while True:
	s.listen(10)
	print 'Socket now listening'

	conn, addr = s.accept()
	#display client information
	print 'Connected with ' + addr[0] + ':' + str(addr[1])
	data = ''
	while True:
		data += conn.recv(2048)
		if '*' in data:
			conn.close()
			break
	if 'yes' in data:
		#scale servers
		#inform host1 to clone to host2		
		pass
