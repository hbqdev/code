# int_erf.py : numerically integrate error function using Romberg method

from pylab import *
from scipy.integrate import quad,romberg

def errintg(x) :
    return exp(-x**2)

def rombf(func,a,b,N,tol=1.48e-08) :
    R = zeros((N,N))
    dx = b - a
    R[0,0] = dx / 2 * (func(a) + func(b)) # first element
    n = 0
    for i in range(1,N) :
        dx /= 2.0
        n += 1
        I_sum = 0.0
#        rombvec = zeros(n+1)
        for k in range(2**(n-1)) :
            I_sum += func(a+(2*k+1)*dx)
        R[i,0] = R[i-1,0] / 2 + dx * I_sum
        m = 1
        for j in range(3,i) :
            m = 4*m
            R[i,j] = R[i,j-1] + (R[i,j-1] - R[i-1,j-1])/(m-1) 
#        R = vstack((R,rombvec))
#    hstack R
    return R

#def rombf(func,a,b,tol=1.48e-08) :
#    R = zeros((1,1))
#    dx = b - a
#    R[0,0] = dx / 2 * (func(a) + func(b)) # first element
#    err = Inf
#    n = 0
#    print type(R)
#    while err > tol :
#        dx /= 2.0
#        n += 1
#        I_sum = 0.0
#        rombvec = zeros(n)
#        for i in range(2**(n-1)) :
#            I_sum += func(a+(2*i+1)*dx)            
#        rombvec[0] = R[-1,0] / 2 + dx * I_sum
#        R = vstack((R,rombvec[0]))
#        R = hstack((R,[[rombvec[0]]]))
#        print R
#        #err = abs(R[n-1,n-1]-R[n-2,n-2])
#        #print rombvec
#    #print R
#    return R
if __name__ == '__main__' :
    a,b,N = 0,1,30
    f = errintg
#    answer = 2/sqrt(pi)*romberg(f,a,b)
    answer = 2/sqrt(pi)*rombf(f,a,b,N)
    print answer
