#rombint.py : computes the integral of a given function using the Romberg method

from pylab import *
from scipy.integrate import quad, romberg

def intfunc(x):
    return 2./sqrt(pi)*exp(-x**2)

def rombf(func,a,b,tol=1.48e-08):
    R = zeros((1,1))
    dx = b-a
    R[0,0] = dx/2. * (func(a)+func(b)) #first term in matrix
    err = 1.0
    n = 0
    while err > tol:
        dx /= 2.0
        n += 1
        I_sum = 0.0
        rombhor = zeros((n+1))
        for i in range (2**(n-1)) :
            I_sum += func(a+(2*i+1)*dx)
        rombhor[0] = R[-1,0]/2. + dx*I_sum
        R = np.hstack((R, np.zeros((R.shape[0], 1), dtype=R.dtype)))
        
        for i in range(1,len(rombhor)):
            rombhor[i] = rombhor[i-1]+1./(4.**i-1)*(rombhor[i-1]-R[-1,i-1])
        R = vstack((R,rombhor))
        
        #print abs(answer[n-1,n-1]-answer[n,n])/answer[n,n]
        #print n
        #now have the first column value in place
        
        #for i in range(1, n+1):
         #   for j in range(n+1,n+1):
                #if j > i:
                 #   R[i,j] = 0
                #else:
          #      R[i,j] = R[i,j-1]+1./(4.**(j)-1.)*(R[i,j-1]-R[i-1,j-1])
        #have now filled up the romberg matrix
        #test the tolerance
        
        err = abs(R[n,n]-R[n-1,n-1])
        if n == 30:
            print "uh oh loop broken"
            break
    print err
    return R,n

if __name__ == '__main__' :
    a,b = 0,1
    f = intfunc
    answer,n = rombf(f,a,b)
    print answer