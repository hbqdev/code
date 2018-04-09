# balle.py : calculate trajectory of a baseball

from pylab import *


# initial conditions and constants:

v0 = input('v0=? ')
theta0 = input('theta0=? ')
air = -1
while air != 0 and air != 1 :
    air = input('air resistance? (0 for no, 1 for yes) ')
delta_t = input('time step in sec? ')
method = -1
while method != 1 and method != 2 and method != 3 :
    method = input('method? (1: Euler, 2: Euler-Cromer, 3: midpoint) ')

max_steps = 1e4
m = 0.15 # mass in kg
g = 9.8 # m/s^2
if air == 0 :
    Cd = 0.0
    alabel = 'no air'
    locx = 'lower center'
else :
    Cd = 0.35 # drag coefficient
    alabel = 'air'
    locx = 'right'
alabel += ', numerical'
A = 0.004 # area in m^2
rho = 1.2 # kg/m^3
air_const = -0.5*Cd*rho*A/m # air resistance constant

# note the double brackets that define these arrays as matrices:
r = array([[0.0,0.0]])    # x is r[0,:], y is r[1,:]
v = array([[v0*cos(theta0),v0*sin(theta0)]])  # vx is v[0,:], vy is v[1,:]
a = array([[0.0,-g] + air_const*norm(v[-1])*v[-1]])
t = array([[0.0]])               # time in sec
r_check = r         # analytical solution
v_check = v
t_flight_check = 2.0 * v0 * sin(theta0) / g
x_max_check = v0**2 * sin(2.0*theta0) / g
y_max_check = v0**2 * (sin(theta0))**2 / (2*g)
step = 0

while r[-1,1] >= 0 and step < max_steps :  # y > 0 test
    if method == 1 : # Euler method
        r = vstack(( r , r[-1,:] + delta_t * v[-1,:] )) # add a row to 'r'
        v = vstack(( v , v[-1,:] + delta_t * a[-1,:] )) # add a row to 'v'
    elif method == 2 : # Euler-Cromer method
        v = vstack(( v , v[-1,:] + delta_t * a[-1,:] )) # add a row to 'v'
        r = vstack(( r , r[-1,:] + delta_t * v[-1,:] )) # add a row to 'r'
    else : # midpoint method
        v = vstack(( v , v[-1,:] + delta_t * a[-1,:] )) # add a row to 'v'
        r = vstack(( r , r[-1,:] + delta_t * (v[-1,:]+v[-2,:])/2.0 )) # add a row to 'r'
    t = vstack(( t , t[-1] + delta_t )) # add an element to 't'
    a = vstack(( a , [0.0,-g] + air_const * norm(v[-1]) * v[-1])) # update acceleration
    r_check = vstack(( r_check, r[0,:] + t[-1] * v[0,:] + [0.0,-0.5*g*t[-1]**2] ))
    step += 1

print 't_fin = %g sec, error = %g sec' % (t[-1],t[-1] - t_flight_check)
print 'x_range = %g m, error = %g m' % (r[-1,0],r[-1,0] - x_max_check) 
plot(r_check[:,0],r_check[:,1],label='no air, analytic')
plot(r[:,0],r[:,1],'-o',label=alabel) # x, y
xlabel('x [m]')
ylabel('y [m]')
legend(loc=locx)    # location of label
title('baseball trajectory')
grid('on')
axis([r[0,0], 1.05*maximum(r[-1,0],r_check[-1,0]), 0.0, 1.05*maximum(max(r[:,1]),max(r_check[:,1]))])
rcParams.update({'font.size': 20})
show()

    
