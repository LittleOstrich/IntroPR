'''
Created on 18 Oct 2017

@author: Benjamin
'''
import numpy as np

def pqsolver(p, q):
    p = float(p)
    q = float(q)
    r = p ** 2 / 2 - q
    assert(r >= 0)
    d = np.sqrt(r)
    return (-1. * p / 2) - d , (-1. * p / 2) + d

