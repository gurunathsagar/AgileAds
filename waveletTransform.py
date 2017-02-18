import pandas as pd
import numpy as np
import math

data = pd.read_csv('input.csv')
ts = data['X']
ts = list(ts[:2048])
avgfactor = 1/math.sqrt(2)
n = len(ts); d = 2048; w= 64

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


