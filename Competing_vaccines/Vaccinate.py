#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 10:20:20 2020

@author: joshuabean
"""
import numpy as np
import matplotlib.pyplot as plt

def Vaccinate(state, post1, post2, q_values, design):
    
    q1 = q_values[np.argmax(post1)]
    q2 = q_values[np.argmax(post2)]

    prop_to_v1 = (q2**design[2]/(q1**design[2]+q2**design[2]))
    
    
    two_functions = np.vstack([post1,post2])
    area_shared = np.trapz(np.min(two_functions,0), q_values)
    vacc_today = np.int(np.ceil(np.min([sum(state[[0,1,2]]),design[1]*(1-area_shared)**(design[3])])))
    
                
    move_to_v1 = np.int(np.floor(vacc_today*prop_to_v1))
    move_to_v2 = vacc_today - move_to_v1
    
    in_control = np.repeat([0,1,2],[state[0],state[1],state[2]])
    
    
    n_control = len(in_control)
    
    sampled_to_move = np.random.choice(n_control,vacc_today,False)
    
    vaccines = in_control[sampled_to_move]
    
    total_vaccinated_today = [sum(vaccines == 0),sum(vaccines == 1),sum(vaccines == 2)]
    
    
    if sum(total_vaccinated_today) != vacc_today:
        raise Exception(state, vacc_today,total_vaccinated_today,vaccines)
            
    
    to_v1 = np.random.choice(vaccines,move_to_v1,False)
    
    to_v1 = [sum(to_v1 == 0),sum(to_v1 == 1),sum(to_v1 == 2)]
    to_v2 = [total_vaccinated_today[0] - to_v1[0], total_vaccinated_today[1] - to_v1[1], total_vaccinated_today[2] - to_v1[2]]
    
    
    if any(np.array(to_v1) + np.array(to_v2) != total_vaccinated_today):
        raise Exception(state, to_v1, to_v2 ,total_vaccinated_today)
             
    
    state_new = state + [-total_vaccinated_today[0],-total_vaccinated_today[1],-total_vaccinated_today[2],0,0,0,to_v1[0],to_v1[1],to_v1[2],0,0,0,to_v2[0],to_v2[1],to_v2[2],0,0,0]
    
    if any(state_new<0):
        raise Exception(state,state_new,total_vaccinated_today,to_v1,to_v2)
        
    state = state_new
        
    vaccinations = [move_to_v1, move_to_v2]
    
    
    return(state,vaccinations)
    
    
    
    
    