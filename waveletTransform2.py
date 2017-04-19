#References for Haar Transform
#https://www.math.cornell.edu/~numb3rs/spulido/Numb3rs_107/Numb3rs_107.html
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
from collections import Counter

def max_index(arr):
	index = 0;m = 0
	n = len(arr)
	for i in range(n):
		if arr[i]>m:
			index = i;
			m = arr[i]
	return index

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
	print "range,n_states,binsize", a_range, nStates,binSize
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
		self.predictionCoeff = []
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


filename = '13324.csv'
#filename = '1805.csv'	
data = pd.read_csv(filename)
timeseries = list(data['X'])
d = 4096; w= 64; haarFactor = 1/math.sqrt(2)
xAxisRange_w = np.array([i for i in range(d, d+w)])
xAxisRange_dw = np.array([i for i in range(d+w)])

ts = list(timeseries[:d]);a=ts[:]
n = len(ts); max_n = max(ts);min_n = min(ts)
nScales = int(math.log(w,2))


haar = WaveletTransform(d=d,w = w)

haar.forwardTransform(ts=a);predicted_wValues=[];predictedPad5=[]
haar.predictCoeffs(ts=a,ret=predicted_wValues)
haar.predictCoeffs(ts=a,ret=predictedPad5,padPercent=5)
haar.inverseTransform(ts=predicted_wValues)
haar.inverseTransform(ts=predictedPad5)
actual_wValues = list(timeseries[d:d+w])

#Now for plotting the predicted values vs original values


plt.plot(xAxisRange_dw[4000:],timeseries[4000:d+w]) #Plotting the original timeseries wrt timeslots

errors = Accuracy(actual_wValues, predicted_wValues)
errorsPad5 = Accuracy(actual_wValues, predictedPad5)
errors.getErrors()
print "pad5"
errorsPad5.getErrors()

#plotting the original values in window w vs predicted values
plt.plot(xAxisRange_w,actual_wValues)
plt.plot(xAxisRange_w,predicted_wValues)
plt.plot(xAxisRange_w,predictedPad5)
plt.show()


"""		
data = pd.read_csv(filename)
timeseries = list(data['X'])
d = 4096; w= 64; haarFactor = 1/math.sqrt(2)
xAxisRange_w = np.array([i for i in range(d, d+w)])
xAxisRange_dw = np.array([i for i in range(d+w)])

ts = list(timeseries[:d]);a=ts[:]
n = len(ts); max_n = max(ts);min_n = min(ts)
nScales = int(math.log(w,2))


haar = WaveletTransform(d=d,w = w)

haar.forwardTransform(ts=a)
predicted_wValues = haar.predictCoeffs(ts=a)
haar.inverseTransform(ts=predicted_wValues)
actual_wValues = list(timeseries[d:d+w])

#Now for plotting the predicted values vs original values


plt.plot(xAxisRange_dw[4000:],timeseries[4000:d+w]) #Plotting the original timeseries wrt timeslots

#plotting the original values in window w vs predicted values
plt.plot(xAxisRange_w,actual_wValues)
plt.plot(xAxisRange_w,predicted_wValues)
plt.show()"""
#for i in b:
#	print i

