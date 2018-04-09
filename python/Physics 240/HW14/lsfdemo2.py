# lsfdemo2.py : demonstration of linear regression techniques:
#  creates a mock data set based on a linear or polynomial model, with
#  mock errors added, then fits with linear regression or
#  polynomial normal equations and plots

from pylab import *
from scipy.linalg import inv

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
    for i in range(N) :
        b[i] = y[i] / sigma[i]
        for j in range(M) :
            A[i,j] = x[i]**j / sigma[i]
    C = inv(dot(A.T,A))
    a = dot(C,dot(A.T,b))
    siga = sqrt(diag(C))
    for i in range(N) :
        Y[i] = a[i] * x[i] # not finished / correct / in right place
#    return a,siga,0.0

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
elif fit_type == 2 :
    N_param = input('How many coefficients? ')
    a,siga,chi2 = pollsf(x,y,data_unc,N_param)
chi2_red = chi2 / (len(x) - N_param)

# set up to plot:
X = arange(0,10,0.001)
Y = a1 + a2 * X

fig1 = figure(figsize=(10,7))
errorbar(x,y,5.0+0*x,fmt='o',label='data')
label_txt='$y= a_1 + a_2 x$'
title_txt = '$a_1=%.3g\pm%.3g,$ $a_2=%.3g\pm%.g,$ $\chi^2_\mathrm{red}=%.3g$' % (a1,siga1,a2,siga2,chi2_red)
plot(X,Y,label=label_txt)
legend(loc='best')
title(title_txt)
rcParams.update({'font.size': 20})
xlabel('$x$')
ylabel('$y$')
show()
