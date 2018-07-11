# orbit.py : simulate a Keplerian orbit

from pylab import *

# user inputs

v_frac = input('v_init / v_circ ? ')
step = input('time steps per orbit? ')
method = -1
while method != 1 and method != 2 and method != 3 :
    method = input('method? (1: Euler, 2: Euler-Cromer, 3: Runge-Kutta) ')

# set up Runge-Kutta functions

def rk4(x,t,delta_t,derivs,param) :
    dt2 = delta_t/2.0
    F1=derivs(x,t,param)
    F2=derivs(x+F1*dt2,t+dt2,param)
    F3=derivs(x+F2*dt2,t+dt2,param)
    F4=derivs(x+F3*delta_t,t+delta_t,param)
    x=x+(F1+2.0*(F2+F3)+F4)*delta_t/6.0
    return x

def g_derivs(x,t,GM) :  # specific function for derivatives
    r = x[0,0:2]
    v = x[0,2:4]
    a = -GM*r/norm(r)**3
    derivs = hstack((v,a))
    return derivs
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
coords = hstack((r,v))  # needed for Runge-Kutta

# integrate the orbit
for i in range(0,1000) :
    a = -GM * r[-1] / (norm(r[-1]))**3
    if method == 1 : # Euler
        r_new = r[-1] + delta_t * v[-1]
        v_new = v[-1] + delta_t * a
        v = vstack((v, v_new))
    elif method == 2 :  # Euler-Cromer
        v_new = v[-1] + delta_t * a
        v = vstack((v, v_new))
        r_new = r[-1] + delta_t * v[-1]
    else : # Runge-Kutta
        coords = rk4(coords,t,delta_t,g_derivs,GM)
        r_new = coords[0,0:2]
        v_new = coords[0,2:4]
        v = vstack((v, v_new))  # we missed this line in class
    r = vstack((r, r_new))
    radius = vstack((radius, norm(r_new)))
    K = vstack((K, v[-1,-1]**2 + v[-1,-2]**2))
    t = vstack((t,t[-1]+delta_t))

# calculate angle and energies
theta=arctan2(r[:,1],r[:,0]) # note math.atan2 can't handle arrays
K = K * m / 2.0 # couldn't figure out how to calculate row-by-row norm here
U = -GM*m/radius
E = K + U

print('energy conservation = %f ' % (max(abs(E/E[0]-1))) )

# time for plotting
fig = figure(figsize=(16,6))    # size hard-wired to fit MacBook Air screen
subplot(1,2,1,polar=True)
plot(theta,radius)
grid('on')
subplot(1,2,2)
plot(t,E,label='Total')
plot(t,K,'-.',lw=2,label='Kinetic')
plot(t,U,'--',lw=2,label='Potential')        
legend(loc='best')  # this command appears to minimize overlap with data
xlabel('t')
ylabel('Energy')
if method == 1 :
    title_text = 'Euler, v_init = %.2f , dt = %.3f ' % (v_frac,delta_t)
elif method == 2 :
    title_text = 'Euler-Cromer, v_init = %.2f , dt = %.3f ' % (v_frac,delta_t)
else :
    title_text = 'Runge-Kutta, v_init = %.2f , dt = %.3f ' % (v_frac,delta_t)
title(title_text)
rcParams.update({'font.size': 15})
show()

    
        
