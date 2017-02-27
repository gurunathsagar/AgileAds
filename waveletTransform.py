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

data = pd.read_csv('input2.csv')
ts = data['X']
ts = list(ts[:2048])
avgfactor1 = 1/math.sqrt(2)
avgfactor = 1/2.0
n = len(ts); d = 2048; w= 64
max_n = max(ts)


nScales = 6 #= log(64,2)
scale = [ts,[],[],[],[],[],[]]
#the last signal is approximation signal
for i in range(1,nScales+1):
	prev = i-1
	n = len(scale[prev])
	j = 0
	while(j<n):
		s0 = scale[prev][j]+scale[prev][j+1]
		s0 = s0 * avgfactor
		scale[i].append(s0)
		j+=2

for i in range(nScales+1):
	print i,len(scale[i])

scale1 = scale[1]
predictedVals1 = []
scale2 = scale[2]
predictedVals2 = []
scale3 = scale[3]
predictedVals3 = []
scale4 = scale[4]
predictedVals4 = []
scale5 = scale[5]
predictedVals5 = []
scale6 = scale[6]

p1 = np.zeros((6,6))
p=1
row_sum = np.zeros(6)

for i in range(len(scale1)-1):
	p1[scale1[i]][scale1[i+1]]+=1
	row_sum[scale1[i]]+=1

for i in range(6):
	row = p1[i]
	s = row_sum[i]
	for j in range(len(row)):
		row[j]=row[j]/s

#predicting the 32 values for scale1 -
i = scale1[-1]
x = np.zeros(6) 
x[i]=1
for i in range(32):
	p = np.dot(p,p1)
	x = np.dot(x,p)
	predictedVals1.append(max_index(x))



