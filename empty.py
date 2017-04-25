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

name = '1805.csv'
tf = list(pd.read_csv(name,header=None)[0])
print tf
