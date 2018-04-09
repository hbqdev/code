# gas_calc.py : calculations related to ideal gas model

from pylab import *

# Hydrogen atom
m = 1.67e-27 # kg

k = 1.38e-23 # J-K
T = 1.0e7 # K : hot gas around massive galaxy
kTm = sqrt(k*T/m)

v_rms = sqrt(3.0)*kTm
v_avg = sqrt(8.0/pi)*kTm
v_mp = sqrt(2.0)*kTm
v_s = sqrt(5.0/3.0)*kTm
v_r = 4.0/sqrt(pi)*kTm

v = arange(0,3*v_rms,v_rms/1000)

# example of an in-line function:
Pv = lambda v : 4*pi*(m/(2*pi*k*T))**1.5 * v**2 * exp(-m*v**2/(2*k*T))

fig1=figure(figsize=(10,8))
plot(v/1000,Pv(v)*1e6)
fill_between(v/1000,0,Pv(v)*1e6,facecolor='c') # example of shading
scatter(v_rms/1000,Pv(v_rms)*1e6,c='r',marker='o',label='$v_\mathrm{rms}$')
scatter(v_avg/1000,Pv(v_avg)*1e6,c='g',marker='D',label='$v_\mathrm{avg}$')
scatter(v_mp/1000,Pv(v_mp)*1e6,c='k',marker='*',label='$v_\mathrm{mp}$')
scatter(v_s/1000,Pv(v_s)*1e6,c='y',marker='s',label='$v_\mathrm{s}$')
axvline(x=v_r/1000,c='0.2',linestyle='dashed',label='$v_\mathrm{rel}$') # draw vertical line
legend(loc='best')
xlabel('$v$ (km/s)')
ylabel('$P_v(v) (10^{-6})$')
ylim(0,Pv(v_mp)*1e6*1.1)
grid('on')
title('Maxwell-Boltzmann distribution')
rcParams.update({'font.size': 20})

# plot histogram of uniform random deviate [0,1)

N=2000
fig2=figure(figsize=(9,7))
hist(rand(N))
xlabel('$x$')
ylabel('$N(x)$')

# select random particles from a Maxwell-Boltzmann distribution,
#   using acceptance-rejection method; over range of v=[0,1600 km/s)

v_try = 1600e3 * rand(N)
Pmax = Pv(v_mp)
y_try = Pmax * rand(N)

keep = where(y_try < Pv(v_try))
v_keep = v_try[keep]

#v = (w for w,z in zip(v_try,y_try) if z < Pv(w))
#v = fromiter(v, float64) # turn iterable into numpy array
#v = []
#for i in range(N) :
#    if y_try[i] < Pv(v_try[i]) :
#        v.append(v_try[i])
        
fig3=figure(figsize=(9,7))
hist(v_keep/1000,20)
xlabel('$v$ (km/s)')
ylabel('$N(v)$')

fig4=figure(figsize=(9,7))
plot(v/1000,Pv(v)*1e6)
plot(v_try/1000,y_try*1e6,'*r')
plot(v_keep/1000,y_try[keep]*1e6,'og')
xlabel('$v$ (km/s)')
ylabel('$P_v(v) (10^{-6})$')
grid('on')

show()


