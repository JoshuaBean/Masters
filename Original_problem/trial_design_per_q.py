#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 18:23:34 2021

@author: joshuabean
"""



import numpy as np




from Simulate_SIR import Simulate_SIR




def trial_design_per_q(model_parameters, x0, design, Q ,k, q_allocation, dist):
    np.random.seed()    
    
    temp_death = np.zeros(5)
    index = np.where(q_allocation == np.mod(k,6))[0]
     
    for j in range(5):
        data,ts = Simulate_SIR(design,Q[index[j]],model_parameters,dist,x0)

        temp_death[j] = data[-1,3] + data[-1,7]
    
    return(temp_death)
     
