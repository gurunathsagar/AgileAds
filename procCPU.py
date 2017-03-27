from time import sleep
import sys
import csv

prev_idle = prev_total = prev_sum = 0
print "hi", sys.argv[1]
fileHandle = open(sys.argv[1]+".csv", 'wb')
csvhandle = csv.writer(fileHandle)
while True:
    with open('/proc/stat') as file1:
    	line = file1.readline()
    	line.strip()
    	words = line.split()[1:]
    	columns = [float(obj) for obj in words]
    file1.close()

    with open('/proc/'+sys.argv[1]+'/stat') as file2:
        line = file2.readline()
        line.strip()
        words = line.split()
        col_14 = words[13]
        col_15 = words[14]
        #print '\n', col_14, '&', col_15, '&', prev_sum
        procCpu = int(col_15) + int(col_14)
    file2.close()

    procCpu_d = procCpu - prev_sum
    #print '\n', procCpu_d
    prev_sum = procCpu

    idle, total = columns[3], sum(columns)
    idle_d = idle - prev_idle
    total_d = total - prev_total
    prev_idle, prev_total = idle, total
    idleCPU = 100.0*(idle_d/total_d)

    procCpuPercent = 100*(procCpu_d/total_d)
    fileHandle.write(str(procCpuPercent)+"\n")
    #csvhandle.writerow(str(procCpuPercent)+"\n")
    print 'writing to file: ', str(procCpuPercent)
    #print('%5.1f%%' % idleCPU)
    #print('%5.1f%%' % procCpuPercent)
    sleep(1)
