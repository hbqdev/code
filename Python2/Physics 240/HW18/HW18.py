# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 20:06:13 2013

@author: ttran
"""
from __future__ import division
# advect.py : advection of cosine-modulated Gaussian pulse

from pylab import *
from mpl_toolkits.mplot3d import Axes3D

N_x = 100 
sig, L, c = 0.1, 400.0, 1.0
k = pi / sig
Dx = L / N_x
tc = Dx / c  # Courant time-step
Dt = tc * 1.0
N_t = L / (Dt * c) # one cycle
coeff = tc/(2*Dx)
coeffflw = tc**2/(2*Dx**2)
v_max = 65

rho_max = 1.0
Flow_max = 0.25*rho_max*v_max
rho = zeros(N_x)
for i in range(int(N_x/4),int(N_x/2-1)) :
    rho[i] = rho_max

i = arange(0,N_x)
n = arange(0,int(N_t))
x = (i+0.5)*Dx - L/2
t = Dt * n
a = zeros((N_x,N_t))

# set up plus and minus indices
ip = i+1
ip[N_x-1] = 0
im = i-1
im[0] = N_x-1

# set up initial conditions:

a[:,0] = rho*(v_max*(1-rho/rho_max))

method = input('Choose a method: FTCS (1), Lax (2), Lax-Wendroff(3) ? ')

for nn in range(int(N_t)-1) :
    if method == 1 : # FTCS
        a[:,nn+1] = a[:,nn] - coeff * (a[ip,nn] - a[im,nn])
        method_txt = 'FTCS'
    elif method == 2 : # Lax
        a[:,nn+1] = 0.5 * (a[ip,nn]+a[im,nn]) - coeff * (a[ip,nn] - a[im,nn])
        method_txt = 'Lax'
    elif method == 3 : # Lax-Wendroff
        a[:,nn+1] = a[:,nn] - coeff * (a[ip,nn] - a[im,nn]) + \
                    2.0*coeff**2*(a[ip,nn] + a[im,nn] - 2.0*a[:,nn])
        method_txt = 'Lax-Wendroff'
#   for ii in i :   # inefficient!
#        a[ii,nn+1] = a[ii,nn] - coeff * (a[ip[ii],nn] - a[im[ii],nn])

fig1=figure(figsize=(10,7))
plot(x,a[:,0],label='initial')
plot(x,a[:,-1],'--',label='final')
legend(loc='best')
xlabel('$x$')
ylabel('$a(x)$')
grid('on')
title_text = 'advection of pulse, $\Delta t / t_\mathrm{c}$ = '
title_text += str(Dt/tc)

title_text += ', ' + method_txt
title(title_text)
rcParams.update({'font.size': 20})

fig2=figure(figsize=(10,7))
ax = fig2.gca(projection='3d')
X,T=meshgrid(x,t)
ax.plot_surface(X,T,a.T,rstride=5,cstride=5,cmap=cm.pink)
xlabel('$x$')
ylabel('$t$')
ax.set_zlabel('$a(x,t)$')
title(title_text)

#fig3=figure(figsize=(10,7))
#con=contour(t,x,a)
##clabel(con,clabels,fmt='%d')
#xlabel('$t$')
#ylabel('$x$')
#title('$T(x,t)$')
#grid('on')
show()

    



