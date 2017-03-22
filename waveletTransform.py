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

data = pd.read_csv('workload1.csv')
ts = data['X']
ts = list(ts[:8192])
haarFactor = 1/math.sqrt(2)
n = len(ts); d = 8192; w= 64
max_n = max(ts)
min_n = min(ts)
nScales = log(w,2)

class WaveletTransform(object) :
	def __init__(self,noScales = 1,wavelet = 'haar', d=8192, w = 64):
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
	def predictSimpleMarkovChain(self,ts, start, end, nV):
		#nV = number of values to predict
		#w -> The array where the predicted values must be appended
		a = ts[start:end+1]
		n = end - start + 1
		a_min = min(a); a_max = max(a); range = a_max-a_min
		nStates = 10
		#Caluclation the Transition Matrix
		p = np.zeros((nStates,nStates))
		row_sum = np.zeros(nStates)
		for i in range(n-1):
			p[a[i]][a[i+1]]+=1
			row_sum[a[i]]+=1	
		for i in range(nScales):
			row = p[i]
			s = row_sum[i]
			for j in range(len(row)):
				row[j]=row[j]/s				
		#predict nV values and append in the array
		lastState = a[-1]
		x = np.zeros(nState)
		x[lastState]=1;p1=1
		predictedCoeffStates = []
		for i in range(nV):
			p1 = np.dot(p1,p)
			x = np.dot(x,p1)
			predictedCoeffStates.append(max_index(x))
		for k in predictedCoeffSates:
			self.predictionCoeff.append(k)
	def predictCoeffs(self,ts):
		d = self.d; w= self.w;scaleNo  = self.noScales
		i = 0; n = self.d / (2**scaleNo), 
		nV = self.w /(2**scaleNo)
		#predict approximation coefficient
		self.predictSimpleMarkovChain(ts,i, n-1,nV)
		#predict the detailed coefficients
		while(scaleNo>0):
			nV = self.w/(2**scaleNo); i +=n
			n = self.d/(2**scaleNo);end = i+n-1
			self.predictSimpleMarkovChain(ts,i,end,nV)
			scaleNo-=1
		return self.predictionCoeff
			
		



