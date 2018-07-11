# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 15:18:20 2013

"""
i = 1
j = 2
fib = []
fib.append(j)
sumfib = 0
c = 0
while c < 4000000 :
    c = i + j
    fib.append(c)
    i = j
    j = c
    
for k in fib :
    if k%2 == 0 :
        sumfib += k
print sumfib
