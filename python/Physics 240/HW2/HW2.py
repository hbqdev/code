# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 19:32:52 2013

@author: ttran
"""
#Plot the first plot
from pylab import *
ax1 = subplot(2,2,1)
x = linspace(0,20,100)
y = exp(-x/4)*sin(x)
plot(x,y)
xlabel('x')
ylabel('f(x)')
title('f(x)=exp(-x/4)*sin(x)')
grid('on')

#Second plot
x = linspace(0,20,100)
y = exp(-x/4)*sin(x)
ax2 = subplot(222)
plot(x,y)
xlabel('x')
ylabel('f(x)')
title('f(x)=exp(-x/4)*sin(x)')
annotate("exp(-x/4)",xy=(0,4))
plot(x,exp(-x/4),'--',label="exp(-x/4)")
text(5,0.3,"exp(-x/4)")
legend()

#Third plot
x = linspace(0,20,100)
y = exp(-x)*(sin(x))**2
ax2 = subplot(223)
semilogy(x,y,'+')
xlabel('x')
ylabel('f(x)')
title('f(x)=exp(-x)*sin(x)^2')
yticks([10**0,10**-10,10**-5])
legend()


#Fourth plot
ax2 = subplot(224,polar=True)
theta = arange(0,360,0.1)
radian = theta*0.01745
a = 4
r = .5 + 0.5*cos(6*radian+pi)
plot(radian,r)
coor = arange(0,360,30)
xticks(coor*0.01745)
yticks([0.5,0.5])
show()
#savefig("hw2")

#

