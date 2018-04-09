# ode.py : module of ODE functions

from pylab import *

def rk4(x,t,delta_t,derivs,param) :
    dt2 = delta_t/2.0
    F1=derivs(x,t,param)
    F2=derivs(x+F1*dt2,t+dt2,param)
    F3=derivs(x+F2*dt2,t+dt2,param)
    F4=derivs(x+F3*delta_t,t+delta_t,param)
    x=x+(F1+2.0*(F2+F3)+F4)*delta_t/6.0
    return x

def rka(x,t,delta_t,derivs,param,epsi) :

    S1, S2 = (0.9, 4.0)     # safety factors
    epsstar = Inf           # initialize error
    N_iter, N_max = (0, 100)
    while epsstar > epsi and N_iter < N_max :
        # take big, trial step
        xb = rk4(x,t,delta_t,derivs,param)
        # take two small, trial steps
        xhalf = rk4(x,t,delta_t/2.0,derivs,param)
        xs = rk4(xhalf,t+delta_t/2.0,delta_t/2.0,derivs,param) # 't' wrong before
        # compute estimated truncation error
        epsstar = abs(xb-xs)   # look for maximum error among coordinates
        epsstar = max(epsstar.flatten()) # convert array to vector if necessary
        # estimate new timestep (including safety factors)
        dtstar = delta_t * abs(epsi/epsstar)**0.2
        dtstar *= S1
        if dtstar > S2*delta_t :
            delta_t *= S2
        elif dtstar < delta_t / S2 :
            delta_t /= S2
        else :
            delta_t = dtstar
        N_iter += 1
    if N_iter == N_max :
        print('Warning: adaptive RK4 routine did not converge.')
    x = xs
    t += delta_t
    return x,t,delta_t

# these commands processed if ode.py run on its own
#  (test commands)
if __name__ == '__main__' :
    print 'test'
    
