# -*- coding: utf-8 -*-
"""
Created on Sat May 18 13:21:07 2013

@author: ttran
"""
from __future__ import division
from pylab import *
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as ax

#d = 384400000
#xc = 46300000
#G = 6.67384*10**-11
#delta = d/100
#x = arange(-2*d, 2*d,delta)
#y = arange(-2*d, 2*d,delta)
#v = zeros((len(x),len(y)))
#M1 = 5.972*10**24
#M2 = 7.35*10**23
#a = xc
#b = -(d-xc)
##T = pi * a**(3/2) * sqrt(2/(G*(M1+M2)))
##T = 27.3*24*3600
#omegasq = G*(M1+M2)/(d)**3
##omegasq = (2*pi/T)**2
##omegasq = (2.66*10**-6)*2 
##omegasq = 0.0
#r1 = 0
#r2 = 0
#
#for i in range(len(x)) :
#    for j in range(len(y)) :
#        #r2 = sqrt(x[i]**2+y[j]**2)
#        r1 = sqrt((x[i])**2 + y[j]**2)
#        r2 = sqrt((x[i]-d)**2 + y[j]**2)
#        v[i,j] = -G*(M1/r1 + M2/r2) - 0.5*omegasq*(((x[i]-xc)**2+y[j]**2))
#
#
#X,Y = meshgrid(x,y)
#
#fig = plt.figure()
#
#p3 = ax.Axes3D(fig)
#p3.contour(X,Y,-log(-v),300)

#contour(X,Y,v3d.T,1003),:],
#contour(x,y,v2,50)

d = 406300000
M1 = 5.972*10**24
M2 = 7.35*10**22.5
xc = d*(M2/(M1+M2))
G = 6.67384*10**-11
delta = d/100
x = arange(-2*d, 2*d,delta)
y = arange(-2*d, 2*d,delta)
v = zeros((len(x),len(y)))
omegasq = G*(M1+M2)/(d)**3
r1 = 0
r2 = 0

for i in range(len(x)) :
    for j in range(len(y)) :
        r1 = sqrt((x[i])**2 + y[j]**2)
        r2 = sqrt((x[i]-d)**2 + y[j]**2)
        v[i,j] = -G*(M1/r1 + M2/r2) - 0.5*omegasq*(((x[i]-xc)**2+y[j]**2))
X,Y = meshgrid(x,y)
fig = plt.figure()
p3 = ax.Axes3D(fig)
p3.plot_surface(v,x,y, rstride=4, cstride=10, color='b')

show()


