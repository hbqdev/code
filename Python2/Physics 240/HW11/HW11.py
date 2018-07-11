# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 23:13:01 2013

@author: ttran
"""
from __future__ import division
from pylab import *


m1 = matrix([[-3.0,2.0,0.0],[2.0,-5.0,3.0],[0,3,-7]])
b1 = matrix(([1],[1],[-15]))

m2 = matrix([[-3.0,2.0,0.0],[2.0,-5.0,3.0],[0,3,-7]])
b2 = matrix(([1],[1],[-39]))

m3 = matrix([[-2.0,1.0,0.0],[1,-2.0,1.0],[0,1,-2]])
b3 = matrix(([0],[-1],[-4]))

m4 = matrix([[-2.0,1.0,0.0],[1,-2.0,1.0],[0,1,-1]])
b4 = matrix(([0],[-1],[-1]))

m5 = matrix([[-1.0,0.0,0.0],[1,-2.0,1.0],[0,1,-1]])
b5 = matrix(([2],[-1],[-1]))

F = []
def inverse(m,b) :
    minverse = linalg.inv(m)
    ans = minverse*b
    return ans

print "Matrix a"
x1 = inverse(m1,b1)
Frw1 = -4*(4-x1[2]-1)
print x1
print "Frw =", Frw1
F1 =  -0.48*(4-4)
print "Numerical Frw", F1
F.append(F1)
print " " 

print "Matrix b"
x2 = inverse(m2,b2)
Frw2 = -4*(10-x2[2]-1)
print x2
print "Frw =", Frw2
F2 = -0.48*(10-4)
print "Numerical Frw", F2
F.append(F2)
print " " 

print "Matrix c"
x3 = inverse(m3,b3)
Frw3 = -1*(4-x3[2]-1)
print x3
print "Frw =", Frw3
F3 = -0.25*(4-6)
print "Numerical Frw", F3
print " " 
F.append(F3)
print " " 
print "Matrix d"
x4 = inverse(m4,b4)
Frw4 = -0*(4-x4[2]-1)
print x4
print "Frw =", Frw3
F4 = -0.33*(4-6)
print "Numerical Frw", F4
F.append(F4)
print ""

print "Matrix e"
x5 = inverse(m5,b5)
Frw5 = -4*(4-x1[2]-1)
print x5
print "Frw =", Frw5
F5 = -0.5*(4-2)
print "Numerical Frw", F5
F.append(F5)

Lw = [4,10,4,4,4]
plot(Lw,F)
xlabel("Lw")
ylabel("Frw")
show()
