from __future__ import division
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  3 20:13:51 2013

@author: ttran
"""
from pylab import *
p1 = figure('Original Model')
#for x = 10
x = 10.0
s = 0
error = []
nfact = arange(0,61)
for n in nfact :
    s += x**n/math.factorial(n)
    error.append((abs(s-e**x))/e**x)
p1 = subplot(2,2,1)
plot(nfact,error)
xlabel('N')
ylabel('Absolute fractional Error')
title('X = 10')
text(27.5,0.60,'e^x value')
text(25,0.5,s)

#for x = 2
x = 2.0
s = 0
error = []
nfact = arange(0,61)
for n in nfact :
    s += x**n/math.factorial(n)
    error.append((abs(s-e**x))/e**x)
p1 = subplot(2,2,2)
plot(nfact,error)
xlabel('N')
ylabel('Absolute fractional Error')
title('X = 2')
text(27.5,0.60,'e^x value')
text(25,0.5,s)

#for x = -2
x = -2.0
s = 0
error = []
nfact = arange(0,61)
for n in nfact :
    s += x**n/math.factorial(n)
    error.append((abs(s-e**x))/e**x)
p1 = subplot(2,2,3)
plot(nfact,error)
xlabel('N')
ylabel('Absolute fractional Error')
title('X = -2')
text(27.5,6,'e^x value')
text(25,5,s)

#for x = -10
x = -10.0
s = 0
error = []
nfact = arange(0,61)
for n in nfact :
    s += x**n/math.factorial(n)
    error.append((abs(s-e**x))/e**x)
p1 = subplot(2,2,4)
plot(nfact,error)
xlabel('N')
ylabel('Absolute fractional Error')
title('X = -10')
text(25,25000000,'e^x value')
text(22,20000000,s)

#new model
p2 = figure('Modified Model')
x = -2.0
s = 0
sn = 0
error = []
nfact = arange(0,61)
x = -x
for n in nfact :
    s += x**n/math.factorial(n)
    sn = 1/s
    error.append(abs(sn-e**-x)/e**-x)
p2 = subplot(2,1,1)
plot(nfact,error)
xlabel('N')
ylabel('Absolute fractional Error')
title('X = -2')
text(25,5,'e^x value')
text(22,4,sn)
print sn

#for x = -10
x = -10.0
s = 0
sn = 0
error = []
nfact = arange(0,61)
x = -x
for n in nfact :
    s += x**n/math.factorial(n)
    sn = 1/s
    error.append(abs(sn-e**-x)/e**-x)
p2 = subplot(2,1,2)
plot(nfact,error)
xlabel('N')
ylabel('Absolute fractional Error')
title('X = -10')
text(25,20000,'e^x value')
text(22,15000,sn)
print sn

#text(27.5,6,'e^x value')
#text(25,5,s)
show()

