#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 15:37:48 2021

@author: joshuabean
"""

import numpy as np

def Perturbation(d,m,N):
    
    prob_same = 0.2
    
    d_new = np.tile(d,[m,1])
    
    n = np.int(np.size(d)/4*m)
    
    
    # Initial_vaccinated
    Initial_vacc_ME = 50
    for i in range(n):
        
        same = np.random.rand()
        if same <= prob_same:
            d_new[i,1] = d_new[i,1]
        else:
            if d_new[i,0] == 0:
                r = 1
            elif d_new[i,0] == N:
                r = 0
            else:
                r = np.random.rand()<=0.5

            
            if r == 0:
                se = np.min([d_new[i,0],Initial_vacc_ME])
                pert = np.random.randint(se)
                d_new[i,0] = d_new[i,0] - pert
            else:
                se = np.min([N-d_new[i,0],Initial_vacc_ME])
                pert = np.random.randint(se)
                d_new[i,0] = d_new[i,0] + pert


    
    
    # Daily_vaccinated
    Daily_vacc_ME = 50;
 
    for i in range(n):
        same = np.random.rand()
        if same <= prob_same:
            d_new[i,1] = d_new[i,1]
        else:
            if d_new[i,1] == 0:
                r = 1
            elif d_new[i,1] == N:
                r = 0
            else:
                r = np.random.rand()<=0.5

            
            if r == 0:
                se = np.min([d_new[i,1],Daily_vacc_ME])
                pert = np.random.randint(se)
                d_new[i,1] = d_new[i,1] - pert
            else:
                se = np.min([N-d_new[i,1],Daily_vacc_ME])
                pert = np.random.randint(se)
                d_new[i,1] = d_new[i,1] + pert
    


    
    
    # Cutoff
    d_new[:,2] = -1
    for i in range(n):
        while d_new[i,2] <0 or d_new[i,2] > 2:
            d_new[i,2] =  np.random.normal(d_new[i,2],0.15)

    
    
    # Threshold
    d_new[:,3] = -1
    for i in range(n):
        while d_new[i,3] <0 or d_new[i,3] >1:
            d_new[i,3] =  np.random.normal(d_new[i,3],0.1)

    

    
    return(d_new)
