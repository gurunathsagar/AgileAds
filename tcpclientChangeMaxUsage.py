from time import sleep
import socket 
from SocketServer import ThreadingMixIn 
import sys

PredictionPort = 8080
PredictionHost = '152.46.17.1'

sendString = ''+sys.argv[1]+'#'+sys.argv[2]+'#*' 
tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
	status = tcpClientA.connect_ex((PredictionHost, PredictionPort))
	tcpClientA.send(sendString)

except socket.error, exc:
	print "Error Connecting to Prediction Module. Not sending this value"

tcpClientA.close()

