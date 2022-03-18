#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 31 15:52:01 2020

@author: joshuabean
"""

import numpy as np


from Posterior import Posterior
from prob_good import prob_good




def Simulate_SIR(design,q,model_parameters,dist,x0):
    np.random.seed()
    
    
    daily_vacc = design[1]
    
    cutoff = design[2]
    threshold = design[3]
    

    t = 0
    ts = t
    
    state = x0
    
    next_day = 1
    
    data = state

    
    up_to_data = 0;
    l = np.zeros(500)
    
    while sum(state[[1,5]]) > 0:
        
        transitions = [
            model_parameters['beta']*(state[1]+state[5])*state[0]/(model_parameters['N']-1-state[3]-state[7]),
            (1-model_parameters['pd'])*model_parameters['gamma']*state[1],
            model_parameters['pd']*model_parameters['gamma']*state[1],
            q*model_parameters['beta']*(state[1]+state[5])*state[4]/(model_parameters['N']-1-state[3]-state[7]),
            (1-model_parameters['pd'])*model_parameters['gamma']*state[5],
            model_parameters['pd']*model_parameters['gamma']*state[5]
            ]
        
        total_rate = np.sum(transitions)
        
        exp_time = np.random.exponential(1/total_rate)
        

        
        if t+exp_time > next_day and state[0] > 0:
        
            t = next_day
    
            post, Q_post, l_updated, new_up_to_data = Posterior(data,ts,model_parameters,dist,l,up_to_data)
            
            l = l_updated;
            up_to_data = new_up_to_data;
           
            prob_eff = prob_good(post,Q_post,cutoff)

            
            if prob_eff > threshold:
            
                v = np.min([daily_vacc,state[0]])
                
                state = state + v*np.array([-1, 0, 0, 0, 1, 0, 0, 0])

            ts = np.append(ts, next_day)
                

            data = np.vstack([data , state])
        
            next_day = next_day+1
        
        else:

            t = t + exp_time
            ts = np.append(ts, t)
            
            prob_trans = transitions/total_rate;
            trans_cdf = np.cumsum(prob_trans);
            
            r = np.random.rand();
            
            transition_to = np.where(r<=trans_cdf)[0][0]
            
            if transition_to == 0:
                state = state + np.array([-1, 1, 0, 0, 0, 0, 0, 0])
            elif transition_to == 1:
                state = state + np.array([0, -1, 1, 0, 0, 0, 0, 0])
            elif transition_to == 2:
                state = state + np.array([0, -1, 0, 1, 0, 0, 0, 0])
            elif transition_to == 3:
                state = state + np.array([0, 0, 0, 0, -1, 1, 0, 0])
            elif transition_to == 4:
                state = state + np.array([0, 0, 0, 0, 0, -1, 1, 0])
            else:
                state = state + np.array([0, 0, 0, 0, 0, -1, 0, 1])
                
            data = np.vstack([data , state])







    return(data,ts)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        