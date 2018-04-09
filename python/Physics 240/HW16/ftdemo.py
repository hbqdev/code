# ftdemo.py : test cases for discrete Fourier transform

from pylab import *

N,Dt = 50, 1.0
# sine wave parameters
fs,phis=0.8,0.0
#fs,phis=0.2,pi/2.0
#fs,phis=0.2123,0.0
#fs,phis=0.8,0.0

# create sine wave data set, N data points
t=arange(0,N*Dt,Dt)
y=sin(2.0*pi*fs*t+phis)

econst = -2.0*pi*1j/Dt/N
# compute Fourier transform
Y = zeros(N)*(0.0+0.0j)
f = zeros(N)
for k in range(N) :
    Y[k] = sum(y*exp(econst*t*k))
    f[k] = k / (N*Dt)
P = abs(Y)**2



fig1=figure(figsize=(9,7))
plot(t,y,'--o')
xlabel('$t$')
ylabel('$y$')
rcParams.update({'font.size': 20})
grid('on')

fig2=figure(figsize=(9,7))
plot(f,real(Y),'-o',label='$Re(Y)$')
plot(f,imag(Y),'--o',label='$Im(Y)$')
xlabel('$f$')
ylabel('$Y$')
legend(loc='best')
grid('on')

fig3=figure(figsize=(9,7))
plot(f,P,'-o')
xlabel('$f$')
ylabel('$P$')
grid('on')
show()
