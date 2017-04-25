from time import sleep
import socket 
from threading import Thread 
from SocketServer import ThreadingMixIn 

class LatestValues():
    def __init__(self):
        self.list = []
        self.ip = ''
        self.badCall = 0

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

    try:
        status = tcpClientA.connect_ex((PredictionHost, PredictionPort))
        tcpClientA.send(sendString)

    except socket.error, exc:
        print "Error Connecting to Prediction Module. Not sending this value"

    tcpClientA.close()

class ResourceManager(Thread):

    def __init__(self, connList, qList):
        Thread.__init__(self)
        self.connList = connList
        self.qList = qList

    def run(self):

        print "Resource manager spawned"
        fileHandle = open('average4096.csv','a+')
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

            dataNotRead = True

            for i in range(len(connListCopy)):
                readyString = "ready#"
                deletedConnection = -1
                try:    
                    connListCopy[i].send(readyString)
                    try:
                        recvData = connListCopy[i].recv(1024)
                    except socket.error, exc:
                        qList[i].badCall += 1
                        if qList[i].badCall >= 3:
                            connList[i].close()
                            connListCopy.pop(i)
                            connList.pop(i)
                            qList.pop(i)
                            deletedConnection = i
                            continue
                    qList[i].badCall = 0
                    if not recvData:
                        qList[i].badCall += 1
                        continue
                        if qList[i].badCall >= 3:
                            connList[i].close()
                            connListCopy.pop(i)
                            connList.pop(i)
                            qList.pop(i)
                            deletedConnection = i
                            print 'deleting ', i
                            continue
                    qList[i].badCall = 0
                    dataNotRead = False
                    parts = recvData.split("#")
                    print i, 'value received = ', parts[0], 'ip = ', qList[i].ip
                    rVal = float(parts[0])
                    vmNames.append(parts[1])
                    qList[i].insertValue(float(rVal))
                    rAvg += float(rVal)
                except socket.error, exc:
                    print "Unable to get latest data"
                    qList[i].badCall += 1
                    if qList[i].badCall >= 3:
                        connList[i].close()
                        #connListCopy.pop(i)
                        #connList.pop(i)
                        #qList.pop(i)
                        deletedConnection = i
                        continue

            if len(connListCopy)==0 or deletedConnection==leastLoaded or dataNotRead :
                if len(connListCopy)==0:
                    print 'No connections available'
                    sleep(2)
                print "Not sending value to Predictor"
                continue

            rAvg /= len(connListCopy)
            fileHandle.write(str(rAvg) + "\n")
            print "avg = ", rAvg, " no. of clients open = ", len(connListCopy)
            rAvgArray.append(rAvg)
            sendToPredictor(rAvgArray, vmNames[leastLoaded], qList[leastLoaded].ip)
            sleep(2)

        fileHandle.close()

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
    obj.ip = ip
    qList.append(obj)
    #newthread = ResourceCollector(conn) 
    #newthread.start() 
    #threads.append(newthread) 
    #resourceThreads.append(newthread)
 
for t in threads: 
    t.join() 
