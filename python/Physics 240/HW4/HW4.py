from __future__ import division
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 20:24:54 2013

@author: ttran
"""

# balle.py : calculate trajectory of a baseball

from pylab import *


# initial conditions and constants:

#v0 = input('v0=? ')
#theta0 = input('theta0=? ')
air = raw_input('Air Resistance? Enter yes or no: ')
if air == 'no' :
    v0 = input('v0?: ')
    theta0 = input('theta0?: ')
    delta_t = input('delta_t?: ')
    max_steps = 1e4
    m = 0.15 # mass in kg
    g = 9.8 # m/s^2
    # timestep in sec, initial guess

    r = array([0.0,0.0])    # x is r[0], y is r[1]
    v = array([v0*cos(theta0),v0*sin(theta0)])  # vx is v[0], vy is v[1]
    a = array([0.0,-g])   
    t = 0.0               # time in sec
    step = 0
    t_plot = []
    x_plot = []
    y_plot = []

    while r[1] >= 0 and step < max_steps :
        t_plot.append(t)
        x_plot.append(r[0])
        y_plot.append(r[1])
        r += v * delta_t
        v += a * delta_t
        t += delta_t
        step += 1

    plot(t_plot,y_plot,label="Numerical")
    print 'Numerical range is: ', v0*cos(theta0)*t
    print 'Numerical Flight time is: ', t
    ymaxn = max(y_plot)

    max_steps = 1e4
    m = 0.15 # mass in kg
    g = 9.8 # m/s^2
    step = 0
    t_plot = []
    x_plot = []
    y_plot = []
    r = array([0.0,0.0])    # x is r[0], y is r[1]
    rt = array([0.0,0.0])
    v = array([v0*cos(theta0),v0*sin(theta0)])  # vx is v[0], vy is v[1]
    a = array([0.0,-g]) 
    tn = 0
    
    while rt[1] >= 0 and step < max_steps :
        t_plot.append(tn)
        rt = r + v*tn + 0.5*a*tn**2
        x_plot.append(rt[0])
        y_plot.append(rt[1])
        tn += delta_t
        step += 1
    #print x_plot
    xlabel("Time(seconds)")
    ylabel('Vertical Displacement(meter)')
    title('Trajectory vs Time')
    ylim(0,10)
    plot(t_plot,y_plot,label="Analytical")
    print 'Analytical range is: ', v0*cos(theta0)*tn
    print 'Analytical Flight time is: ', tn
    
    

#while ry >= 0 and step < max_steps :
 #   ry += vy0*delta_t - 1/2*g*delta_t**2
  #  step += 1
    #print delta_t
    ymaxa = max(y_plot)
    error = abs (ymaxn - ymaxa)
    print error
    legend()
    show()
    
if air == 'yes' : 
    v0 = input('v0?: ')
    theta0 = input('theta0?: ')

    max_steps = 1e4
    m = 0.15 # mass in kg
    g = 9.8 # m/s^2
    delta_t = input('delta_t?: ') # timestep in sec, initial guess

    r = array([0.0,0.0])    # x is r[0], y is r[1]
    v = array([v0*cos(theta0),v0*sin(theta0)])  # vx is v[0], vy is v[1]
    a = array([0.0,-g])   
    t = 0.0               # time in sec
    step = 0
    t_plot = []
    x_plot = []
    y_plot = []

    while r[1] >= 0 and step < max_steps :
        t_plot.append(t)
        x_plot.append(r[0])
        y_plot.append(r[1])
        r += v * delta_t
        v += a * delta_t
        t += delta_t
        step += 1
    #print step
    #print r
    #print x_plot

    plot(t_plot,y_plot,label="Numerical with air resistance")
    print 'Numerical range with air resistance is: ', v0*cos(theta0)*t
    print 'Numerical Flight time with air resistance is: ', t
    
    
    t_plot = []
    x_plot = []
    y_plot = []
    r = array([0.0,0.0])    # x is r[0], y is r[1]
    rt = array([0.0,0.0])
    v = array([v0*cos(theta0),v0*sin(theta0)])  # vx is v[0], vy is v[1]
    a = array([0.0,-g]) 
    tn = 0
    
    while rt[1] >= 0 and step < max_steps :
        t_plot.append(tn)
        rt = r + v*tn + 0.5*a*tn**2        
        y_plot.append(rt[1])
        tn += delta_t
        step += 1
    xlabel("Time(seconds)")
    ylabel('Vertical Displacement(meter)')
    title('Trajectory vs Time')
    plot(t_plot,y_plot,label="Analytical without air resistance")
    print 'Analytical range is: ', v0*cos(theta0)*tn
    print 'Analytical Flight time is: ', tn
    legend()
    show()
else : 
    print 'incorrect value, please try again'
    
    
