# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 23:48:21 2013

@author: ttran
"""

# dftcs.py : use FTCS method to solve 1-D diffusion equation

from pylab import *
from mpl_toolkits.mplot3d import Axes3D

kappa, L = 1.0, 1.0 # diffusion coefficient, bar length
N_x, N_t = 101, 800 # number of space and time grid-points; keep N_x odd
Dx = L / (N_x-1)    # x grid spacing 
#Dt = Dx**2 / kappa / 1.85  # t grid spacing from natural scales: unstable
#Dt = Dx**2 / kappa / 2.00  # t grid spacing from natural scales: borderline
Dt = Dx**2 / kappa / 3.0  # t grid spacing from natural scales: stable
clevels=arange(0.5,10.5,0.5)
clabels=arange(1,11,1)

T = zeros((N_x,N_t))  # initialize temperature matrix

# initial conditions (center of bar has temperature spike):

T[3*N_x/4,0] = 1.0/Dx

x = arange(-L/2,L/2+Dx,Dx)
t = arange(0,Dt*N_t,Dt)
#T[x,0] = kappa*(x-L/4.0)


for n in range(N_t-1) :
    T[1,n] = T [2,n]
    T[0,n] = T[N_x-1,n] # boundary conditions that we won't use
    for i in range(1,N_x-1) :
        T[i,n+1] = T[i,n] + kappa*Dt/Dx**2 \
                   * (T[i+1,n]+T[i-1,n]-2*T[i,n])

fig1=figure(figsize=(10.5,7))
loglog(t,T[N_x/2,:],label='$x=0$')
loglog(t,T[N_x*3/4,:],label='$x=L/4$')
legend(loc='best')
xlabel('$t$')
ylabel('$T(t)$')
rcParams.update({'font.size': 20})

fig2=figure(figsize=(10.5,7))
plot(x,T[:,N_t/20],label='$t=t_\mathrm{fin}/20$')
plot(x,T[:,N_t/4],label='$t=t_\mathrm{fin}/4$')
plot(x,T[:,N_t/2],label='$t=t_\mathrm{fin}/2$')
plot(x,T[:,-1],label='$t=t_\mathrm{fin}$')
legend(loc='best')
xlabel('$x$')
ylabel('$T(x)$')
    
fig3=figure(figsize=(10.5,7))
con=contour(t,x,T,clevels)
clabel(con,clabels,fmt='%d')
xlabel('$t$')
ylabel('$x$')
title('$T(x,t)$')
grid('on')

fig4=figure(figsize=(10.5,7))
ax = fig4.gca(projection='3d')
tt,xx=meshgrid(t,x)
#ax.plot_wireframe(tt,xx,T,rstride=4,cstride=20)
ax.plot_surface(tt,xx,T,rstride=4,cstride=20,cmap=cm.coolwarm)
xlabel('$t$')
ylabel('$x$')
ax.set_zlabel('$T(x,t)$')
title('thermal diffusion of delta function')
show()

