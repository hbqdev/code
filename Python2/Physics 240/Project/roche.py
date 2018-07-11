
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 22:43:40 2013

@author: ttran
"""
from __future__ import division
from pylab import *
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as ax

choice = input("Enter 1 for Earth-moon System\nEnter 2 for Algol Binary System\nEnter 3 for Alpha Centauri Binary System\nEnter 4 for Antares Binary System\nEnter 5 for user input :")
Msun = 2*10**30
au = 149597870700
if choice == 1 :
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
    contour(X,Y,-log(-v.T),300)
    xlabel("X (Meter)")
    ylabel("y (Meter)")
    title("Roche surface potential of Earth-Moon System")
    fig = plt.figure()
    p3 = ax.Axes3D(fig)
    p3.contour(X,Y,-log(-v),300)
    xlabel("X (Meter)")
    ylabel("y (Meter)")
    title("Roche surface potential of Earth-Moon System")

if choice == 2 :
    d = 149597870700*3
    M1 = 7.0*Msun
    M2 = 3.24*Msun
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
            #r2 = sqrt(x[i]**2+y[j]**2)
            r1 = sqrt((x[i])**2 + y[j]**2)
            r2 = sqrt((x[i]-d)**2 + y[j]**2)
            v[i,j] = -G*(M1/r1 + M2/r2) - 0.5*omegasq*(((x[i]-xc)**2+y[j]**2))
    
    
    X,Y = meshgrid(x,y)
    contour(X,Y,-log(-v.T),300)
    xlabel("X (Meter)")
    ylabel("y (Meter)")
    title("Roche surface potential of 2 Algol")
    fig = plt.figure()
    p3 = ax.Axes3D(fig)
    p3.contour(X,Y,-log(-v),300)
    xlabel("X (Meter)")
    ylabel("y (Meter)")
    title("Roche surface potential of 2 Algol")
    
if choice == 3:
    d = 149597870700*23
    M1 = 1.100*Msun
    M2 = 0.907*Msun
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
            #r2 = sqrt(x[i]**2+y[j]**2)
            r1 = sqrt((x[i])**2 + y[j]**2)
            r2 = sqrt((x[i]-d)**2 + y[j]**2)
            v[i,j] = -G*(M1/r1 + M2/r2) - 0.5*omegasq*(((x[i]-xc)**2+y[j]**2))
    X,Y = meshgrid(x,y)
    contour(X,Y,-log(-v.T),300)
    xlabel("X (Meter)")
    ylabel("y (Meter)")
    title("Roche surface potential of Alpha Centauri")
    fig = plt.figure()
    p3 = ax.Axes3D(fig)
    p3.contour(X,Y,-log(-v),300)
    xlabel("X (Meter)")
    ylabel("y (Meter)")
    title("Roche surface potential of Alpha Centauri")
    
if choice == 4:
    d = 149597870700*550
    M1 = 12.4*Msun
    M2 = 10.0*Msun
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
            #r2 = sqrt(x[i]**2+y[j]**2)
            r1 = sqrt((x[i])**2 + y[j]**2)
            r2 = sqrt((x[i]-d)**2 + y[j]**2)
            v[i,j] = -G*(M1/r1 + M2/r2) - 0.5*omegasq*(((x[i]-xc)**2+y[j]**2))
    X,Y = meshgrid(x,y)
    contour(X,Y,-log(-v.T),300)
    xlabel("X (Meter)")
    ylabel("y (Meter)")
    title("Roche surface potential of Antares")
    fig = plt.figure()
    p3 = ax.Axes3D(fig)
    p3.contour(X,Y,-log(-v),300)
    xlabel("X (Meter)")
    ylabel("y (Meter)")
    title("Roche surface potential of Antares")
    
if choice == 5:
    d = input("Enter the distance between 2 stars: ")
    d = d*au
    M1 = input("Enter the mass of Star 1 in kg: ")
    M1 = M1*Msun
    M2 = input("Enter the mass of Star 2 in kg: ")
    M2 = M2*Msun
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
            #r2 = sqrt(x[i]**2+y[j]**2)
            r1 = sqrt((x[i])**2 + y[j]**2)
            r2 = sqrt((x[i]-d)**2 + y[j]**2)
            v[i,j] = -G*(M1/r1 + M2/r2) - 0.5*omegasq*(((x[i]-xc)**2+y[j]**2))
    X,Y = meshgrid(x,y)
    contour(X,Y,-log(-v.T),300)
    xlabel("X (Meter)")
    ylabel("y (Meter)")
    title("Roche surface potential of 2 binary stars")
    fig = plt.figure()
    p3 = ax.Axes3D(fig)
    p3.contour(X,Y,-log(-v),300)
    xlabel("X (Meter)")
    ylabel("y (Meter)")
    title("Roche surface potential of 2 binary stars")
show()

