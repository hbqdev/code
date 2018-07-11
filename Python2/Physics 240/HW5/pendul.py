# penul.py : integrate swing of a pendulum

from pylab import *

# set initial conditions

theta_max=input('starting angle? (in deg) ')
theta_max = radians(theta_max)
method = -1
while method != 1 and method != 2 :
    method = input('method? (1: Euler, 2: Verlet) ')

omega_init = 0.0    # start from rest
g_L = 1.0       # constant g/L set =1
alpha_init = -g_L*sin(theta_max)    # initial acceleration
delta_t = 2.0*pi/100.0   # note period is 2*pi

theta=[]
omega=[]        # angular velocity
theta.append(theta_max)
omega.append(omega_init)
t = arange(0.0,9.0*pi,delta_t)

for i in range(0,len(t)-1) :
    alpha = -g_L * sin(theta[i])
    if method == 1 :    # Euler's simple method
        theta.append(theta[i] + omega[i] * delta_t)
        omega.append(omega[i] + alpha * delta_t)
    else :              # Verlet's method
        if i==0 :           # first backwards step
            theta.append(theta[i] + alpha / 2.0 * delta_t**2)
        else :
            theta.append(2.0 * theta[i] - theta[i-1] + alpha * delta_t**2)

theta = degrees(theta)
theta_check = degrees(theta_max * cos(t))
print len(theta_check)
#print theta_check
plot(t,theta,'o-',label='numerical')
if degrees(theta_max) < 15.0 : # small angle approximation valid 
    plot(t,theta_check,label='analytic')
legend(loc='lower left')
xlabel('t')
ylabel('theta [deg]')
grid('on')
#rcParams.update({'font.size': 20})
show()


