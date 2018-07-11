# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 10:34:55 2013

@author: ttran
"""
from pylab import *

nstep = 1000
m = 0.5
I = 10**-4
k = 5.0
delta = 10**-3
epsilon = 10**-2
T = sqrt(m/k)*2*pi*45
r = array([[0.0,10.0,0.0,0.0]])
delta_t = T/nstep
coordsz = hstack((z,v))
coordstheta = hstack((theta,thetav))
t = ([0.0])

def rk4(x,t,delta_t,derivs,param) :
    dt2 = delta_t/2.0
    F1=derivs(x,t,param)
    F2=derivs(x+F1*dt2,t+dt2,param)
    F3=derivs(x+F2*dt2,t+dt2,param)
    F4=derivs(x+F3*delta_t,t+delta_t,param)
    x=x+(F1+2.0*(F2+F3)+F4)*delta_t/6.0
    return x
    
def zderiv(coordsz,t,theta) :
    r = x[0,0:3]
    v = coordsz[1]
    a =atheta = array([[-(k*z + epsilon*z*theta)/m, -(delta*theta + 1/2*epsilon*z)/I ]])
    derivs = hstack((v,a))
    return derivs

for i in range (0,1000) :
    a = -(k*z[-1] + epsilon*z[-1]*theta[-1])/m
    atheta = -(delta*theta[-1] + 1/2*epsilon*z[-1])
    coordsz = rk4(coordsz,t,delta_t,zderiv,theta[-1])
    coordstheta = rk4(coordstheta,t,delta_t,thetaderiv,z[-1])
    z_new = coordsz[0]
    v_new = coordsz[1]
    theta_new = coordstheta[0]
    thetav_new = coordstheta[1]
    z = vstack((z,z_new))
    v = vstack((v,v_new))
    theta = vstack((theta,theta_new))
    thetav = vstack((thetav,thetav_new))
    t = vstack((t,t[-1]+delta_t))
plot(z,theta)
show()
#this is the best I can do for now. I started on this homework late 
#didn't have enough time to finish