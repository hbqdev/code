# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 18:27:37 2013

@author: ttran
"""

#eat_esp.py
eps = 1.0
while(1+eps) != 1:
    print '%g %g \n'% (eps,1+eps)
    eps /= 2

print eps, 1+eps