'''
Created on Jul 17, 2019

@author: rliu01
'''
def solution(A):
    # write your code in Python 3.6
    smallest = 1
    a = min(A)
    b = max(A)
    if b <= 0 or a > 1:
        return smallest
    else:
        s = set(A)
        for x in range(a,b+1):
            if x in s:
                x = x + 1
                smallest = x
            elif x not in s:
                smallest = x
                break
#             else:
#                 smallest = b + 1
        return smallest 

if __name__ == '__main__':
    arr = map(int, raw_input().rstrip().split())
    print solution(arr)