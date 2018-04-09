# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 01:14:42 2013

@author: ttran
"""

from pylab import *
from mpl_toolkits.mplot3d import Axes3D

e = loadtxt('earth')
c = loadtxt('comet')

fig = figure('Earth and Comet',figsize=(5,5))    # size hard-wired to fit MacBook Air screen
ax = fig.gca(projection='3d')
ax.plot(e[:,0],e[:,1],e[:,2],label = 'Earth')
ax.plot(c[:,0],c[:,1],c[:,2],label = 'Comet')
xlabel('x')
ylabel('y')
legend()
show()