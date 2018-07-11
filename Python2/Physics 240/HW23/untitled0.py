# -*- coding: utf-8 -*-
"""
Created on Mon May 13 15:34:59 2013

@author: ttran
"""
a = 4
b = []
for i in range(1,8) :
    a = a*-3
    print a
    b.append(a)
print sum(b) + 4
