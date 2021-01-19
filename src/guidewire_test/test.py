'''
Created on Jul 17, 2019

@author: rliu01
'''
def solution(X, Y, A):
    N = len(A)
    result = -1
    nX = 0
    nY = 0
    for i in range(N):
        if A[i] == X:
            nX += 1
        elif A[i] == Y:
            nY += 1
        if nX == nY:
            result = i
    return result
if __name__ == '__main__':
    arr = map(int, raw_input().rstrip().split())
    x = int(raw_input())
    y = int(raw_input())
    print solution(x,y,arr)