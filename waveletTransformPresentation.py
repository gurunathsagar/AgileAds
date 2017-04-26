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
import Queue
import threading
import time



def max_index(arr):
	index = 0;m = 0
	n = len(arr)
	for i in range(n):
		if arr[i]>m:
			index = i;
			m = arr[i]
	return index

def return_nextProbableState(currentState,arr):
	index = 0;m = 0;
	s = sum(arr); #print arr
	n = len(arr)
	#print 'sum is', s
	if s == 0:
		#print 'hey'
		if currentState == n-1:
			index = np.random.randint(0,n)
		else:
			index = np.random.randint(currentState+1,n)
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
		self.repetitions = 0
	def isViolated(self, prediction, nlen,actual=None):
		countP=0;countA=0;
		for i in range(nlen):
			if prediction[i]>self.sloDefmaxUsage:
				countP+=1
			if actual != None and actual[i]>self.sloDefmaxUsage:	
				countA+=1
			print "Number of times usage predicted above level:", countP
			#print "usage:",self.sloDefmaxUsage, "Times detected:",self.sloDefn 
			if(countP>self.sloDefn):
				#SLO predicted, increment count
				self.repetitions+=1
			else:
				self.repetitions=0
			if self.repetitions >=3:
				self.repetitions = 0
				return True
			if(countA > self.sloDefn):
				#SLO was not detected. resulted in actual SLO
				self.nTimesSLOundetected+=1
		return False
	def sloParametersUpdate(self,maxUsage, nTimes):
		self.sloDefmaxUsage = maxUsage
		self.sloDefn = nTimes


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
	predictedStates = [];k = lastState 
	for i in range(nV):
		p1 = np.dot(p1,p)
		x = np.dot(x,p1); k = return_nextProbableState(k,x)
		predictedStates.append(k)
		demand =a_min + k*binSize + binSize/2
		w.append(demand + demand*padPercent/100.00)

def predictSimpleMarkovChain2(ts, start, end, nV,w, nStates = 40,padPercent=0):
	#nV = number of values to predict
	#w -> The array where the predicted values will be appended
	#print "in prediction Algo:",start,end
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
		#else:
		#	for j in range(i,len(row)):
		#		row[j] = 1.0/nStates
	#predict nV values and append in the array
	lastState = stateTs[-1];k=lastState
	x = np.zeros(nStates)
	x[lastState]=1;p1=1
	predictedStates = []; 
	for i in range(nV):
		p1 = np.dot(p1,p)
		x = np.dot(x,p1); k = return_nextProbableState(k,x)
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
			predictionAlgo = predictSimpleMarkovChain2

		predictionAlgo(ts,i, n-1,nV,ret,padPercent=padPercent)
		#predict the detailed coefficients
		while(scaleNo>0):
			nV = self.w/(2**scaleNo); i +=n;
			n = self.d/(2**scaleNo);end = i+n-1
			predictionAlgo(ts,i,end,nV,ret,padPercent=padPercent)
			scaleNo-=1


class timeseries(object):
	def __init__(self,lengthTs=0):
		self.ts = []
		self.lengthTs = 0
		try:
			name = 'fileWithValues.csv'
			self.ts = list(pd.read_csv(name,header=None)[0])
			self.lengthTs = len(self.ts)
		except:
			print "Could not open initial file"
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



def changeMaxUsageLevel(threadName, q):
	HOST = ''   # Symbolic name meaning all available interfaces
	PORT = 8080 # Arbitrary non-privileged port

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print 'MaxUsage Socket Created'
	try:
		s.bind((HOST, PORT))
	except socket.error , msg:
		print 'MaxUsage Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
	print 'MaxUsage Socket bind complete'

	while True:
		s.listen(10)
		conn, addr = s.accept()
		#display client information
		data = ''
		while True:
			data += conn.recv(2048)
			if '*' in data:
				conn.close()
				break
		data = data.split('#')
		print data
		level = int(data[0]); times = int(data[1])
		queueLock.acquire()
		q[0]=level;q[1]=times
		queueLock.release()


#https://www.tutorialspoint.com/python/python_multithreading.htm
class myThread (threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
    def run(self):
        print "Starting " + self.name
        changeMaxUsageLevel(self.name, self.q)
        print "Exiting " + self.name




d = 4096; w=64; haarFactor = 1/math.sqrt(2)
timeSeries1 = timeseries(lengthTs=d);n = timeSeries1.lengthTs

print "length of ts",n
dx = np.arange(0,d,1)
wx = np.arange(d,d+w,1)
maxx = np.arange(0,d+w,1)
dM = [100,65]
slo = sloCheck(maxUsage=dM[0], nTimes=dM[1])
dMaxUsage = [dM[0]]*(d+w)
#plt.ion()
#plt.show()

finalPredicted = []
for jk in range(n-d):
	plt.clf()
	tsPredict0 = []
	tsPredict5 = []

	tsList = timeSeries1.ts[jk:d+jk];max_n = max(tsList);min_n = min(tsList)
	haar = WaveletTransform(d=d,w = w)

	haar.forwardTransform(ts=tsList);
	haar.predictCoeffs(ts=tsList,ret=tsPredict0)
	haar.predictCoeffs(ts=tsList,ret=tsPredict5)

	haar.inverseTransform(ts=tsPredict0)
	haar.inverseTransform(ts=tsPredict5)

	for i in range(len(tsPredict5)):
		tsPredict5[i] = tsPredict5[i]*1.05


	#plot Resource Usage vs Prediction
	#print ts.ts[4080:]
	#plt.clf()
	#usagePlot = plt.plot(dx[:], ts.ts[:d],'b')
	usagePlot = plt.plot(wx[:], timeSeries1.ts[d+jk:d+w+jk],'r')
	predictedPlot = plt.plot(wx, tsPredict5[:],'b')
	predictedPlot = plt.plot(wx, tsPredict0[:],'g')
	#plt.plot(ts.ts)

	#ani = animation.FuncAnimation(fig, animate, dx, interval=2)
	
	plt.show()
	#plt.draw()
	plt.pause(0.002)

		


