#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 10:40:18 2020

@author: joshuabean
"""
import numpy as np

from Likelihood import Likelihood
from scipy.stats import gaussian_kde
                      
def MH(data, model_parameters, x0):

    Nits = 2300
    sigma = 0.01
    
    P = np.zeros([Nits,2])
    P[0] = [0.5,0.5]
    
    L_prev = 0 + Likelihood(data, P[0] , model_parameters, x0)
    
    for i in range(1,Nits):
        
#        print(i)
        
        prop_parameters = np.random.normal(P[i-1],sigma)
        
        if all(prop_parameters > 0) and all(prop_parameters < 1):
            
            L_prop = 0 + Likelihood(data, prop_parameters, model_parameters,x0)
            
            A = L_prop - L_prev
            
            u = np.log(np.random.rand())
            
            if u < A:
                P[i] = prop_parameters
                L_prev = L_prop
            else:
                P[i] = P[i-1]
            
        else:
            P[i] = P[i-1]

    return(P)

#
#P = P[100:,:]
#kde1 = gaussian_kde(P[~np.isnan(P[:,0]),0])
#kde2 = gaussian_kde(P[~np.isnan(P[:,1]),1])
#
#q1_values = np.linspace(np.min(P[:,0]),np.max(P[:,0]),1000)
#q2_values = np.linspace(np.min(P[:,1]),np.max(P[:,1]),1000)
#
#
#density_values1 = kde1.evaluate(q1_values)
#density_values2 = kde2.evaluate(q2_values)
#
#f, (ax1, ax2) = plt.subplots(1, 2)
#ax1.plot(P)
#ax2.hist(P,100,density=True)
#ax2.plot(q1_values, density_values1, color = u'#1f77b4')
#ax2.plot(q2_values, density_values2, color =  u'#ff7f0e')





        
        
        