# lorenz.py : ODE Lorenz model

# helps with mistaken integer arithmetic
from __future__ import division

from pylab import *
from mpl_toolkits.mplot3d import Axes3D
from ode import rk4,rka
from time import time, clock
def l_derivs(r,t,params) :
    x = r[0]
    y = r[1]
    z = r[2]
    sigma = params[0,0]
    b = params[0,1]
    R = params[0,2]
    dx = sigma*(y-x)
    dy = R*x - y - x*z
    dz = x*y - b*z
    derivs = hstack((dx,dy,dz))
    return derivs

sigma, b, R = 10.0, 8.0/3.0, 28.0
params = array([[sigma, b, R]])
val_init = r1 = array([[1.0,1.0,20.0]])
r2 = array([[1.0,1.0,20.01]])
t1 = array([[0.0]]) # note the two curves need their own time arrays
t2 = array([[0.0]]) #   because timesteps will be different !
steps = input('how many timesteps? ')
epsi = input('how accurate? ')
dt_min = Inf
delta_t1 = 0.001 # mistake earlier to use fixed delta_t as input to 'rka'
delta_t2 = 0.001

for i in range(steps) :
    coords, t_new, delta_t1 = rka(r1[-1],t1[-1],delta_t1,l_derivs,params,epsi)
    if delta_t1 < dt_min :
        dt_min = delta_t1
    r1 = vstack((r1, coords))
    t1 = vstack((t1, t_new)) 
    coords, t_new, delta_t2 = rka(r2[-1],t2[-1],delta_t2,l_derivs,params,epsi)
    r2 = vstack((r2, coords))
    t2 = vstack((t2, t_new)) 

fig1 = figure()
plot(t1,r1[:,0],label='$z_0=20$')
plot(t2,r2[:,0],label='$z_0=20.01$')
xlabel('$t$',fontsize=25)
ylabel('$x$',fontsize=25)
legend(loc='best')
title('Lorenz model time series')

fig2 = figure()
ax = fig2.gca(projection='3d')
ax.plot(r1[:,0],r1[:,1],r1[:,2],label='$z_0=20$')
ax.plot(r2[:,0],r2[:,1],r2[:,2],label='$z_0=20.01$')
xlabel('$x$',fontsize=25)
ylabel('$y$',fontsize=25)
ax.set_zlabel('$z$',fontsize=25)
# steady-state points : 
ss = array([[0,0,0],[sqrt(b*(R-1.0)),sqrt(b*(R-1.0)),R-1.0], \
            [-sqrt(b*(R-1.0)),-sqrt(b*(R-1.0)),R-1.0]])
ax.plot(ss[:,0],ss[:,1],ss[:,2],'*')
ax.plot(val_init[:,0],val_init[:,1],val_init[:,2],'o') # initial value
legend(loc='best')
title('Lorenz model phase space')
print clock()
show()




          

