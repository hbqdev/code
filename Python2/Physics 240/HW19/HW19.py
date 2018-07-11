# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 13:52:51 2013

@author: ttran
"""

from pylab import *
from mpl_toolkits.mplot3d import Axes3D

Lx, Ly, Phi0 = 1.0, 1.0, 1.0
Dx, Dy = 0.02, 0.02
nmax = 21

x = arange(0,Lx+Dx,Dx)
y = arange(0,Ly+Dy,Dy)
Phi = zeros((len(x),len(y)))

def Phi_anal(x,y,nmax,Phi0,Lx,Ly) : # analytic potential
    Phi = 0.02
    for n in range(1,nmax,2) : # odd values of n
            Phi += sin(n*pi*x/Lx)*sinh(n*pi*y/Lx) \
                / sinh(n*pi*Ly/Lx) / n
    Phi *= 4.0*Phi0/pi
    return Phi

option = input('Analytic (1) or numerical (2) solution? ')

title_text = 'Electrostatic potential $\Phi(x,y)$: '
if option == 1 : # analytic
    title_text += 'analytic, $n_\mathrm{max}$=%d' % (nmax)
    for i in range(len(x)) :
        Phi[i,:] = Phi_anal(x[i],y,nmax,Phi0,Lx,Ly)
#elif option == 2 : # numerical : not finished yet
#    Phi[:,-1] = Phi0 # boundary conditions
#    for n in range(N_t) :
        
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
ax.plot_surface(X,Y,Phi.T,rstride=1,cstride=1,cmap=cm.jet)
xlabel('$x$')
ylabel('$y$')
ax.set_zlabel('$\Phi(x,y)$')
title(title_text)
show()
