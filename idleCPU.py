from time import sleep

prev_idle = prev_total = 0
while True:
    with open('/proc/stat') as file:
    	line = file.readline()
    	line.strip()
    	words = line.split()[1:]
    	columns = [float(obj) for obj in words]

    idle, total = columns[3], sum(columns)
    idle_d = idle - prev_idle
    total_d = total - prev_total
    prev_idle, prev_total = idle, total
    idleCPU = 100.0*(idle_d/total_d)
    print('%5.1f%%' % idleCPU)
    sleep(2)
