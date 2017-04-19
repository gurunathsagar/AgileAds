#References for Haar Transform
#https://www.math.cornell.edu/~numb3rs/spulido/Numb3rs_107/Numb3rs_107.html
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
from collections import Counter

def max_index(stateVector,p):
	newState = np.random.choice(a=stateVector,p =p)
	d = {}
	for i in stateVector:
		d[i]=p[i]
	#print "The state vector probablity p is\n",p	
	#print "The seleceted State is \n",newState
	#print "The dictionary d is \n",d
	#print "\n"
	return newState


class WaveletTransform(object) :
	def __init__(self,noScales = None,wavelet = 'haar', d=8192, w = 64,binSize = 2):
		scales = int(math.log(w,2))
		if(noScales==None):
			self.noScales = scales
		else:
			self.noScales = noScales
		self.waveletFunction = wavelet
		self.d = d
		self.w = w
		self.predictionCoeff = []
		self.binSize = binSize			#size of each bin of markov chain. If total range is 100, then number of states = 100/2.5 = 40
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
	def predictSimpleMarkovChain(self,ts, start, end, nV):
		#nV = number of values to predict
		#w -> The array where the predicted values must be appended
		a = ts[start:end+1]; b = a[:]
		n = end - start + 1; binSize = self.binSize
		a_min = min(a); a_max = max(a); a_range = a_max-a_min
		nStates = int(math.ceil((a_range+1)/binSize))
		if nStates < 40:
			nStates = 40
			binSize = int(math.ceil((a_range+1)/nStates))
		print "range and n_states ", a_range, nStates
		for i in range(len(a)):
			a[i] = int(math.floor((a[i]-a_min)/binSize))
		#Caluclation the Transition Matrix
		p = np.zeros((nStates,nStates))
		row_sum = np.zeros(nStates)
		stateVector = range(nStates)
		for i in range(n-1):
			p[a[i]][a[i+1]]+=1
			row_sum[a[i]]+=1
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
		lastState = a[-1]
		x = np.zeros(nStates)
		x[lastState]=1;p1=1
		predictedCoeffStates = []
		graph = [];step = self.d/len(a);i = 0;X_AxisScale = [];X_PredictedScale = []
		while(i<self.d):
			X_AxisScale.append(i);
			i+=step
		for i in range(nV):
			p1 = np.dot(p1,p)
			x = np.dot(x,p1)
			predictedCoeffStates.append(max_index(stateVector,x))
		i = step
		for k in predictedCoeffStates:
			X_PredictedScale.append(self.d + i);i+=step
			graph.append(a_min + k*binSize + binSize/2)
			self.predictionCoeff.append(a_min + k*binSize + binSize/2)
		#print len(a);
		#print len(X_AxisScale)
		#print len(graph)
		#print len(X_PredictedScale)
		ret = [X_AxisScale,b,X_PredictedScale,graph]
		#plt.plot(X_AxisScale,b); plt.plot(X_PredictedScale,graph)
		return ret
		#print X_PredictedScale
	def predictCoeffs(self,ts):
		d = self.d; w= self.w;scaleNo  = self.noScales
		i = 0; n = self.d / (2**scaleNo); 
		nV = int(self.w /(2**scaleNo))
		ret = self.predictSimpleMarkovChain(ts,i, n-1,nV)
		#plt.plot(ret[0],ret[1]);plt.plot(ret[2],ret[3])
		#print "Approx Signal Predicted Value-"
		#print self.predictionCoeff
		#predict the detailed coefficients
		while(scaleNo>0):
			nV = self.w/(2**scaleNo); i +=n;
			n = self.d/(2**scaleNo);end = i+n-1
			ret = self.predictSimpleMarkovChain(ts,i,end,nV)
			#if(scaleNo == 1):
			#	plt.plot(ret[0],ret[1]);plt.plot(ret[2],ret[3])
			#print "Detailed signal Scale ",scaleNo
			#print self.predictionCoeff
			scaleNo-=1
		return self.predictionCoeff


filename = '13324.csv'
filename = '1805.csv'	
data = pd.read_csv(filename)
timeseries = list(data['X'])
d = 4096; w= 64; haarFactor = 1/math.sqrt(2)
xAxisRange_w = np.array([i for i in range(d, d+w)])
xAxisRange_dw = np.array([i for i in range(d+w)])

ts = list(timeseries[:d]);a=ts[:]
n = len(ts); max_n = max(ts);min_n = min(ts)
nScales = int(math.log(w,2))


haar = WaveletTransform(d=d,w = w,binSize = 1)

haar.forwardTransform(ts=a)
predicted_wValues = haar.predictCoeffs(ts=a)
haar.inverseTransform(ts=predicted_wValues)
actual_wValues = list(timeseries[d:d+w])

#Now for plotting the predicted values vs original values


plt.plot(xAxisRange_dw[4000:],timeseries[4000:d+w]) #Plotting the original timeseries wrt timeslots
rmse_array = np.array(predicted_wValues) - np.array(actual_wValues); n = len(predicted_wValues)
rmse = sum(np.multiply(rmse_array , rmse_array))
rmse = sum(np.multiply(rmse_array , rmse_array))
print math.sqrt(rmse/n)
#plotting the original values in window w vs predicted values
plt.plot(xAxisRange_w,actual_wValues)
plt.plot(xAxisRange_w,predicted_wValues)
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

