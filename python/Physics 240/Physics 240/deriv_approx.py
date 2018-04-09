# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 17:46:46 2013

@author: ttran
"""

from pylab import *

error_list=[]
h_list= []
x=1
df_true = 2*x
h = 0.1

for i in range(10) :
    df_approx = ((x+h)*2 - x**2)/h
    error = df_approx / df_true - 1
    error_list.append(error)
    h_list.append(h)
    h /= 10
    print "error", error

x = 2
x1 = pi/12
x2 = pi/2
y1 = x1 *a - (x1 * a)**3 /6
    