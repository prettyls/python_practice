'''
Created on Feb 24, 2019

@author: rliu01
'''
N = int(raw_input())


def split(inputString):
    evenString = ""
    oddString = ""
    for i in range (len(inputString)):
        if (i % 2 == 0):
            evenString=evenString+inputString[i]
        else:
            oddString = oddString + inputString[i]
    print (evenString + " " + oddString)

for j in range (N):
    input = raw_input()
    split(input)
    
