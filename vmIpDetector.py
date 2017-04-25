#!/usr/bin/python
import sys
import os

def detectVMIP(portCount, macListMap, IpPortMap):

	listOfVms = ''
	while not listOfVms:
		listOfVms = os.popen("/usr/sbin/arp -a | grep virbr0").read()
	
	lines = listOfVms.split("\n")
	lines = lines[0:-1]
	addedIps = []
	for line in lines:
		#print line
		fields = line.split(" ")
		print fields
		macId = fields[3]
		ip = fields[1]
		ip = ip[1:-1]
		print macId, ip
		if macId not in macListMap:
			macListMap[macId] = ip
			addedIps.append(ip)

	for ip in addedIps:
		os.system("sudo ./addForwardRule.sh " + HOST_PUBLIC_IP + " " + str(portCount) + " " + ip)
		#print("sudo ./addForwarding.sh " + HOST_PUBLIC_IP + " " + str(portCount) + " " + ip)
		IpPortMap[ip] = str(portCount)
		portCount += 1

portCount = 4050
macListMap = {}
IpPortMap = {}
HOST_PUBLIC_IP = sys.argv[1]

while True:
	detectVMIP(portCount, macListMap, IpPortMap)
