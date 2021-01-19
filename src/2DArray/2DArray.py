'''
Created on Mar 1, 2019

@author: rliu01
'''
import math
import os
import random
import re
import sys

if __name__ == '__main__':
    arr = []

    for _ in xrange(6):
        arr.append(map(int, raw_input().rstrip().split()))
    
sum = []
for i in range (4):
    for j in range (4):
        
        sum.append(arr[i][j] + arr[i][j + 1] + arr[i][j + 2] + arr[i + 1][j + 1] + arr[i + 2][j] + arr[i + 2][j + 1] + arr[i + 2][j + 2])
sum.sort()
print sum[15]
     
