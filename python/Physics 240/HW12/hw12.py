# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 13:55:52 2013

@author: ttran
"""
from __future__ import division
from pylab import *
from sympy import *

print "Testing Newton's method"

x = Symbol('E')
f = x**2 - 612
fprime = diff(f,x)
y = []
x0 = 10.0
for i in range(0,5,1) : 
    xi = x0 - (f.subs(x,x0)/fprime.subs(x,x0))
    y.append(xi)
    x0 = xi
print y
print ''
print 'correct value for sqrt(612)', 24.7386
print ''

print 'Now computing E'

a = 20 * 5.29 * 10**-11
h = 1.054*10**-34
m = 9.31 * 10**-31
V = -2.17895999 * 10**-18
v = -1.602*10**-19
ev =[0*v,1*v,12*v,3*v,4*v,5*v,6*v,7*v,8*v,9*v,10*v,11*v,12*v,13*v]
E = Symbol('E')
fv = []
for i in range(len(ev)) :
    fv.append(sqrt(-ev[i])-sqrt(ev[i]-V)*tan(a/h*sqrt(2*m*(ev[i]-V))))
    
plot(fv,ev) #plot the test function of E

#Define the
fe = sqrt(-E)-sqrt(E-V)*tan(a/h*sqrt(2*m*(E-V)))
feprime = diff(fe,E) 
fo = sqrt(E)+sqrt(E-V)*(1/(tan(a/h*sqrt(2*m*(E-V)))))
foprime = diff(fo,E)

Eeven = []
Eodd = []
feven = []
fodd = []
E0 = -1.9*10**-9
for i in range(0,5,1) : 
    x = E0 - (fe.subs(E,E0)/feprime.subs(E,E0))
    Eeven.append(x)
    feven.append(fe.subs(E,E0))
    E0 = x

for i in range(0,5,1) : 
    y = E0 - (fe.subs(E,E0)/feprime.subs(E,E0))
    Eodd.append(y)
    fodd.append(fe.subs(E,E0))
    E0 = y
#The implementation works but the values doesn't seem to convert and
#and I get i in my answers which prevent my from plotting it, no matter which values of E0 I tried.
