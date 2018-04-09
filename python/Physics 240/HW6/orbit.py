# orbit.py : simulate a Keplerian orbit

from pylab import *

v_frac = input('v_init / v_circ ? ')
step = input('time steps per orbit? ')
method = -1
while method != 1 and method != 2 :
    method = input('method? (1: Euler, 2: Euler-Cromer) ')
    
# set initial conditions and constants

m = 1.0
GM = 1.0

r=array([[1.0,0.0]])
a=array([[-1.0,0.0]])
radius=array([[norm(r)]])
v_c = sqrt(GM/radius)    # circular velocity
T = 2.0 * pi * radius / v_c     # very approximate period
delta_t = T / step
v=array([[0.0,v_c*v_frac]])
K=array([[v[-1,-1]**2+v[-1,-2]**2]])
t=array([[0.0]])

for i in range(0,1000) :
    a = -GM * r[-1] / (norm(r[-1]))**3
    if method == 1 : # Euler
        r_new = r[-1] + delta_t * v[-1]
        v_new = v[-1] + delta_t * a
        v = vstack((v, v_new))
    else :  # Euler-Cromer
        v_new = v[-1] + delta_t * a
        v = vstack((v, v_new))
        r_new = r[-1] + delta_t * v[-1]
    r = vstack((r, r_new))
    radius = vstack((radius, norm(r_new)))
    K = vstack((K, v[-1,-1]**2 + v[-1,-2]**2))
    t = vstack((t,t[-1]+delta_t))

#maxlim=abs(r).max()
theta=arctan2(r[:,1],r[:,0]) # note math.atan2 can't handle arrays
K = K * m / 2.0
U = -GM*m/radius
E = K + U

figure()
subplot(1,2,1,polar=True)
plot(theta,radius)
grid('on')
subplot(1,2,2)
plot(t,E,label='Total')
plot(t,K,'-.',lw=2,label='Kinetic')
plot(t,U,'--',lw=2,label='Potential')        
legend(loc='best')
xlabel('t')
ylabel('Energy')
if method == 1 :
    title_text = 'Euler, v_init = %.2f , dt = %.3f ' % (v_frac,delta_t)
else :
    title_text = 'Euler-Cromer, v_init = %.2f , dt = %.3f ' % (v_frac,delta_t)
title(title_text)
#axis([-maxlim,maxlim,-maxlim,maxlim])
rcParams.update({'font.size': 15})
show()

    
        
