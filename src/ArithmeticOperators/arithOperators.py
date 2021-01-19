'''
Created on Feb 19, 2019

@author: rliu01
'''
import math
import os
import random
import re
import sys

def solve(meal_cost, tip_percent, tax_percent):
    totalCost = meal_cost + (meal_cost * (tip_percent + tax_percent)/100)
    print(int(round(totalCost)))

if __name__ == '__main__':
    meal_cost = float(raw_input())

    tip_percent = int(raw_input())

    tax_percent = int(raw_input())

    solve(meal_cost, tip_percent, tax_percent)