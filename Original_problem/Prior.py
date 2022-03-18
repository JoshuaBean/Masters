#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 11:08:19 2021

@author: joshuabean
"""
from scipy.stats import beta
import numpy as np


def Prior(q,t,dist):
    
    if t == "sample":
        sample = 1
    elif t == "prob":
        sample = 0
        
    
    
    if dist == "uniform":
        
        p = (1-sample)*np.log(1/2) + sample*2*np.random.rand()
        
    elif dist == "step0.7":
        if np.random.rand() < 0.7:
            p_sample = np.random.rand()
        else:
            p_sample = 2*np.random.rand()
            
        
        if q < 1:
            p_prob = 0.7
        else:
            p_prob = 0.3

        
        p = (1-sample)*np.log(p_prob) + sample*p_sample
        
    elif dist == "step0.9":
        if np.random.rand() < 0.9:
            p_sample = np.random.rand()
        else:
            p_sample = 2*np.random.rand()

        
        if q < 1:
            p_prob = 0.9
        else:
            p_prob = 0.1

        
        p = (1-sample)*np.log(p_prob) + sample*p_sample
        
    elif dist == "scaledbeta1":
        p = (1-sample)*np.log(beta.pdf(q/2,2,6)) + sample*2*np.random.beta(2,6)
    elif dist == "scaledbeta2":
        p = (1-sample)*np.log(beta.pdf(q/2,2,8)) + sample*2*np.random.beta(2,8)
    elif dist == "qstar":
        p = (1-sample)*np.log(1/1.105) + sample*1.105*np.random.rand()
    elif dist == "qbeta":
        p = (1-sample)*np.log(beta.pdf(q/1.5,2.525,3.535)) + sample*1.5*np.random.beta(2.525,3.535)

    
    
    
    
    
    return(p)
    