# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 20:48:36 2013

@author: ttran
"""

from pylab import *
stop = input ('Enter 0 to quit, 1 to continue: ')
while stop != 0 :
    starttheta = input('Starting angle?in degree: ')
    startperiod = input('Enter period value: ' )
    startamp = input('Enter amplitude value: ')
    L = input('Enter length: ')
    
    g = 9.8
    starttheta = radians(starttheta)
    startomega = 0.0
    delta_t = startperiod/100
    
    theta=[]
    omega=[]        
    theta.append(starttheta)
    omega.append(startomega)
    time = arange(0.0,10.0*pi,delta_t)
    i = 0
    
    for t in time :
        ad = startamp*sin((2*pi*t)/startperiod)
        alpha = -((g+ad)/L)*sin(theta[i])
        theta.append(theta[i] + omega[i]* delta_t)
        omega.append(omega[i] + alpha * delta_t)
        i = i + 1
        if i == len(time)-1 :
            break
    theta = degrees(theta)
    theta_check = degrees(starttheta * cos(time))
    
    plot(time,theta,label='numerical'+ ' ' + str(degrees(starttheta)) + ' ' + 'degree')
    if degrees(starttheta) < 15.0 : # small angle approximation valid 
        plot(time,theta_check,label='analytic' + ' ' + str(degrees(starttheta)) + ' ' + 'degree')
    if degrees(starttheta) == 180 : # small angle approximation valid 
        plot(time,theta_check,'o',label='analytic' + ' ' + str(degrees(starttheta)) + ' ' + 'degree')
    legend()
    xlabel('t')
    ylabel('theta [deg]')
    grid('on')
    stop = input ('Enter 0 to quit, 1 to continue: ')
#rcParams.update({'font.size': 20})
show()
    
    
