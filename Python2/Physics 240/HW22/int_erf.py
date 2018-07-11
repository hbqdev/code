# int_erf.py : numerically integrate error function using Romberg method

from pylab import *
from scipy.integrate import quad,romberg

def errintg(x) :
    return exp(-x**2)

def rombf(func,a,b,tol=1.48e-08) :
    R = zeros((1,1))
    dx = b - a
    R[0,0] = dx / 2 * (func(a) + func(b)) # first element
    err = Inf
    n = 0
    while err > tol :
        dx /= 2.0
        n += 1
        I_sum = 0.0
        rombvec = zeros(n+1)
        for i in range(2**(n-2)) :
            I_sum += func(a+(2*i+1)*dx)            
        rombvec[0] = R[-1,0] / 2 + dx * I_sum
        rombvec ...
        R = vstack((R,rombvec))
    hstack R
    return R

if __name__ == '__main__' :
    a,b = 0,1
    f = errintg
#    answer = 2/sqrt(pi)*romberg(f,a,b)
    answer = 2/sqrt(pi)*rombf(f,a,b)
