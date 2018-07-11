# -*- coding: utf-8 -*-
"""
Created on Thu May  9 21:49:50 2013

@author: ttran
"""

from __future__ import division
from pylab import *

def errintg(x) :
    return sqrt(x)
    
def lsphere(x1,x2,x3,x4) :
    return((x1-1)**2+(x2-1)**2+(x3-1)**2+(x4-1)**2)
    
def rsphere(x1,x2,x3,x4,d):
    return ((x1-(1+d))**2+(x2-1)**2+(x3-1)**2+(x4-1)**2)
    
def montcf(func,a,b,n) : #function to integrate 1 dimension function
    N = rand(n)
    f = 0
    fn = 0
    error = []
    for i in range(len(N)) :
        f +=  1/n*(func(N[i]))
        fn += 1/n*(func(N[i])**2)
        error.append((b-a)*sqrt((fn-f**2)/n)) 
    avg = (b-a)*f
    return avg, error, N

def montsph(funct1,funct2,a,b,n,d) : #function to integrate spheres
    hits = 0
    for i in range(n):
        x1 = a+(b-a)*random()
        x2 = a+(b-a)*random()
        x3 = a+(b-a)*random()
        x4 = a+(b-a)*random()
        if funct1(x1,x2,x3,x4) <= 1 or funct2(x1,x2,x3,x4,d) <= 1:
            hits += 1
    ratio = hits/N
    volume = ratio*(b-a)**4     
    return volume

if __name__ == '__main__' :
    a,b,n = 0,1,100
    f = errintg
    answer, error, N = montcf(f,a,b,n)
    print "Integral of sqrt(x)" , answer
    scatter(N,error)
    xlabel("N data points")
    ylabel("Error")
    title("Error as a function of N")
    d = 3/2
    a,b = 0, 2+d
    N = 100000
    f1 = lsphere
    f2 = rsphere
    answer = montsph(f1,f2,a,b,N,d)
    print "The volume of the union of the sphere" , answer
    show()