from __future__ import division
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 14:42:15 2013

@author: ttran
"""
from pylab import *
from copy import deepcopy
from scipy import linalg

# this function, swapRows, was adapted from
# Numerical Methods Engineering with Python, Jean Kiusalaas
def swapRows(v,i,j):
	"""Swaps rows i and j of vector or matrix [v]."""
	if len(v) == 1:
		v[i],v[j] = v[j],v[i]
	else:
		temp = v[i].copy()
		v[i] = v[j]
		v[j] = temp
	
def pivoting(a, b):
	"""changes matrix A by pivoting"""
	n = len(b)
	for k in range(0, n-1):
		p = int(argmax(abs(a[k:n, k]))) + k
		if (p != k):
			swapRows(b, k, p)
			swapRows(a,k,p)

def gauss(a, b, t=1.0e-9, verbose=False):
	""" Solves [a|b] by gauss elimination"""
	n = len(b)
	tempa = deepcopy(a)
	tempb = deepcopy(b)
	if abs(linalg.det(tempa)) < t:
		print "asn"
		return -1
	pivoting(tempa, tempb)
	for k in range(0,n-1):	
		for i in range(k+1, n):
			if tempa[i,k] != 0.0:
				m = tempa[i,k]/tempa[k,k]
				if verbose:
				    print "m =", m
				tempa[i,k+1:n] = tempa[i,k+1:n] - m * tempa[k,k+1:n]
				tempb[i] = tempb[i] - m * tempb[k]
	for k in range(n-1,-1,-1):
		tempb[k] = (tempb[k] - dot(tempa[k,k+1:n], tempb[k+1:n]))/tempa[k,k]
	return tempb

a = array([[1.0, 1, 0],[0, -2, 7], [1, -1, -1]])
b = array([[-9],[15],[0]]);

x = gauss(a,b)
y = linalg.lu(a)
print "Solution = ", x