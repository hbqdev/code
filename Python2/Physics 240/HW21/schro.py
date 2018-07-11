# schro.py : solve time evolution of Gaussian wave-packet using
#               Schrodinger's equation (1D)

from pylab import *

# set up initial parameter values

N_x = 100
L, m, hbar, p0 = 100.0, 1.0, 1.0, 0.5
k0, v0, sig0 = p0/hbar, p0/m, L/10.0
Dx, t_max, Dt = L/(N_x-1.0), L/v0, 1.0
N_t = int(t_max / Dt)

# build Hamiltonian:
I = identity(N_x)
H = -2.0*I + roll(I,-1) + roll(I,1)
H[0,0] = -2.0
H[-1,-1] = -2.0
H[0,-1] = 1.0
H[-1,0] = 1.0
H *= -hbar**2/(2.0*m*Dx**2)

# calculate Crank-Nicolson matrix:
D_CN = inner(linalg.inv(I + 0.5j*Dt/hbar*H) , (I - 0.5j*Dt/hbar*H))

x = linspace(-L/2,L/2,N_x)

# initial conditions:
psi = exp(1j*k0*x)*exp(-0.5*(x/sig0)**2) / sqrt(sqrt(pi)*sig0)
P = abs(psi)**2

fig1=figure(figsize=(10,7))
plot(x,real(psi),label='real')
plot(x,imag(psi),'--',label='imaginary')
legend()
xlabel('$x$')
ylabel('$\psi(x)$')
title('wavepacket initial conditions, $N_x =$ %d' % (N_x))
grid('on')
rcParams.update({'font.size': 20})

# loop over time
for n in range(N_t) :
    psi = inner(D_CN,psi) # evolve wavefunction one timestep
    P = vstack((P, abs(psi)**2)) # compute probability distribution

fig2=figure(figsize=(10,7))
for n in range(0,N_t+1,20) : # plot P(x) every 20 timesteps
    plot(x,P[n,:])
xlabel('$x$')
ylabel('$P(x)$')
grid('on')
title('probability density at various times, $N_x=$ %d' % (N_x))
show()





