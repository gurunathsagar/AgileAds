#References for Haar Transform
#https://www.math.cornell.edu/~numb3rs/spulido/Numb3rs_107/Numb3rs_107.html

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

data = pd.read_csv('workload2.csv')
ts = data['X']
ts = list(ts[:8192])
haarFactor = 1/math.sqrt(2)
n = len(ts); d = 8192; w= 4
max_n = max(ts)
min_n = min(ts)
nScales = int(math.log(w,2))

class WaveletTransform(object) :
	def __init__(self,noScales = None,wavelet = 'haar', d=8192, w = 64,binSize = 2.5):
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
		n = end - start + 1
		a_min = min(a); a_max = max(a); a_range = a_max-a_min
		nStates = int(math.ceil((a_range+1)/self.binSize))
		#print "range, states, min, max ->",a_range,nStates,a_min,a_max
		for i in range(len(a)):
			a[i] = int(math.floor((a[i]-a_min)/self.binSize))
		#Caluclation the Transition Matrix
		#print "aaaaaaaaaaaaaaaaaaaaaa",a,b
		p = np.zeros((nStates,nStates))
		row_sum = np.zeros(nStates)
		#print p
		#print "The states are ->",a,b
		for i in range(n-1):
			p[a[i]][a[i+1]]+=1
			row_sum[a[i]]+=1
		#print p	
		for i in range(nStates):
			row = p[i]
			s = row_sum[i]
			#print "here",i,s
			if s!=0:
				#print s
				for j in range(len(row)):
					row[j]=row[j]/s			
			else:
				#print "hola"
				for j in range(len(row)):
					row[j] = 1.0/nStates
		#predict nV values and append in the array
		lastState = a[-1]
		x = np.zeros(nStates)
		x[lastState]=1;p1=1
		predictedCoeffStates = []
		for i in range(nV):
			p1 = np.dot(p1,p)
			x = np.dot(x,p1)
			predictedCoeffStates.append(max_index(x))
			#print "The next state vector is ->", x
		#print "predicted Coeff States ->",predictedCoeffStates, "end"
		for k in predictedCoeffStates:
			self.predictionCoeff.append(a_min + k*self.binSize + self.binSize/2)
	def predictCoeffs(self,ts):
		d = self.d; w= self.w;scaleNo  = self.noScales
		i = 0; n = self.d / (2**scaleNo); 
		nV = int(self.w /(2**scaleNo))
		#predict approximation coefficient
		self.predictSimpleMarkovChain(ts,i, n-1,nV)
#		print "predicted elements", nV , self.predictionCoeff
		#predict the detailed coefficients
		while(scaleNo>0):
			nV = self.w/(2**scaleNo); i +=n;
			n = self.d/(2**scaleNo);end = i+n-1
			#print "Predicting detailed coeffs, scale, signal", scaleNo,ts[i:n]
			self.predictSimpleMarkovChain(ts,i,end,nV)
			#print "predicted values",self.predictionCoeff
			scaleNo-=1
#		print "The final predicted coefficients are as follows ->", self.predictionCoeff
		return self.predictionCoeff
			

a=ts[:]
haar = WaveletTransform(d=8192,w = 32)
haar.forwardTransform(ts=a)
b = haar.predictCoeffs(ts=a)
haar.inverseTransform(ts=b)
for i in b:
	print i

