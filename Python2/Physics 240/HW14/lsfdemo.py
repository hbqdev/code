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

# create mock data set :
b,slope = 3.0,5.0
x = arange(0,10,0.1)
# set random number seed for reproducible results:
seed([1.0])
# random number drawn from normal distribution:
y = slope * x + b + normal(0*x,5.0)

# do the fitting:
a1,a2,siga1,siga2,chi2 = linreg(x,y,5.0+0*x)
chi2_red = chi2 / (len(x)-2.0)

# set up to plot:
X = arange(0,10,0.001)
Y = a1 + a2 * X

fig1 = figure(figsize=(10,7))
plot(x,y,'o',label='data')
label_txt='$y= a_1 + a_2 x$'
title_txt = '$a_1=%.3g\pm%.3g,$ $a_2=%.3g\pm%.g,$ $\chi^2_\mathrm{red}=%.3g$' % (a1,siga1,a2,siga2,chi2_red)
plot(X,Y,label=label_txt)
legend(loc='best')
title(title_txt)
rcParams.update({'font.size': 20})
xlabel('$x$')
ylabel('$y$')
show()
