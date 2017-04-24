#References for Haar Transform
#https://www.math.cornell.edu/~numb3rs/spulido/Numb3rs_107/Numb3rs_107.html
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import numpy as np
import math
from collections import Counter
import socket
import sys

def max_index(arr):
	index = 0;m = 0
	n = len(arr)
	for i in range(n):
		if arr[i]>m:
			index = i;
			m = arr[i]
	return index

class sloCheck(object):
	def __init__(self,maxUsage, nTimes):
		self.sloDefmaxUsage = maxUsage
		self.sloDefn = nTimes
		#By definition, SLO is violated if resource usage in a 2 minute(64 units) interval is above maxUsage nTimes
		self.nTimesSLOundetected=0
	def isViolated(self, prediction, nlen,actual=None):
		countP=0;countA=0;
		for i in range(nlen):
			if prediction[i]>self.sloDefmaxUsage:
				countP+=1
			if actual != None and actual[i]>self.sloDefmaxUsage:	
				countA+=1
			if(countP>self.sloDefn):
				#SLO predicted, return True
				return True
			if(countA > self.sloDefn):
				#SLO was not detected. resulted in actual SLO
				self.nTimesSLOundetected+=1
		return False
		


class Accuracy(object):
	def __init__(self, actualTs, predictedTs):
		#self.rmse
		#self.underAllocationPercent = 0
		self.rmse = 0
		self.underAllocationPercent = 0
		self.overAllocationPercent = 0

		error = np.array(predictedTs) - np.array(actual_wValues); n = len(actualTs); sumSquares = 0
		for e in error:
			sumSquares += (float(e*e))/n
			if e < 0:
				self.underAllocationPercent+=1
			elif e > 0:
				self.overAllocationPercent+=1
		self.rmse = math.sqrt(sumSquares)
		self.underAllocationPercent = (self.underAllocationPercent/float(n))*100
		self.overAllocationPercent = (self.overAllocationPercent/float(n))*100
		pass
	def getErrors(self):
		print "rmse:", self.rmse
		print "overallocation percent:", self.overAllocationPercent
		print "underallocation percent:", self.underAllocationPercent
	def getRmse(self):
		return self.rmse
	
		

def predictSimpleMarkovChain(ts, start, end, nV,w, nStates = 40,padPercent=0):
	#nV = number of values to predict
	#w -> The array where the predicted values will be appended
	stateTs = ts[start:end+1];
	n = end - start + 1; 
	a_min = min(stateTs); a_max = max(stateTs); a_range = a_max-a_min
	binSize = (float(a_range+1))/nStates
	#print "range,n_states,binsize", a_range, nStates,binSize
	for i in range(len(stateTs)):
		stateTs[i] = int(math.floor((stateTs[i]-a_min)/binSize))
	#Caluclation the Transition Matrix
	p = np.zeros((nStates,nStates))
	row_sum = np.zeros(nStates)
	stateVector = range(nStates)
	for i in range(n-1):
		p[stateTs[i]][stateTs[i+1]]+=1
		row_sum[stateTs[i]]+=1
	for i in range(nStates):
		row = p[i]
		s = row_sum[i]
		if s!=0:
			for j in range(len(row)):
				row[j]=row[j]/s			
		else:
			for j in range(len(row)):
				row[j] = 1.0/nStates
	#predict nV values and append in the array
	lastState = stateTs[-1]
	x = np.zeros(nStates)
	x[lastState]=1;p1=1
	predictedStates = []; 
	for i in range(nV):
		p1 = np.dot(p1,p)
		x = np.dot(x,p1); k = max_index(x)
		predictedStates.append(k)
		demand =a_min + k*binSize + binSize/2
		w.append(demand + demand*padPercent/100.00)


