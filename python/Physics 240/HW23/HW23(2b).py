# -*- coding: utf-8 -*-
"""
Created on Fri May 10 17:25:23 2013

@author: ttran
"""

from pylab import *
import scipy
import scipy.fftpack
#Generating white noise
#for i in range(0,4) :
#    np.random.seed(i)    
#    t = np.random.normal(0,1,1024)
#    FFT = scipy.fft(t)
#    fig = figure()
#    plot(np.abs(FFT)**2)

fs,phis=0.8,0.0
A = input("Enter the value fo the amplitude: ")
t1 = np.random.normal(0,1,20)
FFT = scipy.fft(t1)
#ts = arange(0,20,1)
#x = A*sin(ts)
ts=arange(0,20,1)
x=A*sin(2.0*pi*fs*ts+phis)
xFFT = scipy.fft(x)
series = FFT + xFFT
fig = figure()
power = abs(FFT+xFFT)**2
plot(power)
title("The power Spectrum")

fig = figure()
plot(series)

show()