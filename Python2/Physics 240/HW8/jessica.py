# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 00:12:15 2013

@author: ttran
"""

#orbit.py calculates and plot the trajectory using orbital elements using adaptive time step
from pylab import *
from mpl_toolkits.mplot3d import Axes3D

#input parameters



def rk4(x,t,delta_t,derivs,param) :
    #rk4 program needed eventually for adaptive time steps
    dt2 = delta_t/2.0
    F1=derivs(x,t,param)
    F2=derivs(x+F1*dt2,t+dt2,param)
    F3=derivs(x+F2*dt2,t+dt2,param)
    F4=derivs(x+F3*delta_t,t+delta_t,param)
    x=x+(F1+2.0*(F2+F3)+F4)*delta_t/6.0
    return x
    
def rka(x,t,delta_t,derivs,param,epsi) :
#adaptive time step function
    S1, S2 = (0.9, 4.0)     # safety factors
    epsstar = Inf           # initialize error
    N_iter, N_max = (0, 100)
    while epsstar > epsi and N_iter < N_max :
        # take big, trial step
        xb = rk4(x,t,delta_t,derivs,param)
        # take two small, trial steps
        xhalf = rk4(x,t,delta_t/2.0,derivs,param)
        xs = rk4(xhalf,t,delta_t/2.0,derivs,param)
        # compute estimated truncation error
        epsstar = abs(xb-xs)   # look for maximum error among coordinates
        epsstar = max(epsstar.flatten()) # convert array to vector if necessary
        # estimate new timestep (including safety factors)
        dtstar = delta_t * abs(epsi/epsstar)**0.2
        dtstar *= S1
        if dtstar > S2*delta_t :
            delta_t *= S2
        elif dtstar < delta_t / S2 :
            delta_t /= S2
        else :
            delta_t = dtstar
        N_iter += 1
    if N_iter == N_max :
        print('Warning: adaptive RK4 routine did not converge.')
    x = xs
    t += delta_t
    return x,t,delta_t

def g_derivs(x,t,params) :  # specific function for derivatives
    pos = x[0,0:3]
    v = x[0,3:6]
    a = -GM*pos/norm(pos)**3
    derivs = hstack((v,a))
    return derivs


incl = 12.4
incl = incl*pi/180. #converting to rads
semi = .389/(1.-.847)
ecc = .847
GM = 1.


r = array([[0.,(semi-semi*ecc)*cos(incl),(semi-semi*ecc)*sin(incl)]]) #position x,y,z, at periapsis

radius=array([[norm(r)]])
v = array([[(2./radius[0,0]-1./semi)**.5,0.,0.]]) #right hand rule and velocity at periapsis
print v
t = array([[0.]])
T=2.*pi*(semi**3)**.5
steps = 1000
delta_t = T / steps
coords = hstack((r,v))


delta_t_set = array([[delta_t]]) # set up timestep array for adaptive method


epsi = .0001 #desired fractional accuracy

for i in range(steps):
    coords, t_new, delta_t = rka(coords,t[-1],delta_t,g_derivs,GM,epsi)
    r_new = coords[0,0:3]
    v_new = coords[0,3:6]
    v = vstack((v, v_new))
    r = vstack((r, r_new))
    radius = vstack((radius, norm(r_new)))
    t = vstack((t,t[-1]+delta_t))

x = r[:,0]
y = r[:,1]
z = r[:,2]



fig = figure()
ax = Axes3D(fig) #using this because i have an older version of matplotlib (need to update)
ax.plot(x,y,z)
#grid('on')
show()