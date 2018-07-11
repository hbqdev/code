# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 22:46:59 2013

@author: ttran
"""

# lsfdemo2.py : demonstration of linear regression techniques:
#  creates a mock data set based on a linear or polynomial model, with
#  mock errors added, then fits with linear regression or
#  polynomial normal equations and plots

from pylab import *
from scipy.linalg import inv
from numpy import polyfit

# linear regression function: given vector inputs of data
#   and uncertainties, returns best-fit parameters and
#   uncertainties, along with chi^2 value
def linreg(x,y,sigma) :
    S = sum(1.0/sigma**2)
    Sx = sum(x/sigma**2)
    Sy = sum(y/sigma**2)
    Sxx = sum(x**2/sigma**2)
    Sxy = sum(x*y/sigma**2)
    SD = Sxx * S - Sx**2
    a1 = (Sxx * Sy - Sxy * Sx) / SD
    a2 = (Sxy * S - Sx * Sy) / SD
    siga1 = sqrt(Sxx / SD)
    siga2 = sqrt(S / SD)
    Y = a1 + a2 * x
    chi2 = sum( ( (y-Y)/sigma )**2 )
    return a1,a2,siga1,siga2,chi2

def pollsf(x,y,sigma,M) :
    N = len(x)
    A = zeros((N,M))
    b = zeros(N)
    Y = zeros(N)
    for i in range(N) :
        b[i] = y[i] / sigma[i]
        for j in range(M) :
            A[i,j] = x[i]**j / sigma[i]
    C = inv(dot(A.T,A))
    a = dot(C,dot(A.T,b))
    siga = sqrt(diag(C))
    for i in range(N) :
        for j in range(M):
            Y[i] = a[j]*x[i]**j
    chi2 = sum(((y-Y)/sigma)**2)
    return a,siga,chi2,Y
fit_type = input('Linear (1) or polynomial (2) fit? ')

# create mock data set :
x = arange(0,10,0.1)
# set random number seed for reproducible results:
seed([1.0])
if fit_type == 1 :   
    b,slope = 3.0,5.0
    # random number drawn from normal distribution:
    y = slope * x + b
elif fit_type == 2 :
    p1,p2,p3 = 1.0,2.0,-3.0
    y = p1 + p2 * x + p3 * x**2
else :
    print('oops!')
# add mock errors:
y += normal(0*x,5.0)
data_unc = 5.0+0*x

# do the fitting:
if fit_type == 1 :
    a1,a2,siga1,siga2,chi2 = linreg(x,y,data_unc)
    N_param = 2
    Y = a1 + a2 * x
elif fit_type == 2 :
    N_param = input('How many coefficients? ')
    a,siga,chi2,Y = pollsf(x,y,data_unc,N_param)
chi2_red = chi2 / (len(x) - N_param)
print chi2_red
 #set up to plot:
if fit_type == 1 :
    X = chi2/a1
    Y1 = chi2/a2
    #Z = arange(len(X))
fig1 = figure(figsize=(10,7))
errorbar(x,y,5.0+0*x,fmt='o',label='data')
label_txt='$y= a_1 + a_2 x$'
if fit_type == 1 :
    title_txt = '$a_1=%.3g\pm%.3g,$ $a_2=%.3g\pm%.g,$ $\chi^2_\mathrm{red}=%.3g$' % (a1,siga1,a2,siga2,chi2_red)
elif fit_type == 2 :
    title_txt = '$\chi^2_\mathrm{red}=%.3g$' % (chi2_red)
plot(x,Y,label=label_txt)
legend(loc='best')
title(title_txt)
rcParams.update({'font.size': 20})
xlabel('$x$')
ylabel('$y$')
#contour(X,Y,Z)


data_unc = 0.15+0*x
x,y,z = loadtxt('data.txt', unpack = True)

# do the fitting:
data_unc = 0.15+0*x
if fit_type == 1 :
    a1,a2,siga1,siga2,chi2 = linreg(x,y,data_unc)
    N_param = 2
    Y = a1 + a2 * x
elif fit_type == 2 :
    N_param = input('How many coefficients? ')
    a,siga,chi2,Y = pollsf(x,y,data_unc,N_param)
chi2_red = chi2 / (len(x) - N_param)
print chi2_red
 #set up to plot:


fig2 = figure(figsize=(10,7))
errorbar(x,y,0.15+0*x,fmt='o',label='data')
label_txt='$y=a x$'
if fit_type == 1 :
    title_txt = '$a_1=%.3g\pm%.3g,$ $a_2=%.3g\pm%.g,$ $\chi^2_\mathrm{red}=%.3g$' % (a1,siga1,a2,siga2,chi2_red)
elif fit_type == 2 :
    title_txt = '$\chi^2_\mathrm{red}=%.3g$' % (chi2_red)
    
plot(x,y,'bo',label='data')
#Y = polyfit(x,y,3)
print Y
plot(x,Y,label=label_txt)
legend(loc='best')
title(title_txt)
rcParams.update({'font.size': 20})
xlabel('$x$')
ylabel('$y$')
show()
