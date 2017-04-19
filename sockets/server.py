import socket 
from threading import Thread 
from SocketServer import ThreadingMixIn 
 
# Multithreaded Python server : TCP Server Socket Thread Pool
class ClientThread(Thread): 
 
    def __init__(self,ip,port): 
        Thread.__init__(self) 
        self.ip = ip 
        self.port = port 
        print "[+] New server socket thread started for " + ip + ":" + str(port)
        fname = ''
        file_handle = ''
        
    def run(self): 
        data = ''
        while True : 
            data += conn.recv(2048)
            if 'nameofprocess' in data:
                recvBuffer = data.split('#')
                filename = recvBuffer[1:]
                if recvBuffer[-1]:
                    data = recvBuffer[-1]
                else:
                    data = ''
                #print 'filename is ', filename[0]
                #print 'data: ', data
                fname = filename[0]
                file_handle = open(fname, 'a')
                continue
            file_handle = open(fname, 'a')
            #file_handle.write(str(data))
            recvBuffer = data.split('#')
            #print "Recv Buffer as follows: ", recvBuffer
            if recvBuffer[-1]:
                data = recvBuffer[-1]
            else:
                data = ''
            for values in recvBuffer:
                if values:
                    print "Server received data:", values, 'fname = ', fname
                    file_handle.write(str(values)+"\n")
            file_handle.close()
            #MESSAGE = raw_input("Multithreaded Python server : Enter Response from Server/Enter exit:")
            #if MESSAGE == 'exit':
                #break
            #conn.send()  # echo 
 
# Multithreaded Python server : TCP Server Socket Program Stub
TCP_IP = '0.0.0.0' 
TCP_PORT = 2000 
BUFFER_SIZE = 20  # Usually 1024, but we need quick response 
 
tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
tcpServer.bind((TCP_IP, TCP_PORT)) 
threads = [] 
 
while True: 
    tcpServer.listen(4) 
    print "Multithreaded Python server : Waiting for connections from TCP clients..." 
    (conn, (ip,port)) = tcpServer.accept() 
    newthread = ClientThread(ip,port) 
    newthread.start() 
    threads.append(newthread) 
 
for t in threads: 
    t.join() 
