# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 20:49:32 2013

@author: ttran
"""
from pylab import *
from mpl_toolkits.mplot3d import Axes3D
B = array([[0.0,0.6,0.0]])
E = array([[0.0,0.0,15.0]])
q = -1.6*10**-19
m = 9.1*10**-31
v = array([[100.0,0.0,0.0]])
F = q*(E+cross(v,B))
a = F/m
r = array([[0.0,0.0,0.0]])
delta_t = 10**-13

#x = [0 for i in xrange(10)]
#y = [0 for i in xrange(10)]
t= arange(0,10**-9,delta_t)
timestep = []
for i in range(0,len(t)-1) :
    F = q*(E+cross(v,B))
    a = F/m
    r = vstack(( r , r[-1,:] + delta_t * v[-1,:] )) # add a row to 'r'
    v = vstack(( v , v[-1,:] + delta_t * a[-1,:] ))
    timestep.append(delta_t)
    
udrift = (min(r[:,0])-max(r[:,0]))/10**-9
print udrift
print cross(E,B)/norm(B)**2
fig = figure()
ax = fig.gca(projection='3d')
ax.plot(r[:,0],r[:,1],r[:,2],lw=2,label='numerical')
xlabel('x [m]')
ylabel('y [m]')
ax.legend()
ax.set_zlabel('z')
#grid('on')
#rcParams.update({'font.size': 20})
show()
    
