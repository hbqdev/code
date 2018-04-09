# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 23:43:21 2013

@author: ttran
"""

# lsfdemo.py : demonstration of linear regression techniques:
#  creates a mock data set based on a linear model, with
#  mock errors added, then fits with linear regression and plots

from pylab import *

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

x,y,z = loadtxt('data.txt', unpack = True)
#x = log(x)
#for i in range(len(y)) :
#    if y[i] < 0:
#        y[i] = log(-y[i])
#    else:
#        y[i] = -log(y[i])
a1,a2,siga1,siga2,chi2 = linreg(x,y,0.15+0*x)
chi2_red = chi2 / (len(x)-2.0)

# set up to plot:
Y = a1 + a2 * x
error_bar = Y-x
fig1 = figure(figsize=(10,7))
plot(x,y,'bo',label='data')
errorbar(x,y,Y,fmt='o',label='data')
label_txt='$y= a_1 + a_2 x$'
title_txt = '$a_1=%.3g\pm%.3g,$ $a_2=%.3g\pm%.g,$ $\chi^2_\mathrm{red}=%.3g$' % (a1,siga1,a2,siga2,chi2_red)
plot(x,Y,label=label_txt)
legend(loc='best')
title(title_txt)
rcParams.update({'font.size': 20})

xlabel('$time$')
ylabel('$Temperature$')
show()
