#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 11:00:21 2021

@author: joshuabean
"""

import numpy as np

from Posterior_dist import Posterior_dist


def Posterior(data,ts,model_parameters,dist,l,up_to_data):
    
    Q = np.linspace(0.01,2,500)

    post = 0*Q
    l_updated = 0*Q
    
    if np.size(data) < 9:
        post = 1/2*np.ones(len(Q))
        new_up_to_data = up_to_data
    else:
        new_up_to_data = np.shape(data)[0]
    
        new_data = data[up_to_data:,:]
        
        new_ts = ts[up_to_data:]
        
        
        for i in range(len(Q)):
            post[i], l_updated[i] = Posterior_dist(model_parameters,new_data,new_ts,Q[i],dist,l[i])

        post[np.isnan(post)] = -np.inf
        post = post - np.max(post)
        post[post<-500] = -np.inf
        post = np.exp(post)
        norm = np.trapz(post,Q)
        post = post/norm
    
    
    return(post,Q,l_updated,new_up_to_data)