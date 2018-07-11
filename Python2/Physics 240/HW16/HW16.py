# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 00:01:23 2013

@author: ttran
"""
from pylab import *
answer = raw_input('What fucntion(a,b,c,d?), Enter Q to quit: ')
while answer != 'Q' :
    Ndata = input ('Number of data points?' )
    frq = input ('Frequency? ')
    N,Dt = Ndata, 1.0
    # sine wave parameters
    fs,phis=frq,0.0
    thetaj = 2.0*pi*fs*Dt
    if answer == 'a':
    #fs,phis=0.2,pi/2.0
    #fs,phis=0.2123,0.0
    #fs,phis=0.8,0
        # create sine wave data set, N data points
        t=arange(0,N,pi/10.0)
        y=(thetaj/(2.0*pi))*(t%(2.0*pi))
        econst = -2.0*pi*1j/Dt/N
    # compute Fourier transform
        Y = zeros(N)*(0.0+0.0j)
        f = zeros(N)
        for k in range(N) :
            Y[k] = sum(y*exp(econst*t*k))
            f[k] = k / (N*Dt)
        P = abs(Y)**2
    if answer == 'b' :
        y=[]
        t=arange(0,N,pi/10.0)
        for i in range(len(t)) :
            if 0 <= thetaj*(t[i]%(2.0*pi)) <= pi :
                y.append(1)
            else :
                y.append(-1)
        econst = -2.0*pi*1j/Dt/N
        # compute Fourier transform
        Y = zeros(N)*(0.0+0.0j)
        f = zeros(N)
        for k in range(N) :
            Y[k] = sum(y*exp(econst*t*k))
            f[k] = k / (N*Dt)
        P = abs(Y)**2
    if answer == 'c' :
        y=[]
        t=arange(0,N,pi/12)
        for i in range(len(t)) :
            if 0 <= thetaj*(t[i]%(2.0*pi)) <= pi :
                y.append(1)
            else :
                y.append(0)
        econst = -2.0*pi*1j/Dt/N
        # compute Fourier transform
        Y = zeros(N)*(0.0+0.0j)
        f = zeros(N)
        for k in range(N) :
            Y[k] = sum(y*exp(econst*t*k))
            f[k] = k / (N*Dt)
        P = abs(Y)**2
    if answer == 'd' :
        y=[]
        t=arange(0,N,pi)
        for i in range(len(t)) :
            if 0 <= thetaj*(t[i]%(2.0*pi)) <= pi :
                y.append(thetaj/pi)
            else :
                y.append((2.0*pi-thetaj)/pi)
        econst = -2.0*pi*1j/Dt/N
        # compute Fourier transform
        Y = zeros(N)*(0.0+0.0j)
        f = zeros(N)
        for k in range(N) :
            Y[k] = sum(y*exp(econst*t*k))
            f[k] = k / (N*Dt)
        P = abs(Y)**2
                
    fig1=figure(figsize=(9,7))
    plot(t,y,'--o')
    xlabel('$t$')
    ylabel('$y$')
    rcParams.update({'font.size': 20})
    grid('on')
                
    fig2=figure(figsize=(9,7))
    plot(f,real(Y),'-o',label='$Re(Y)$')
    plot(f,imag(Y),'--o',label='$Im(Y)$')
    xlabel('$f$')
    ylabel('$Y$')
    legend(loc='best')
    grid('on')
    
    fig3=figure(figsize=(9,7))
    plot(f,P,'-o')
    xlabel('$f$')
    ylabel('$P$')
    grid('on')
    answer = raw_input('What fucntion(a,b,c,d?), Enter Q to quit: ')
show()
