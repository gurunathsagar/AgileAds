from time import sleep
import sys
import socket

host = '127.0.0.1'
port = 2000
BUFFER_SIZE = 2000 
#MESSAGE = raw_input("tcpClientA: Enter message/ Enter exit:")
tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
tcpClientA.connect((host, port))
prev_idle = prev_total = prev_sum = 0
print "hi", sys.argv[1]
INITIAL_MESSAGE = 'nameofprocess#'+sys.argv[1]
tcpClientA.send(INITIAL_MESSAGE)

while True:
    with open('/proc/stat') as file:
    	line = file.readline()
    	line.strip()
    	words = line.split()[1:]
    	columns = [float(obj) for obj in words]

    with open('/proc/'+sys.argv[1]+'/stat') as file2:
        line = file2.readline()
        line.strip()
        words = line.split()
        col_14 = words[13]
        col_15 = words[14]
        #print '\n', col_14, '&', col_15, '&', prev_sum
        procCpu = int(col_15) + int(col_14)

    procCpu_d = procCpu - prev_sum
    print '\n', procCpu_d
    prev_sum = procCpu

    idle, total = columns[3], sum(columns)
    idle_d = idle - prev_idle
    total_d = total - prev_total
    prev_idle, prev_total = idle, total
    idleCPU = 100.0*(idle_d/total_d)

    procCpuPercent = 100*(procCpu_d/total_d)

    print('%5.1f%%' % idleCPU)
    print('%5.1f%%' % procCpuPercent)

    MESSAGE = str(procCpuPercent)
    tcpClientA.send(MESSAGE)
    
    sleep(2)
