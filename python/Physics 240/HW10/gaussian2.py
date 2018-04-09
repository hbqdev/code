# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 18:20:12 2013

@author: ttran
"""
from __future__ import division
from pylab import *
def gausselm(m):
    for col in range(len(m[0])):
        for row in range(col+1, len(m)):
            r = [(rowValue * (-(m[row][col] / m[col][col]))) for rowValue in m[col]]
            m[row] = [sum(pair) for pair in zip(m[row], r)]
    ans = []
    m.reverse() 
    for sol in range(len(m)):
            if sol == 0:
                ans.append(m[sol][-1] / m[sol][-2])
            else:
                inner = 0
                for x in range(sol):
                    inner += (ans[x]*m[sol][-2-x])
                    ans.append((m[sol][-1]-inner)/m[sol][-sol-2])
    ans.reverse()
    return ans
    

print gausselm(([[1.0,1.0,0.0,-9],[0,-2.0,7.0,15.0], [1,-1,-1,0.0]]))