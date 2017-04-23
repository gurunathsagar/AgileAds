from time import sleep
import socket 
from threading import Thread 
from SocketServer import ThreadingMixIn 

class LatestValues():
    def __init__(self):
        self.list = []
        self.ip = ''

    def insertValue(self, value):
        if len(self.list) >= 64:
            self.list.pop(0)
        
        self.list.append(value)

    def returnAverage(self):
        if len(self.list) > 0:
            return sum(self.list) / float(len(self.list))

def sendToPredictor(rAvgArray, vmName, ip):
    
    sendString = str(len(rAvgArray))+"#"

    for values in rAvgArray:
        sendString += str(values) + "#"

    sendString += vmName + "#" + ip + "#"

    sendString += "*"

    tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    status = tcpClientA.connect_ex((PredictionHost, PredictionPort))

    tcpClientA.send(sendString)

    tcpClientA.close()

class ResourceManager(Thread):

    def __init__(self, connList, qList):
        Thread.__init__(self)
        self.connList = connList
        self.qList = qList

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

            averages = []
            vmNames = []
            for i in range(len(connListCopy)):
                averages.append(qList[i].returnAverage())
            leastLoaded = averages.index(min(averages))

            for i in range(len(connListCopy)):
                readyString = "ready#"
                connListCopy[i].send(readyString)
                recvData = connListCopy[i].recv(1024)
                parts = recvData.split("#")
                rVal = float(parts[0])
                vmNames.append(parts[1])
                qList[i].insertValue(float(rVal))
                rAvg += float(rVal)

            rAvg /= len(connListCopy)
            print "avg = ", rAvg, " no. of clients open = ", len(connListCopy)
            rAvgArray.append(rAvg)
            sendToPredictor(rAvgArray, vmNames[leastLoaded], qList[leastLoaded].ip)
            sleep(2)

"""
            for conn in connListCopy:
                conn.send("ready#")
                rVal = conn.recv(1024)
                rAvg += float(rVal)
"""


            #for i in range(len(resourceThreads)):
                #resourceThreads[i].start()

            #for thread in resourceThreads:
                #thread.join()

            # avgResourceVal = 0.0

            # for value in resourceValue:
            #     print "value being added: ", value
            #     avgResourceVal += value

            # avgResourceVal /= len(resourceValue)


 
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
qList = []
newthread = ResourceManager(connList, qList)
newthread.start()
threads.append(newthread)




while True: 
    tcpServer.listen(4) 
    print "Multithreaded Python server : Waiting for connections from TCP clients..." 

    (conn, (ip,port)) = tcpServer.accept() 
    connList.append(conn)
    obj = LatestValues()
    qList.append(obj)
    #newthread = ResourceCollector(conn) 
    #newthread.start() 
    #threads.append(newthread) 
    #resourceThreads.append(newthread)
 
for t in threads: 
    t.join() 
