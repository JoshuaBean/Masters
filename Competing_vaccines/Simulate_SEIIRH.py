#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 10:53:26 2020

@author: joshuabean
"""
import numpy as np
import matplotlib.pyplot as plt



from Posterior import Posterior
from Posterior import unnormalised_posterior
from Vaccinate import Vaccinate



def Simulate_SEIIRH(model_parameters, q, x0, design):
    
    # Initialise the parameters
    t = 0
    stochastic_ts = np.array(t)
    weekly_ts = np.array(t)
    state = x0
    
    deterministic_state = np.tile(state,(50, 50,1))
    
    stochastic_data = state
    weekly_data = state
    
    obs_data = np.zeros([1,3])
    
    next_stop = 7
    
    vaccinations = np.zeros([2,2])
    
    unnormalised_post = np.zeros([50,50])
    k=1
    flag = 1
    #    last_vacc = 0
    
    # Keeps looping until the outbreak ends
    while sum(state[[1,2,3,7,8,9,13,14,15]]) > 0:
        
        
        # Calculates all the transition rates 
        transition_rates = np.array([
        model_parameters['beta']*sum(state[[2,3,8,9,14,15]])*state[0]/(model_parameters['N']-1), 
        model_parameters['sigma']*state[1],
        model_parameters['gamma1']*state[2],
        (1-model_parameters['prob_hospitalisation'])*model_parameters['gamma2']*state[3],
        model_parameters['prob_hospitalisation']*model_parameters['gamma2']*state[3],
        
        q[0]*model_parameters['beta']*sum(state[[2,3,8,9,14,15]])*state[6]/(model_parameters['N']-1), 
        model_parameters['sigma']*state[7],
        model_parameters['gamma1']*state[8],
        (1-model_parameters['prob_hospitalisation'])*model_parameters['gamma2']*state[9],
        model_parameters['prob_hospitalisation']*model_parameters['gamma2']*state[9],
        
        q[1]*model_parameters['beta']*sum(state[[2,3,8,9,14,15]])*state[12]/(model_parameters['N']-1), 
        model_parameters['sigma']*state[13],
        model_parameters['gamma1']*state[14],
        (1-model_parameters['prob_hospitalisation'])*model_parameters['gamma2']*state[15],
        model_parameters['prob_hospitalisation']*model_parameters['gamma2']*state[15]
        ])
        
        # Total rate of something happening
        total_rate = sum(transition_rates)
        
        # Samples a time from exponential distribution
        exp_time = np.random.exponential(1/total_rate)
    
        if t+exp_time > next_stop and sum(state[[0,1,2]]) > 0 and design[1] > 0:
    
            
            if np.size(weekly_data) > 18:
                flag = 1
                observed_data_this_week = Extract_observation(weekly_data,weekly_ts,flag)
                flag = 0
            else:
                observed_data_this_week = np.zeros([7,3])
                
    
            obs_data = np.vstack((obs_data,observed_data_this_week))
            
            
            if design[0] > 0:
                q_values, unnormalised_post_temp, deterministic_state = unnormalised_posterior(observed_data_this_week, model_parameters, deterministic_state, vaccinations[k])
                    
                unnormalised_post = unnormalised_post + unnormalised_post_temp
                
                q_values, post1, post2 = Posterior(q_values,unnormalised_post)
    
                k=k+1
                if sum(state[[0,1,2]]) > 0 and design[1] > 0:
                    state, vaccinations_temp = Vaccinate(state, post1, post2, q_values, design)
                    vaccinations = np.vstack((vaccinations, vaccinations_temp))
                else:
                    vaccinations = np.vstack((vaccinations, [0,0]))
    
            
            
            
            
            t = next_stop
            
            next_stop = next_stop + 7
            
            if np.size(weekly_data) > 18:
                weekly_data = weekly_data[-1]
            
            
            weekly_ts = np.array(0)
            
            
    #        if next_stop == 21:
    #            plt.plot(q_values, post1)
    #            plt.plot(q_values, post2)
    #            plt.legend(["q1","q2"])
    #            break
            
    
                    
            
        else:    
    
        
            # Updates the time for the proposed event           
            t = t + exp_time
        
            # Updates the cummulative time overall and this week
            stochastic_ts = np.append(stochastic_ts, t)
            weekly_ts = np.append(weekly_ts, t-next_stop+7)
        
            # Calculates the distribution for the transition options
            transition_distribution = transition_rates/total_rate
            transition_CDF = np.cumsum(transition_distribution)
            
            # Samples from the transition distribution
            r = np.random.rand()
            transition_to = np.where(r<=transition_CDF)[0][0]
            
            # Updates the state using the Transition function
            state = Transition(state, transition_to)
        
            # Updates the full data and data this week
            stochastic_data = np.vstack((stochastic_data,state))
            weekly_data = np.vstack((weekly_data,state))
    
    
    if np.size(weekly_data) > 18:    
       observed_data_this_week = Extract_observation(weekly_data, weekly_ts, flag)
            
       obs_data = np.vstack((obs_data,observed_data_this_week))
       
    #       q_values, unnormalised_post_temp, deterministic_state = unnormalised_posterior(observed_data_this_week, model_parameters, deterministic_state, vaccinations[k])
    #       
    #       unnormalised_post = unnormalised_post + unnormalised_post_temp
    
    
    obs_data = obs_data[1:,:]
        
    


    
    return(obs_data,stochastic_ts,stochastic_data,vaccinations)   
        
    
#    
#    plt.plot(q_values, post1)
#    plt.plot(q_values, post2)
#    plt.legend(["q1","q2"])
#    
    
    
    
    
    
    
# This function takes the full data and extracts the parts we partially observe
def Extract_observation(data,ts,flag):
    
    temp_data = data
    temp_ts = ts
#    print(temp_ts)
    # The number of days in a week
    if flag == 1:
        n_days = 7
    else:      
        n_days = np.int(np.ceil(temp_ts[-1]))
    
    # preallocates the observed data
    obs_data = np.zeros([n_days,3])
    
    # Loops over the days this week
    for i in range(n_days):
        
        # Finds the rows in the data that are events for day i+1
        today_index = np.where(np.array(temp_ts)<i+1)[0]
        
        # Checks if there are any events happening today
        if len(today_index) > 0:
               
            # Extracts the data for today from the index
            today = temp_data[today_index,:]
            
            # Pre-allocates the count for this day
            count = np.zeros([1,3])
            
            # Loops over events this week
            for k in range(1,max(today_index)+1):
                # Checks to see if the events is I1c -> I2c
                if all(today[k,:] - today[k-1,:] == [0,0,-1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0]):
                    # Adds to the count
                    count = count + [1,0,0]
                    
                # Checks to see if the events is I1v1 -> I2v1
                elif all(today[k,:] - today[k-1,:] == [0,0,0,0,0,0,0,0,-1,1,0,0,0,0,0,0,0,0]):
                    # Adds to the count
                    count = count + [0,1,0]
                # Checks to see if the events is I1v2 -> I2v2   
                elif all(today[k,:] - today[k-1,:] == [0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,1,0,0]):
                    # Adds to the count
                    count = count + [0,0,1]
            
            # Update the observed data
            obs_data[i,:] = count
            
            # Removes elements of data and ts that have already been used
            temp_data = np.delete(temp_data, today_index[0:len(today_index)-1], axis=0)
            
            temp_ts = np.delete(temp_ts, today_index[0:len(today_index)-1], axis=0)
            
    
    return(obs_data)
        
  
        
        
        
        
        
        
        
        
        



def Transition(state,transition_to):
    
    if transition_to == 0:
        state = state + np.array([-1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
    elif transition_to == 1:
        state = state + np.array([0,-1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
    elif transition_to == 2:
        state = state + np.array([0,0,-1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
    elif transition_to == 3:
        state = state + np.array([0,0,0,-1,1,0,0,0,0,0,0,0,0,0,0,0,0,0])        
    elif transition_to == 4:
        state = state + np.array([0,0,0,-1,0,1,0,0,0,0,0,0,0,0,0,0,0,0])        
    elif transition_to == 5:
        state = state + np.array([0,0,0,0,0,0,-1,1,0,0,0,0,0,0,0,0,0,0])        
    elif transition_to == 6:
        state = state + np.array([0,0,0,0,0,0,0,-1,1,0,0,0,0,0,0,0,0,0])
    elif transition_to == 7:
        state = state + np.array([0,0,0,0,0,0,0,0,-1,1,0,0,0,0,0,0,0,0])
    elif transition_to == 8:
        state = state + np.array([0,0,0,0,0,0,0,0,0,-1,1,0,0,0,0,0,0,0])
    elif transition_to == 9:
        state = state + np.array([0,0,0,0,0,0,0,0,0,-1,0,1,0,0,0,0,0,0]) 
    elif transition_to == 10:
        state = state + np.array([0,0,0,0,0,0,0,0,0,0,0,0,-1,1,0,0,0,0])  
    elif transition_to == 11:
        state = state + np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,-1,1,0,0,0])   
    elif transition_to == 12:
        state = state + np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,1,0,0]) 
    elif transition_to == 13:
        state = state + np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,1,0]) 
    else:
        state = state + np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,0,1])
        
    return(state)
        
        
        
        
