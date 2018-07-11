# orbit_anim.py : simulate and animate a Keplerian orbit

from pylab import *

# user inputs
mass = input("Enter the mass ratio : ")
ecc = input("Enter 1 for eccentricity, 0 for no eccentricity: ")
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
v_frac = 1
v_frac2 = -1
step = 600
step2 = 600
if mass == 1 and ecc == 0 :
    #Star 1
    m = 1.0
    GM = 1.0
    r=array([[3.0,0.0]])
    m2 = 1.0
    GM2 = 1.0
    r2=array([[-3.0,0.0]])
    
if mass == 1 and ecc == 1 :
    m = 1.0
    GM = 1.0
    r=array([[3.0,3.0]])
    a=array([[-1.0,0.0]])
    m2 = 1.0
    GM2 = 1.0
    r2=array([[-3.0,-3.0]])
   
    
if mass == 2 and ecc == 0 :
    step = 800
    step2 = 800
    #Star 1
    m = 2.0
    GM = 2.0
    r=array([[2.0,0.0]])
    a=array([[-1.0,0.0]])
    m2 = 1.0
    GM2 = 1.0
    r2=array([[-4.0,0.0]])

if mass == 2 and ecc == 1 :
    step = 975
    step2 = 800
    #Star 1
    m = 2.0
    GM = 2.0
    r=array([[2.0,0.0]])
    #star 2
    m2 = 1.0
    GM2 = 1.0
    r2=array([[-3,-3]])
    
a=array([[-1.0,0.0]])
radius=array([[norm(r)]])
v_c = sqrt(GM/radius)    
T = 2.0 * pi * radius / v_c   
delta_t = T / step
v=array([[0.0,v_c*v_frac]])
K=array([[v[-1,-1]**2+v[-1,-2]**2]])
t=array([[0.0]])
coords = hstack((r,v))

# integrate the orbit
for i in range(0,1000) :
    a = -GM * r[-1] / (norm(r[-1]))**3
    coords = rk4(coords,t,delta_t,g_derivs,GM)
    r_new = coords[0,0:2]
    v_new = coords[0,2:4]
    v = vstack((v, v_new))
    r = vstack((r, r_new))
    radius = vstack((radius, norm(r_new)))
    K = vstack((K, v[-1,-1]**2 + v[-1,-2]**2))
    t = vstack((t,t[-1]+delta_t))

# calculate angle and energies
theta=arctan2(r[:,1],r[:,0]) 

#star2
   
a2=array([[-1.0,0.0]])
radius2=array([[norm(r2)]])
v_c2 = sqrt(GM2/radius2)
T2= 2.0 * pi * radius2 / v_c2    
delta_t2 = T2 / step2
v2=array([[0.0,v_c2*v_frac2]])
K2=array([[v2[-1,-1]**2+v2[-1,-2]**2]])
t2=array([[0.0]])
coords2 = hstack((r2,v2))  # needed for Runge-Kutta
    
    # integrate the orbit
for i in range(0,1000) :
    a2 = -GM * r2[-1] / (norm(r2[-1]))**3
    coords2 = rk4(coords2,t2,delta_t2,g_derivs,GM2)
    r_new2 = coords2[0,0:2]
    v_new2 = coords2[0,2:4]
    v2 = vstack((v2, v_new2))  # we missed this line in class
    r2 = vstack((r2, r_new2))
    radius2 = vstack((radius2, norm(r_new2)))
    K2 = vstack((K2, v2[-1,-1]**2 + v2[-1,-2]**2))
    t2 = vstack((t2,t2[-1]+delta_t2))


theta2=arctan2(r2[:,1],r2[:,0]) 

from matplotlib.pyplot import *
from matplotlib.animation import *
# set up figure frame:
fig = figure() 
Ax = fig.add_subplot(111,polar=True)
Ax.set_ylim([0,10])
trajpt, = Ax.plot([],[],'o')  
trajln, = Ax.plot([],[])
#star 2
trajpt2, = Ax.plot([],[],'o')  
trajln2, = Ax.plot([],[])

def init(): 
    trajpt.set_data([],[])
    trajln.set_data([],[])
    trajpt2.set_data([],[])
    trajln2.set_data([],[])
    return trajpt, trajln,trajpt2, trajln2
    
def animate(i) : 
    trajpt.set_data(theta[i], radius[i])
    trajln.set_data(theta[0:i], radius[0:i])
    trajpt2.set_data(theta2[i], radius2[i])
    trajln2.set_data(theta2[0:i], radius2[0:i])
    return trajpt, trajln, trajpt2, trajln2
  
ani = FuncAnimation(fig, animate, init_func=init, frames=len(theta), interval=0, blit=True)
    
    
 
show()
    
        
            
