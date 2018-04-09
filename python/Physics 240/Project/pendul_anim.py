# penul_anim.py : integrate and animate swing of a pendulum

from pylab import *

# set initial conditions

theta_max=input('starting angle? (in deg) ')
theta_max = radians(theta_max)
method = -1
while method != 1 and method != 2 :
    method = input('method? (1: Euler, 2: Verlet) ')

omega_init = 0.0    # start from rest
g_L = 1.0       # constant g/L set =1
delta_t = 2.0*pi/100.0   # note period is 2*pi

theta=[]
omega=[]        # angular velocity
theta.append(theta_max)
omega.append(omega_init)
t = arange(0.0,30.0*pi,delta_t)

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

# some animation methods adapted from Jake Vanderplas, http://jakevdp.github.com

from matplotlib.pyplot import *
from matplotlib.animation import *
r = array([0,1])   # pendulum string

# set up figure frame:
fig = figure()
ax = fig.add_subplot(111,aspect='equal',xlim=(-1.05,1.05),ylim=(-1.05,1.05))
pend, = ax.plot([],[],'o-',lw=2)
theta_text = ax.text(0.02, 0.92, '', transform=ax.transAxes)
xlabel('x')
ylabel('y')
rcParams.update({'font.size': 20})

def init():     # initialize blank frames
    pend.set_data([],[])
    theta_text.set_text('')
    return pend, theta_text,

def animate(i): # frame number i
    x = r * sin(theta[i])
    y = -r * cos(theta[i])
    pend.set_data(x, y)
    theta_text.set_text('theta = %.1f' % degrees(theta[i]))
    return pend, theta_text,

# 50 ms delay:
ani = FuncAnimation(fig, animate, init_func=init, frames=len(theta), interval=50, blit=True)
# you will need to install ffmpeg to save video to file:
#ani.save('pendul_anim.mp4', fps=30, extra_args=['-vcodec', 'libx264'])
show()