class WaveletTransform(object) :
	def __init__(self,noScales = None,wavelet = 'haar', d=8192, w = 64):
		scales = int(math.log(w,2))
		if(noScales==None):
			self.noScales = scales
		else:
			self.noScales = noScales
		self.waveletFunction = wavelet
		self.d = d
		self.w = w
		if(wavelet == 'haar'):
			self.factor = 1/math.sqrt(2)
	def forwardTransformSingleScale(self,ts, n):
		h = n/2; i = 0;a=[0]*n
		while(i<h):
			a[i] = (ts[2*i]+ts[2*i+1]) * self.factor
			a[i+h] = (ts[2*i]-ts[2*i+1]) * self.factor
			i+=1
		i = 0;
		while(i<n):
			ts[i]=a[i]
			i+=1
	def forwardTransform(self,ts):
		n = len(ts);i=1
		while(i<=self.noScales):
			self.forwardTransformSingleScale(ts,n)
			n = n/2
			i+=1	
	def inverseTransformSingleScale(self,ts,n):
		h = n/2; i = 0; a = [0]*n
		while(i<h):
			a[2*i] = (ts[i]+ts[i+h])*((self.factor))
			a[2*i+1] = (ts[i]-ts[i+h])*((self.factor))
			i+=1
		i=0
		while(i<n):
			ts[i]=a[i]
			i+=1	
	def inverseTransform(self,ts):
		n = len(ts); i = self.noScales-1
		while(i>=0):
			self.inverseTransformSingleScale(ts,n/(2**i))
			i-=1

	def predictCoeffs(self,ts, ret,algo = 'simplemarkov',padPercent = 0):
		d = self.d; w= self.w;scaleNo  = self.noScales;
		i = 0; n = self.d / (2**scaleNo); 
		nV = int(self.w /(2**scaleNo))
		if algo == 'simplemarkov':
			predictionAlgo = predictSimpleMarkovChain

		predictionAlgo(ts,i, n-1,nV,ret,padPercent=padPercent)
		#predict the detailed coefficients
		while(scaleNo>0):
			nV = self.w/(2**scaleNo); i +=n;
			n = self.d/(2**scaleNo);end = i+n-1
			predictionAlgo(ts,i,end,nV,ret,padPercent=padPercent)
			scaleNo-=1


class timeseries(object):
	def __init__(self,lengthTs=0):
		self.ts = [5]*lengthTs
		self.lengthTs = lengthTs
	def updateTs(self, recentData):
		n = len(recentData);i=0;j=0
		while i< self.lengthTs - n:
			self.ts[i]=self.ts[i+n]
			i+=1
		while j<n:
			self.ts[i] = recentData[j]
			i+=1;j+=1
	def getTs(self):
		return self.ts			    	










d = 4096; w=64; haarFactor = 1/math.sqrt(2)
ts = timeseries(lengthTs=d);n = ts.lengthTs
dx = np.arange(0,d,1)
wx = np.arange(d,d+w,1)
maxx = [0,d+w-1]
dMaxUsage = [75]*(2)
i=0
plt.ion()
plt.show()





#Init only required for blitting to give a clean slate.

"""
Socket Server Program 
http://www.binarytides.com/python-socket-programming-tutorial/
"""
HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
print 'Socket bind complete'


while True:
	s.listen(10)
	print 'Socket now listening'

	conn, addr = s.accept()
	#display client information
	print 'Connected with ' + addr[0] + ':' + str(addr[1])
	data = ''
	while True:
		data += conn.recv(2048)
		if '*' in data:
			conn.close()
			break
    
	"""
		The prediction Module gets the data. Close the TCP socket and process the data.
		The first integer n represents how many resource usages are sent
	"""
	
	print data
	data = data.split('#')
	n = int(data[0])
	recentData = []
	for i in range(1,n+1):
		recentData.append(float(data[i]))			
	i+=1
	vmName = data[i];i+=1
	hostIp = data[i];
	ts.updateTs(recentData)
	tsPredict0 = []
	tsPredict5 = []
	tsList = ts.ts[:];max_n = max(tsList);min_n = min(tsList)
	haar = WaveletTransform(d=d,w = w)

	haar.forwardTransform(ts=tsList);
	haar.predictCoeffs(ts=tsList,ret=tsPredict0,padPercent=0)
	haar.predictCoeffs(ts=tsList,ret=tsPredict5,padPercent=5)

	haar.inverseTransform(ts=tsPredict0)
	haar.inverseTransform(ts=tsPredict5)

	slo = sloCheck(maxUsage=75, nTimes=10)
	isSloViolated = slo.isViolated(tsPredict5,len(tsPredict5))
	if(isSloViolated):
		#Trigger the VM Cloning. Send a reqest to host hostIp at port number 9000
		hostPort = 9000
		tcpSocketHost = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		status = tcpSocketHost.connect_ex((hostIp, hostPort))
		if status:
			print 'could not establish a connection'
			tcpSocketHost.close()
		else:
			stringTosend = ''+vmName+'#*'
		pass
	
	#plot Resource Usage vs Prediction
	#print ts.ts[4080:]
	plt.clf()
	usagePlot = plt.plot(dx[4000:], ts.ts[4000:],'b')
	predictedPlot = plt.plot(wx, tsPredict5,'g')
	predictedPlot = plt.plot(wx, tsPredict0)
	maxUsagePlot = plt.plot(maxx[4000:],dMaxUsage[4000:],'r')
	
	
	#ani = animation.FuncAnimation(fig, animate, dx, interval=2)
	plt.draw()
	plt.pause(0.001)
	



		


