# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 00:01:40 2013

@author: ttran
"""
from pylab import *
v0 = 15
theta0 = 45

max_steps = 1e4
m = 0.15 # mass in kg
g = 9.8 # m/s^2
delta_t = 0.1 # timestep in sec, initial guess

r0 = [0.0,]    # x is r[0], y is r[1]
v0 = [sin(pi/4)*vi,cos(pi/4)*vi]  # vx is v[0], vy is v[1]
a = [0,-g]
t = 0.0               # time in sec
step = 0
t_plot = []
x_plot = []
y_plot = []

r = r0+v0*t+0.5*a*t**2

    #print step
    #print r
    #print x_plot

plot(t_plot,y_plot)

    

show()

    
