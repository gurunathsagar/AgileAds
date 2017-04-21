from time import sleep
import socket 
from threading import Thread 
from SocketServer import ThreadingMixIn 

def sendToPredictor(rAvgArray):
    
    sendString = str(len(rAvgArray))+"#"

    for values in rAvgArray:
        sendString += str(values) + "#"

    sendString += "*"

    tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    status = tcpClientA.connect_ex((PredictionHost, PredictionPort))

    tcpClientA.send(sendString)

    tcpClientA.close()

class ResourceManager(Thread):

    def __init__(self, connList):
        Thread.__init__(self)
        self.connList = connList

    def sendToPredictor(rAvgArray):
        
        sendString = str(len(rAvgArray))+"#"

        for values in rAvgArray:
            sendString += str(values) + "#"

        sendString += "*"

        tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        status = tcpClientA.connect_ex((PredictionHost, PredictionPort))

        tcpClientA.send(sendString)

        tcpClientA.close()

    def run(self):

        print "Resource manager spawned"
        while True:

            if len(connList) == 0:
                continue

            print "new time", "len of list = ", len(connList)
            rAvgArray = []
            #resourceValue = [0.0] * len(connList)

            #runningThreads = []
            connListCopy = connList
            # for i in range(len(connListCopy)):
            #     newthread = ResourceCollector(connListCopy[i])
            #     newthread.start()
            #     runningThreads.append(newthread)

            # for thread in runningThreads:
            #     thread.join()

            # for i in range(len(runningThreads)):
            #     resourceValue[i] = runningThreads[i].receivedValue
            #     print "Inserted Value ", resourceValue[i]

            rAvg = 0.0

            for conn in connListCopy:
                conn.send("ready#")
                rVal = conn.recv(1024)
                rAvg += float(rVal)

            rAvg /= len(connListCopy)

            #for i in range(len(resourceThreads)):
                #resourceThreads[i].start()

            #for thread in resourceThreads:
                #thread.join()

            # avgResourceVal = 0.0

            # for value in resourceValue:
            #     print "value being added: ", value
            #     avgResourceVal += value

            # avgResourceVal /= len(resourceValue)

            print "avg = ", rAvg, " no. of clients open = ", len(connListCopy)

            rAvgArray.append(rAvg)

            sendToPredictor(rAvgArray)


            sleep(2)


# class ResourceCollector(Thread):

#     def __init__(self, conn):
#         Thread.__init__(self)
#         self.conn = conn
#         # self.i = i
#         self.receivedValue = 0.0
#         # #self.resourceValue = resourceValue

#     def run(self):
#         print "Sending ready message"
#         self.conn.send("ready#")
#         print "Sent ready message"
#         recvValue = conn.recv(2048)
#         print "Received value from client as: ", recvValue
#         self.receivedValue = float(recvValue)


# # Multithreaded Python server : TCP Server Socket Thread Pool
# class ClientThread(Thread): 
 
#     def __init__(self,ip,port): 
#         Thread.__init__(self) 
#         self.ip = ip 
#         self.port = port 
#         print "[+] New server socket thread started for " + ip + ":" + str(port)
#         fname = ''
#         file_handle = ''
        
#     def run(self): 
#         data = ''
#         while True : 
#             data += conn.recv(2048)
#             if 'nameofprocess' in data:
#                 recvBuffer = data.split('#')
#                 filename = recvBuffer[1:]
#                 if recvBuffer[-1]:
#                     data = recvBuffer[-1]
#                 else:
#                     data = ''
#                 #print 'filename is ', filename[0]
#                 #print 'data: ', data
#                 fname = filename[0]
#                 file_handle = open(fname, 'a')
#                 continue
#             file_handle = open(fname, 'a')
#             #file_handle.write(str(data))
#             recvBuffer = data.split('#')
#             #print "Recv Buffer as follows: ", recvBuffer
#             if recvBuffer[-1]:
#                 data = recvBuffer[-1]
#             else:
#                 data = ''
#             for values in recvBuffer:
#                 if values:
#                     print "Server received data:", values, 'fname = ', fname
#                     file_handle.write(str(values)+"\n")
#             file_handle.close()
#             #MESSAGE = raw_input("Multithreaded Python server : Enter Response from Server/Enter exit:")
#             #if MESSAGE == 'exit':
#                 #break
#             #conn.send()  # echo 
 
# Multithreaded Python server : TCP Server Socket Program Stub
TCP_IP = '0.0.0.0' 
TCP_PORT = 3000
BUFFER_SIZE = 20  # Usually 1024, but we need quick response 

PredictionPort = 8888
PredictionHost = '127.0.0.1'
 
tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
tcpServer.bind((TCP_IP, TCP_PORT)) 
threads = [] 
resourceThreads = []

connList = []
newthread = ResourceManager(connList)
newthread.start()
threads.append(newthread)


while True: 
    tcpServer.listen(4) 
    print "Multithreaded Python server : Waiting for connections from TCP clients..." 

    (conn, (ip,port)) = tcpServer.accept() 
    connList.append(conn)
    #newthread = ResourceCollector(conn) 
    #newthread.start() 
    #threads.append(newthread) 
    #resourceThreads.append(newthread)
 
for t in threads: 
    t.join() 
