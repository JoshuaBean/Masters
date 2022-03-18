#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 08:20:26 2021

@author: joshuabean
"""


import numpy as np
from scipy.stats import multivariate_normal

def Prior(q1,q2,ind):
    
    if ind == 0: #prior with two big peaks
        mu = [0.3,0.6]
        sigma = [[0.02,0],[0,0.02]]
        
        p = multivariate_normal.pdf([q1,q2],mu,sigma)
    elif ind == 1: #prior with two flat peaks
        mu = [0.3,0.6]
        sigma = [[0.2,0],[0,0.2]]
        
        p = multivariate_normal.pdf([q1,q2],mu,sigma)
    elif ind == 2: #prior with one of each and some correlation
        mu = [0.3,0.6]
        sigma = [[0.1,0.1],[0,0.1]]

        p = multivariate_normal.pdf([q1,q2],mu,sigma)
    else :
        p = 1
    return(np.log(p))