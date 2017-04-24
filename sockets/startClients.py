#!/usr/bin/python
import commands
import os

def startPollingClients(pidMap, clientMap):
	
	data = os.popen("ps aux | grep vb1 | grep libvirt | awk -F ' ' \'{print $2; print $14}\' ").read()
	
	lines = data.split('\n')

	for i in xrange(0, len(lines)-1, 2):
		if "aux" not in lines[i+1]:
			pidMap.update({str(lines[i]): lines[i+1]})
			if str(lines[i]) not in clientMap:
				os.system('python pollClient.py ' + str(lines[i]) + ' ' + lines[i+1] )
				clientMap.update({str(lines[i]): True})
		
pidMap = {}
clientMap = {}
while True:
	startPollingClients(pidMap, clientMap)

