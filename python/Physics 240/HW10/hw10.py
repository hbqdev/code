# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 01:03:40 2013

@author: ttran
"""

from __future__ import division
from pylab import *
from scipy import linalg

a=array([[1.0,1.0,0.0,-9],[0,-2.0,7.0,15.0],[1,-1,-1,0.0]])
m = matrix([[1.0,1.0,0.0],[0,-2.0,7.0],[1,-1,-1]])
b = matrix(([-9],[15],[0]))

m5 = matrix([[-1.0,1.0,0.0],[1,-2.0,1.0],[0,1,-1]])
b5 = matrix(([2],[-1],[-1]))

def GE(matrix) :
    ans = zeros(matrix.shape[0])
    #Begin elimination
    for columns in range(matrix.shape[1]) :
       for rows in range(columns+1, matrix.shape[0]) :
           rowtemp = matrix[columns] * (-matrix[rows][columns]/matrix[columns][columns])
           matrix[rows] = rowtemp+matrix[rows]
           
    #Begin backward substitution        
    for columns in (arange(matrix.shape[0]).shape[0] - arange(matrix.shape[0])-1) :
       if (columns < matrix.shape[1]-2) :
           matrix[columns][matrix.shape[1]-1] = matrix[columns][matrix.shape[1]-1] - (sum(matrix[columns]) - matrix[columns][columns]-matrix[columns][matrix.shape[1]-1])
       ans[columns]=matrix[columns][matrix.shape[1]-1]/(matrix[columns][columns])
       for rows in range(columns) :
           matrix[rows][columns] = matrix[rows][columns]*ans[columns]
       
    return ans


print "x1 = ", GE(a)[0]
print "x2 = ", GE(a)[1]
print "x3 = ", GE(a)[2]

print "Testing using Numpy LinAlg"
print linalg.solve(m5,b5)

        