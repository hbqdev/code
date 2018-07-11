# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 14:21:04 2013

@author: ttran
"""

# relax.py : solution of electrostatic problem (Laplace's equation)

from pylab import *
from mpl_toolkits.mplot3d import Axes3D

Nx = 60
Ny = 60
Lx, Ly, Phi0 = 1.0, 1.0, 1.0
Dx, Dy = 0.02, 0.02
nmax = 60
x = arange(0,Lx+Dx,Dx)
y = arange(0,Ly+Dy,Dy)
Phi = zeros((len(x),len(y)))
#Phi = Phi0 * 4/(pi*sinh(pi)) * sin(pi*x/Lx) * sinh(pi*y/Ly)
newphi = Phi
omega = 2.0/(1.0+sin(pi/Nx))
Phi[1,:] = 0
Phi[0,:] = 100
Phi[:,1] = 0


title_text = 'Electrostatic potential $\Phi(x,y)$: '
for n in range(1,nmax) :
    changesum = 0
    for i in range(2,Nx-1):
        for j in range(2,Ny-1) :
            newphi = 0.25*omega*(Phi[i+1,j] + Phi[i-1,j] + Phi[i,j-1] + Phi[i,j+1])+(1-omega)*Phi[i,j]
            changesum = changesum + abs(1-Phi[i,j]/newphi)
            Phi = newphi

fig1=figure(figsize=(9,7))
clevels=arange(0.1,1.0,0.1)
clabels=arange(0.1,1.0,0.1)
con=contour(x,y,Phi.T,clevels)
clabel(con,clabels,fmt='%.1g')
xlabel('$x$')
ylabel('$y$')
title(title_text)
rcParams.update({'font.size': 20})

fig2=figure(figsize=(9,7))
ax = fig2.gca(projection='3d')
X,Y=meshgrid(x,y)
ax.plot_surface(X,Y,Phi.T,rstride=0.5,cstride=0.5,cmap=cm.jet)
xlabel('$x$')
ylabel('$y$')
ax.set_zlabel('$\Phi(x,y)$')
title(title_text)
show()
