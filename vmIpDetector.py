#!/usr/bin/python
import sys
import os

def detectVMIP():

	listOfVms = ''
	while not listOfVms:
		listOfVms = os.system("/usr/sbin/arp -a | grep virbr0").read()
	
	lines = listOfVms.split("\n")
	addedIps = []
	for line in lines:
		fields = line.split(" ")
		macId = fields[3]
		ip = fields[1]
		ip = ip[1:-1]

		if macId not in macListMap:
			macListMap[macId] = ip
			addedIps.append(ip)

	for ip in addedIps:
		#os.system("sudo ./addForwarding.sh " + HOST_PUBLIC_IP + " " + str(portCount) + " " + ip)
		print("sudo ./addForwarding.sh " + HOST_PUBLIC_IP + " " + str(portCount) + " " + ip)
		IpPortMap[ip] = str(portCount)
		portCount += 1

portCount = 4050
macListMap = {}
IpPortMap = {}
HOST_PUBLIC_IP = sys.argv[1]

while True:
	detectVMIP(portCount, macListMap)
