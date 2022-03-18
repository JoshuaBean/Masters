#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 09:27:58 2020

@author: joshuabean
"""
import numpy as np
from Likelihood import Likelihood
from Prior import Prior




def unnormalised_posterior(obs_data, model_parameters, x0, vaccinations):
    
    ind = 3
    
    q = np.linspace(0.05,1,50)
    [q1,q2] = np.meshgrid(q,q)
    
    l = np.zeros([len(q),len(q)])
    
    end_of_week_state = np.zeros([50,50,18])
    
    for i in range(len(q)):
        for j in range(len(q)):
            l[i,j], end_of_week_state[i,j,:] =  Likelihood(obs_data, [q1[i,j],q2[i,j]], model_parameters, x0[i,j,:], vaccinations)
            l[i,j] = l[i,j] + Prior(q1[i,j],q2[i,j],ind)
    
    return(q,l,end_of_week_state)
    
    
    
    
    
def Posterior(q,l):
    l[np.isnan(l)] = -np.inf
    l = l - np.max(l)
    l[l<-500] = -np.inf
    post = np.exp(l)
    norm = np.trapz(post,q,axis=0)
    norm = np.trapz(norm,q)
    post = post/norm
    
    post1 = np.trapz(post,q,axis=0)
    post2 = np.trapz(post,q,axis=1)
    
    return(q,post1,post2)
    
    
